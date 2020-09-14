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
# import win32com.client as win32
from . import peewee, Database, databases
import xlsxwriter
from .database_importer import Importer
try:
   import cPickle as pickle
except:
   import pickle    
        
#%%
class SetUpDatabase():
    """A means of setting up lci databases with brightway backend. Inventory data can 
    be exported to excel. This class enables importing, managing,
    and manipulating the databases and activities and exchanges in the database.
    
    Attributes
    ----------
        
    database_name : str 

        Name of the lci databases or datasets 

    db : obj

        An instance of the database to be set up. 
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
#            name= "{}".format(s for s in stored if self.database_name in s)
            if len(Database(self.database_name))==0:   
                #if database exists as object to Database dictionary, but it's empty. Then delete the database.
                print ("{} database is empty, please reinstall".format([s for s in stored if self.database_name in s]))
#                del databases[self.database_name]             
        elif 'forwast' in self.database_name.lower():
            #download forwast database in the current file path
            Importer(self.c_path).forwast_db() 
        elif 'ecoinvent' in self.database_name.lower():
            #eoinvent 3.6 has unlinked exchanges! Use 3.5 for now. 
            #do not chosse version 'c cut-off', it's an error from ecoinvent site. Use 'd cutoff' instead
            Importer(self.c_path).ecoinvent_db()
        elif 'us_lci' in self.database_name.lower():
            Importer(self.c_path).uslci_db()
        elif 'user_customized_database'in self.database_name.lower():
            Importer(self.c_path).user_customized_db()
#           elif self.db_name.lower() == ('all'):
#               SetUp.all_db()  
        else:
            UserWarning ("Please choose a valid databasename")
        self.db = Database(self.database_name)
                 
    def __repr__(self):
        return ('Inventory database in Biosteam_LCA: {}'.format(self.database_name))
    
    def __str__(self):
        return self.__class__.__name__ 
    
    def check_dir(dirpath):
        """A method to check that path is a directory, and that the system has 
        write permissions.
        
        Parameters
        ----------

        dirpath : str

            The filepath to the directory in question. 

        Returns
        -------

        True : bool

            If the input path is a directory and writeable.

        False : bool

            If the input path is either not a directory or is not writeable
        """
        return os.path.isdir(dirpath) and os.access(dirpath, os.W_OK)


    def size(self):
        """A method to get the number of total activities in the imported database, 
        if the database is not empty

        Returns
        -------
        
        db_activities : str

            A count of the total activities in the db. 

        Raises
        ------

        ImportError

            If the db fails to load.

        """
        if not self.db:
            raise ImportError ('Database is empty!')
        else:
            db_activities = (('Total activities in {} database is {}'.format(self.database_name, len(self.db))), len(self.db))
            return db_activities
        
    def data(self):
        """A method to load the db."""
        return self.db.load()
    
    def activities(self):
        """A method for getting a list of all activities in a `self.db`. 

        Returns 
        -------
        db_activities_list : list

            A list of all activities in this database.

        Raises
        ------
        
        TypeError

            If dict keys being iterated over cannot be interpreted as an activity.

        """
        try:
            return [self.db.get(ds[1]) for ds in self.data()]
        except TypeError:
            raise Exception ("Key {} cannot be understood as an activity".format(ds[1]) for ds in self.db.load())
            
    def statistics (self):
        """A method to get the number of activities and exchanges in the database.

        Returns
        -------

        activities_and_num_of_exchanges : str

            A count of all datasets and exchanges in `self.db`. 

        """
#        num_exchanges = sum([len(ds.get('exchanges', [])) for ds in self.db.load()])
        data = self.data()
        num_exchanges = sum([len((self.db.get(ds[1])).exchanges()) for ds in data])
        num_datasets = len(self.db)
        activities_and_num_of_exchanges = ('Number of activities and exchanges:', num_datasets, num_exchanges)
        return activities_and_num_of_exchanges
    
    def delete(self):
        """A method to delete a previously installed database."""
        assert self.database_name in databases, "Database you tend to delete doesn't exist"
        del databases[self.database_name]
    
    def delete_activity (self,activity):
        """A method to delete a flow from database.
        
        Parameters
        ----------

        activity: str

            The flow to be deleted.
        """
        data = self.db.load()
        del data[activity]
        from bw2data.utils import recursive_str_to_unicode
        self.db.write(recursive_str_to_unicode(data))
        self.db.process()
        print ("deleted activity flow: %s" % (str(activity)))

#    def exchanges (self, activity):
#        """get exchanges for the activity"""
#        exchgs = self.data[activity].get('exchanges',[])
#        num = len (activity.exchanges())
#        return (exchgs, 'Total number of exchanges: {}'.format(num))  

    def all_exchanges (self):
        """A method to get all exchanges in `self.db`

        Returns
        -------
        exchanges_description : str

            A statement of the total number of exchanges in the db.
        """
        data = self.data()
        all_exchgs = [(data[ds].get('exchanges',[])) for ds in data]
        num = len (all_exchgs)
        exchanges_description = (all_exchgs, 'Total number of exchanges in the database {}:{}'.format(self.database_name, num))
        return   exchanges_description
            
    def uncertainty(self):
        """A method to get the most common uncertainty type for `self.db`.

        Returns
        -------

        most_common_uncertainty : str

            The most common uncertainty type in the db. 

        """
        if self.size:
            flow_type = lambda x: 'technosphere' if x != 'biosphere' else 'biosphere'
            uncert = []
            for exchgs in peewee.schema.ExchangeDataset.select().where(peewee.schema.ExchangeDataset.output_database == self.database_name):
                # obtain default uncertainty distribution for each exchanges in selected database 
                objs = exchgs.data.get('uncertainty type', 0)
                uncertainty_type = stats_arrays.uncertainty_choices[objs].description
                uncert.append((flow_type(exchgs.type), uncertainty_type))
                most_common_uncertainty = collections.Counter(uncert).most_common() 
            return most_common_uncertainty
    
    def storeData(self):
        """A method to write a binary representation of the db to a local file `MyExport.pickle`."""
         self.db_as_dict = self.db.load()
         with open('MyExport.pickle', 'wb') as f:
             pickle.dump(self.db_as_dict, f)

    def _loadData(self):
        db_file = open('MyExport.pickle', 'rb')
        db = pickle.load(db_file)
        for keys in db:
            print (keys, '=>', db(keys))
        db_file.close()

#    @staticmethod
    #def geto_locations():
    #    """Returns a list of ecoinvent location abbreviations"""
    #    fp = os.path.join(os.path.abspath(os.path.dirname(__file__)),'data', "geodata.json")
    #    return json.load(open(fp, encoding='utf-8'))['names']
#    def clean_exchanges(data):
#        """Make sure all exchange inputs are tuples, not lists."""
#        def tupleize(value):
#            for exc in value.get('exchanges', []):
#                exc['input'] = tuple(exc['input'])
#            return value
#        return {key: tupleize(value) for key, value in data.items()}
#        
    
#def export_excel():
def db_write_toExcel(lci_data, db_name):
    """A function to write inventory database to an Excel file. 

    Parameters
    ----------

    lci_data : 

    db_name : str

        The name of the database. 

    Returns
    ------- 

    fp : string

        The filepath to the spreadsheet file.
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
        """A nested function to write a database row to an Excel file.

        Parameters
        ----------

        sheet : file obj

            The Excel file to write to.

        row : int

            The row to write.


        data : dict

            The data to be written to the db.

        exchgs : boolean, optional

            Include exchanges. Default is `True`

        Raises
        ------

        ValueError

            If `amount` not specified in `data`.
        """
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
    # excel = win32.gencache.EnsureDispatch('Excel.Application')
    # wb = excel.Workbooks.Open(fp)
    # ws = wb.Worksheets("inventory")
    # ws.Columns.AutoFit()
    # wb.Save()
    # excel.Application.Quit()
    # print("Exported inventory database file to:\n{}".format(fp))
    return fp
    
SetUp = SetUpDatabase