"""Parsers for PhantomConfig."""

import datetime
import json
import re
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import tomlkit


def parse_dict_nested(dictionary: Dict[str, Dict[str, tuple]]) -> Any:
    """Parse nested dictionary.

    Parameters
    ----------
    dictionary
        The dictionary to parse like:
            {'block': 'variable': (value, comment), ...}.

    Returns
    -------
    date_time : datetime.datetime
    header : list
    block_names : list
    (variables, values, comments, blocks) : Tuple[str, Any, str, str]
    """
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
            sub_dict = item
            for sub_key, val in sub_dict.items():
                variables.append(sub_key)
                values.append(val[0])
                comments.append(val[1])
                blocks.append(key)

    block_names = list(OrderedDict.fromkeys(blocks))

    return date_time, header, block_names, (variables, values, comments, blocks)


def parse_dict_flat(dictionary: Dict) -> Any:
    """Parse flat dictionary.

    Parameters
    ----------
    dictionary
        The dictionary to parse like:
            {'variable': [value, comment, block], ...}.

    Returns
    -------
    date_time : datetime.datetime
    header : list
    block_names : list
    (variables, values, comments, blocks) : Tuple[str, Any, str, str]
    """
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


def parse_toml_file(filepath: Union[str, Path]) -> Any:
    """Parse TOML config file.

    Parameters
    ----------
    filepath
        The file name or path to the TOML file.

    Returns
    -------
    date_time : datetime.datetime
    header : list
    block_names : list
    (variables, values, comments, blocks) : Tuple[str, Any, str, str]
    """
    with open(filepath, 'r') as fp:
        toml_dict = tomlkit.loads(fp.read())

    blocks = list()
    variables = list()
    values = list()
    comments = list()

    header = None
    date_time = None

    for key, item in toml_dict.items():
        if key in ['__header__', 'header']:
            header = item
        elif key in ['__datetime__', 'datetime']:
            date_time = item
        else:
            for var, val in item.items():
                if isinstance(val, str):
                    if re.fullmatch(r'\d\d\d:\d\d', val):
                        val = val.split(':')
                        val = datetime.timedelta(hours=int(val[0]), minutes=int(val[1]))
                variables.append(var)
                values.append(val)
                blocks.append(key)

    variable_comment = dict()
    for key in toml_dict.keys():
        lines = toml_dict[key].as_string().split('\n')
        while '' in lines:
            lines.remove('')
        comment = list()
        for line in lines:
            if line.startswith('#'):
                comment.append(line[2:])
            else:
                variable_comment[line.split('=')[0].strip()] = '\n'.join(comment)
                comment = list()

    for var in variables:
        if var in variable_comment:
            comments.append(variable_comment[var])
        else:
            comments.append('')

    block_names = list(toml_dict.keys())
    try:
        block_names.remove('__header__')
    except ValueError:
        pass
    try:
        block_names.remove('__datetime__')
    except ValueError:
        pass

    header = list()
    lines = toml_dict.as_string().split('\n')
    for line in lines:
        if line.startswith('#'):
            header.append(line.strip().split('# ')[1])
        if line == '':
            break

    date_time = _get_datetime_from_header(header)

    return date_time, header, block_names, (variables, values, comments, blocks)


def parse_json_file(filepath: Union[str, Path]) -> Any:
    """Parse JSON config file.

    Parameters
    ----------
    filepath
        The file name or path to the JSON file.

    Returns
    -------
    date_time : datetime.datetime
    header : list
    block_names : list
    (variables, values, comments, blocks) : Tuple[str, Any, str, str]
    """
    with open(filepath, mode='r') as fp:
        json_dict = json.load(fp)

    blocks = list()
    variables = list()
    values = list()
    comments = list()

    header = None
    date_time = None

    for key, item in json_dict.items():
        if key in ['__header__', 'header']:
            header = item
        elif key in ['__datetime__', 'datetime']:
            date_time = datetime.datetime.strptime(item, '%d/%m/%Y %H:%M:%S.%f')
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


def parse_phantom_file(filepath: Union[str, Path]) -> Any:
    """Parse Phantom config file.

    Parameters
    ----------
    filepath
        The file name or path to the JSON file.

    Returns
    -------
    date_time : datetime.datetime
    header : list
    block_names : list
    (variables, values, comments, blocks) : Tuple[str, Any, str, str]
    """
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


def _get_datetime_from_header(header: List[str]) -> Optional[datetime.datetime]:
    """Get datetime from Phantom timestamp in header.

    Phantom timestamp is like dd/mm/yyyy hh:mm:s.ms

    Parameters
    ----------
    header
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
            date_time = datetime.datetime.strptime(matches[0], '%d/%m/%Y %H:%M:%S.%f')
        else:
            raise ValueError('Too many date time values in line')

    return date_time


def _convert_value_type_phantom(value: str) -> Any:
    """Convert string from Phantom config to appropriate type.

    Parameters
    ----------
    value
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
            hours, minutes = value.split(':')
            return datetime.timedelta(hours=int(hours), minutes=int(minutes))

    for regex in int_regexes:
        if re.fullmatch(regex, value):
            return int(value)

    return value
