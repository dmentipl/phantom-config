import datetime
import json
import pathlib
import re
from collections import OrderedDict, namedtuple

import numpy as np

ConfigVariable = namedtuple('ConfigVariable', ['name', 'value', 'comment', 'block'])


class PhantomConfig:
    """
    Phantom config file.

    Parameters
    ----------
    filename : str or pathlib.Path
        Name of Phantom config file. Typically of the form prefix.in or
        prefix.setup.

    filetype : str
        The file type of the config file. The default is a standard
        Phantom config type, specified by 'phantom'. The alternative is
        'json'.

    dictionary : dict
        A dictionary encoding a Phantom config structure like:
            {'variable': [value, comment, block], ...}
        There are two special keys. '__header__' whose value should be a
        list of strings, corresponding to lines in the "header" of a
        Phantom config file. And '__datetime__' whose value should be a
        datetime.datetime object.
    """

    def __init__(self, filename=None, filetype=None, dictionary=None):

        filepath = None

        self.config = None
        self.datetime = None
        self.header = None

        if filename is not None:

            if filetype is None:
                print('Assuming Phantom config file.')
                filetype = 'phantom'
            elif isinstance(filetype, str):
                if filetype.lower() == 'phantom':
                    filetype = 'phantom'
                elif filetype.lower() == 'json':
                    filetype = 'json'
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

        else:
            if dictionary is None:
                raise ValueError('Need a file name or dictionary.')

        if filetype is None:
            self._initialize_from_dictionary(dictionary)
        elif filetype == 'phantom':
            self._initialize_from_phantom(filepath)
        elif filetype == 'json':
            self._initialize_from_json(filepath)

    def _initialize_from_phantom(self, filepath):
        date_time, header, block_names, conf = _parse_phantom_file(filepath)
        self._initialize(date_time, header, block_names, conf)

    def _initialize_from_json(self, filepath):
        date_time, header, block_names, conf = _parse_json_file(filepath)
        self._initialize(date_time, header, block_names, conf)

    def _initialize_from_dictionary(self, dictionary):
        date_time, header, block_names, conf = _parse_dict(dictionary)
        self._initialize(date_time, header, block_names, conf)

    def _initialize(self, date_time, header, block_names, conf):
        """Initialize PhantomConfig."""

        variables, values, comments, blocks = conf[0], conf[1], conf[2], conf[3]

        self.header = header
        self.datetime = date_time
        self.config = {
            var: ConfigVariable(var, val, comment, block)
            for var, val, comment, block in zip(variables, values, comments, blocks)
        }

    @property
    def variables(self):
        return [self.config[key].name for key in self.config]

    @property
    def values(self):
        return [self.config[key].value for key in self.config]

    @property
    def comments(self):
        return [self.config[key].comment for key in self.config]

    @property
    def blocks(self):
        return [self.config[key].block for key in self.config]

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
                default=_convert_json_to_datetime,
            )

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
        name_width = 25
        print()
        print(18 * ' ' + 'variable   value')
        print(18 * ' ' + '--------   -----')
        for entry in self.config.values():
            print(f'{entry.name.rjust(name_width)}   {entry.value}')

    def to_ordered_dict(self, only_values=False):
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
                [var, val] for var, val in zip(self.variables, self.values)
            )
        return OrderedDict(
            [var, [val, comment, block]]
            for var, val, comment, block in zip(
                self.variables,
                self.values,
                self.comments,
                [config.block for config in self.config.values()],
            )
        )

    def add_variable(self, variable, value, comment=None, block=None):
        """Add a variable to the config.

        Parameters
        ----------
        variable : str
            The name of the variable.
        value
            The value of the variable.
        comment : str
            The comment string describing the variable.
        block : str
            The block to which the variable is associated.
        """

        if comment is None:
            comment = 'No description'
        if block is None:
            block = 'Miscellaneous'

        self.config[variable] = ConfigVariable(variable, value, comment, block)

    def remove_variable(self, variable):
        """Remove a variable from the config.

        Parameters
        ----------
        variable : str
            The variable to remove.
        """
        self.config.pop(variable)

    def change_value(self, variable, value):
        """Change a value on a variable.

        Parameters
        ----------
        variable : str
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

    def _to_phantom_lines(self):
        """Convert config to a list of lines in Phantom style.

        Returns
        -------
        list
            The config file as a list of lines.
        """

        _length = 12

        lines = list()
        if self.header is not None:
            [lines.append('# ' + header_line + '\n') for header_line in self.header]
            lines.append('\n')

        for block, block_contents in self._dictionary_in_blocks().items():
            lines.append('# ' + block + '\n')
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

    def _dictionary_in_blocks(self):
        """Return dictionary of config values with blocks as keys."""
        block_dict = dict()
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
        return block_dict

    def _make_attrs(self):
        """Make each config variable an attribute."""
        for entry in self.config.values():
            setattr(self, entry.name, entry)


def _parse_dict(dictionary):
    """Parse dictionary {'variable': [value, comment, block], ...}."""

    blocks = list()
    variables = list()
    values = list()
    comments = list()

    header = None
    date_time = None

    for key, item in dictionary.items():
        if key == '__header__':
            header = item
        elif key == '__datetime__':
            date_time = item
        else:
            var = key
            val = item[0]
            comment = item[1]
            block = item[2]
            variables.append(var)
            values.append(val)
            comments.append(comment)
            blocks.append(block)

    block_names = list(OrderedDict.fromkeys(blocks))

    return date_time, header, block_names, (variables, values, comments, blocks)


def _parse_json_file(filepath):
    """Parse JSON config file."""

    with open(filepath, mode='r') as fp:
        json_dict = json.load(fp)

    blocks = list()
    variables = list()
    values = list()
    comments = list()

    header = None
    date_time = None

    for key, item in json_dict.items():
        if key == '__header__':
            header = item
        elif key == '__datetime__':
            date_time = datetime.datetime.strptime(
                item, '%d/%m/%Y %H:%M:%S.%f'
            )
        else:
            for var, val, comment in item:
                if isinstance(val, str):
                    if re.fullmatch(r'\d\d\d:\d\d', val):
                        val = val.split(':')
                        val = datetime.timedelta(hours=int(val[0]), minutes=int(val[1]))
                variables.append(var)
                values.append(val)
                comments.append(comment)
                blocks.append(key)

    block_names = list(json_dict.keys())
    try:
        block_names.remove('__header__')
    except ValueError:
        pass
    try:
        block_names.remove('__datetime__')
    except ValueError:
        pass

    return date_time, header, block_names, (variables, values, comments, blocks)


def _parse_phantom_file(filepath):
    """Parse Phantom config file."""

    with open(filepath, mode='r') as fp:
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
                variable, value = line.split('=', 1)
                variables.append(variable.strip())
                value = value.strip()
                value = _convert_value_type_phantom(value)
                values.append(value)
                blocks.append(block_name)

    date_time = _get_datetime_from_header(header)

    return date_time, header, block_names, (variables, values, comments, blocks)


def _get_datetime_from_header(header):
    """Get datetime from Phantom timestamp in header.

    Phantom timestamp is like dd/mm/yyyy hh:mm:s.ms

    Parameters
    ----------
    header : list
        The header as a list of strings.

    Returns
    -------
    datetime.datetime
        The datetime of the config.
    """

    date_time = None
    for line in header:
        if date_time is not None:
            break
        matches = re.findall(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}.\d+', line)
        if len(matches) == 0:
            continue
        elif len(matches) == 1:
            date_time = datetime.datetime.strptime(
                matches[0], '%d/%m/%Y %H:%M:%S.%f'
            )
        else:
            raise ValueError('Too many date time values in line')

    return date_time


def _convert_json_to_datetime(val):
    """Convert datetime string from JSON config to datetime.timedelta.

    Parameters
    ----------
    value : str
        The value as a string.

    Returns
    -------
    value
        The value as datetime.timedelta
    """
    hhh = int(val.total_seconds() / 3600)
    mm = int((val.total_seconds() - 3600 * hhh) / 60)
    return f'{hhh:03}:{mm:02}'


def _convert_value_type_phantom(value):
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

    float_regexes = [r'\d*\.\d*[Ee][-+]\d*', r'-*\d*\.\d*']
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
            return datetime.timedelta(hours=int(value[0]), minutes=int(value[1]))

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
