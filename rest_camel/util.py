import re
from collections import OrderedDict
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


class ProtectedDict(dict):
    """
    A dict variant for which keys will be preserved when passed
    to :func:`camelize` or :func:`underscorize`, but keys of all nested
    dictionaries will be still transformed.
    """
    pass


def preserve_dict_keys(dictionary):
    """
    Utility function which sets preserve keys flag on the dictionary.
    Either constructs a new :class:`ProtectedDict` (if the dictionary is built-in dict object),
    or sets the `_preserve_keys` attribute and returns the original dictionary.

    :param dictionary: Dictionary of which the keys should be protected.
    :return: :class:`ProtectedDict` or the original dictionary with `_preserve_keys` attribute.
    """
    data_type = type(dictionary)
    if data_type is dict:
        return ProtectedDict(dictionary)
    elif data_type is ProtectedDict:
        return dictionary
    else:
        setattr(dictionary, '_preserve_keys', True)
        return dictionary


def camelize_key(key, uppercase_first_letter=True):
    """
    From: https://github.com/jpvanhal/inflection

    Convert strings to CamelCase.
    Examples::
        >>> camelize("device_type")
        "DeviceType"
        >>> camelize("device_type", False)
        "deviceType"
    :func:`camelize` can be though as a inverse of :func:`underscore`, although
    there are some cases where that does not hold::
        >>> camelize(underscore("IOError"))
        "IoError"
    :param uppercase_first_letter: if set to `True` :func:`camelize` converts
        strings to UpperCamelCase. If set to `False` :func:`camelize` produces
        lowerCamelCase. Defaults to `True`.
    """

    if type(key) is int:
        # Could be an integer (Field.choices, for example): { 1: "foo" }
        key = str(key)

    if uppercase_first_letter:
        return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), key)
    else:
        return key[0].lower() + camelize_key(key)[1:]


def underscore_key(key):
    """
    From: https://github.com/jpvanhal/inflection

    Make an underscored, lowercase form from the expression in the string.
    Example::
        >>> underscore("DeviceType")
        "device_type"
    As a rule of thumb you can think of :func:`underscore` as the inverse of
    :func:`camelize`, though there are cases where that does not hold::
        >>> camelize(underscore("IOError"))
        "IoError"
    """

    if type(key) is int:
        key = str(key)

    key = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', key)
    key = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', key)
    key = key.replace("-", "_")
    return key.lower()


def camelize(data):
    data_type = type(data)

    if data_type in (dict, OrderedDict, ReturnDict, ProtectedDict):
        kwargs = {}
        if data_type is ReturnDict:
            kwargs['serializer'] = data.serializer
        new_dict = data_type(**kwargs)

        has_preserve_keys_attr = hasattr(data, '_preserve_keys')
        if data_type is not ProtectedDict and not has_preserve_keys_attr:
            for k, v in data.items():
                new_dict[camelize_key(k, False)] = camelize(v)
        else:
            for k, v in data.items():
                new_dict[k] = camelize(v)
            if has_preserve_keys_attr:
                setattr(new_dict, '_preserve_keys', getattr(data, '_preserve_keys'))

        return new_dict

    if data_type in (list, tuple, ReturnList):
        kwargs = {}
        if data_type is ReturnList:
            kwargs['serializer'] = data.serializer
        return data_type((camelize(x) for x in data), **kwargs)

    return data


def underscorize(data):
    data_type = type(data)

    if data_type in (dict, OrderedDict, ReturnDict, ProtectedDict):
        kwargs = {}
        if data_type is ReturnDict:
            kwargs['serializer'] = data.serializer
        new_dict = data_type(**kwargs)

        has_preserve_keys_attr = hasattr(data, '_preserve_keys')
        if data_type is not ProtectedDict and not has_preserve_keys_attr:
            for key, value in data.items():
                new_dict[underscore_key(key)] = underscorize(value)
        else:
            for key, value in data.items():
                new_dict[key] = underscorize(value)
            if has_preserve_keys_attr:
                setattr(new_dict, '_preserve_keys', getattr(data, '_preserve_keys'))

        return new_dict

    if data_type in (list, tuple, ReturnList):
        kwargs = {}
        if data_type is ReturnList:
            kwargs['serializer'] = data.serializer
        return data_type((underscorize(x) for x in data), **kwargs)

    return data
