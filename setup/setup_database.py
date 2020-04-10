# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 15:36:43 2019

@author: cyshi
"""

import stats_arrays
import collections
from eight import *
import pandas as pd
import os
import win32com.client as win32
from . import strategies, peewee, Database, databases
import xlsxwriter
from .importer import Importer
try:
   import cPickle as pickle
except:
   import pickle    
        
#%%
class SetUpDatabase(Database):
    """Setting up lci databases. Inventory data can be exported to excel. This class includes all functions for lci database manipulation
    **initialization parameter**
        
            ** database_name:** [str] Name of the lci databases or datasets 
    """
    
    download_path=None
    store_download=True
    c_path=os.path.abspath(os.path.dirname(__file__))
    
    
    def __init__(self, database_name):
        """database_names are string"""
        assert type (database_name) == str, "Invalid database name"
        self.database_name = database_name 
        stored = [x.lower() for x in databases.list] #turn databases dictionary to list
        #the stored database name might be different from input database name, it could contain version, system, etc. Forexample, the stored name might be "Ecoinvent cutoff35".
        if any(self.database_name in s for s in stored):
            name= "{}".format([s for s in stored if self.database_name in s])
            if not len(Database(name))==0:   
                self.db = Database(name)
            else:
                #if database exists as object to Database dictionary, but it's empty. Then delete the database.
                print ("{} database is empty, please reinstall".format([s for s in stored if self.database_name in s]))
                Database(self.database_name).delete()
             
        elif 'forwast' in self.database_name.lower():
            #download forwast database in the current file path
            Importer(self.c_path).forwast_db() 
        elif 'ecoinvent' in self.database_name.lower():
            #eoinvent 3.6 has unlinked exchanges! Use 3.5 for now. 
            Importer(self.c_path).ecoinvent_db()
        elif 'us_lci' in self.database_name.lower():
            Importer(self.c_path).uslci_db()
        elif 'user_customized_database'in self.database_name.lower():
            Importer(self.c_path).user_customized_db()
#           elif self.db_name.lower() == ('all'):
#               SetUp.all_db()  
        else:
            UserWarning ("Please choose a valid databasename")
                 
    def __repr__(self):
        return self.__class__.__name__
    
    def __str__(self):
        return ('Set Up Life Cycle Inventory Database{}'.format(self.database_name))
    
    def check_dir(dirpath):
        """Returns ``True`` if the input path is a directory and writeable."""
        return os.path.isdir(dirpath) and os.access(dirpath, os.W_OK)
     
    def stats (self):
        return statistics()
#        self.db= Database(self.database_name)
#        num_datasets = len(self.db)
#        num_exchanges = sum([len(ds.get('exchanges', [])) for ds in self.db.load()])
#        num_unlinked = len([1 for ds in self.db for exc in ds.get('exchanges', [])
#                            if not exc.get("input")])
#        if print_stats:
#            unique_unlinked = collections.defaultdict(set)
#            for ds in self.data:
#                for exc in (e for e in ds.get('exchanges', [])
#                            if not e.get('input')):
#                    unique_unlinked[exc.get('type')].add(activity_hash(exc))
#            unique_unlinked = sorted([(k, len(v)) for k, v
#                                      in list(unique_unlinked.items())])
#
#            print((u"{} datasets\n{} exchanges\n{} unlinked exchanges\n  " +
#                "\n  ".join([u"Type {}: {} unique unlinked exchanges".format(*o)
#                             for o in unique_unlinked])
#                ).format(num_datasets, num_exchanges, num_unlinked))
        #return num_datasets, num_exchanges, num_unlinked
   
    
    def delete(self):
        assert self.database_name in self.databases, "Database you tend to delete doesn't exist"
        del self.databases[self.database_name]
    
    def delete_activity_flow(self,inputs_flow):
        """Delete an flow from database"""
        self.db= Database(self.database_name)
        data = self.db.load()
        del data[inputs_flow]
        from bw2data.utils import recursive_str_to_unicode
        self.db.write(recursive_str_to_unicode(data))
        self.db.process()
        print ("deleted activity flow: %s" % (str(inputs_flow)))
     
    def size(self):
        self.db= Database(self.database_name)
        if not self.db:
            raise ImportError ('Database is empty!')
        else:
            print ('Total activities in {} database is {}'.format(self.database_name, len(self.db)))
            return len(self.db)

#def create_product (self, name, location='GLO', unit='kg', **kwargs): 
#    """Create a new activity database"""
#    new_product = item_factory(name=name, location=location, unit=unit, type='product', **kwargs)
#
#    if not self.exists_in_database(new_product['code']):
#        self.add_to_database(new_product)
#        #print ('{} added to database'.format(name))
#        return self.get_exchange(name)
#    else:
#        #print('{} already exists in this database'.format(name))
#        return False
            
    def uncertainty(self):
        if self.size:
            flow_type = lambda x: 'technosphere' if x != 'biosphere' else 'biosphere'
            uncert = []
            for exchgs in peewee.schema.ExchangeDataset.select().where(peewee.schema.ExchangeDataset.output_database == self.database_name):
                # obtain default uncertainty distribution for each exchanges in selected database 
                objs = exchgs.data.get('uncertainty type', 0)
                uncertainty_type = stats_arrays.uncertainty_choices[objs].description
                uncert.append((flow_type(exchgs.type), uncertainty_type))
                
            return collections.Counter(uncert).most_common()  
    
    def storeData(self):
         self.db_as_dict = Database(self.database_name).load()
         with open('MyExport.pickle', 'wb') as f:
             pickle.dump(self.db_as_dict, f)

    def _loadData(self):
        db_file = open('MyExport.pickle', 'rb')
        db = pickle.load(db_file)
        for keys in db:
            print (keys, '=>', db(keys))
        db_file.close()

##Examining database data
#num_exchanges = [(activity, len(activity.exchanges())) for activity in db]

#
#def clean_exchanges(data):
#    """Make sure all exchange inputs are tuples, not lists."""
#    def tupleize(value):
#        for exc in value.get('exchanges', []):
#            exc['input'] = tuple(exc['input'])
#        return value
#    return {key: tupleize(value) for key, value in data.items()}
   
## check if something already exists
#def exists_in_specific_database(code, database):
#    for key in database['items'].keys():
#        item = database['items'][key]
#        if item['code'] == code:
#            return True
#    return False
#exists_in_database = partial(exists_in_specific_database, database=self.database)

#    @staticmethod
    #def geto_locations():
    #    """Returns a list of ecoinvent location abbreviations"""
    #    fp = os.path.join(os.path.abspath(os.path.dirname(__file__)),'data', "geodata.json")
    #    return json.load(open(fp, encoding='utf-8'))['names']

#def export_excel():
def db_write_toExcel(lci_data, db_name):
    """Write inventory database to Excel file.
    
    Returns the filepath to the spreadsheet file.
    
    """
    #creat lci data sheet
    dirpath = os.path.join(os.path.abspath(os.path.dirname(__file__)),'database')
    export_path = os.path.join(dirpath,"Exported")      
    if not os.path.isdir(export_path):
            os.makedirs(export_path)
    fp = os.path.join(export_path, "Exported" +" " + db_name +" Inventory" + ".xlsx")
    Wb = xlsxwriter.Workbook(fp)
    bold = Wb.add_format({'bold': True})                   
    Ws = Wb.add_worksheet('inventory')
    row = 0
    
    def write_row(sheet, row, data, exchgs=True):
        sheet.write_string(row, 0, data.get('name', '(unknown)'), bold)
        #include both linked and unlinked exchanges
        if exchgs:
            sheet.write_string(row, 0, data.get('name', '(unknown)'))
            sheet.write_string(row, 1, data.get('reference product', '(unknown)'))
            try:
                sheet.write_number(row, 2, float(data.get('amount')))
            except ValueError:
                sheet.write_string(row, 2, 'Unknown')
        sheet.write_string(row, 3, data.get('input', [''])[0])
        sheet.write_string(row, 4, data.get('unit', '(unknown)'))
        sheet.write_string(row, 5, u":".join(data.get('categories', ['(unknown)'])))
        sheet.write_string(row, 6, data.get('location', '(unknown)'))
        if exchgs:
            sheet.write_string(row, 7, data.get('type', '(unknown)'))
            sheet.write_boolean(row, 8, 'input' in data)
    #writing lci data to excel
    for ds in lci_data:
        if not ds.get('exchanges'):
            continue
        write_row(Ws, row, ds, False)
        cols = ('Name','Reference Product','Amount','Database','Unit','Categories','Location','Type','Matched')
        for index, col in enumerate(cols):
            Ws.write_string(row+1, index, col, bold)
        row += 2
        for exchgs in sorted(ds.get('exchanges', []), key=lambda x: x.get('name')):
            write_row(Ws, row, exchgs)
            row += 1
        row += 1 
    Wb.close()
#    def get_col_widths(dataframe):
#        # maximum length of the index column   
#        idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
#        # concatenate this to the max of the lengths of column name and its values for each column, left to right
#        return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]
#
#    for i, width in enumerate(get_col_widths(dataframe)):
#        sheet.set_column(i, i, width)
    #Aut adjust coloum fit
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(fp)
    ws = wb.Worksheets("inventory")
    ws.Columns.AutoFit()
    wb.Save()
    excel.Application.Quit()
    print("Exported inventory database file to:\n{}".format(fp))
    return fp
    
SetUp = SetUpDatabase