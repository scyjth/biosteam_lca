# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 15:36:43 2019

@author: cyshi
"""

import pprint
import os
try:
    import pandas as pd
except ImportError:
    pd = None

dir_path = os.path.dirname(os.path.realpath(__file__)) #+ '\\'

class EmisssionFactorFinder:
    """
    Returns a inventory profile from customized database that includes emission factor. Selection criterias are specified as input name and location.
    """
    def __init__(self, filename, directory='.\\', sheetname=None):
        self.df = pd.read_excel(filename, sheetname=sheetname)    

    def find (self, name, location=None):
        df = self.df
        if location is None:
            i_profile = df[(df['Name'].str.contains(name, case=False))]
            if i_profile.shape[0] > 0:
                pass
            else: 
                raise ValueError("Refine Your Search: No Results Matching Your Search Were Found")             
        else:
            i_profile = df.loc[(df['Name'].str.contains(name, case=False )) & (df['Location'].str.contains(location, case=False))]
            
            if i_profile.shape[0] > 0:
                pass
            else: 
                raise ValueError("Refine Your Search: No Results Matching Your Search Combination of 'Name' and 'Location' ")
        return i_profile
    
    def value(self, key):
        "Vlues contains in the inventory database file."
        return self.df[key].tolist()
    
    def category(self):
        "Caegories of the seleced database file"
        return self.df.keys()
    
class BuiltInEmissionFactor(EmisssionFactorFinder):   
    """
    Returns to the emission factors for all material inputs and energy inputs that are required by the selected process or products.
    By default it uses the biosteam_lca customized emission factor database, data sources are all from public databases such as eGrid, US EIA, GREET Model, etc.
    Emission factors have been charactorized and will be used for baseLCA calculation.
    """
    
    def __init__(self, name, location=None):
        new_path = os.path.join(dir_path,'database')
        filename = os.path.join(new_path,'CABBI_Inventory_Database.xlsx')
        try:
            inventory = EmisssionFactorFinder(filename, sheetname='Sheet1')
        except Exception as e:
            print (e)
        self.profile = inventory.find (name, location)
        self.match_name = self.profile['Name'].tolist()
        self.match_location = self.profile['Location'].tolist()
        self.database = self.profile['Database'].tolist()
        self.emission = self.profile["Emission"].tolist()
        self.unit = self.profile["Unit"].tolist()
    
    def __repr__(self):
        return "Inventory matched:{}, Location:{}".format(self.match_name,self.match_location)
    
#    def overview(self):
#        "Show all inventory flows that matches the selecting criteria"
#        return self.profile
       
    def select(self):
        "A function to select inputs, selecting criteria based on the process, location, and datasource"
        mapped = zip(self.match_name,self.match_location,self.database,self.emission, self.unit)
        return set(mapped)

    def show(self):
        "Shows the emission factors, units, and datasources for selected inventory inputs."
        return {'emission(g CO2eq)': self.emission[0],'unit': self.unit[0],'datasource': self.database[0]}

    def __str__(self):
        return "{}".format(self.match_name)

BuitInEF=BuiltInEmissionFactor