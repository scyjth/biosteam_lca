# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 14:23:21 2019

@author: cyshi
"""
name = 'biosteam_lca'
#
#from setuptools import setup,find_packages
#setup(name='biosteam_lca',packages=find_packages(),)

#from units import *
__version__ = (0, 1)

try:
    from .setup import * # databases, methods, Database, SetUp
except ImportError:
    None
# from .method_finder import Method, Methods
from .activity_builder import ActivityBuilder
from .inventory_constructor import InventoryConstructor
from .monte_carlo import MultiMonteCarlo
from .multilca import MultiLCA
#        

__all__ = [
    'databases',
    'Database',
    'methods',
    'static_calc',
    'SetUp',
    'Method',
    'Methods'
    'importers',
    'Activity',
    'SetUp',
    'Importer',
    'strategies',
    'config',
    'UnicodeReader',
    'SerializedLCAReport',
    'peewee',
    'config'
    'InventoryConstructor', 
    'ActivityBuilder',
    'MultiMonteCarlo', 
    'MultiLCA'
    ]
  
### %% Import base utils
##import pandas as pd
##import numpy as np
##from pint import UnitRegistry
##import os
##
#
##from .allocation import *
#from .correlation import *
#from preset import *
##

#

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