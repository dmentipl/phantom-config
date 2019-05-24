"""
Parse Phantom config files.

Daniel Mentiplay, 2019.
"""

import datetime
import json
import re
from collections import OrderedDict, namedtuple

import numpy as np

Config = namedtuple('Config', ['name', 'value', 'comment', 'block'])


class PhantomConfig:
    """
    Phantom config file.

    Parameters
    ----------
    filename : str or pathlib.Path
        Name of Phantom config file. E.g. prefix.in or prefix.setup.
    """

    def __init__(self, filename):

        self.filename = None
        self.variables = None
        self.values = None
        self.comments = None
        self.config = None
        self.datetime = None
        self.header = None
        self.blocks = None

        self.read_phantom(filename)

    def write_json(self, filename):
        """Write config to JSON file.

        Parameters
        ----------
        filename : str or pathlib.Path
            The name of the JSON output file.
        """
        with open(filename, mode='w') as fp:
            json.dump(
                self._dictionary_in_blocks(),
                fp,
                indent=4,
                sort_keys=False,
                default=str,
            )

    def read_json(self, filename):
        """Read config from JSON file.

        Parameters
        ----------
        filename : str or pathlib.Path
            The name of the JSON input file.
        """
        with open(filename, mode='r') as fp:
            return json.load(fp)
        self.filename = filename

    def read_phantom(self, filename):

        self.filename = filename
        header, variables, values, comments, blocks = self._parse_phantom_file(
            filename
        )
        self.header = header
        self.blocks = blocks
        self.variables = variables
        self.values = values
        self.comments = comments
        self.config = tuple(
            [
                Config(var, val, comment, block)
                for var, val, comment, block in zip(
                    variables, values, comments, blocks
                )
            ]
        )
        self._make_attrs()

    def write_phantom(self, filename):
        """Write config to Phantom config file.

        Parameters
        ----------
        filename : str or pathlib.Path
            The name of the JSON output file.
        """
        with open(filename, mode='w') as fp:
            for line in self._to_phantom_lines():
                fp.write(line)

    def summary(self):
        """Print summary of config."""
        for entry in self.config:
            print(f'{entry.name:25} {entry.value}')

    def _to_ordered_dict(self, only_values=False):
        """Convert config to ordered dictionary.

        Parameters
        ----------
        only_values : bool, optional (False)
            If True, keys are names, items are values.
            If False, keys are names, items are tuples like
                (val, comment, block).

        Returns
        -------
        OrderedDict
            The config file as an ordered dictionary, like
                {'variable': (value, comment, block)}
            If only values:
                {'variable': value}
        """
        if only_values:
            return OrderedDict(
                ((var, val) for var, val in zip(self.variables, self.values))
            )
        return OrderedDict(
            (
                (var, (val, comment, block))
                for var, val, comment, block in zip(
                    self.variables,
                    self.values,
                    self.comments,
                    [config.block for config in self.config],
                )
            )
        )

    def _to_phantom_lines(self):
        """Convert config to a list of lines in Phantom style.

        Returns
        -------
        list
            The config file as a list of lines.
        """

        lines = list()
        [lines.append('# ' + header_line + '\n') for header_line in self.header]
        lines.append('\n')

        for block, block_contents in self._dictionary_in_blocks().items():
            lines.append('# ' + block + '\n')
            for var, val, comment in block_contents:
                if isinstance(val, float):
                    val_string = _phantom_float_format(
                        val, length=12, justify='right'
                    )
                elif isinstance(val, int):
                    val_string = f'{val:>12}'
                elif isinstance(val, str):
                    val_string = f'{val:>12}'
                elif isinstance(val, datetime.timedelta):
                    hhh = int(val.total_seconds() / 3600)
                    mm = int((val.total_seconds() - 3600 * hhh) / 60)
                    val_string = 6 * ' ' + f'{hhh:03}:{mm:02}'
                else:
                    raise ValueError('Cannot determine type')
                lines.append(f'{var:>20} = ' + val_string + f'   ! {comment}\n')
            lines.append('\n')

        return lines[:-1]

    def _parse_phantom_file(self, filename):
        """Parse config file."""

        self._get_datetime_from_phantom_infile(filename)

        with open(filename, mode='r') as fp:
            variables = list()
            values = list()
            comments = list()
            header = list()
            blocks = list()
            block_names = list()
            _read_in_header = False
            for line in fp:
                if line.startswith('#'):
                    if not _read_in_header:
                        header.append(line.strip().split('# ')[1])
                    else:
                        block_name = line.strip().split('# ')[1]
                        block_names.append(block_name)
                if not _read_in_header and line == '\n':
                    _read_in_header = True
                line = line.split('#', 1)[0].strip()
                if line:
                    line, comment = line.split('!')
                    comments.append(comment.strip())
                    variable, value = line.split('=')
                    variables.append(variable.strip())
                    value = value.strip()
                    value = _convert_value_type(value)
                    values.append(value)
                    blocks.append(block_name)

        return header, variables, values, comments, blocks

    def _dictionary_in_blocks(self):
        """Return dictionary of config values with blocks as keys."""
        block_dict = dict()
        for block in self.blocks:
            block_dict[block] = list()
            names = [conf.name for conf in self.config if conf.block == block]
            values = [conf.value for conf in self.config if conf.block == block]
            comments = [
                conf.comment for conf in self.config if conf.block == block
            ]
            for name, value, comment in zip(names, values, comments):
                block_dict[block].append([name, value, comment])
        return block_dict

    def _get_datetime_from_phantom_infile(self, filename):
        """Get datetime from Phantom timestamp in infile.

        Phantom timestamp is like dd/mm/yyyy hh:mm:s.ms
        """
        with open(filename, mode='r') as fp:
            for line in fp:
                if 'Runtime options file for Phantom, written' in line:
                    date, time = line.split()[-2:]
                    self.datetime = datetime.datetime.strptime(
                        date + time, '%d/%m/%Y%H:%M:%S.%f'
                    )

    def _make_attrs(self):
        """Make each config variable an attribute."""
        for entry in self.config:
            setattr(self, entry.name, entry)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(f'<PhantomConfig: "{self.filename}">')


def _convert_value_type(value):
    """Convert string from Phantom config to appropriate type.

    Parameters
    ----------
    value : str
        The value as a string.

    Returns
    -------
    value
        The value as appropriate type.
    """

    float_regexes = [r'\d*\.\d*E[-+]\d*', r'-*\d*\.\d*']
    timedelta_regexes = [r'\d\d\d:\d\d']
    int_regexes = [r'-*\d+']

    if value == 'T':
        return True
    if value == 'F':
        return False

    for regex in float_regexes:
        if re.fullmatch(regex, value):
            return float(value)

    for regex in timedelta_regexes:
        if re.fullmatch(regex, value):
            value = value.split(':')
            return datetime.timedelta(
                hours=int(value[0]), minutes=int(value[1])
            )

    for regex in int_regexes:
        if re.fullmatch(regex, value):
            return int(value)

    return value


def _phantom_float_format(val, length=None, justify=None):
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

    if np.isclose(abs(val), 0, atol=1e-50):
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


if __name__ == '__main__':
    infile = PhantomConfig('twhya.in')
    setupfile = PhantomConfig('twhya.setup')
