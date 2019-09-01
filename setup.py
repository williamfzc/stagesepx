from setuptools import setup, find_packages

setup(
    name='stagesepx',
    version='0.6.1',
    description='detect stages in video automatically',
    author='williamfzc',
    author_email='fengzc@vip.qq.com',
    url='https://github.com/williamfzc/stagesepx',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires=">=3.6",
    install_requires=[
        'opencv-python>=4.1.0.25',
        'opencv-contrib-python==3.4.2.17',
        'numpy>=0.16.2',
        'loguru>=0.2.5',
        'scikit-image>=0.14.2',
        'scikit-learn>=0.21.0',
        'pyecharts>=1.3.1',
        'findit>=0.5.6',
        'Jinja2>=2.10.1',
        'fire>=0.2.1',
    ],
    entry_points={
        "console_scripts": [
            "stagesepx = stagesepx.cli:main",
        ],
    },
)
