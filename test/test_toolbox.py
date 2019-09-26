import os

from stagesepx import toolbox

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
IMAGE_NAME = "demo.jpg"
IMAGE_PATH = os.path.join(PROJECT_PATH, IMAGE_NAME)
assert os.path.isfile(IMAGE_PATH), f"{IMAGE_NAME} not existed!"


def test_turn_blur():
    image = toolbox.imread(IMAGE_PATH)
    grey = toolbox.turn_grey(image)
    toolbox.turn_blur(grey)


def test_turn_grey():
    image = toolbox.imread(IMAGE_PATH)
    toolbox.turn_grey(image)


def test_turn_binary():
    image = toolbox.imread(IMAGE_PATH)
    toolbox.turn_binary(image)


def test_turn_surf_desc():
    image = toolbox.imread(IMAGE_PATH)
    toolbox.turn_surf_desc(image)


def test_turn_lbp_desc():
    image = toolbox.imread(IMAGE_PATH)
    toolbox.turn_lbp_desc(image)
