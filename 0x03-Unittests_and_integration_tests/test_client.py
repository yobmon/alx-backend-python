#!/usr/bin/env python3
"""Unit tests for GithubOrgClient."""

import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient
from utils import get_json


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value."""
        # Mock return value
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        # Instantiate client
        client = GithubOrgClient(org_name)

        # Access org property (memoized)
        result = client.org

        # Assertions
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)
