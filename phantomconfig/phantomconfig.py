"""Phantom config."""

from __future__ import annotations

import datetime
import json
import math
import pathlib
from collections import namedtuple
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import tomlkit

from .parsers import (
    parse_dict_flat,
    parse_dict_nested,
    parse_json_file,
    parse_phantom_file,
    parse_toml_file,
)

ConfigVariable = namedtuple('ConfigVariable', ['name', 'value', 'comment', 'block'])


class PhantomConfig:
    """Phantom config file.

    Parameters
    ----------
    filename
        Name of Phantom config file. Typically of the form prefix.in or
        prefix.setup.
    filetype
        The file type of the config file. The default is a standard
        Phantom config type, specified by 'phantom'. The alternatives
        are 'json' and 'toml'.
    dictionary
        A dictionary encoding a Phantom config structure. Can be flat
        like
            {'variable': [value, comment, block], ...}
        or nested like
            {'block': 'variable': (value, comment), ...}.
        There are two special keys. '__header__' whose value should be a
        list of strings, corresponding to lines in the "header" of a
        Phantom config file. And '__datetime__' whose value should be a
        datetime.datetime object.
    dictionary_type
        The type of dictionary passed: either 'nested' or 'flat'.
    """

    def __init__(
        self,
        filename: Union[str, Path] = None,
        filetype: str = None,
        dictionary: Dict = None,
        dictionary_type: str = None,
    ) -> None:

        self.name: str
        self.filepath: Path

        self.config: Dict[str, ConfigVariable]
        self.datetime: Optional[datetime.datetime] = None
        self.header: Optional[List[str]] = None

        if filename is not None:

            if filetype is None:
                filetype = 'phantom'
            elif isinstance(filetype, str):
                if filetype.lower() == 'phantom':
                    filetype = 'phantom'
                elif filetype.lower() == 'json':
                    filetype = 'json'
                elif filetype.lower() == 'toml':
                    filetype = 'toml'
                else:
                    raise ValueError('Cannot determine file type.')
            else:
                raise TypeError('filetype must be str.')

            if isinstance(filename, str):
                filepath = pathlib.Path(filename).expanduser().resolve()
                filename = filepath.name
            elif isinstance(filename, pathlib.Path):
                filepath = filename.expanduser().resolve()
                filename = filepath.name
            if not filepath.exists():
                raise FileNotFoundError(f'Cannot find config file: {filename}')

            self.name = filename
            self.filepath = filepath

        else:
            self.name = 'dict'
            if dictionary is None:
                raise ValueError('Need a file name or dictionary.')
            if dictionary_type is None:
                dictionary_type = 'flat'
            if dictionary_type not in ('nested', 'flat'):
                raise ValueError('Cannot determine dictionary type')

        if filetype is None:
            assert isinstance(dictionary, Dict)
            if dictionary_type == 'nested':
                try:
                    date_time, header, block_names, conf = parse_dict_nested(dictionary)
                except KeyError:
                    raise ValueError('Cannot read dictionary; is the dictionary flat?')
            elif dictionary_type == 'flat':
                try:
                    date_time, header, block_names, conf = parse_dict_flat(dictionary)
                except KeyError:
                    raise ValueError(
                        'Cannot read dictionary; is the dictionary nested?'
                    )
            self._initialize(date_time, header, block_names, conf)
        elif filetype == 'phantom':
            date_time, header, block_names, conf = parse_phantom_file(filepath)
            self._initialize(date_time, header, block_names, conf)
        elif filetype == 'json':
            date_time, header, block_names, conf = parse_json_file(filepath)
            self._initialize(date_time, header, block_names, conf)
        elif filetype == 'toml':
            date_time, header, block_names, conf = parse_toml_file(filepath)
            self._initialize(date_time, header, block_names, conf)

    def _initialize(
        self,
        date_time: datetime.datetime,
        header: List[str],
        block_names: List[str],
        conf: Tuple,
    ) -> None:
        """Initialize PhantomConfig."""
        variables, values, comments, blocks = conf[0], conf[1], conf[2], conf[3]

        self.header = header
        self.datetime = date_time
        self.config = {
            var: ConfigVariable(var, val, comment, block)
            for var, val, comment, block in zip(variables, values, comments, blocks)
        }

    @property
    def variables(self) -> List[str]:
        """List of variables."""
        return [self.config[key].name for key in self.config]

    @property
    def values(self) -> List:
        """List of values."""
        return [self.config[key].value for key in self.config]

    @property
    def comments(self) -> List[str]:
        """List of comments."""
        return [self.config[key].comment for key in self.config]

    @property
    def blocks(self) -> List[str]:
        """List of blocks."""
        return [self.config[key].block for key in self.config]

    def write_toml(self, filename: Union[str, Path]) -> PhantomConfig:
        """Write config to TOML file.

        Parameters
        ----------
        filename
            The name of the TOML output file.
        """
        # TODO: writing to TOML does not preserve the comments.

        document = tomlkit.document()

        if self.header is not None:
            for line in self.header:
                document.add(tomlkit.comment(line))
            document.add(tomlkit.nl())

        d = self.to_dict()
        for block_key, block_val in d.items():
            block = tomlkit.table()
            if isinstance(block_val, dict):
                for name, item in block_val.items():
                    value, comment = item
                    if isinstance(value, datetime.timedelta):
                        value = _convert_timedelta_to_str(value)
                    block.add(tomlkit.nl())
                    if comment is not None:
                        block.add(tomlkit.comment(comment))
                    block.add(name, value)
                document.add(block_key, block)

        with open(filename, 'w') as fp:
            fp.write(tomlkit.dumps(document))

        return self

    def write_json(self, filename: Union[str, Path]) -> PhantomConfig:
        """Write config to JSON file.

        Parameters
        ----------
        filename
            The name of the JSON output file.
        """
        with open(filename, mode='w') as fp:
            json.dump(
                self._dictionary_in_blocks(),
                fp,
                indent=4,
                sort_keys=False,
                default=_serialize_datetime_for_json,
            )

        return self

    def write_phantom(self, filename: Union[str, Path]) -> PhantomConfig:
        """Write config to Phantom config file.

        Parameters
        ----------
        filename
            The name of the Phantom output file.
        """
        with open(filename, mode='w') as fp:
            for line in self._to_phantom_lines():
                fp.write(line)

        return self

    def summary(self, block: str = None) -> None:
        """Print summary of config.

        Optional Parameters
        -------------------
        block
            Only print the lines of the specified block.
        """
        for line in self._to_phantom_lines(block=block):
            print(line.strip('\n'))

    def __repr__(self) -> str:
        """Repr method."""
        return f"PhantomConfig('{self.name}')"

    def to_dict(
        self, flattened: bool = False, only_values: bool = False
    ) -> Dict[str, Any]:
        """Convert config to a dictionary.

        Parameters
        ----------
        flattened
            Whether to return a nested (by block) or flattened
            dictionary.
        only_values
            If True, (possibly nested) items are values only.
            If False, (possibly nested) items are tuples like
                (val, comment, block).

        Returns
        -------
        dict
            Depending on options, the config file as a dictionary, like
                {'block': 'variable': (value, comment), ...}.
                {'block': 'variable': value, ...}.
                {'variable': (value, comment, block), ...}
                {'variable': value, ...}
        """
        if flattened:
            return self._to_dict_flat(only_values=only_values)
        else:
            return self._to_dict_nested(only_values=only_values)

    def _to_dict_nested(self, only_values: bool = False) -> Dict[str, Any]:
        """Convert config to a nested dictionary.

        Parameters
        ----------
        only_values
            If True, keys are names, items are values.
            If False, keys are names, items are tuples like
                (val, comment, block).

        Returns
        -------
        dict
            The config file as a dictionary, like
                {'block': 'variable': (value, comment), ...}.
            or, if only_values is True, like
                {'block': 'variable': value, ...}.
        """
        nested_dict: Dict[str, Any] = dict()

        for block in self.blocks:
            names = [conf.name for conf in self.config.values() if conf.block == block]
            values = [
                conf.value for conf in self.config.values() if conf.block == block
            ]
            comments = [
                conf.comment for conf in self.config.values() if conf.block == block
            ]
            if only_values:
                nested_dict[block] = {name: value for name, value in zip(names, values)}
            else:
                nested_dict[block] = {
                    name: (value, comment)
                    for name, value, comment in zip(names, values, comments)
                }

        if self.header is not None:
            nested_dict['__header__'] = self.header
        if self.datetime is not None:
            nested_dict['__datetime__'] = self.datetime
        return nested_dict

    def _to_dict_flat(self, only_values: bool = False) -> Dict:
        """Convert config to a flat dictionary.

        Parameters
        ----------
        only_values
            If True, keys are names, items are values.
            If False, keys are names, items are tuples like
                (val, comment, block).

        Returns
        -------
        dict
            The config file as an ordered dictionary, like
                {'variable': (value, comment, block), ...}
            If only values:
                {'variable': value, ...}
        """
        if only_values:
            return {var: val for var, val in zip(self.variables, self.values)}
        return {
            var: [val, comment, block]
            for var, val, comment, block in zip(
                self.variables,
                self.values,
                self.comments,
                [config.block for config in self.config.values()],
            )
        }

    def add_variable(
        self, variable: str, value: Any, comment: str = None, block: str = None,
    ) -> PhantomConfig:
        """Add a variable to the config.

        Parameters
        ----------
        variable
            The name of the variable.
        value
            The value of the variable.
        comment
            The comment string describing the variable.
        block
            The block to which the variable is associated.
        """
        if comment is None:
            comment = 'No description'
        if block is None:
            block = 'Miscellaneous'

        self.config[variable] = ConfigVariable(variable, value, comment, block)

        return self

    def remove_variable(self, variable: str) -> PhantomConfig:
        """Remove a variable from the config.

        Parameters
        ----------
        variable
            The variable to remove.
        """
        self.config.pop(variable)

        return self

    def get_value(self, variable: str) -> Any:
        """Get the value of a variable.

        Parameters
        ----------
        variable
            The name of the variable.

        Returns
        -------
        The value of the variable.
        """
        return self.config[variable].value

    def change_value(self, variable: str, value: Any) -> PhantomConfig:
        """Change a value on a variable.

        Parameters
        ----------
        variable
            Change the value of this variable.
        value
            Set the variable to this value.
        """
        if variable not in self.config:
            raise ValueError(f'{variable} not in config')

        tmp = self.config[variable]

        if not isinstance(value, type(tmp[1])):
            raise ValueError('Value and variable are not compatible')

        self.config[variable] = ConfigVariable(tmp[0], value, tmp[2], tmp[3])

        return self

    def _to_phantom_lines(self, block: str = None) -> List[str]:
        """Convert config to a list of lines in Phantom style.

        Optional Parameters
        -------------------
        block
            Only return the lines of the specified block.

        Returns
        -------
        list
            The config file as a list of lines.
        """
        _length = 12

        only_block = None
        if block is not None:
            only_block = block

        lines = list()

        if only_block is None:
            if self.header is not None:
                for header_line in self.header:
                    lines.append('# ' + header_line + '\n')
                lines.append('\n')

        for block_name, block_contents in self._dictionary_in_blocks().items():
            if only_block is not None and block_name != only_block:
                continue
            if block_name in ['__header__', '__datetime__']:
                pass
            else:
                lines.append('# ' + block_name + '\n')
                for var, val, comment in block_contents:
                    if isinstance(val, bool):
                        val_string = 'T'.rjust(_length) if val else 'F'.rjust(_length)
                    elif isinstance(val, float):
                        val_string = _phantom_float_format(
                            val, length=_length, justify='right'
                        )
                    elif isinstance(val, int):
                        val_string = f'{val:>{_length}}'
                    elif isinstance(val, str):
                        val_string = f'{val:>{_length}}'
                    elif isinstance(val, datetime.timedelta):
                        hhh = int(val.total_seconds() / 3600)
                        mm = int((val.total_seconds() - 3600 * hhh) / 60)
                        val_string = f'{hhh:03}:{mm:02}'.rjust(_length)
                    else:
                        raise ValueError('Cannot determine type')
                    lines.append(f'{var:>20} = ' + val_string + f'   ! {comment}\n')
                lines.append('\n')

        return lines[:-1]

    def _dictionary_in_blocks(self) -> Dict:
        """Return dictionary of config values with blocks as keys."""
        block_dict: Dict = dict()

        for block in self.blocks:
            block_dict[block] = list()
            names = [conf.name for conf in self.config.values() if conf.block == block]
            values = [
                conf.value for conf in self.config.values() if conf.block == block
            ]
            comments = [
                conf.comment for conf in self.config.values() if conf.block == block
            ]
            for name, value, comment in zip(names, values, comments):
                block_dict[block].append([name, value, comment])

        if self.header is not None:
            block_dict['__header__'] = self.header
        if self.datetime is not None:
            block_dict['__datetime__'] = self.datetime

        return block_dict

    def _make_attrs(self) -> None:
        """Make each config variable an attribute."""
        for entry in self.config.values():
            setattr(self, entry.name, entry)

    def __eq__(self, other):
        """Equivalence method."""
        return self.config == other.config


