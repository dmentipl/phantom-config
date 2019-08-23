"""
Testing phantomconfig.
"""

import pathlib
import unittest

import phantomconfig as pc

from .stub import test_data

test_file = pathlib.Path(__file__).parent / 'stub' / 'config.in'


class TestReadPhantom(unittest.TestCase):
    """Test reading Phantom config files."""

    def test_read_phantom_config(self):

        conf = pc.read_config(test_file)
        self.assertEqual(conf.config, test_data.test_config)
        self.assertEqual(conf.header, test_data.test_header)


if __name__ == '__main__':
    unittest.main(verbosity=2)
