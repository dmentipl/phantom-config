"""Generate multiple config files."""

from itertools import product
from pathlib import Path
from typing import Any, Dict, List, Union

from .phantomconfig import PhantomConfig


def parameter_sweep(
    *,
    filename: str,
    template: PhantomConfig,
    parameters: Dict[str, List[Any]],
    dummy_parameters: List[str] = None,
    dependent_parameters: Dict[str, List[Dict[str, Any]]] = None,
    filetype: str = 'Phantom',
    prefix: str = None,
    output_dir: Union[str, Path] = None,
):
    """Generate Phantom files in a parameter sweep.

    This function takes a dictionary of keys with parameter names and
    values are parameter values and generates the Cartesian product
    over those parameters and writes them to a Phantom config file.

    Each file is placed in a directory like "a-1_b-2_c-3" where "a",
    "b", "c" are parameter names and 1, 2, 3 their values.

    All parameters must exist in the template file. If you require
    additional parameters, you can generate multiple template files.

    Parameters
    ----------
    filename
        The name of each file.
    template
        The PhantomConfig template file.
    parameters
        A dict of parameters where each key is a parameter name, and
        each value is a list of parameter values. Make sure the values
        have the correct type as phantomconfig distinguishes between,
        for example, floats and ints.
    dummy_parameters
        A list of parameter names which is a subset of parameters above.
        This set of parameters does not modify the config file. This is
        useful if there are parameters in one of a Phantom ".in" or
        ".setup" file, and you want to generate a grid of parameters in
        both files.
    dependent_parameters
        A dict of dict of parameters. Each key is a parameter in
        parameters above, and each value is a dict with multiple
        parameters and values dependent on the first key. E.g.
        d = {'a': [{'b': 1.0, 'c': -2.0}, {'b': 2.0, 'c': -4.0}]},
        where 'a' is in parameters and has two values.
    filetype
        The file type to write. Can be 'Phantom', 'TOML', or 'JSON'.
    prefix
        A common prefix for the directories containing each config
        file.
    output_dir
        A path in which to output the directories containing each config
        file.

    Examples
    --------
    Generate multiple dustyshock .setup and .in files.

    The parameters to loop over.

    >>> parameters = {
    ...     'ndust': [1, 3], 'nx': [32, 128], 'hfact': [1.0, 1.2, 1.5]
    ... }

    More parameters which are dependent on 'ndust'.

    >>> dependent_parameters = {
    ...     'ndust': [
    ...         {'densright': 8.0, 'prright': 8.0, 'vxright': 0.25},
    ...         {'densright': 16.0, 'prright': 16.0, 'vxright': 0.125},
    ...     ]
    ... }

    Generate the .setup files.

    >>> template = read_config('dustyshock.setup')
    >>> pc.parameter_sweep(
    ...     filename='dustyshock.setup',
    ...     template=template,
    ...     parameters=parameters,
    ...     dependent_parameters=dependent_parameters,
    ...     dummy_parameters=['hfact'],
    ... )

    Generate the .in files.

    >>> template = read_config('dustyshock.in')
    >>> pc.parameter_sweep(
    ...     filename='dustyshock.in',
    ...     template=template,
    ...     parameters=parameters,
    ...     dummy_parameters=['ndust', 'nx'],
    ... )
    """
    if filetype.lower() not in ('phantom', 'toml', 'json'):
        raise ValueError('Cannot determine filetype')
    if dummy_parameters is None:
        dummy_parameters = []
    if dependent_parameters is None:
        dependent_parameters = {}
    if not set(dummy_parameters).issubset(set(parameters.keys())):
        raise ValueError('dummy_parameters must be a subset of keys in parameters')
    if not set(dependent_parameters.keys()).issubset(set(parameters.keys())):
        raise ValueError(
            'dependent_parameters keys must be a subset of keys in parameters'
        )
    if output_dir is not None:
        _output_dir = Path(output_dir).expanduser()
    else:
        _output_dir = Path()
    if not _output_dir.exists():
        _output_dir.mkdir(parents=True)

    names = parameters.keys()
    values = [element for element in product(*parameters.values())]
    for params in values:
        directory = '-'.join([f'{k}_{v}' for k, v in zip(names, params)])
        if prefix is not None:
            directory = prefix + directory
        _directory = _output_dir / directory
        if not _directory.exists():
            _directory.mkdir()
        for idx, name in enumerate(names):
            if name not in dummy_parameters:
                template.change_value(name, params[idx])
            if name in dependent_parameters.keys():
                _idx = parameters[name].index(params[idx])
                _params = dependent_parameters[name][_idx]
                for key, val in _params.items():
                    template.change_value(key, val)
        template.write_phantom(filename=_directory / filename)
