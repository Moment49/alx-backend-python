#!/usr/bin/env python3
import unittest
from utils import access_nested_map, get_json, memoize, Dict
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map function.
    This class contains unit tests for the access_nested_map utility,
    which retrieves values from nested dictionaries using a tuple path.
    """
    # The parameterized.expand decorator runs the test with multiple sets of inputs.
    @parameterized.expand([
     ({"a": 1}, ("a",), 1),   
     ({"a": {"b":2}}, ("a",), {"b":2} ), 
     ({"a": {"b":2}}, ("a","b"), 2)  
    ])
    def test_access_nested_map(self,nested_map, path,expected_result):
        """
        Test that access_nested_map returns correct value.

        Args:
            nested_map (dict): Input nested dictionary.
            path (tuple): Keys to follow.
            expected_result (Any): Expected value at the end of the path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected_result)


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map function with KeyError.""
    """

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b')
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """
        Test that accesss_nested_map raises KeyError for invalid path."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        
        self.assertEqual(str(context.exception), f"'{expected_key}'")

class TestGetJson(unittest.TestCase):
    """This is to test the Get Json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url: str, test_payload: Dict, mock_get: Mock) -> None:
        """
        Test that get_json returns the expected payload without making actual HTTP requests.
        """
        # Set up the mock response
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function under test
        result = get_json(test_url)

        # Assert it returned the correct payload
        self.assertEqual(result, test_payload)

        # Assert requests.get was called once with the correct URL
        mock_get.assert_called_once_with(test_url)


# Test class to test the memoize decorator
class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        # Define a test class with a method and a memoized property
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Use patch to mock a_method so we can track how many times it's called
        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()

            # Call the memoized property twice
            result1 = obj.a_property  # First call - should call a_method
            result2 = obj.a_property  # Second call - should use cached value

            # Assert that the return values are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert that a_method was called only once due to memoization
            mock_method.assert_called_once()