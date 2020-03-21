import os
import typing
import json
import numpy as np
from jinja2 import Markup, Template
from pyecharts.charts import Line, Bar, Page
from pyecharts import options as opts
from loguru import logger

from stagesepx.classifier import ClassifierResult, SingleClassifierResult
from stagesepx import toolbox
from stagesepx import constants
from stagesepx.cutter import VideoCutResult, VideoCutRange
from stagesepx.video import VideoFrame
from stagesepx import __VERSION__

# load template
template_dir_path = os.path.join(os.path.dirname(__file__), "template")
template_path = os.path.join(template_dir_path, "report.html")


def get_template() -> str:
    with open(template_path, encoding=constants.CHARSET) as t:
        template = t.read()
    return template


class Reporter(object):
    # 3 status:
    # - `stable` means nothing happened (nearly) during this period
    # - `unstable` means something happened
    # - `unspecific` means your model has no idea about `which class this frame should be` (lower than threshold)
    LABEL_STABLE: str = "stable"
    LABEL_UNSTABLE: str = "unstable"
    # unknown stage actually
    LABEL_UNSPECIFIC: str = "unspecific"

    def __init__(self):
        self.thumbnail_list: typing.List[typing.Tuple[str, str]] = list()
        self.extra_dict: typing.Dict[str, str] = dict()

    def add_thumbnail(self, name: str, pic_object: np.ndarray):
        """
        add picture object (cv2) to your report

        :param name:
        :param pic_object:
        :return:
        """
        b64_str = toolbox.np2b64str(pic_object)
        self.thumbnail_list.append((name, b64_str))

    def add_extra(self, name: str, value: str):
        """
        add some extra info ( key-value part) to your report

        :param name:
        :param value:
        :return:
        """
        self.extra_dict[name] = value

    @staticmethod
    def _draw_line(result: ClassifierResult) -> Line:
        # draw line chart
        x_axis = [str(i) for i in result.get_timestamp_list()]
        y_axis = result.get_stage_list()

        line = Line(init_opts=opts.InitOpts(bg_color=constants.BACKGROUND_COLOR))
        line.add_xaxis(x_axis)
        line.add_yaxis("stage", y_axis, is_step=False, is_symbol_show=True)
        line.set_global_opts(
            title_opts=opts.TitleOpts(
                title="Trend", subtitle="describe how these stages switching"
            ),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="cross"
            ),
            brush_opts=opts.BrushOpts(x_axis_index="all", tool_box=["lineX"]),
        )
        return line

    @staticmethod
    def _draw_sim(data: VideoCutResult) -> Line:
        x_axis = [str(i.start) for i in data.range_list]
        ssim_axis = [i.ssim for i in data.range_list]
        mse_axis = [i.mse for i in data.range_list]
        psnr_axis = [i.psnr for i in data.range_list]

        line = Line(init_opts=opts.InitOpts(bg_color=constants.BACKGROUND_COLOR))
        line.add_xaxis(x_axis)
        line.add_yaxis("ssim", ssim_axis)
        line.add_yaxis("mse", mse_axis)
        line.add_yaxis("psnr", psnr_axis)
        line.set_global_opts(
            title_opts=opts.TitleOpts(title="SIM"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="cross"
            ),
        )
        line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        return line

    @staticmethod
    def _draw_bar(result: ClassifierResult) -> Bar:
        # draw bar chart
        bar = Bar(init_opts=opts.InitOpts(bg_color=constants.BACKGROUND_COLOR))
        x_axis = sorted(list(result.get_stage_set()))
        y_axis = list()
        offset = result.get_offset()
        for each_stage_name in x_axis:
            ranges = result.get_specific_stage_range(each_stage_name)
            time_cost: float = 0.0
            for each in ranges:
                # last frame - first frame
                time_cost += each[-1].timestamp - each[0].timestamp + offset
            y_axis.append(time_cost)

        bar.add_xaxis(x_axis)
        bar.add_yaxis("time cost", y_axis)
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="Time Cost", subtitle="... of each stages"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
        )
        logger.debug(f"time cost: {dict(zip(x_axis, y_axis))}")
        return bar

    @staticmethod
    def get_stable_stage_sample_frame_list(
        result: ClassifierResult, *args, **kwargs
    ) -> typing.List[VideoFrame]:
        # VideoFrame: with data
        # SingleClassifierResult: without data
        last = result.data[0]
        picked: typing.List[SingleClassifierResult] = [last]
        for each in result.data:
            # ignore unstable stage
            if not each.is_stable():
                continue
            if last.stage != each.stage:
                last = each
                picked.append(each)

        return [each.to_video_frame(*args, **kwargs) for each in picked]

    @classmethod
    def get_stable_stage_sample(
        cls, result: ClassifierResult, *args, **kwargs
    ) -> np.ndarray:
        def get_split_line(f):
            return np.zeros((f.shape[0], 5))

        frame_list: typing.List[np.ndarray] = list()
        for each in cls.get_stable_stage_sample_frame_list(result, *args, **kwargs):
            frame_list.append(each.data)
            frame_list.append(get_split_line(each.data))
        return np.hstack(frame_list)

    @classmethod
    def save(cls, to_file: str, result: ClassifierResult):
        assert not os.path.isfile(to_file), f"file {to_file} already existed"
        data = [i.to_dict() for i in result.data]
        with open(to_file, "w", encoding=constants.CHARSET) as f:
            json.dump(data, f)

    @classmethod
    def load(cls, from_file: str) -> ClassifierResult:
        assert os.path.isfile(from_file), f"file {from_file} not existed"
        with open(from_file, encoding=constants.CHARSET) as f:
            content = json.load(f)
        return ClassifierResult([SingleClassifierResult(**each) for each in content])

    def draw(
        self,
        classifier_result: ClassifierResult,
        report_path: str = None,
        unstable_ranges: typing.List[VideoCutRange] = None,
        cut_result: VideoCutResult = None,
        compress_rate: float = None,
        *_,
        **__,
    ):
        """
        draw report file

        :param classifier_result: classifierResult, output of classifier
        :param report_path: your report will be there
        :param unstable_ranges: for marking unstable ranges
        :param cut_result: more charts would be built
        :param compress_rate:
        :return:
        """
        # default: compress_rate
        if not compress_rate:
            compress_rate = 0.2
        if not unstable_ranges:
            unstable_ranges = []

        # draw
        line = self._draw_line(classifier_result)
        bar = self._draw_bar(classifier_result)

        # merge charts
        page = Page()
        page.add(line)
        page.add(bar)

        # insert pictures
        if cut_result:
            # sim chart
            sim_line = self._draw_sim(cut_result)
            page.add(sim_line)

        # mark range
        for each in unstable_ranges:
            classifier_result.mark_range_unstable(each.start, each.end)

        offset = classifier_result.get_offset()
        stage_range = classifier_result.get_stage_range()
        for cur_index in range(len(stage_range)):
            each = stage_range[cur_index]
            middle = each[len(each) // 2]
            if middle.is_stable():
                label = self.LABEL_STABLE
                frame = toolbox.compress_frame(
                    middle.get_data(), compress_rate=compress_rate
                )
            else:
                # todo: looks not good enough. `unspecific` looks a little weird but I have no idea now
                if middle.stage == constants.UNKNOWN_STAGE_FLAG:
                    label = self.LABEL_UNSPECIFIC
                else:
                    label = self.LABEL_UNSTABLE
                # add a frame
                if cur_index + 1 < len(stage_range):
                    new_each = [*each, stage_range[cur_index + 1][0]]
                else:
                    new_each = each
                frame = np.hstack(
                    [
                        toolbox.compress_frame(
                            i.get_data(), compress_rate=compress_rate
                        )
                        for i in new_each
                    ]
                )

            first, last = each[0], each[-1]
            self.add_thumbnail(
                f"{label} range {first.frame_id}({first.timestamp}) - {last.frame_id}({last.timestamp + offset}), "
                f"duration: {last.timestamp - first.timestamp + offset}",
                frame,
            )
        # calc time cost
        cost_dict = classifier_result.calc_changing_cost()

        # time stamp
        timestamp = toolbox.get_timestamp_str()

        # video
        self.add_extra("video path", classifier_result.video_path)
        self.add_extra("frame count", str(classifier_result.get_length()))
        self.add_extra("offset between frames", str(classifier_result.get_offset()))

        # insert extras
        template = Template(get_template())
        template_content = template.render(
            chart=Markup(page.render_embed()),
            thumbnail_list=self.thumbnail_list,
            extras=self.extra_dict,
            background_color=constants.BACKGROUND_COLOR,
            cost_dict=cost_dict,
            timestamp=timestamp,
            version_code=__VERSION__,
        )

        # save to file
        if not report_path:
            report_path = f"{timestamp}.html"
        with open(report_path, "w", encoding=constants.CHARSET) as fh:
            fh.write(template_content)
        logger.info(f"save report to {report_path}")
