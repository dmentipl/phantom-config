"""Phantom-config setup.py."""

import io
import pathlib
import re

from setuptools import setup

version = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    io.open('phantomconfig/__init__.py', encoding='utf_8_sig').read(),
).group(1)

description = (
    'phantom-config: parse, convert, modify, and generate Phantom config files'
)
long_description = (pathlib.Path(__file__).parent / 'README.md').read_text()

setup(
    name='phantomconfig',
    version=version,
    author='Daniel Mentiplay',
    author_email='d.mentiplay@gmail.com',
    packages=['phantomconfig'],
    url='http://github.com/dmentipl/phantom-config',
    license='MIT',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['tomlkit'],
    python_requires='>=3.7',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
)
