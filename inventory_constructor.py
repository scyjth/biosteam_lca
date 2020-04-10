# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 15:36:43 2019

@author: cyshi
"""
from .database import SetUp
from .static import Database
from copy import deepcopy
import warnings
import hashlib
from collections import OrderedDict

class InventoryConstructor(object):
    """Creat a object that selects, modifies, and get exchanges for inventory inputs from a imported life cycle inventory database.
    This allows uders to select inventory flow from imported database to assemly product stages. Note that SimaPro 
    differentiates between materials and processes inputs, in this module, they will all be "flows".
        
    **Args**
        * *database_name* (``str``): Name of the inventory database that the activity flow is from
        * *flow_name* (``str``): Name of the searching string for inventory input, such as 'electricity', 'steel
        * *limits* (``int``): Number of the matching activities to show
        
    ** Returns **  
        * One or a list of activity object that matches the searching criteria. 
        
    Glossary of LCA terminology including activities, exchanges, technopshere flow, etc., can be found via eco-invent website https://www.ecoinvent.org/support/glossary/glossary.html        

    **References**
        [1] Wernet, G., Bauer, C., Steubing, B., Reinhard, J., Moreno-Ruiz, E., and Weidema, B., 2016. The ecoinvent database version 3 (part I): overview and methodology. The International Journal of Life Cycle Assessment, [online] 21(9), pp.1218–1230.
        
        [2] ISO 14044. ISO 14044: Environmental management--Life cycle assessment--Requirements and guidelines. International Organization for Standardization; Switzerland: 2006. 

        [3] Edelen, A., Ingwersen, W. W., Rodríguez, C., Alvarenga, R. A., de Almeida, A. R., & Wernet, G. (2018). Critical review of elementary flows in LCA data. The international journal of life cycle assessment, 23(6), 1261-1273.  
    """
    
    def set_weighting_criteria (self, weight = None):
       """ Returns a Dict of the weighting set of each searching field. By default, name and location were given the most weight"""
       new_weight = weight or {
               "name": 5,
               "comment": 1,
               "product": 3,
               "categories": 1,
               "location": 5,
               "code": 4,
               }
       return new_weight
   
    weight = set_weighting_criteria ()
    
    def __init__(self, flow_name, database_name = 'Ecoinvent cutoff35', limits=None):
        self.database_name = database_name
        self.flow_name = flow_name
        self.limits = limits
        if not Database(self.database_name):
            raise ValueError ('Database {} is empty! Please select a valid database before building up life cycle inventory'.format(self.database_name)) 
#       self.flows_dict= [x for x in Database(self.database_name) if x['name'] ==  self.flow_name]
        self.flows = Database(self.database_name).search(flow_name, limit=limits, boosts = self.weight)
        #database = {'items': OrderedDict(), 'name': '{}_Database'.format(self.name)}
        if not self.flows:
            raise ValueError("No activity flows, please refine searching criteria")

    def flows(self):
        return self.flows
   
    def edit_flow (self, flow):
        """
        Edit inputs by firstly making a copy of the original inputs. Orginal inputs flow is selected from of the imported databases. 
        """
        self.edit_input_flow_key = flow
        self.edit_input_flow_values = deepcopy(Database(flow[0]).load()[flow])
    
    def get_exchanges(self):
        """
        A method to acess exchange data. Exchanges were set up similar to ecoinvent's definition of exchanges. Two basic types of exchanges exist:
            Elementary exchange: Exchange with the natural, social or economic environment. Examples: Unprocessed inputs from nature, emissions to air, water and soil, physical impacts, working hours under specified conditions.
            Intermedia exchange:An exchange between two activities that stays within the technosphere and is not emitted to or taken from the environment.
        """
        exchgs = Database(self.database_name).load()[self.flow_name].get("exchanges", []) 
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

    def exhanges_num(self):
        """A method to get the number of exchanges for activity"""
        self.num_exchanges = [(self.flow_name, len((self.flow_name).exchanges()))]
        return self.num_exchanges
    
    def add_exchange(self):
        """ 
        A method to add additiona exchanges to selected activity flow. This function enables feature similar to Simapro -Inventory- processes-input/output
        """
        self.edit_activity = (Database(self.database_name).load()[self.flow_name]) 
        #only edit one activity flow each time
        ds = self.edit_activity
        exchgs = {
            'input': self.flow_name,
            'name': ds.get('reference product', '') or ds.get('name', ''),
            'amount': 1.0,
            'unit': ds.get('unit', ''),
            'type': "biosphere" if self.flow_name in Database('biosphere').load().keys()
                                or self.flow_name in Database('biosphere3').load().keys()
                                else "technosphere",
        }
        warnings.warn ("\nAdding Exchange: " + str(exchgs))
        self.edit_input_flow_values['exchanges'].append(exchgs)

    def delete_exchange(self):
        """A method to delete exchange of activity"""
        for exchgs in self.edit_input_flow_values['exchanges']:
            if exchgs['input'] == self.flow_name:
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

if __name__ == "__main__":
    InventoryConstructor()