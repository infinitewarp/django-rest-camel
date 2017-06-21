#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict
from unittest.case import TestCase

# Bootstrap django before importing anything from rest_framework.
from django.conf import settings

settings.configure()

from rest_camel.util import camelize, underscorize, ProtectedDict, preserve_dict_keys
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


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

    def test_return_dict(self):
        """
        camelize() should convert keys in an instance of rest_framework.utils.serializer_helpers.ReturnDict
        and keep the same serializer.
        """
        fake_serializer_instance = (42,)

        input = ReturnDict([("title_display", 1), ("title_field", 2)], serializer=fake_serializer_instance)
        output = ReturnDict([("titleDisplay", 1), ("titleField", 2)], serializer=fake_serializer_instance)

        result = camelize(input)
        self.assertEqual(result, output)
        self.assertIs(result.serializer, output.serializer)

    def test_return_list(self):
        """
        camelize() should convert keys in all objects contained in an instance
        of rest_framework.utils.serializer_helpers.ReturnList and keep the same serializer.
        """
        fake_serializer_instance = (42,)

        input = ReturnList([{"title_display": 1}, {"title_field": 2}], serializer=fake_serializer_instance)
        output = ReturnList([{"titleDisplay": 1}, {"titleField": 2}], serializer=fake_serializer_instance)

        result = camelize(input)
        self.assertEqual(result, output)
        self.assertIs(result.serializer, output.serializer)

    def test_protected_dict(self):
        """
        camelize() should not convert keys in instances of ProtectedDict, but should convert keys
        of all nested dictionaries.
        """
        input = {
            "an_int": 42,
            "protected_dict": ProtectedDict([("title_display", 1), ("nested_dict", {
                "test_field": 1, "any_field": 2
            })]),
            "the_str": "abc",
        }
        output = {
            "anInt": 42,
            "protectedDict": ProtectedDict([("title_display", 1), ("nested_dict", {
                "testField": 1, "anyField": 2
            })]),
            "theStr": "abc",
        }

        result = camelize(input)
        self.assertEqual(result, output)

    def test_protected_attr(self):
        """
        camelize() should not convert keys in instances with `_preserve_keys` attribute set,
         but should convert keys of all nested dictionaries.
        """
        input = {
            "an_int": 42,
            "protected_dict": OrderedDict([("title_display", 1), ("nested_dict", {
                "test_field": 1, "any_field": 2
            })]),
            "the_str": "abc",
        }
        setattr(input['protected_dict'], '_preserve_keys', True)
        output = {
            "anInt": 42,
            "protectedDict": OrderedDict([("title_display", 1), ("nested_dict", {
                "testField": 1, "anyField": 2
            })]),
            "theStr": "abc",
        }
        result = camelize(input)
        self.assertEqual(result, output)
        self.assertTrue(getattr(result['protectedDict'], '_preserve_keys'))


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

    def test_return_dict(self):
        """
        underscorize() should convert keys in an instance of rest_framework.utils.serializer_helpers.ReturnDict
        and keep the same serializer.
        """
        fake_serializer_instance = (42,)

        input = ReturnDict([("titleDisplay", 1), ("titleField", 2)], serializer=fake_serializer_instance)
        output = ReturnDict([("title_display", 1), ("title_field", 2)], serializer=fake_serializer_instance)

        result = underscorize(input)
        self.assertEqual(result, output)
        self.assertIs(result.serializer, output.serializer)

    def test_return_list(self):
        """
        underscorize() should convert keys in all objects contained in an instance
        of rest_framework.utils.serializer_helpers.ReturnList and keep the same serializer.
        """
        fake_serializer_instance = (42,)

        input = ReturnList([{"titleDisplay": 1}, {"titleField": 2}], serializer=fake_serializer_instance)
        output = ReturnList([{"title_display": 1}, {"title_field": 2}], serializer=fake_serializer_instance)

        result = underscorize(input)
        self.assertEqual(result, output)
        self.assertIs(result.serializer, output.serializer)

    def test_protected_dict(self):
        """
        underscorize() should not convert keys in instances of ProtectedDict, but should convert keys
        of all nested dictionaries.
        """
        input = {
            "anInt": 42,
            "protectedDict": ProtectedDict([("titleDisplay", 1), ("nestedDict", {
                "testField": 1, "anyField": 2
            })]),
            "theStr": "abc",
        }
        output = {
            "an_int": 42,
            "protected_dict": ProtectedDict([("titleDisplay", 1), ("nestedDict", {
                "test_field": 1, "any_field": 2
            })]),
            "the_str": "abc",
        }

        result = underscorize(input)
        self.assertEqual(result, output)

    def test_protected_attr(self):
        """
        underscorize() should not convert keys in instances of ProtectedDict, but should convert keys
        of all nested dictionaries.
        """
        input = {
            "anInt": 42,
            "protectedDict": OrderedDict([("titleDisplay", 1), ("nestedDict", {
                "testField": 1, "anyField": 2
            })]),
            "theStr": "abc",
        }
        setattr(input['protectedDict'], '_preserve_keys', True)
        output = {
            "an_int": 42,
            "protected_dict": OrderedDict([("titleDisplay", 1), ("nestedDict", {
                "test_field": 1, "any_field": 2
            })]),
            "the_str": "abc",
        }

        result = underscorize(input)
        self.assertEqual(result, output)
        self.assertTrue(getattr(result['protected_dict'], '_preserve_keys'))


