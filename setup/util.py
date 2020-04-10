# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 21:37:26 2019

@author: cyshi
"""
from voluptuous import Schema, Required, Invalid, Any, Optional
from .import Database
from numbers import Number

def valid_tuple(obj):
    """A method to validate if a impact assesment name is a valid key tuple. Ia_method should follow the format such as
    ('TRACI', 'environmental impact', 'acidification')
    """
    try:
        assert isinstance(obj, tuple)
        assert isinstance(obj[0], str)
        assert isinstance(obj[1], str)
    except:
        raise Invalid("{} is not a valid key tuple".format(obj))
    return obj


uncertainty_dict = {
    Required("amount"): Number,
    Optional("uncertainty type"): int,
    Optional("loc"): Number,
    Optional("scale"): Number,
    Optional("shape"): Number,
    Optional("minimum"): Number,
    Optional("maximum"): Number}


exchange = {Required("input"): valid_tuple, Required("type"): str,}
exchange.update(uncertainty_dict)

maybe_uncertainty = Any(Number, uncertainty_dict)
ia_validator = Schema([Any([valid_tuple, maybe_uncertainty],[valid_tuple, maybe_uncertainty, object])])


def get_activity(key):
    try:
        return Database(key[0]).get(key[1])
    except TypeError:
        raise Exception ("Key {} cannot be understood as an activity"
                            " or `(database, code)` tuple.")
#        raise UnknownObject("Key {} cannot be understood as an activity"
#                            " or `(database, code)` tuple.")