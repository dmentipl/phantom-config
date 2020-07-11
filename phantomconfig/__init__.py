"""
Phantom config files: parse, convert, modify, and generate
==========================================================

phantomconfig is designed to:

- read and write the Phantom config file format,
- to modify, add, and remove variables,
- convert to and from JSON or TOML,
- convert to and from a Python dictionary.

See [Phantom](https://github.com/danieljprice/phantom/) for details on Phantom.

Daniel Mentiplay, 2019-2020.
"""

from pathlib import Path
from typing import Dict, Union

from .generators import parameter_sweep
from .phantomconfig import PhantomConfig


def read_dict(dictionary: Dict, dtype: str = None) -> PhantomConfig:
    """Initialize PhantomConfig from a dictionary.

    Parameters
    ----------
    dictionary
        A dictionary of the form:
            {'variable': [value, comment, block], ...}
        There are two special keys,
            '__header__': a list of strings, corresponding to lines in
                          the "header" of a Phantom config file,
            '__datetime__': a datetime.datetime object for the time
                            stamp of the file.
    dtype
        The dictionary type: either 'nested' or 'flat'. The default is
        'nested'.

    Returns
    -------
    PhantomConfig
        Generated from the dictionary.
    """
    if dtype is None:
        dtype = 'nested'
    return PhantomConfig(dictionary=dictionary, dictionary_type=dtype)


def read_config(filename: Union[str, Path]) -> PhantomConfig:
    """Initialize PhantomConfig from a Phantom config file.

    Parameters
    ----------
    filename
        The Phantom config file.

    Returns
    -------
    PhantomConfig
        Generated from the file.
    """
    return PhantomConfig(filename=filename, filetype='phantom')


def read_json(filename: Union[str, Path]) -> PhantomConfig:
    """Initialize PhantomConfig from a JSON config file.

    Parameters
    ----------
    filename
        The JSON config file.

    Returns
    -------
    PhantomConfig
        Generated from the file.
    """
    return PhantomConfig(filename=filename, filetype='json')


def read_toml(filename: Union[str, Path]) -> PhantomConfig:
    """Initialize PhantomConfig from a TOML config file.

    Parameters
    ----------
    filename
        The TOML config file.

    Returns
    -------
    PhantomConfig
        Generated from the file.
    """
    return PhantomConfig(filename=filename, filetype='toml')


__all__ = ['parameter_sweep', 'read_config', 'read_dict', 'read_json', 'read_toml']

__version__ = '0.3.3'
