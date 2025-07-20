#!/usr/bin/env python3
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