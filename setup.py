import io
import pathlib
import re

from setuptools import setup

version = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    io.open('phantomconfig/__init__.py', encoding='utf_8_sig').read(),
).group(1)

here = pathlib.Path(__file__).parent
long_description = (here / 'README.md').read_text()
install_requires = (here / 'requirements.txt').read_text()

setup(
    name='phantomconfig',
    version=version,
    author='Daniel Mentiplay',
    packages=['phantomconfig'],
    url='http://github.com/dmentipl/phantom-config',
    license='MIT',
    description='Phantom config files: parse, convert, modify, and generate.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=install_requires,
)
