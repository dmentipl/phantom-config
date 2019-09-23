Phantom config
==============

> [Phantom](https://bitbucket.org/danielprice/phantom) config files: parse, convert, modify, and generate.

phantom-config can read Phantom `.in` and `.setup` files. (They have the same format.) You can, for example:

- modify config values or comment strings,
- add new variables or delete old ones,
- write the config to a JSON or TOML file,
- generate a config file from a dictionary.

[![Build Status](https://travis-ci.org/dmentipl/phantom-config.svg?branch=master)](https://travis-ci.org/dmentipl/phantom-config)
[![Coverage Status](https://coveralls.io/repos/github/dmentipl/phantom-config/badge.svg?branch=master)](https://coveralls.io/github/dmentipl/phantom-config?branch=master)
[![PyPI](https://img.shields.io/pypi/v/phantomconfig)](https://pypi.org/project/phantomconfig/)

Installation
------------

Install phantom-config with pip

```bash
pip install phantomconfig
```

Usage
-----

### Basic usage

Import phantom-config.

```python
>>> import phantomconfig
```

To read in a Phantom config file

```python
>>> input_file = phantomconfig.read_config('prefix.in')
```

Print a summary

```python
>>> input_file.summary()
```

The variables, with their values, comment string, and the block they are a member of, are stored in a dictionary accessed by the `.config` method.

```python
>>> dtmax = input_file.config['dtmax']
```

The keys of this dictionary correspond to the variable name, and values are a `ConfigVariable` named tuple with the variable name, value, comment, and block.

```python
>>> dtmax.name
>>> dtmax.value
>>> dtmax.comment
>>> dtmax.block
```

You can just get the value if you want.

```python
input_file.get_value('dtmax')
```

If you like, you can write the Phantom config as a JSON file, and you can read the JSON file.

```python
>>> input_file.write_json('prefix-in.json')
>>> json_file = phantomconfig.read_json('prefix-in.json')
```

Check that the configs are equal

```python
>>> input_file.config == json_file.config
```

You can also read and write TOML files.

```python
>>> input_file.write_toml('prefix-in.toml')
>>> toml_file = phantomconfig.read_toml('prefix-in.toml')
```

You can add a new variable, remove a variable, and change the value of a variable.

```python
# Add new variable
>>> input_file.add_variable(
... 'new_var',
... 12345678,
... comment='Sets thing',
... block='options controlling things',
... )

# Remove a variable
>>> input_file.remove_variable('dtmax')

# Change the value of a variable
>>> input_file.change_value('dumpfile', 'new_dumpfile_name')
```

Then you can write the Phantom config file with the modified values.

```python
>>> input_file.write_phantom('new.in')
```

Examples
--------

### Generate a config from a dictionary

You can create a Phantom `.setup` file from a Python dictionary. First create the dictionary

```python
>>> setup = {}
>>> setup['gas properties'] = {
... 'cs': (cs, 'sound speed'),
... 'npart': (npart, 'number of particles in x direction'),
... 'rhozero': (rhozero, 'initial density'),
... 'ilattice': (ilattice, 'lattice type'),
... }
```

Then you can read the dictionary with `phantomconfig`, and write to a Phantom `.setup` file

```python
>>> setup_config = phantomconfig.read_dict(setup)
>>> setup_config.header = [
...     'input file for some particular setup routine',
...     'short description of what it does']
... ]
>>> setup_config.write_phantom('filename.setup')
```

This writes a file like

```
# input file for some particular setup routine
# short description of what it does

# gas properties
                  cs =        1.000   ! sound speed
               npart =         9999   ! number of particles in x direction
             rhozero =        0.100   ! initial density
            ilattice =            2   ! lattice type
```

### Writing multiple configs

Say you want to write multiple configs, each with a different parameter value. For example, you have a template `.in` file and you want to vary the alpha parameter. The following

1. reads the template file
2. loops over a list of `alpha` values, writing a new `.in` file for each value in the list

```python
alphas = [0.1, 0.2, 0.3]
infile = phantomconfig.read_config('template.in')

for alpha in alphas:
    infile.change_value('alpha', alpha)
    infile.write_phantom(f'alpha={alpha}.in')
```
