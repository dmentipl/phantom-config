# phantom-config

Phantom config files: parse, convert, make.

## How to use

```python
import phantom_config as pc

# Read in Phantom config file
infile = pc.read('prefix.in')

# Print a summary
infile.summary()

# Get a ConfigVariable namedtuple
logfile = infile.get_config('logfile')
logfile.variable
logfile.value
logfile.comment
logfile.block

# Convert to an ordered dictionary
ordered_dict = infile.to_ordered_dict()

# Write to JSON
infile.write_json('prefix-in.json')

# Read in JSON
infile_json = pc.read('prefix-in.json')
```
