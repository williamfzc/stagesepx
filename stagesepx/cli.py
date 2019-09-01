import fire
import os

from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SVMClassifier
from stagesepx.reporter import Reporter


class TerminalCli(object):
    """ this is a client for stagesepx, for easier usage. """

    def one_step(self, video_path: str, output_path: str = None):
        # --- cutter ---
        cutter = VideoCutter()
        res = cutter.cut(video_path)
        stable, unstable = res.get_range()

        data_home = res.pick_and_save(stable, 5, to_dir=output_path)

        # --- classify ---

        cl = SVMClassifier()
        cl.load(data_home)
        cl.train()
        classify_result = cl.classify(video_path, stable)

        # --- draw ---
        r = Reporter()
        r.add_dir_link(data_home)
        r.draw(
            classify_result,
            report_path=os.path.join(data_home, 'report.html'),
            cut_result=res,
        )


def main():
    fire.Fire(TerminalCli)


if __name__ == '__main__':
    main()
