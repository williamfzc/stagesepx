import typing
import os
from jinja2 import Markup, Template
from pyecharts.charts import Line, Bar, Page, Pie
from pyecharts import options as opts
from loguru import logger

from stagesepx.classifier import ClassifierResult
from stagesepx import toolbox

TEMPLATE = r'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>stagesep-x report :)</title>
</head>
<body>
    <h1>stagesep-x report</h1>
    {% if pic_list %}
        <h2>Stage Pictures</h2>
            <ul>
                {% for each_pic_list in pic_list %}
                    <ul>
                        {% for each_pic in each_pic_list %}
                            <li><a href="{{ each_pic }}">{{ each_pic }}</a></li>
                        {% endfor %}
                    </ul>
                {% endfor %}
            </ul>
    {% endif %}
    
    <h2>Charts</h2>
    <div>
        {{ chart }}
    </div>
</body>
</html>
<body>

</body>
</html>
'''


class Reporter(object):
    @classmethod
    def draw(cls,
             data_list: typing.List[ClassifierResult],
             report_path: str = None,
             data_path: str = None):
        x_axis = [str(i.timestamp) for i in data_list]
        y_axis = [i.stage for i in data_list]

        line = Line()
        line.add_xaxis(x_axis)
        line.add_yaxis("stage",
                       y_axis,
                       is_step=True,
                       is_symbol_show=True)
        line.set_global_opts(
            title_opts=opts.TitleOpts(title='Trend'),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            tooltip_opts=opts.TooltipOpts(is_show=True, trigger='axis', axis_pointer_type='cross'),
        )

        bar = Bar()
        x_axis = sorted(list(set([i.stage for i in data_list])))
        bar.add_xaxis(x_axis)
        y_axis = list()
        offset = data_list[1].timestamp - data_list[0].timestamp
        for each_stage_name in x_axis:
            each_stage = sorted([i for i in data_list if i.stage == each_stage_name], key=lambda x: x.frame_id)
            time_cost = each_stage[-1].timestamp - each_stage[0].timestamp + offset
            y_axis.append(time_cost)
        bar.add_yaxis('time cost', y_axis)
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="Time Cost"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
        )
        logger.debug(f'time cost: {dict(zip(x_axis, y_axis))}')

        pie = Pie()
        pie.add('', [list(z) for z in zip(x_axis, y_axis)])
        pie.set_global_opts(
            toolbox_opts=opts.ToolboxOpts(is_show=True),
        )

        page = Page()
        page.add(line)
        page.add(bar)
        page.add(pie)

        if data_path and os.path.isdir(data_path):
            stage_list = [os.path.join(data_path, i) for i in os.listdir(data_path)]
            stage_list = [
                [os.path.join(i, j) for j in os.listdir(i)]
                for i in stage_list]
        else:
            logger.warning(f'data path {data_path} not existed')
            stage_list = []

        if not report_path:
            report_path = f'{toolbox.get_timestamp_str()}.html'
        logger.info(f'save report to {report_path}')

        template = Template(TEMPLATE)
        template_content = template.render(
            chart=Markup(page.render_embed()),
            pic_list=stage_list,
        )
        with open(report_path, "w") as fh:
            fh.write(template_content)
