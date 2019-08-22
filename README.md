# Phantom config

[Phantom](https://bitbucket.org/danielprice/phantom) config files: parse, convert, modify, and  generate.

## How to use

```python
import phantomconfig as pc

# Read in Phantom config file
config = pc.read_config('prefix.in')

# Print a summary
config.summary()

# Get a ConfigVariable namedtuple
logfile = config.config['logfile']
logfile.name
logfile.value
logfile.comment
logfile.block

# Convert to an ordered dictionary
ordered_dict = config.to_ordered_dict()

# Write to JSON
config.write_json('prefix-in.json')

# Read in JSON
config_json = pc.read_json('prefix-in.json')

# Check that the configs are equal
config.config == config_json.config
```
