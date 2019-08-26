"""
Phantom config files: parse, convert, modify, and generate
----------------------------------------------------------

phantomconfig is designed to:

- read and write the Phantom config file format,
- to modify, add, and remove variables,
- convert to and from JSON
- convert to and from a Python dictionary.

See [Phantom](https://phantomsph.bitbucket.io/) for details on Phantom.

Daniel Mentiplay, 2019.
"""

from .phantomconfig import PhantomConfig


def read_dict(dictionary):
    """
    Initialize PhantomConfig from a dictionary.

    Parameters
    ----------
    dictionary : dict
        A dictionary of the form:
            {'variable': [value, comment, block], ...}
        There are two special keys,
            '__header__': a list of strings, corresponding to lines in
                          the "header" of a Phantom config file,
            '__datetime__': a datetime.datetime object for the time
                            stamp of the file.

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

__version__ = '0.2.1'
