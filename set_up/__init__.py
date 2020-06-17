# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 14:23:21 2019

@author: cyshi
"""

# initial set up of brightway2 model for static calculation basis. Doc: https://brightwaylca.org/
import brightway2 as bw2
methods = bw2.methods
Database = bw2.Database
from bw2io import strategies, config, importers, databases
from bw2analyzer import SerializedLCAReport
from bw2data.backends import peewee
if 'biosphere3' not in databases:
    try:
        bw2.bw2setup()
    except:
        pass

try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping
    
#def Database(name):
#    """
#    Returns a bw2 database class instance. Database types are specified in `databases[database_name]['backend']`.
#    Only SQLitebackend is supported the module currently .
#    """
#    if name in databases:
#        backend = databases[name].get("backend", "sqlite")
#        assert (backend == "sqlite"), "{} backend not supported in BioSTEAM.LCA".format(backend)
#        return peewee.SQLiteBackend(name)
#    else:
#        raise ValueError("Database {} not found".format(name)) 
        
#class Database():
#    """
#    Returns a database class instance. Database types are specified in `databases[database_name]['backend']`.
#    Only SQLitebackend is supported the module currently .
#    """
#    def __init__(self, name):
#        self.name=name
#        if self.name in databases:
#            name=self.name
#            backend = databases[name].get("backend", "sqlite")
#            assert (backend == "sqlite"), "{} backend not supported in BioSTEAM.LCA".format(backend)
#            peewee.SQLiteBackend(name)
#        else:
#            raise ValueError("Database {} not found".format(name))                
#    def __str__(self):
#        return "Database name %s: %s" % (self.__class__.__name__, self.name)   
    

def static_calc (flow, amount, methods, factorize=False):
    """Establish static lca basis. By default no factorization."""
    if not isinstance(flow, Mapping):
            raise ValueError("Flow must be a dictionary")
    for key in flow:
        if not key:
            raise ValueError("Invalid dictionary")
    lca = bw2.LCA({flow: amount}, method=methods) 
    lca.lci()
    if factorize:
        lca.decompose_technosphere()
    lca.lcia()                                   
    return lca.score


from .util import  get_activity  
from ._unicode import UnicodeReader
#from .database_setup import SetUp
from .importer import Importer

__all__ = [
    'databases',
    'Database',
    'methods',
    'static_calc',
    'importers',
    'get_activity',
    'Importer',
    'strategies',
    'config',
    'UnicodeReader',
    'SerializedLCAReport',
    'peewee',
    'config'
]

# edited to reinsert capitalisation of units
UNITS_NORMALIZATION = {
    "a": "year",
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
    'Wh': 'watt hour'}