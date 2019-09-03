"""
Testing phantomconfig.
"""

import pathlib
import unittest

import phantomconfig as pc

from .stub import test_data

test_phantom_file = pathlib.Path(__file__).parent / 'stub' / 'config.in'
test_json_file = pathlib.Path(__file__).parent / 'stub' / 'config.json'
test_toml_file = pathlib.Path(__file__).parent / 'stub' / 'config.toml'
test_dict = test_data._dict


class TestReadPhantom(unittest.TestCase):
    """Test reading Phantom config files."""

    def test_read_phantom_config(self):

        conf = pc.read_config(test_phantom_file)
        self.assertEqual(conf.config, test_data.config)
        self.assertEqual(conf.header, test_data.header)
        self.assertEqual(conf.datetime, test_data._datetime)


class TestReadJSON(unittest.TestCase):
    """Test reading JSON config files."""

    def test_read_json_config(self):

        conf = pc.read_json(test_json_file)
        self.assertEqual(conf.config, test_data.config)
        self.assertEqual(conf.header, test_data.header)
        self.assertEqual(conf.datetime, test_data._datetime)


class TestReadTOML(unittest.TestCase):
    """Test reading TOML config files."""

    def test_read_toml_config(self):

        conf = pc.read_toml(test_toml_file)
        self.assertEqual(conf.variables, test_data.variables)
        self.assertEqual(conf.values, test_data.values)
        self.assertEqual(conf.header, test_data.header)
        self.assertEqual(conf.datetime, test_data._datetime)


class TestReadDict(unittest.TestCase):
    """Test reading Python dictionaries."""

    def test_read_dict(self):

        conf = pc.read_dict(test_dict)
        self.assertEqual(conf.config, test_data.config)
        self.assertEqual(conf.header, test_data.header)
        self.assertEqual(conf.datetime, test_data._datetime)


class TestWritePhantom(unittest.TestCase):
    """Test writing Phantom config files."""

    def test_write_phantom_config(self):

        tmp_file = pathlib.Path('tmp.in')

        conf = pc.read_config(test_phantom_file)
        conf.write_phantom(tmp_file)

        conf = pc.read_config(tmp_file)

        self.assertEqual(conf.config, test_data.config)
        self.assertEqual(conf.header, test_data.header)
        self.assertEqual(conf.datetime, test_data._datetime)

        tmp_file.unlink()


class TestWriteJSON(unittest.TestCase):
    """Test writing JSON config files."""

    def test_write_json_config(self):

        tmp_file = pathlib.Path('tmp.json')

        conf = pc.read_config(test_phantom_file)
        conf.write_json(tmp_file)

        conf = pc.read_json(tmp_file)

        self.assertEqual(conf.config, test_data.config)
        self.assertEqual(conf.header, test_data.header)
        self.assertEqual(conf.datetime, test_data._datetime)

        tmp_file.unlink()


class TestWriteTOML(unittest.TestCase):
    """Test writing TOML config files."""

    def test_write_toml_config(self):

        tmp_file = pathlib.Path('tmp.toml')

        conf = pc.read_config(test_phantom_file)
        conf.write_toml(tmp_file)

        conf = pc.read_toml(tmp_file)

        self.assertEqual(conf.variables, test_data.variables)
        self.assertEqual(conf.values, test_data.values)
        self.assertEqual(conf.header, test_data.header)
        self.assertEqual(conf.datetime, test_data._datetime)

        tmp_file.unlink()


class TestModify(unittest.TestCase):
    """Testing adding, removing, modifying values."""

    def test_add_value(self):

        conf = pc.read_config(test_phantom_file)
        conf.add_variable('new_variable', 999)
        conf.add_variable('new_variable', 999, comment='No comment', block='New block')
        self.assertEqual(conf.config['new_variable'].value, 999)

    def test_remove_variable(self):

        conf = pc.read_config(test_phantom_file)
        conf.remove_variable('dtmax')
        self.assertFalse('dtmax' in conf.variables)

    def test_change_variable(self):

        conf = pc.read_config(test_phantom_file)
        hfact_prev = conf.config['hfact'].value
        conf.change_value('hfact', 1.2)
        self.assertNotEqual(conf.config['hfact'].value, hfact_prev)


if __name__ == '__main__':
    unittest.main(verbosity=2)
