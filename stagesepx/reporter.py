import typing
from pyecharts.charts import Line, Bar, Page
from pyecharts import options as opts
from loguru import logger

from stagesepx.classifier import ClassifierResult
from stagesepx import toolbox


class Reporter(object):
    __TITLE__ = 'stagesep-x report'

    @classmethod
    def draw(cls, data_list: typing.List[ClassifierResult], report_path: str = None):
        x_axis = [str(i.timestamp) for i in data_list]
        y_axis = [i.stage for i in data_list]

        line = Line()
        line.add_xaxis(x_axis)
        line.add_yaxis("stage",
                       y_axis,
                       is_step=True,
                       is_symbol_show=True)
        line.set_global_opts(
            title_opts=opts.TitleOpts(title=cls.__TITLE__),

            toolbox_opts=opts.ToolboxOpts(is_show=True),
            tooltip_opts=opts.TooltipOpts(is_show=True, trigger='axis', axis_pointer_type='cross'),
        )

        bar = Bar()
        x_axis = sorted(list(set([i.stage for i in data_list])))
        bar.add_xaxis(x_axis)
        y_axis = list()
        for each_stage_name in x_axis:
            each_stage = sorted([i for i in data_list if i.stage == each_stage_name], key=lambda x: x.frame_id)
            time_cost = each_stage[-1].timestamp - each_stage[0].timestamp
            y_axis.append(time_cost)
        bar.add_yaxis('time cost', y_axis)
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="Time Cost"),
        )
        logger.debug(f'time cost: {dict(zip(x_axis, y_axis))}')

        page = Page(page_title=cls.__TITLE__)
        page.add(line)
        page.add(bar)

        if not report_path:
            report_path = f'{toolbox.get_timestamp_str()}.html'
        logger.info(f'save report to {report_path}')
        page.render(path=report_path)
