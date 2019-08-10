import os
import typing
import cv2
import uuid
import numpy as np
from loguru import logger

from stagesepx import toolbox
from stagesepx.video import VideoObject
from stagesepx.cutter.cut_range import VideoCutRange


class VideoCutResult(object):
    def __init__(self,
                 video: VideoObject,
                 range_list: typing.List[VideoCutRange]):
        self.video = video
        self.range_list = range_list

    def get_target_range_by_id(self, frame_id: int) -> VideoCutRange:
        """ get target VideoCutRange by id (which belongs to) """
        for each in self.range_list:
            if each.contain(frame_id):
                return each
        raise RuntimeError(f'frame {frame_id} not found in video')

    @staticmethod
    def _length_filter(range_list: typing.List[VideoCutRange], limit: int) -> typing.List[VideoCutRange]:
        after = list()
        for each in range_list:
            if each.get_length() >= limit:
                after.append(each)
        return after

    def get_unstable_range(self,
                           limit: int = None,
                           range_threshold: float = None,
                           **kwargs) -> typing.List[VideoCutRange]:
        """ return unstable range only """
        change_range_list = sorted(
            [i for i in self.range_list if not i.is_stable(**kwargs)],
            key=lambda x: x.start)

        # video can be totally stable ( nothing changed )
        # or only one unstable range
        if len(change_range_list) <= 1:
            return change_range_list

        # merge
        i = 0
        merged_change_range_list = list()
        while i < len(change_range_list) - 1:
            cur = change_range_list[i]
            while cur.can_merge(change_range_list[i + 1], **kwargs):
                # can be merged
                i += 1
                cur = cur.merge(change_range_list[i], **kwargs)

                # out of range
                if i + 1 >= len(change_range_list):
                    break
            merged_change_range_list.append(cur)
            i += 1
        if change_range_list[-1].start > merged_change_range_list[-1].end:
            merged_change_range_list.append(change_range_list[-1])

        if limit:
            merged_change_range_list = self._length_filter(merged_change_range_list, limit)
        # merged range check
        if range_threshold:
            merged_change_range_list = [i for i in merged_change_range_list if not i.is_loop(range_threshold)]
        logger.debug(f'unstable range of [{self.video.path}]: {merged_change_range_list}')
        return merged_change_range_list

    def get_range(self,
                  limit: int = None,
                  **kwargs) -> typing.Tuple[typing.List[VideoCutRange], typing.List[VideoCutRange]]:
        """
        return stable_range_list and unstable_range_list

        :param limit: ignore some ranges which are too short, 5 means ignore unstable ranges which length < 5
        :param kwargs:
            threshold: float, 0-1, default to 0.95. decided whether a range is stable. larger => more unstable ranges
            range_threshold:
                same as threshold, but it decided whether a merged range is stable.
                see https://github.com/williamfzc/stagesepx/issues/17 for details
            offset:
                it will change the way to decided whether two ranges can be merged
                before: first_range.end == second_range.start
                after: first_range.end + offset >= secord_range.start
        :return:
        """

        """
        videos have 4 kinds of status:
        
            - stable start + stable end (usually)
            - stable start + unstable end
            - unstable start + stable end
            - unstable start + unstable end
            
        so, unstable range list can be:
        
            - start > 0, end < frame_count
            - start = 0, end < frame_count
            - start > 0, end = frame_count
            - start = 0, end = frame_count
        """
        unstable_range_list = self.get_unstable_range(limit, **kwargs)

        # it is not a real frame (not existed)
        # just take it as a beginning
        # real frame id is started with 1, with non-zero timestamp
        video_start_frame_id = 0
        video_start_timestamp = 0.

        video_end_frame_id = self.range_list[-1].end
        video_end_timestamp = self.range_list[-1].end_time

        # stable all the time
        if len(unstable_range_list) == 0:
            logger.warning('no unstable stage detected, seems nothing happened in your video')
            return (
                # stable
                [VideoCutRange(
                    self.video,
                    video_start_frame_id,
                    video_end_frame_id,
                    [1.],
                    video_start_timestamp,
                    video_end_timestamp
                )],
                # unstable
                [],
            )

        # ATTENTION: +1 and -1 easily cause error
        # end of first stable range == start of first unstable range
        first_stable_range_end_id = unstable_range_list[0].start - 1
        # start of last stable range == end of last unstable range
        end_stable_range_start_id = unstable_range_list[-1].end + 1

        # IMPORTANT: len(ssim_list) + 1 == video_end_frame_id
        range_list: typing.List[VideoCutRange] = list()
        # stable start
        if first_stable_range_end_id >= 1:
            logger.debug(f'stable start')
            range_list.append(
                VideoCutRange(
                    self.video,
                    video_start_frame_id,
                    first_stable_range_end_id,
                    [1.],
                    video_start_timestamp,
                    self.get_target_range_by_id(first_stable_range_end_id).start_time,
                )
            )
        # unstable start
        else:
            logger.debug('unstable start')

        # stable end
        if end_stable_range_start_id <= video_end_frame_id:
            logger.debug('stable end')
            range_list.append(
                VideoCutRange(
                    self.video,
                    end_stable_range_start_id,
                    video_end_frame_id,
                    [1.],
                    self.get_target_range_by_id(end_stable_range_start_id).end_time,
                    video_end_timestamp,
                )
            )
        # unstable end
        else:
            logger.debug('unstable end')

        # diff range
        for i in range(len(unstable_range_list) - 1):
            range_start_id = unstable_range_list[i].end + 1
            range_end_id = unstable_range_list[i + 1].start - 1
            range_list.append(
                VideoCutRange(
                    self.video,
                    range_start_id,
                    range_end_id,
                    [1.],
                    self.get_target_range_by_id(range_start_id).start_time,
                    self.get_target_range_by_id(range_end_id).end_time,
                )
            )

        # remove some ranges, which is limit
        if limit:
            range_list = self._length_filter(range_list, limit)
        logger.debug(f'stable range of [{self.video.path}]: {range_list}')
        stable_range_list = sorted(range_list, key=lambda x: x.start)
        return stable_range_list, unstable_range_list

    def get_stable_range(self, limit: int = None, **kwargs) -> typing.List[VideoCutRange]:
        """ return stable range only """
        return self.get_range(limit, **kwargs)[0]

    def thumbnail(self,
                  target_range: VideoCutRange,
                  to_dir: str = None,
                  compress_rate: float = None,
                  is_vertical: bool = None) -> np.ndarray:
        """
        build a thumbnail, for easier debug or something else

        :param target_range: VideoCutRange
        :param to_dir: your thumbnail will be saved to this path
        :param compress_rate: float, 0 - 1, about thumbnail's size, default to 0.1 (1/10)
        :param is_vertical: direction
        :return:
        """
        if not compress_rate:
            compress_rate = 0.1
        # direction
        if is_vertical:
            stack_func = np.vstack
        else:
            stack_func = np.hstack

        frame_list = list()
        with toolbox.video_capture(self.video.path) as cap:
            toolbox.video_jump(cap, target_range.start)
            ret, frame = cap.read()
            count = 1
            length = target_range.get_length()
            while ret and count <= length:
                frame = toolbox.compress_frame(frame, compress_rate)
                frame_list.append(frame)
                ret, frame = cap.read()
                count += 1
        merged = stack_func(frame_list)

        # create parent dir
        if to_dir:
            target_path = os.path.join(to_dir, f'thumbnail_{target_range.start}-{target_range.end}.png')
            cv2.imwrite(target_path, merged)
            logger.debug(f'save thumbnail to {target_path}')
        return merged

    def pick_and_save(self,
                      range_list: typing.List[VideoCutRange],
                      frame_count: int,
                      to_dir: str = None,

                      # in kwargs
                      # compress_rate: float = None,
                      # target_size: typing.Tuple[int, int] = None,
                      # to_grey: bool = None,

                      *args, **kwargs) -> str:
        """
        pick some frames from range, and save them as files

        :param range_list: VideoCutRange list
        :param frame_count: default to 3, and finally you will get 3 frames for each range
        :param to_dir: will saved to this path
        :param args:
        :param kwargs:
        :return:
        """
        stage_list = list()
        for index, each_range in enumerate(range_list):
            picked = each_range.pick(frame_count, *args, **kwargs)
            logger.info(f'pick {picked} in range {each_range}')
            stage_list.append((index, picked))

        # create parent dir
        if not to_dir:
            to_dir = toolbox.get_timestamp_str()
        os.makedirs(to_dir, exist_ok=True)

        for each_stage_id, each_frame_list in stage_list:
            # create sub dir
            each_stage_dir = os.path.join(to_dir, str(each_stage_id))
            os.makedirs(each_stage_dir, exist_ok=True)

            with toolbox.video_capture(self.video.path) as cap:
                for each_frame_id in each_frame_list:
                    each_frame_path = os.path.join(each_stage_dir, f'{uuid.uuid4()}.png')
                    each_frame = toolbox.get_frame(cap, each_frame_id - 1)
                    each_frame = toolbox.compress_frame(each_frame, **kwargs)
                    cv2.imwrite(each_frame_path, each_frame)
                    logger.debug(f'frame [{each_frame_id}] saved to {each_frame_path}')

        return to_dir
