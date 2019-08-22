Phantom config
==============

> [Phantom](https://bitbucket.org/danielprice/phantom) config files: parse, convert, modify, and  generate.

`phantomconfig` can read Phantom `.in` and `.setup` files. (They have the same format.) You can, for example:

- modify config values,
- add new variables,
- write the config as a JSON file,
- generate a config file from a dictionary.

Usage
-----

### Basic usage

Import `phantomconfig` as `pc`.

```python
import phantomconfig as pc
```

To read in a Phantom config file

```python
input_file = pc.read_config('prefix.in')
```

Print a summary

```python
input_file.summary()
```

The variables, with their values, comment string, and the block they are a member of, are stored in a dictionary accessed by the `.config` method.

```python
dtmax = input_file.config['dtmax']
```

The keys of this dictionary correspond to the variable name, and values are a `ConfigVariable` named tuple with the variable name, value, comment, and block.

```python
dtmax.name
dtmax.value
dtmax.comment
dtmax.block
```

If you like, you can write the Phantom config as a JSON file, and you can read the JSON file.

```python
input_file.write_json('prefix-in.json')
json_file = pc.read_json('prefix-in.json')
```

Check that the configs are equal

```python
input_file.config == json_file.config
```

You can add a new variable, remove a variable, and change the value of a variable.

```python
# Add new variable
input_file.add_variable(
    'new_var',
    12345678,
    comment='Sets thing',
    block='options controlling things',
)

# Remove a variable
input_file.remove_variable('dtmax')

# Change the value of a variable
input_file.change_value('dumpfile', 'new_dumpfile_name')
```

Examples
--------

### Generate a config from a dictionary

You can create a Phantom `.setup` file from a Python dictionary. First create the dictionary

```python
setup = {
    'cs': [cs, 'sound speed', 'gas properties'],
    'npart': [npart, 'number of particles in x direction', 'gas properties'],
    'rhozero': [rhozero, 'initial density', 'gas properties'],
    'ilattice': [ilattice, 'lattice type', 'gas properties'],
}
```

Then you can read the dictionary with `phantomconfig`, and write to a Phantom `.setup` file

```python
setup_config = pc.read_dict(setup)
setup_config.header = ['input file for some particular setup routine']
setup_config.write_phantom('filename.setup')
```

This writes a file like

```
# input file for some particular setup routine

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
infile = pc.read_config('template.in')

for alpha in alphas:
    infile.change_value('alpha', alpha)
    infile.write_phantom(f'alpha={alpha}.in')
```
