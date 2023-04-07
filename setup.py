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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
    install_requires=[
        "opencv-python>=4.1.2.30",
        "opencv-contrib-python>=4.1.2.30",
        "moviepy>=1.0.3",
        "imageio>=2.5.0",
        "imageio-ffmpeg>=0.4.7",
        "numpy>=0.18.0",
        "loguru>=0.2.5",
        "scikit-image>=0.16.0",
        "scikit-learn>=0.21.0",
        "pyecharts>=1.3.1",
        "findit>=0.5.8",
        "Jinja2>=3.0.3",
        "MarkupSafe>=2.1.1;python_version>='3.7'",
        "MarkupSafe==2.0.1;python_version<'3.7'",
        "fire>=0.2.1",
        "keras>=2.3.1",
        "pydantic>=0.32.2",
    ],
    entry_points={"console_scripts": ["stagesepx = stagesepx.cli:main"]},
)
