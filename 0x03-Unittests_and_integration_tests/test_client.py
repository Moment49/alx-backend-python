#!/usr/bin/env python3
"""Unittest module for GithubOrgClient."""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock, Mock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Tests for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: MagicMock) -> None:
        """
        Tests that GithubOrgClient.org returns the correct URL.

        Args:
            org_name: The organization name to test.
            mock_get_json: The mocked get_json method.
        """
        # Define mock_get_json's expected return value.
        # This simulates get_json's return for a real API call.
        expected_json_payload = {"login": org_name}
        mock_get_json.return_value = expected_json_payload

        # Instantiate the client with the current org_name
        client = GithubOrgClient(org_name)

        # Call the method being tested
        result = client.org

        # Assert that the result matches expected JSON.
        self.assertEqual(result, expected_json_payload)

        # Assert that get_json was called exactly once
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self) -> None:
        """
        Tests _public_repos_url returns correct URL from mocked org payload.
        """
        test_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }
        with patch(
            'client.GithubOrgClient.org', new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("testorg")
            result = client._public_repos_url
            self.assertEqual(result, test_payload["repos_url"])

    # Decorator to mock get_json
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: PropertyMock) -> None:
        """
        Tests public_repos returns expected list;
        mocks get_json, _public_repos_url.
        """
        # Define URL for mocked _public_repos_url property.
        mock_repos_url = "https://api.github.com/orgs/testorg/repos"

        # Define the payload that mock_get_json should return
        expected_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]
        mock_get_json.return_value = expected_repos_payload

        # Patch _public_repos_url property using context manager.
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = mock_repos_url

            # Instantiate the client
            client = GithubOrgClient("testorg")

            # Call the method being tested
            result = client.public_repos()

            # Test repo list
            self.assertEqual(result, ["repo1", "repo2", "repo3"])

            # Test that mocked get_json called once with the correct URL
            mock_get_json.assert_called_once_with(mock_repos_url)

            # Test that mocked _public_repos_url property called once.
            mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": None}, "my_license", False),  # Test case: no license key
        ({}, "my_license", False),  # Test case: empty repo dict
        ({"license": {"key": "my_license"},
          "name": "test_repo"}, "my_license", True),  # Additional test case
        ({"license": {"key": "MY_LICENSE"}},
         "my_license", False),  # Case sensitivity test
    ])
    def test_has_license(
        self, repo: dict, license_key: str, expected_result: bool
    ) -> None:
        """
        Tests `has_license` returns correct boolean for repo, license.

        Args:
            repo (dict): A dictionary representing a repository.
            license_key (str): The license key to check for.
            expected_result (bool): Expected has_license result
        """
        # Instantiate client; org_name irrelevant for this method.
        client = GithubOrgClient("some_org")

        # Call the method being tested
        result = client.has_license(repo, license_key)

        # Assert that the result matches the expected value
        self.assertEqual(result, expected_result)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Tests public_repos flow by mocking external requests.
    This class mocks HTTP requests to test public_repos's
    full flow without network calls.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        Sets up the class-level fixtures for integration tests.
        Mocks requests.get to return URL-specific payloads.
        """
        # Start a patcher for requests.get
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Define the side_effect function for the mocked requests.get
        def side_effect_func(url: str) -> Mock:
            """
            Mocks requests.get for varied responses by URL.
            """
            mock_response = Mock()
            if url == cls.org_payload["repos_url"].replace("/repos", ""):
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:  # URL for repos data
                mock_response.json.return_value = cls.repos_payload
            else:
                # Raise error for unexpected URL; ensures strict testing.
                raise ValueError(f"Unexpected URL in mock: {url}")
            return mock_response

        cls.mock_get.side_effect = side_effect_func

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Stops the patcher after all class integration tests.
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Tests the public_repos method in an integration context.
        Verifies that it returns the expected list of repository names.
        """
        # Instantiate client using an organization name.
        client = GithubOrgClient("google")

        # Call the method being tested
        result = client.public_repos()

        # Assert that the result matches the expected_repos from the fixture
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Tests public_repos with license filter in integration..
        Verifies that it returns expected repo names, filtered by license..
        """
        # Instantiate client using an organization name.
        client = GithubOrgClient("google")

        # Call test method using license argument.
        result = client.public_repos(license="apache-2.0")

        # Assert the result matches the apache2_repos from fixture
        self.assertEqual(result, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
    