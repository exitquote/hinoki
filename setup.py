#! /usr/bin/python3

#import hinoki.sensuapi
#import hinoki.config
#import argparse


import setuptools
import os

# config_file = os.path.join(os.path.expanduser('~'), '.sensusync/test_config.yml')
# print(config_file)

setuptools.setup(
    version="0.0.1",
    long_description_content_type="text/markdown",
    keywords = ['hinoki'],
    url="https://github.com/exitquote/hinoki",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires = [
        'requests',
        'PyYAML',
        'urllib3',
        'click'
    ]
)