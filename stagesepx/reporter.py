import typing
from pyecharts.charts import Line, Bar, Grid
from pyecharts import options as opts
from loguru import logger

from stagesepx.classifier import ClassifierResult
from stagesepx import toolbox


class Reporter(object):
    __TITLE__ = 'stagesep-x report'

    @classmethod
    def draw(cls, data_list: typing.List[ClassifierResult], report_path: str = None):
        x_axis = [i.frame_id for i in data_list]
        y_axis = [i.stage for i in data_list]

        # ugly chained call ...
        line = Line() \
            .add_xaxis(x_axis) \
            .add_yaxis("stage", y_axis, is_step=True, is_symbol_show=True) \
            .set_global_opts(title_opts=opts.TitleOpts(title=cls.__TITLE__))

        x_axis = sorted(list(set([i.stage for i in data_list])))
        bar = Bar() \
            .add_xaxis(x_axis)
        y_axis = list()
        for each_stage_name in x_axis:
            each_stage = sorted([i for i in data_list if i.stage == each_stage_name], key=lambda x: x.frame_id)
            time_cost = each_stage[-1].timestamp - each_stage[0].timestamp
            y_axis.append(time_cost)
        bar.add_yaxis('time cost', y_axis)
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="Time Cost", pos_top="48%"),
            legend_opts=opts.LegendOpts(pos_top="48%"),
        )
        logger.debug(f'time cost: {dict(zip(x_axis, y_axis))}')

        grid = Grid() \
            .add(line, grid_opts=opts.GridOpts(pos_bottom="60%")) \
            .add(bar, grid_opts=opts.GridOpts(pos_top="60%"))

        if not report_path:
            report_path = f'{toolbox.get_timestamp_str()}.html'
        logger.info(f'save report to {report_path}')
        grid.render(path=report_path)
