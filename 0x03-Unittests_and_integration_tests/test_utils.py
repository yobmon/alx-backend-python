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
        mock_response = Mock()
        expected_payload = {"key": "value"}
        mock_response.json.return_value = expected_payload
        mock_get.return_value = mock_response

        url = "http://example.com/apikokos"
        result = get_json(url)
        self.assertEqual(result, expected_payload)
        mock_get.assert_called_once_with(url)
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