class CompatibilityTest(TestCase):
    def test_compatibility(self):
        input = {
            "title_display": 1,
            "a_list": [1, "two_three", {"three_four": 5}],
            "a_tuple": ("one_two", 3)
        }
        self.assertEqual(underscorize(camelize(input)), input)

    def test_compatibility_return_collections(self):
        """
        When the input with ReturnDict and ReturnList collections is processed by camelize() and then by underscorize(),
        the result should be same. Serializers should be preserved in all nested ReturnDict and ReturnList collections.
        """
        fake_serializer_instance_1 = (42,)
        fake_serializer_instance_2 = (42,)
        fake_serializer_instance_3 = (42,)
        input = ReturnDict([
            ("title_display", 1),
            ("a_list", ReturnList(
                [1, "two_three", ReturnDict([("threee_four", 5)], serializer=fake_serializer_instance_3)],
                serializer=fake_serializer_instance_2)
             ),
            ("a_tuple", ("one_two", 3))
        ], serializer=fake_serializer_instance_1)

        result = underscorize(camelize(input))
        self.assertEqual(result, input)
        self.assertIs(result.serializer, input.serializer)
        self.assertIs(result['a_list'].serializer, input['a_list'].serializer)
        self.assertIs(result['a_list'][2].serializer, input['a_list'][2].serializer)


class PreserveDictKeysTest(TestCase):
    def test_dict(self):
        """
        Tests that :func:`preserve_dict_keys` converts a :class:`dict` to :class:`ProtectedDict`.
        """
        input = {'a': 1, 'b': 2, 'c': 3}
        output = ProtectedDict([('a', 1), ('b', 2), ('c', 3)])
        result = preserve_dict_keys(input)
        self.assertEqual(result, output)

    def test_ordered_dict(self):
        """
        Tests that :func:`preserve_dict_keys` adds a :attr:`_preserve_keys` attribute to custom dictionary.
        """
        input = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
        result = preserve_dict_keys(input)
        self.assertIs(result, input)
        self.assertTrue(getattr(result, '_preserve_keys'))

    def test_protected_dict(self):
        """
        Tests that :func:`preserve_dict_keys` returns the same instance if passed :class:`ProtectedDict`.
        """
        input = ProtectedDict([('a', 1), ('b', 2), ('c', 3)])
        result = preserve_dict_keys(input)
        self.assertIs(input, result)
