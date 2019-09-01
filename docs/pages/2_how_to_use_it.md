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

## 为你的业务建立稳定的视频分析服务

参见 [这里](https://github.com/williamfzc/stagesepx/tree/master/example#训练与预测)

## 视频比较（实验性质）

参见 [这里](https://github.com/williamfzc/stagesepx/tree/master/example#视频比较实验性质)

## 命令行使用（>=0.6.1）

?> 该功能旨在面向较为通用的场景提供一种简单的使用方式。较为复杂的场景还是推荐使用脚本实现。

在 0.6.1 之后，stagesepx支持直接从命令行启动。你可以不需要编写脚本直接使用。下面的例子是分析 demo.mp4 并将结果输出到 output 中。

```bash
stagesepx one_step ./demo.mp4 ./output
```

当然，它同样支持不少参数：

```bash
Usage: stagesepx one_step VIDEO_PATH <flags>
  optional flags:        --output_path | --threshold | --frame_count |
                         --compress_rate | --limit

For detailed information on this command, run:
  stagesepx one_step --help
```
