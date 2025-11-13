#!/usr/bin/env python3


import unittest
from utils import access_nested_map
from parameterized import parameterized
from utils import get_json
from unittest.mock import patch,Mock
class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand( [
        ({"a": 1}, ["a"], 1),
        ({"a":{"b": 2}}, ["a", "b"], 2),
        ({"outer": {"inner": {"key": "value"}}}, ["outer", "inner", "key"], "value"),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
         result =access_nested_map (nested_map, path)
         self.assertEqual(result, expected)
    @parameterized.expand( [
        ({}, ("a")),
        ({"a": 1},("a", "b"))
        ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)
class   TestGetJson(unittest.TestCase):
    @patch("requests.get")
    def test_get_json(self, mock_get):
        mock_response = Mock()
        expected_payload = {"key": "value"}
        mock_response.json.return_value = expected_payload
        mock_get.return_value = mock_response

        url = "http://example.com/api"
        result = get_json(url)
        self.assertEqual(result, expected_payload)
        mock_get.assert_called_once_with(url)
        
if __name__ == '__main__':
    unittest.main()