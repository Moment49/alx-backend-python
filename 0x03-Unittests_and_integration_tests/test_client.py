#!/usr/bin/env python3
"""
Unit and integration tests for GithubOrgClient.
"""
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
from fixtures import fixtures
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google", {"login": "google", "id": 1}),
        ("abc", {"login": "abc", "id": 2}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_response, mock_get_json):
        """Test org property"""
        mock_get_json.return_value = mock_response
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, mock_response)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test _public_repos_url"""
        test_payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("test_org")
            self.assertEqual(client._public_repos_url, test_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos"""
        test_payload = [{"name": "repo1"}, {"name": "repo2"}, {"name": "repo3"}]
        mock_get_json.return_value = test_payload
        expected_repos = ["repo1", "repo2", "repo3"]
        test_url = "https://api.github.com/orgs/test_org/repos"

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = test_url
            client = GithubOrgClient("test_org")
            self.assertEqual(client.public_repos(), expected_repos)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license"""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class(fixtures)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class-wide mock for requests.get"""
        org_url = "https://api.github.com/orgs/{}".format(cls.org_payload["login"])
        repos_url = cls.org_payload["repos_url"]

        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Side effects: return different responses based on URL
        cls.mock_get.side_effect = lambda url: unittest.mock.Mock(
            json=lambda: (
                cls.org_payload if url == org_url
                else cls.repos_payload if url == repos_url
                else None
            )
        )

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns correct list"""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos returns only Apache-2.0 licensed repos"""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
