# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 15:36:43 2019

@author: cyshi
"""
from .setup import Database
from copy import deepcopy
import warnings
from bw2data.backends.single_file import Activity
import hashlib
from collections import OrderedDict

class ActivityBuilder(Activity):
    """Creat a object that searches, modifies, and get exchanges for activity/unit process from a imported life cycle inventory database.
    This allows uders to select inventory flow from imported database to assemly product stages. Note that SimaPro 
    differentiates between materials and processes inputs, in this module, they will all be "flows".
        
    **Args**
        * *database_name* (``str``): Name of the inventory database that the activity flow is from
        * *flow_name* (``str``): Name of the searching string for unit process, such as 'electricity', 'steel
        * *limits* (``int``): Number of the matching activities to show
        
    ** Returns **  
        * One or a list of activity object that matches the searching criteria. 
        
    Glossary of LCA terminology including activities, exchanges, technopshere flow, etc., can be found via eco-invent website https://www.ecoinvent.org/support/glossary/glossary.html        

    **References**
        [1] Wernet, G., Bauer, C., Steubing, B., Reinhard, J., Moreno-Ruiz, E., and Weidema, B., 2016. The ecoinvent database version 3 (part I): overview and methodology. The International Journal of Life Cycle Assessment, [online] 21(9), pp.1218–1230.
        
        [2] ISO 14044. ISO 14044: Environmental management--Life cycle assessment--Requirements and guidelines. International Organization for Standardization; Switzerland: 2006. 

        [3] Edelen, A., Ingwersen, W. W., Rodríguez, C., Alvarenga, R. A., de Almeida, A. R., & Wernet, G. (2018). Critical review of elementary flows in LCA data. The international journal of life cycle assessment, 23(6), 1261-1273.  
    """
    weights = {"name": 5,
               "comment": 1,
               "product": 4,
               "categories": 2,
               "location": 4,
               "code": 4,
               } 
    
    def __init__(self, flow_name, database_name = 'ecoinvent', limits=None):
        self.database_name = database_name
        self.db = Database(self.database_name)
        self.flow_name = flow_name
        self.limits = limits
        if not Database(self.database_name):
            raise ValueError ('Database {} is empty! Please select a valid database before building up life cycle inventory'.format(self.database_name)) 
#       self.flows_dict= [x for x in Database(self.database_name) if x['name'] ==  self.flow_name] #use the line below to update searching crateria including locations, outputs, etc. than just the names
        self.search = self.db.search(flow_name, limit=limits, boosts = self.weights)
        #database = {'items': OrderedDict(), 'name': '{}_Database'.format(self.name)}
        if not self.search:
            raise ValueError("No activity flows, please refine searching criteria")

        self.flow = self.search[0] #covert list to Activity object
        
    @property 
    def activity_type(self):
        """Returns the activity type, such as "market activity', 'transforming activity', 'treatment activities',
        'import and export activities, 'production', and 'supply mixes', etc.
        
        An activity dataset represents a unit process of a human activity and its exchanges with the environment and with other human activities.
        
        ***References***
        Ecoinvent glossary, acessed Apr 2020, https://www.ecoinvent.org/support/glossary/glossary-detail.html
        """
        return self.flow.get('activity type',[])    
    @property 
    def parameters(self):
        """Returns the parameters of the unit process.
        
        Parameter represents different types of values used in a dataset and defined by the data provider. 
        The new ecoSpold2 data format allows the use of formulas to calculate the amounts of flows 
        and other entities in the datasets. For example the yield of chemical reaction can be inserted 
        in the dataset as a parameter."""
        return self.flow.get('parameters',[]) 
    @property            
    def comment(self):
        """Review the comments provided for the inventory flow"""
        return self.flow.get('comment',[]) 
    @property 
    def astype(self):
        """Get the input type , such as 'process'"""
        return self.flow.get('type',[])
    @property 
    def location(self):
        """Returns the location of the inventory flow"""
        return self.flow.get('location',[])    
    @property 
    def unit(self):
        """Returns the unit of the inventory flow"""
        return self.flow.get('unit',[])  
    @property 
    def reference_product(self):
        """See the reference product used for creating this inventory flow"""
        return self.flow.get('reference product',[])  
    @property 
    def production_amount(self):
        """Returns the production amount of the unit process"""
        return self.flow.get('production amount',[])      
    @property 
    def classification(self):
        """Returns the classification of the unit process"""
        return self.flow.get('classifications',[])         
    @property
    def num_exchanges(self):
        """Get the number of exchanges for the activity"""
        num = len (self.flow.exchanges())
        return (self.flow, 'Total number of exchanges: {}'.format(num))  
    @property
    def get_exchanges(self):
        """
        Access exchange data, returns as a dict. Two basic types of exchanges exist:
            Elementary exchange: Exchange with the natural, social or economic environment. Examples: Unprocessed inputs from nature, emissions to air, water and soil, physical impacts, working hours under specified conditions.
            Intermedia exchange:An exchange between two activities that stays within the technosphere and is not emitted to or taken from the environment.
        """
        assert len (self.search) == 1, "please select only one unit process"""
#        act = self.search[0]
        data=self.db.load()
        exchgs = data[self.flow].get("exchanges", []) 
        objs = []
        for exc in exchgs:
            #if exc['type'] == type:
            ds = Database(exc.get('input', None)[0]).load()[exc.get('input', None)]
            objs.append({
                'name': ds.get('name', ''),
                'product': ds.get('reference product', ''),  
                'location': ds.get('location', 'unknown'),
                'amount': exc['amount'],
                'unit': ds.get('unit', 'unknown'),
                'database': exc.get('input', 'unknown')[0],
                'key': exc.get('input', 'unknown'),
                'key_type': 'activity',
            })
        objs.sort(key=lambda x: x['name'])
        return objs
           
    def edit_flow (self):
        """Edit inputs by firstly making a copy of the original inputs."""
        self.edit_input_flow_key = self.flow
        self.edit_input_flow_values = deepcopy(Database(self.flow[0]).load()[self.flow])
    
    
    def add_exchange(self,edit_flow):
        """ 
        A method to add additiona exchanges to selected activity flow. This function 
        enables featured similar to inventory- processes-input/output in the Simapro.
        """
        self.edit_activity = (self.data()[self.edit_flow]) 
        #only edit one activity flow each time
        ds = self.edit_activity
        exchgs = {
            'input': self.flow,
            'name': ds.get('reference product', '') or ds.get('name', ''),
            'amount': 1.0,
            'unit': ds.get('unit', ''),
            'type': "biosphere" if self.flow in Database('biosphere').load().keys()
                                or self.flow in Database('biosphere3').load().keys()
                                else "technosphere",
        }
        warnings.warn ("\nAdding Exchange: " + str(exchgs))
        self.edit_input_flow_values['exchanges'].append(exchgs)

    def delete_exchange(self):
        """A method to delete exchange of activity"""
        for exchgs in self.edit_input_flow_values['exchanges']:
            if exchgs['input'] == self.flow:
                self.edit_input_flow_values['exchanges'].remove(exchgs)

    
    def __repr__(self):
        return self.__class__.__name__
    
    def __str__(self):
        return "{}".format(self.database_name, self.flow_name)
    
    #def unnormalise_unit(unit):
    #    if unit in UNITS_NORMALIZATION.keys():
    #        return unit
    #    else: 
    #        un_units = list(filter(lambda x: UNITS_NORMALIZATION[x] == unit, UNITS_NORMALIZATION))
    #        #print (un_units)
    #        return un_units[0]  

# exact match
# water=[act for act in db if 'water' in act['name']]

if __name__ == "__main__":
    ActivityBuilder()