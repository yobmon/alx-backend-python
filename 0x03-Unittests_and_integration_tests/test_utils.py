#!/usr/bin/env python3


import unittest
from utils import access_nested_map
from parameterized import parameterized
from utils import get_json
from unittest.mock import patch,Mock
from utils import memoize
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
class TestGetJson(unittest.TestCase):
    @patch("utils.requests.get")
    def test_get_json(self, mock_get):
        test_values = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
        for test_url, test_payload in test_values:
            # Configure the mock for this iteration
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            # Call the function
            result = get_json(test_url)

            # Assertions
            mock_get.assert_called_once_with(test_url)  # Called once with URL
            self.assertEqual(result, test_payload)       # Correct JSON returned

            # Reset mock between iterations
            mock_get.reset_mock()
class TestMemoize(unittest.TestCase):
    class test_memoize:
         def a_method(self):
          return 42

         @memoize
         def a_property(self):
          return self.a_method()
    def test_memoize(self):
        test_instance = self.test_memoize()
        with patch.object(test_instance, 'a_method', return_value=42) as mock_a_method:
            result1 = test_instance.a_property
            result2 = test_instance.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_a_method.assert_called_once()
        
if __name__ == '__main__':
    unittest.main()