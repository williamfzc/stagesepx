# 使用

## 安装

Python >= 3.6

```bash
pip install stagesepx
```

## 快速开始

?> sample code中提供了详细的注释。

[完整例子](https://github.com/williamfzc/stagesepx/tree/master/example#all-in-one) 包括了三个部分：拆分阶段、分析视频、生成报告。你可以用它快速开始试用 stagesepx。

例子中使用的视频可以[点此](https://raw.githubusercontent.com/williamfzc/stagesep2-sample/master/videos/demo.mp4)下载。

## 更多内容

你可以通过 [这个例子](https://github.com/williamfzc/stagesepx/tree/master/example/train_and_predict)：

- 了解如何训练一个针对特定业务的模型
    - 利用 cutter 从视频中自动拆分
    - 手工采集
- 利用训练好的模型，建立长期稳定的、回归性质的视频分析
- 当有业务变更时如何调整你的模型

## 命令行使用（>=0.6.1）

?> 该功能旨在面向较为通用的场景提供一种简单的使用方式。较为复杂的场景还是推荐使用脚本实现。

在 0.6.1 之后，stagesepx支持直接从命令行启动。你可以不需要编写脚本直接使用。下面的例子是分析 demo.mp4 并将结果输出到 output 中。

```bash
stagesepx one_step ./demo.mp4 ./output
```

它同样支持不少参数：

```bash
Usage: stagesepx one_step VIDEO_PATH <flags>
  optional flags:        --output_path | --threshold | --frame_count |
                         --compress_rate | --limit

For detailed information on this command, run:
  stagesepx one_step --help
```

你同样可以通过脚本调用 cli 中的方法，`one_step` 的功能几乎与 [完整例子](https://github.com/williamfzc/stagesepx/tree/master/example#all-in-one) 保持一致。

```python
from stagesepx.cli import TerminalCli

cli = TerminalCli()
cli.one_step('demo.mp4')
```
