"""
Testing phantomconfig.
"""

import pathlib
import unittest

import phantomconfig as pc

from .stub import test_data

test_phantom_file = pathlib.Path(__file__).parent / 'stub' / 'config.in'
test_json_file = pathlib.Path(__file__).parent / 'stub' / 'config.json'
test_dict = test_data.test_dict


class TestReadPhantom(unittest.TestCase):
    """Test reading Phantom config files."""

    def test_read_phantom_config(self):

        conf = pc.read_config(test_phantom_file)
        self.assertEqual(conf.config, test_data.test_config)
        self.assertEqual(conf.header, test_data.test_header)
        self.assertEqual(conf.datetime, test_data.test_datetime)


class TestReadJSON(unittest.TestCase):
    """Test reading JSON config files."""

    def test_read_json_config(self):

        conf = pc.read_json(test_json_file)
        self.assertEqual(conf.config, test_data.test_config)
        self.assertEqual(conf.header, test_data.test_header)
        self.assertEqual(conf.datetime, test_data.test_datetime)


class TestReadDict(unittest.TestCase):
    """Test reading Python dictionaries."""

    def test_read_dict(self):

        conf = pc.read_dict(test_dict)
        self.assertEqual(conf.config, test_data.test_config)
        self.assertEqual(conf.header, test_data.test_header)
        self.assertEqual(conf.datetime, test_data.test_datetime)


if __name__ == '__main__':
    unittest.main(verbosity=2)
