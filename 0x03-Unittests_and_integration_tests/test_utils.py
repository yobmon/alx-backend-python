#!/usr/bin/env python3


import unittest
from utils import access_nested_map
from parameterized import parameterized
class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand( [
        ({"a": 1}, ["a"], 1),
        ({"a":{"b": 2}}, ["a", "b"], 2),
        ({"outer": {"inner": {"key": "value"}}}, ["outer", "inner", "key"], "value"),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
         result =access_nested_map (nested_map, path)
         self.assertEqual(result, expected)
if __name__ == '__main__':
    unittest.main()