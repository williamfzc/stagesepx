import typing
import numpy as np
from jinja2 import Markup, Template
from base64 import b64encode
import cv2
from pyecharts.charts import Line, Bar, Page
from pyecharts import options as opts
from loguru import logger

from stagesepx.classifier import ClassifierResult
from stagesepx import toolbox

TEMPLATE = r'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>stagesep-x report</title>
    <link rel="stylesheet" href="https://cdn.staticfile.org/twitter-bootstrap/4.1.0/css/bootstrap.min.css">
    <script src="https://cdn.staticfile.org/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://cdn.staticfile.org/popper.js/1.12.5/umd/popper.min.js"></script>
    <script src="https://cdn.staticfile.org/twitter-bootstrap/4.1.0/js/bootstrap.min.js"></script>
</head>

<style>
    .container {
        margin: 20px;
    }
    .footer {
        margin-bottom: 20px;
    }
</style>

<body>
<nav class="navbar navbar-dark bg-dark">
    <a class="navbar-brand" href="https://github.com/williamfzc/stagesepx">stagesep x report</a>
</nav>

{% if dir_link_list %}
<div class="container">
    <div class="card border-light">
        <div class="card-body">
            <h2>Raw Pictures</h2>
            <ul>
                {% for each_link in dir_link_list %}
                <li>
                    <a href="{{ each_link }}">{{ each_link }}</a>
                </li>
                {% endfor %}
            </ul>
        </div>
    </div>
</div>
{% endif %}

{% if thumbnail_list %}
<div class="container">
    <div class="card border-light">
        <div class="card-body">
            <h2>Thumbnail</h2>
            <ul>
                {% for name, each_thumbnail in thumbnail_list %}
                <li>
                    <h3> {{ name }} </h3>
                    <img src="data:image/png;base64,{{ each_thumbnail }}"/>
                </li>
                {% endfor %}
            </ul>
        </div>
    </div>
</div>
{% endif %}

{% if extras %}
<div class="container">
    <div class="card border-light">
        <div class="card-body">
            <h2>Extras</h2>
            {% for name, value in extras.items() %}
            <h3> {{ name }} </h3>
            <p> {{ value }} </p>
            {% endfor %}
        </div>
    </div>
</div>
{% endif %}

<div class="container">
    <div class="card border-light">
        <div class="card-body">
            <h2>Charts</h2>
            <div>
                {{ chart }}
            </div>
        </div>
    </div>
</div>

<footer class="footer" style="text-align:center">
    <div class="container-fluid">
        <HR>
        <span class="text-muted">
            Build with <a href="https://github.com/williamfzc/stagesepx">@stagesepx</a> :)
        </span>
    </div>
</footer>

</body>
</html>
'''


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
        buffer = cv2.imencode(".png", pic_object)[1].tostring()
        b64_str = b64encode(buffer).decode()
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
    def _draw_line(data_list: typing.List[ClassifierResult]) -> Line:
        # draw line chart
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
        return line

    @staticmethod
    def _draw_bar(data_list: typing.List[ClassifierResult]) -> Bar:
        # draw bar chart
        bar = Bar()
        x_axis = sorted(list(set([i.stage for i in data_list])))
        y_axis = list()
        offset = data_list[1].timestamp - data_list[0].timestamp
        for each_stage_name in x_axis:
            each_stage = sorted([i for i in data_list if i.stage == each_stage_name], key=lambda x: x.frame_id)
            time_cost = each_stage[-1].timestamp - each_stage[0].timestamp + offset
            y_axis.append(time_cost)

        bar.add_xaxis(x_axis)
        bar.add_yaxis('time cost', y_axis)
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="Time Cost"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
        )
        logger.debug(f'time cost: {dict(zip(x_axis, y_axis))}')
        return bar

    def draw(self,
             data_list: typing.List[ClassifierResult],
             report_path: str = None):
        """
        draw report file

        :param data_list: classifierResult list, output of classifier
        :param report_path: your report will be there
        :return:
        """

        # draw
        line = self._draw_line(data_list)
        bar = self._draw_bar(data_list)

        # merge charts
        page = Page()
        page.add(line)
        page.add(bar)

        # insert extras
        template = Template(TEMPLATE)
        template_content = template.render(
            chart=Markup(page.render_embed()),
            dir_link_list=self.dir_link_list,
            thumbnail_list=self.thumbnail_list,
            extras=self.extra_dict,
        )

        # save to file
        if not report_path:
            report_path = f'{toolbox.get_timestamp_str()}.html'
        with open(report_path, "w") as fh:
            fh.write(template_content)
        logger.info(f'save report to {report_path}')
