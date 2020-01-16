<h1 align="center">
  <img src="./docs/pics/brand.svg">
</h1>

<h3 align="center">stage sep(aration) x</h3>
<p align="center">
    <em>detect stages in video automatically</em>
</p>

---

| Type                 | Status                                                                                                                                                                                            |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| package version      | [![PyPI version](https://badge.fury.io/py/stagesepx.svg)](https://badge.fury.io/py/stagesepx)                                                                                                    |
| python version       | ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stagesepx)                                                                                                                       |
| auto test            | ![CI Status](https://github.com/williamfzc/stagesepx/workflows/smoketest/badge.svg)                                                                                                              |
| code maintainability | [![Maintainability](https://api.codeclimate.com/v1/badges/ef27756ce9a4f7f4ba94/maintainability)](https://codeclimate.com/github/williamfzc/stagesepx/maintainability)                            |
| code coverage        | [![codecov](https://codecov.io/gh/williamfzc/stagesepx/branch/master/graph/badge.svg)](https://codecov.io/gh/williamfzc/stagesepx)                                                               |
| docker build status  | ![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/williamfzc/stagesepx) ![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/williamfzc/stagesepx) |
| code style           | [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)                                                                                 |

---

> For English users:
>
> Mainly we used Chinese in discussions and communications, so maybe the most of issues/document are wrote in Chinese currently.
>
> But don't worry:
> - maybe google translate is a good helper :)
> - read the code directly (all the code and comments are wrote in English)
> - feel free to contact with us via building a new issue with your questions
>
> Thanks !

---

This video shows the complete startup process of an app: 

![video_readme.gif](https://i.loli.net/2019/09/01/tXRhB6ai9jAZFmc.gif)

By sending this video to stagesepx, you would get a report like this automatically:

![taobao_startup.png](https://i.loli.net/2019/11/23/Cio39V4AhmWOyFL.png)

You can get the exact time consumption for each stage easily. Of course it is cross-platform, which can be also used in Android/Web/PC or something like that. Even, any platforms:

![sugar.gif](https://i.loli.net/2019/11/23/BCjI8PiJrgmxQUt.gif)

![sugar](https://i.loli.net/2019/11/23/DCpbdlNftcQ3v2w.png)

And precisely:

![accuracy.png](https://i.loli.net/2019/10/02/Cboj743UwRQmgPS.png)

As you can see, its result is very close to the timer.

---

- Fully automatic, no pre-training required
- Less code required
- Configurable for different scenes
- All you need is a video!

## Structure

![structure](./docs/pics/stagesepx.svg)

## Quick Start

> Translation is working in progress. But not ready. You can use something like google translate instead for now. Feel free to leave me a issue when you are confused.

- [30 lines demo](example/mini.py)
- [how to use it in production (in Chinese)](https://github.com/williamfzc/stagesepx/blob/master/README_en.md)
- [demo with all the features (in Chinese)](example/cut_and_classify.py)
- [i have some questions](https://github.com/williamfzc/stagesepx/issues/new)

## Installation

```bash
pip install stagesepx
```

## License

[MIT](LICENSE)

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fwilliamfzc%2Fstagesepx.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fwilliamfzc%2Fstagesepx?ref=badge_large)
