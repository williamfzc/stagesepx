import fire

from stagesepx import __PROJECT_NAME__, __VERSION__, __URL__
from stagesepx import api


class TerminalCli(object):
    __doc__ = f"""
    {__PROJECT_NAME__} version {__VERSION__}

    this is a client for stagesepx, for easier usage.
    for much more flexible functions, you 'd better use the script way.
    more detail: {__URL__}
    """

    # this layer was built for (pre) controlling args and kwargs
    # or, some translations, default value, and so on
    one_step = staticmethod(api.one_step)
    train = staticmethod(api.keras_train)


def main():
    fire.Fire(TerminalCli)


if __name__ == "__main__":
    main()
