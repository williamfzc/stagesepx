from setuptools import setup, find_packages

setup(
    name='stagesepx',
    version='0.4.2',
    description='detect stages in video automatically',
    author='williamfzc',
    author_email='fengzc@vip.qq.com',
    url='https://github.com/williamfzc/stagesepx',
    packages=find_packages(),
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
        'opencv-python',
        'opencv-contrib-python==3.4.2.17',
        'numpy',
        'loguru',
        'scikit-image',
        'scikit-learn',
        'pyecharts',
        'findit',
        'jinja2',
    ]
)
