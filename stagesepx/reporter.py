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
from stagesepx.cutter import VideoCutResult
from stagesepx import __VERSION__

# load template
template_dir_path = os.path.join(os.path.dirname(__file__), "template")
template_path = os.path.join(template_dir_path, "report.html")
template_zh_path = os.path.join(template_dir_path, "report_zh.html")


def get_template(lang: str) -> str:
    lang_dict = {"en": template_path, "zh": template_zh_path}
    assert lang in lang_dict, f"template {lang} not found"
    with open(lang_dict[lang], encoding=constants.CHARSET) as t:
        template = t.read()
    return template


class Reporter(object):
    def __init__(self):
        self.dir_link_list: typing.List[str] = list()
        self.thumbnail_list: typing.List[typing.Tuple[str, str]] = list()
        self.extra_dict: typing.Dict[str, str] = dict()

    def add_dir_link(self, data_path: str):
        """
        add relative dir (or file) link to your report

        :param data_path:
        :return:
        """
        self.dir_link_list.append(data_path)

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
        x_axis = result.get_timestamp_list()
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
            each_stage = result.get_specific_stage(each_stage_name)
            # last frame - first frame
            time_cost = each_stage[-1].timestamp - each_stage[0].timestamp + offset
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
    def get_stable_stage_sample(
        result: ClassifierResult, *args, **kwargs
    ) -> np.ndarray:
        last = result.data[0]
        picked: typing.List[SingleClassifierResult] = [last]
        for each in result.data:
            # ignore unstable stage
            if each.stage == constants.UNSTABLE_FLAG:
                continue
            if last.stage != each.stage:
                last = each
                picked.append(each)

        def get_split_line(f):
            return np.zeros((f.shape[0], 5))

        with toolbox.video_capture(last.video_path) as cap:
            frame_list: typing.List[np.ndarray] = []
            for each in picked:
                frame = toolbox.get_frame(cap, each.frame_id)
                frame = toolbox.compress_frame(frame, *args, **kwargs)
                split_line = get_split_line(frame)
                frame_list.append(frame)
                frame_list.append(split_line)
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
        cut_result: VideoCutResult = None,
        language: str = None,
        *args,
        **kwargs,
    ):
        """
        draw report file

        :param classifier_result: classifierResult, output of classifier
        :param report_path: your report will be there
        :param cut_result: more charts would be built
        :param language: 'en' or 'zh'
        :return:
        """

        # draw
        line = self._draw_line(classifier_result)
        bar = self._draw_bar(classifier_result)

        # merge charts
        page = Page()
        page.add(line)
        page.add(bar)

        # calc time cost
        cost_dict = classifier_result.calc_changing_cost()

        # insert pictures
        if cut_result:
            # sim chart
            sim_line = self._draw_sim(cut_result)
            page.add(sim_line)

            _, unstable = cut_result.get_range(*args, **kwargs)
            # insert thumbnail
            if not self.thumbnail_list:
                logger.debug("auto insert thumbnail ...")

                for each in unstable:
                    self.add_thumbnail(
                        f"{each.start}({each.start_time}) - {each.end}({each.end_time}), "
                        f"duration: {each.end_time - each.start_time}",
                        cut_result.thumbnail(each, *args, **kwargs),
                    )

        # insert stable frames
        stable_stage_sample = self.get_stable_stage_sample(classifier_result, compress_rate=0.2)
        stable_stage_sample = toolbox.np2b64str(stable_stage_sample)

        # time stamp
        timestamp = toolbox.get_timestamp_str()

        # insert extras
        # default: zh_cn report
        if not language:
            language = "zh"
        template = Template(get_template(language))
        template_content = template.render(
            chart=Markup(page.render_embed()),
            dir_link_list=self.dir_link_list,
            thumbnail_list=self.thumbnail_list,
            stable_sample=stable_stage_sample,
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
