#!/usr/bin/env python3
"""Unit and integration tests for GithubOrgClient."""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import (
    org_payload,
    repos_payload,
    expected_repos,
    apache2_repos,
)


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct payload."""
        expected = {"key": "value"}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns repos_url from org."""
        expected_url = "https://api.github.com/orgs/google/repos"
        fake_org = {"repos_url": expected_url}

        # Patch the org property (memoized) with a PropertyMock
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = fake_org

            client = GithubOrgClient("google")
            result = client._public_repos_url

            self.assertEqual(result, expected_url)
            mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns a list of repo names."""
        # repos payload returned by get_json
        repo_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = repo_payload

        # Patch the _public_repos_url property to return a test URL
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_pub_url:
            mock_pub_url.return_value = "https://api.github.com/orgs/google/repos"

            client = GithubOrgClient("google")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_pub_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns True/False depending on license key."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key),
                         expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using fixtures."""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get and set side_effect based on URL."""
        # Patch the requests.get used by utils.get_json (utils imports requests)
        cls.get_patcher = patch("utils.requests.get")
        mocked_get = cls.get_patcher.start()

        # Create a MagicMock response and set .json() return_value dynamically
        mock_response = MagicMock()

        def _side_effect(url, *args, **kwargs):
            """Return a mock response whose .json() returns the right payload."""
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload.get("repos_url"):
                mock_response.json.return_value = cls.repos_payload
            else:
                # default empty
                mock_response.json.return_value = {}
            return mock_response

        mocked_get.side_effect = _side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test: public_repos returns the expected list."""
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test: public_repos filters by license key."""
        client = GithubOrgClient("google")
        result = client.public_repos("apache-2.0")
        self.assertEqual(result, self.apache2_repos)
