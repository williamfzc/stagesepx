from setuptools import setup, find_packages
from stagesepx import (
    __AUTHOR__,
    __AUTHOR_EMAIL__,
    __URL__,
    __LICENSE__,
    __VERSION__,
    __PROJECT_NAME__,
    __DESCRIPTION__,
)

setup(
    name=__PROJECT_NAME__,
    version=__VERSION__,
    description=__DESCRIPTION__,
    author=__AUTHOR__,
    author_email=__AUTHOR_EMAIL__,
    url=__URL__,
    packages=find_packages(),
    include_package_data=True,
    license=__LICENSE__,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.6,<3.8",
    install_requires=[
        "opencv-python>=4.1.0.25",
        "opencv-contrib-python==3.4.2.17",
        "numpy>=0.16.2",
        "loguru>=0.2.5",
        "scikit-image>=0.16.0",
        "scikit-learn>=0.21.0",
        "pyecharts>=1.3.1",
        "findit>=0.5.6",
        "Jinja2>=2.10.1",
        "fire>=0.2.1",
    ],
    entry_points={"console_scripts": ["stagesepx = stagesepx.cli:main"]},
)
