"""
Parse Phantom config files
--------------------------

phantom_config is designed to read and write the Phantom config file
format. And to convert to and from JSON. Files usually have names like
prefix.in or prefix.setup.

Daniel Mentiplay, 2019.
"""

from .phantom_config import PhantomConfig


def read_dict(dictionary):
    return PhantomConfig(dictionary=dictionary)


def read_config(filename):
    return PhantomConfig(filename=filename, filetype='phantom')


def read_json(filename):
    return PhantomConfig(filename=filename, filetype='json')


__all__ = ['read_config', 'read_dict', 'read_json']
