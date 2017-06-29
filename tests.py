#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from unittest.case import TestCase

from rest_camel.util import camelize, underscorize


class MockReturnDict(OrderedDict):
    """
    Simulate Django Rest Framework's ReturnDict class.

    Using this mock class is necessary so you don't have to load a lot more
    configuration baggage to get a "real" instance of a ReturnDict.
    """
    def __init__(self, *args, **kwargs):
        super(MockReturnDict, self).__init__(*args, **kwargs)

    def copy(self):
        return MockReturnDict(self)

    def __repr__(self):
        return dict.__repr__(self)

    def __reduce__(self):
        return (dict, (dict(self),))


class UnderscoreToCamelTestCase(TestCase):

    def test_under_to_camel_dict(self):
        input = {
            "title_display": 1
        }
        output = {
            "titleDisplay": 1
        }
        result = camelize(input)
        self.assertEqual(result, output)
        self.assertIsNot(result, input, "should not change original dict")

    def test_under_to_camel_list(self):
        input = [
            {"title_display": 1}
        ]
        output = [
            {"titleDisplay": 1}
        ]
        result = camelize(input)
        self.assertEqual(result, output)
        self.assertIsNot(result, input, "should not change original list")

    def test_under_to_camel_tuple(self):
        input = (
            {"title_display": 1},
        )
        output = (
            {"titleDisplay": 1},
        )
        result = camelize(input)
        self.assertEqual(result, output)
        self.assertIsNot(result, input, "should not change original tuple")

    def test_under_to_camel_nested(self):
        input = {
            "title_display": 1,
            "a_list": [1, "two_three", {"three_four": 5}],
            "a_tuple": ("one_two", 3)
        }
        output = {
            "titleDisplay": 1,
            "aList": [1, "two_three", {"threeFour": 5}],
            "aTuple": ("one_two", 3)
        }
        self.assertEqual(camelize(input), output)

    def test_tuples(self):
        input = {
            "multiple_values": (1, 2)
        }
        output = {
            "multipleValues": (1, 2)
        }
        self.assertEqual(camelize(input), output)

    def test_integer_key(self):
        input = {
            1: 1
        }
        output = {
            "1": 1
        }
        self.assertEqual(camelize(input), output)

    def test_under_to_camel_drf_ReturnDict(self):
        input = MockReturnDict(
            {"title_display": 1},
        )
        output = {
            "titleDisplay": 1,
        }
        result = camelize(input)
        self.assertEqual(result, output)


class CamelToUnderscoreTestCase(TestCase):
    def test_camel_to_under_dict(self):
        input = {
            "titleDisplay": 1
        }
        output = {
            "title_display": 1
        }
        result = underscorize(input)
        self.assertEqual(result, output)
        self.assertIsNot(result, input, "should not change original dict")

    def test_camel_to_under_list(self):
        input = [
            {"titleDisplay": 1}
        ]
        output = [
            {"title_display": 1}
        ]
        result = underscorize(input)
        self.assertEqual(result, output)
        self.assertIsNot(result, input, "should not change original list")

    def test_camel_to_under_tuple(self):
        input = [
            {"titleDisplay": 1}
        ]
        output = [
            {"title_display": 1}
        ]
        result = underscorize(input)
        self.assertEqual(result, output)
        self.assertIsNot(result, input, "should not change original tuple")

    def test_camel_to_under_nested(self):
        input = {
            "titleDisplay": 1,
            "aList": [1, "two_three", {"threeFour": 5}],
            "aTuple": ("one_two", 3)
        }
        output = {
            "title_display": 1,
            "a_list": [1, "two_three", {"three_four": 5}],
            "a_tuple": ("one_two", 3)
        }
        self.assertEqual(underscorize(input), output)

    def test_integer_key(self):
        input = [
            {1: 1}
        ]
        output = [
            {"1": 1}
        ]
        result = underscorize(input)
        self.assertEqual(result, output)


class CompatibilityTest(TestCase):
    def test_compatibility(self):
        input = {
            "title_display": 1,
            "a_list": [1, "two_three", {"three_four": 5}],
            "a_tuple": ("one_two", 3)
        }
        self.assertEqual(underscorize(camelize(input)), input)
