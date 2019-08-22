import io
import pathlib
import re

from setuptools import setup

version = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    io.open('phantomconfig/__init__.py', encoding='utf_8_sig').read(),
).group(1)


def readfile(filename):
    with open(filename) as fp:
        contents = fp.read()
    return contents


setup(
    name='phantomconfig',
    version=version,
    author='Daniel Mentiplay',
    packages=['phantomconfig'],
    url='http://github.com/dmentipl/phantom-config',
    license='MIT',
    description='Phantom config files: parse, convert, modify, and generate.',
    long_description=readfile(pathlib.Path('README.md').resolve()),
    install_requires=readfile(pathlib.Path('requirements.txt').resolve()),
)
