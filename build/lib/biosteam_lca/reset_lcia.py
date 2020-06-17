# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 14:23:21 2019

@author: cyshi
"""
from __future__ import unicode_literals
from ._unicode import UnicodeReader
import xlrd
from numbers import Number
import os 
import warnings
from .import methods, strategies, config, importers, Database
import functools 
import sys
PY3 = sys.version_info > (3,)
if PY3:
    dt = ";"
else:
    dt = b";"

dirpath = os.path.dirname(__file__)


LCIAImporter = importers.base_lcia.LCIAImporter 

class SetLCIA(LCIAImporter):
    """Create and/or update lcia methods. A dictionary for method metadata. File data is saved in ``methods.json``.
    filename = "methods.json". See data_serialization
    lcia_methods in ecoinvent can be found at "http://www.ecoinvent.org/support/documents-and-files/information-on-ecoinvent-3/information-on-ecoinvent-3.html"
    """
    _metadata = methods

    def __init__(self):
        self.strategies = [strategies.normalize_units, strategies.set_biosphere_type, 
                           strategies.drop_unspecified_subcategories,
                           functools.partial(strategies.link_iterable_by_fields,
                                             other = Database(config.biosphere),
                                             fields = ('name', 'categories')),]
        self.applied_strategies = []
        self.csv_data, self.cf_data, self.units, self.file = self.lcia_methods__metadata()
        self.separate_methods()
        
    def lcia_methods__metadata(self):
        """convert impact assessment data. Raw data is saved in the "lcia_implemnetation_2019" file"""
        with UnicodeReader(os.path.join(dirpath, "categoryUUIDs.csv"), 
                           encoding='latin-1', 
                           delimiter=dt) as csv_file:
            next(csv_file) 
            csv_data = [{'name': (line[0], line[2], line[4]),
                'description': line[7]
            } for line in csv_file]
    
        filename = "LCIA_implementation_2019.xlsx" # this was donwloaded and updated on Oct 2019 from ecoinvent website. 
        wb = xlrd.open_workbook(os.path.join(dirpath, filename))
        #characterizaton factors
        sheet= wb.sheet_by_name("CFs")
        cf_data = [{
            'method': (sheet.cell(row, 0).value,
                       sheet.cell(row, 1).value,
                       sheet.cell(row, 2).value),
            'name': sheet.cell(row, 3).value,
            'categories': (sheet.cell(row, 4).value, sheet.cell(row, 5).value),
            'amount': sheet.cell(row, 7).value
            }
            for row in range(1, sheet.nrows)
            if sheet.cell(row, 0).value not in 
            {'selected LCI results, additional', 'selected LCI results'} and isinstance(sheet.cell(row, 7).value, Number)]
        #units
        sheet= wb.sheet_by_name("units")
        units = {(sheet.cell(row, 0).value, sheet.cell(row, 1).value, 
                  sheet.cell(row, 2).value): sheet.cell(row, 4).value for row in range(1, sheet.nrows)}
        return csv_data, cf_data, units, filename

    def separate_methods(self):
        """Separate the list of CFs into distinct methods"""
        methods = {obj['method'] for obj in self.cf_data}
        metadata = {obj['name']: obj for obj in self.csv_data}
        self.data = {}
        missing = set()
        for line in self.cf_data:
            if line['method'] not in self.units:
                missing.add(line['method'])

        if missing:
            _ = lambda x: sorted([str(y) for y in x])
            warnings.warn("Missing units for following:" +
                             " | ".join(_(missing)))

        for line in self.cf_data:
            assert isinstance(line['amount'], Number)

            if line['method'] not in self.data:
                self.data[line['method']] = {
                    'filename': self.file,
                    'unit': self.units.get(line['method'], ''),
                    'name': line['method'],
                    'description': '',
                    'exchanges': []}
            self.data[line['method']]['exchanges'].append({
                'name': line['name'],
                'categories': line['categories'],
                'amount': line['amount']})

        self.data = list(self.data.values())

        for obj in self.data:
            obj.update(metadata.get(obj['name'], {}))  
