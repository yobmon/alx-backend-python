#!/usr/bin/env python3
"""Unit tests for GithubOrgClient."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


from unittest import TestCase
from unittest.mock import patch, MagicMock
from parameterized import parameterized_class

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos



class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org returns the correct value."""
        expected = {"payload": True}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected)

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos(self):
        """Test that _public_repos_url returns expected repos_url."""
        expected_url = (
            "https://api.github.com/orgs/google/repos"
        )
        mock_org_payload = {"repos_url": expected_url}

        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = mock_org_payload

            client = GithubOrgClient("google")
            result = client._public_repos_url

        self.assertEqual(result, expected_url)



@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(TestCase):
    """Integration tests for GithubOrgClient with fixtures."""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get and mock external calls."""

        cls.get_patcher = patch("requests.get")
        mocked_get = cls.get_patcher.start()

        # Create mock response object
        mock_response = MagicMock()

        # Use side_effect to return correct fixture payloads per URL
        def side_effect(url):
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        mocked_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo list."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering repos by Apache-2.0 license."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos("apache-2.0"),
            self.apache2_repos
        )