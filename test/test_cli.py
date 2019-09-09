from loguru import logger
import subprocess
import os
import shutil

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, 'demo.mp4')


def test_cli():
    logger.info('checking one_step ...')
    subprocess.check_call(['stagesepx', 'one_step', VIDEO_PATH], shell=True)
    subprocess.check_call(['stagesepx', 'one_step', VIDEO_PATH, 'output'], shell=True)
    shutil.rmtree('output')

    logger.info('checking cutter ...')
    subprocess.check_call(['stagesepx', 'cut', VIDEO_PATH], shell=True)
    subprocess.check_call(['stagesepx', 'cut', VIDEO_PATH, 'output'], shell=True)

    logger.info('checking classifier ...')
    subprocess.check_call(['stagesepx', 'classify', VIDEO_PATH, 'output'], shell=True)
    shutil.rmtree('output')

# same as:
# stagesepx one_step ./demo.mp4
# stagesepx one_step ./demo.mp4 ./output
# rm -rf ./output
#
# stagesepx cut ./demo.mp4
# stagesepx cut ./demo.mp4 ./output
# stagesepx classify ./demo.mp4 ./output
