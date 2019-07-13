import typing
from pyecharts.charts import Line
from loguru import logger

from stagesepx.classifier import ClassifierResult
from stagesepx import toolbox


class Reporter(object):

    @classmethod
    def draw(cls, data_list: typing.List[ClassifierResult], report_path: str = None):
        x_axis = [i.frame_id for i in data_list]
        y_axis = [i.stage for i in data_list]
        line = Line()\
            .add_xaxis(x_axis)\
            .add_yaxis("stage", y_axis, is_step=True, is_symbol_show=True)
        if not report_path:
            report_path = f'{toolbox.get_timestamp_str()}.html'
        logger.debug(f'save report to {report_path}')
        line.render(path=report_path)
