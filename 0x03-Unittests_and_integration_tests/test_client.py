#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class in client.py. This module uses unittest,
parameterized,mock to test organization data retrieval and repository
listing from the GitHub API client.
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient.org method."""

    @parameterized.expand([
        ("google", {"login": "google", "id": 1}),
        ("abc", {"login": "abc", "id": 2}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_response, mock_get_json):
        """Test that GithubOrgClient.org returns correct data
        and calls get_json with expected URL once.
        """
        mock_get_json.return_value = mock_response

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, mock_response)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient class."""

    def test_public_repos_url(self):
        """Test _public_repos_url returns expected repos_url
        from the mocked GithubOrgClient.org property.
        """
        test_payload = {
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }

        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = test_payload

            client = GithubOrgClient("test_org")
            result = client._public_repos_url

            self.assertEqual(result, test_payload["repos_url"])
            mock_org.assert_called_once()


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient class."""

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected list of repo names
        and that get_json and _public_repos_url are called once.
        """
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_payload

        expected_repos = ["repo1", "repo2", "repo3"]
        test_url = "https://api.github.com/orgs/test_org/repos"

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = test_url

            client = GithubOrgClient("test_org")
            result = client.public_repos()

            self.assertEqual(result, expected_repos)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_url)
