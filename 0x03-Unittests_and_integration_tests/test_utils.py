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
#          nested_map={}, path=("a",)
# nested_map={"a": 1}, path=("a", "b")
    @parameterized.expand( [
        ({}, ("a",)),
        ({"a": 1},("a", "b"))
        ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)
if __name__ == '__main__':
    unittest.main()