import unittest
from unittest.mock import patch
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
