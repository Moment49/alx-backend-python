#!/usr/bin/env python3
import unittest
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized, parameterized_class


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

