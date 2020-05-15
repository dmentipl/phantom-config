"""Testing phantomconfig."""

import pathlib

import phantomconfig as pc

from .stub import test_data

test_phantom_file = pathlib.Path(__file__).parent / 'stub' / 'config.in'
test_json_file = pathlib.Path(__file__).parent / 'stub' / 'config.json'
test_toml_file = pathlib.Path(__file__).parent / 'stub' / 'config.toml'
test_dict_flat = test_data.dict_flat
test_dict_nested = test_data.dict_nested


def test_read_phantom_config():
    """Test reading Phantom config files."""
    conf = pc.read_config(test_phantom_file)
    assert conf.config == test_data.config
    assert conf.header == test_data.header
    assert conf.datetime == test_data._datetime


def test_read_json_config():
    """Test reading JSON config files."""
    conf = pc.read_json(test_json_file)
    assert conf.config == test_data.config
    assert conf.header == test_data.header
    assert conf.datetime == test_data._datetime


def test_read_toml_config():
    """Test reading TOML config files."""
    conf = pc.read_toml(test_toml_file)
    assert conf.variables == test_data.variables
    assert conf.values == test_data.values
    assert conf.header == test_data.header
    assert conf.datetime == test_data._datetime


def test_read_dict_flat():
    """Test reading flat Python dictionaries."""
    conf = pc.read_dict(test_dict_flat, dtype='flat')
    assert conf.config == test_data.config
    assert conf.header == test_data.header
    assert conf.datetime == test_data._datetime


def test_read_dict_nested():
    """Test reading nested Python dictionaries."""
    conf = pc.read_dict(test_dict_nested, dtype='nested')
    assert conf.config == test_data.config
    assert conf.header == test_data.header
    assert conf.datetime == test_data._datetime


def test_write_phantom_config():
    """Test writing Phantom config files."""
    tmp_file = pathlib.Path('tmp.in')

    conf = pc.read_config(test_phantom_file)
    conf.write_phantom(tmp_file)

    conf = pc.read_config(tmp_file)

    assert conf.config == test_data.config
    assert conf.header == test_data.header
    assert conf.datetime == test_data._datetime

    tmp_file.unlink()


def test_write_json_config():
    """Test writing JSON config files."""
    tmp_file = pathlib.Path('tmp.json')

    conf = pc.read_config(test_phantom_file)
    conf.write_json(tmp_file)

    conf = pc.read_json(tmp_file)

    assert conf.config == test_data.config
    assert conf.header == test_data.header
    assert conf.datetime == test_data._datetime

    tmp_file.unlink()


def test_write_toml_config():
    """Test writing TOML config files."""
    tmp_file = pathlib.Path('tmp.toml')

    conf = pc.read_config(test_phantom_file)
    conf.write_toml(tmp_file)

    conf = pc.read_toml(tmp_file)

    assert conf.variables == test_data.variables
    assert conf.values == test_data.values
    assert conf.header == test_data.header
    assert conf.datetime == test_data._datetime

    tmp_file.unlink()


def test_add_value():
    """Testing adding, removing, modifying values."""
    conf = pc.read_config(test_phantom_file)
    conf.add_variable('new_variable', 999)
    conf.add_variable('new_variable', 999, comment='No comment', block='New block')
    assert conf.config['new_variable'].value == 999


def test_remove_variable():
    """Test removing a variable."""
    conf = pc.read_config(test_phantom_file)
    conf.remove_variable('dtmax')
    assert 'dtmax' not in conf.variables


def test_change_variable():
    """Test changing a variable."""
    conf = pc.read_config(test_phantom_file)
    hfact_prev = conf.config['hfact'].value
    conf.change_value('hfact', 1.2)
    assert conf.config['hfact'].value != hfact_prev
