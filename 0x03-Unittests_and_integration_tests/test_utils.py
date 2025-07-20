#!/usr/bin/env python3
"""
Unit tests for utility functions in utils.py, including access_nested_map, get_json, and memoize.
This module uses unittest and parameterized for test cases and ensures all functions
are properly tested.
"""
import unittest
from utils import access_nested_map, get_json, memoize, Dict
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock

  

class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for access_nested_map function.
    This class contains unit tests for the access_nested_map utility,
    which retrieves values from nested dictionaries using a tuple path.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """
        Test that access_nested_map returns correct value.

        Args:
            nested_map (dict): Input nested dictionary.
            path (tuple): Keys to follow.
            expected_result (Any): Expected value at the end of the path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b')
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """
        Test that access_nested_map raises KeyError for invalid path.
        Args:
            nested_map (dict): Input nested dictionary.
            path (tuple): Keys to follow.
            expected_key (str): The key expected to raise KeyError.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{expected_key}'")

class TestGetJson(unittest.TestCase):
    """
    Test class for the get_json function.
    Ensures get_json returns the expected payload using mocked HTTP requests.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url: str, test_payload: Dict,
                     mock_get: Mock) -> None:
        """
        Test that get_json returns the expected payload without making actual
        HTTP requests.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)

  

class TestMemoize(unittest.TestCase):
    """
    Test class for the memoize decorator.
    Ensures that memoization caches method results and avoids repeated calls.
    """

    def test_memoize(self):
        """
        Test that the memoize decorator caches the result of a method.
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()
            result1 = obj.a_property
            result2 = obj.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
