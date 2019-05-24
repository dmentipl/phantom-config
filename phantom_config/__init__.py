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
    """
    Initialize PhantomConfig from a dictionary.

    Parameters
    ----------
    dictionary : dict
        A dictionary of the form:
            {'variable': [value, comment, block], ...}

    Returns
    -------
    PhantomConfig
        Generated from the dictionary.
    """
    return PhantomConfig(dictionary=dictionary)


def read_config(filename):
    """
    Initialize PhantomConfig from a Phantom config file.

    Parameters
    ----------
    filename : str or pathlib.Path
        The Phanton config file.

    Returns
    -------
    PhantomConfig
        Generated from the file.
    """
    return PhantomConfig(filename=filename, filetype='phantom')


def read_json(filename):
    """
    Initialize PhantomConfig from a JSON config file.

    Parameters
    ----------
    filename : str or pathlib.Path
        The JSON config file.

    Returns
    -------
    PhantomConfig
        Generated from the file.
    """
    return PhantomConfig(filename=filename, filetype='json')


__all__ = ['read_config', 'read_dict', 'read_json']
