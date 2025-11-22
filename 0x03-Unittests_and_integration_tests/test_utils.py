#!/usr/bin/env python3
"""
Unit tests for utility functions: access_nested_map, get_json, and memoize.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):

    """Unit tests for the get_json function."""

    @parameterized.expand([
        ({"a": 1}, ["a"], 1),
        ({"a": {"b": 2}}, ["a", "b"], 2),
        (
            {"outer": {"inner": {"key": "value"}}},
            ["outer", "inner", "key"],
            "value",
        ),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):

    """Unit tests for the memoize decorator."""

    @patch("utils.requests.get")
    def test_get_json(self, mock_get):
        test_values = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]

        for test_url, test_payload in test_values:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)

            mock_get.reset_mock()


class TestClass:
    """Class used for testing memoization decorator."""

    def a_method(self):
        return 42

    @memoize
    def a_property(self):
        return self.a_method()


class TestMemoize(unittest.TestCase):

    def test_memoize(self):
        test_instance = TestClass()

        with patch.object(
            test_instance,
            "a_method",
            return_value=42
        ) as mock_a_method:
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            mock_a_method.assert_called_once()
