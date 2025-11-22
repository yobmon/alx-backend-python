#!/usr/bin/env python3
"""
Unit tests for utility functions: access_nested_map, get_json, and memoize.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ["a"], 1),
        ({"a": {"b": 2}}, ["a", "b"], 2),
        (
            {"outer": {"inner": {"key": "value"}}},
            ["outer", "inner", "key"],
            "value"
        ),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns the correct value for a given path."""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError when path is invalid."""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Unit tests for the get_json function."""

    @patch("utils.requests.get")
    def test_get_json(self, mock_get):
        """Test that get_json returns the expected JSON payload from a URL."""
        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]

        for url, expected_json in test_cases:
            # Mock the response object
            mock_response = unittest.mock.Mock()
            mock_response.json.return_value = expected_json
            mock_get.return_value = mock_response

            # Call the function
            result = get_json(url)

            # Assert the function returns the expected JSON
            self.assertEqual(result, expected_json)

            # Assert requests.get was called once with the correct URL
            mock_get.assert_called_once_with(url)

            # Reset mock for the next iteration
            mock_get.reset_mock()


class TestClass:
    """Class used for testing the memoize decorator."""

    def a_method(self):
        """Method that returns a fixed value for testing."""
        return 42

    @memoize
    def a_property(self):
        """Property decorated with memoize to cache the method result."""
        return self.a_method()


class TestMemoize(unittest.TestCase):
    """Unit tests for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result of a method call."""
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

