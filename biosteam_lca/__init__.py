# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 14:23:21 2019

@author: cyshi
"""
name = 'biosteam_lca'
#
#from inventory_finder import InventoryFinder,BuiltInInventory
#from units import *
__version__ = (0, 1)

from .setup import databases, methods
from . method_constructor import Method, Methods
from .monte_carlo import MultiMonteCarlo
#
__all__ = [ 'databases', 'methods', 'MultiMonteCarlo', 'Method', 'Methods']
##
##
### %% Import base utils
##
##import pandas as pd
##import numpy as np
##from pint import UnitRegistry
##import os
##
#
##from .allocation import *
#from .correlation import *
#from .databases import *
#from ._imports import *
#from .inventory_finder import *
#from preset import *
##
##from . import allocation
#from . import correlation
#from . import databases
#from . import _imports
#from . import inventory_finder
#from . import preset

#
#try:
#    from .monte_carlo import (
#        ComparativeMonteCarlo,
#        direct_solving_worker,
#        DirectSolvingMixin,
#        DirectSolvingMonteCarloLCA,
#        MonteCarloLCA,
#        MultiMonteCarlo,
#        ParallelMonteCarlo,
#    )
#    from .mc_vector import ParameterVectorLCA
#except ImportError:
#    None

#import sys
#import warnings
#
#
#if sys.version_info < (3, 0):
#    def warning_message(message, *args, **kwargs):
#        # All strings are unicode, but Py2 warning doesn't like unicode
#        return b"Warning: " + str(message).encode("utf-8", "ignore") + b"\n"
#
#    warnings.formatwarning = warning_message
#import brightway2 as bw2
#databases = bw2.databases 
#
#
#if 'biosphere3' not in databases:
#    try:
#        bw2.bw2setup()
#    except:
#        pass



UNITS_NORMALIZATION = {
    "a": "year",  # Common in LCA circles; could be confused with acre
    "Bq": "Becquerel",
    "g": "gram",
    "Gj": "gigajoule",
    "h": "hour",
    "ha": "hectare",
    "hr": "hour",
    "kBq": "kilo Becquerel",
    "kg": "kilogram",
    "kgkm": "kilogram kilometer",
    "km": "kilometer",
    "kj": "kilojoule",
    "kWh": "kilowatt hour",
    "l": "litre",
    "lu": "livestock unit",
    "m": "meter",
    "m*year": "meter-year",
    "m2": "square meter",
    "m2*year": "square meter-year",
    "m2a": "square meter-year",
    "m2y": "square meter-year",
    "m3": "cubic meter",
    "m3*year": "cubic meter-year",
    "m3a": "cubic meter-year",
    "m3y": "cubic meter-year",
    "ma": "meter-year",
    "metric ton*km": "ton kilometer",
    "MJ": "megajoule",
    "my": "meter-year",
    "nm3": "cubic meter",
    "p": "unit",
    "personkm": "person kilometer",
    "person*km": "person kilometer",
    "pkm": "person kilometer",
    "tkm": "ton kilometer",
    "vkm": "vehicle kilometer",
    'kg sw': "kilogram separative work unit",
    'km*year': "kilometer-year",
    'metric ton*km': "ton kilometer",
    'person*km': "person kilometer",
    'Wh': 'watt hour',
}