def _serialize_datetime_for_json(
    val: Union[datetime.datetime, datetime.timedelta]
) -> str:
    """Serialize datetime objects for JSON.

    Parameters
    ----------
    val
        The value as datetime.datetime or datetime.timedelta.

    Returns
    -------
    str
        The datetime as a string like "dd/mm/yyyy HH:MM:SS.f", or
        timdelta as string like "HHH:MM".
    """
    if isinstance(val, datetime.datetime):
        return _convert_datetime_to_str(val)
    elif isinstance(val, datetime.timedelta):
        return _convert_timedelta_to_str(val)
    else:
        raise ValueError('Cannot serialize object')


def _convert_datetime_to_str(val: datetime.datetime) -> str:
    """Convert datetime.datetime to a string.

    Parameters
    ----------
    val
        The value as datetime.datetime.

    Returns
    -------
    str
        The datetime as a string like "dd/mm/yyyy HH:MM:SS.f".
    """
    return datetime.datetime.strftime(val, '%d/%m/%Y %H:%M:%S.%f')


def _convert_timedelta_to_str(val: datetime.timedelta) -> str:
    """Convert datetime.timedelta to a string.

    Parameters
    ----------
    val
        The value as datetime.timedelta.

    Returns
    -------
    str
        The timedelta as a string like "HHH:MM".
    """
    hhh = int(val.total_seconds() / 3600)
    mm = int((val.total_seconds() - 3600 * hhh) / 60)
    return f'{hhh:03}:{mm:02}'


def _phantom_float_format(
    val: float, length: Optional[int] = None, justify: Optional[str] = None
):
    """Float to Phantom style float string.

    Parameters
    ----------
    val : float
        The value to convert.
    length : int
        A string length for the return value.
    justify : str
        Justify text left or right by padding based on length.

    Returns
    -------
    str
        The float as formatted str.
    """
    if math.isclose(abs(val), 0, abs_tol=1e-50):
        string = '0.000'
    elif abs(val) < 0.001:
        string = f'{val:.3e}'
    elif abs(val) < 1000:
        string = f'{val:.3f}'
    elif abs(val) < 10000:
        string = f'{val:g}'
    else:
        string = f'{val:.3e}'

    if isinstance(length, int):
        if justify is None:
            justify = 'left'
        else:
            if justify.lower() in ['r', 'right']:
                return string.rjust(length)
            elif justify.lower() in ['l', 'left']:
                return string.ljust(length)
            else:
                raise ValueError('justify is either "left" or "right"')
    else:
        raise TypeError('length must be int')
    return string
