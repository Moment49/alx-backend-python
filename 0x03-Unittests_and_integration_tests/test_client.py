#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class in client.py.
This module uses unittest, parameterized, and mock to test organization data retrieval
and repository listing from the GitHub API client.
"""
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
import requests
from fixtures import fixtures 
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

    @parameterized.expand([
    ({"license": {"key": "my_license"}}, "my_license", True),
    ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean."""
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(fixtures)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos method"""

    @classmethod
    def setUpClass(cls):
        """Patch only external requests for integration test"""
        cls.get_patcher = patch('client.get_json', side_effect=[
            cls.org_payload,    # First call: org data
            cls.repos_payload   # Second call: repos list
        ])
        cls.mock_get = cls.get_patcher.start()

        # Instantiate the client using the org's login
        cls.client = GithubOrgClient(cls.org_payload["login"])

    @classmethod
    def tearDownClass(cls):
        """Stop patched get_json"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repository names"""
        self.assertEqual(self.client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filtering"""
        self.assertEqual(
            self.client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
