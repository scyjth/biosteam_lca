# -*- coding: utf-8 -*-
"""
Created on Thu Mar 7 16:12:21 2019

@author: cyshi
"""
from biosteam import HeatUtility
from biosteam_lca.regd import ureg
from biosteam_lca.multilca import MultiLCA
#from decimal import Decimal
from biosteam_lca.inventory_constructor import InventoryConstructor 
import pandas as pd
#INC = InventoryConstructor()

def demand_per_hr(heat_utilities, power_utility):
    """Return a dictionary of power utilities and heat utilities for each unit process."""
    util_demand = {}
    power = 0
    if heat_utilities:
        for index,util in enumerate (heat_utilities):
            if util.duty < 0 :
                cooling_utilities = [i for i in heat_utilities]
                cooling_demand = sum([i.duty for i in cooling_utilities])*ureg.kJ
                #Cooling['unit'] = 'kJ/hr'
                util_demand['Cooling_energy']=cooling_demand
            elif util.duty > 0:
                heating_demand = util.duty*ureg.kJ
                util_demand['Heating_energy']=heating_demand 
            #Cooling['unit'] = 'kJ/hr'
#            cooling_demand= sum([util.duty for util in util.heat_utilities if util.duty<0])*ureg.kJ
#            util_demand['Cooling_energy']=cooling_demand
#            heating_demand= sum([util.duty for util in util.heat_utilities if util.duty>0])*ureg.kJ
#            util_demand['Heating_energy']=heating_demand
    if power_utility:
        power+= power_utility.rate
        power_demand = power*ureg.kWh
        util_demand['Power']=power_demand
    return util_demand
    #Power['unit']= 'kWh/h'

def amount(heat_utilities, power_utility):
    demand=demand_per_hr(heat_utilities, power_utility)
    cooling= demand.get('Cooling_energy',0*ureg.kJ) #get cooling energy, if for units have no cooling, return 0
    heating = demand.get('Heating_energy',0*ureg.kJ)
    power = demand.get('Power',0*ureg.kWh)
    return cooling, heating, power

def _unit_lci_as_dict(heat_utilities, power_utility):
    INC=InventoryConstructor()
    inventory = {}  
    [cooling_p, heating_p, power_p] = [INC.hx_cooling, INC.hx_heating, INC.electricity]
    cooling, heating, power = amount(heat_utilities, power_utility)
    inventory[cooling_p] = abs((cooling).to(cooling_p['unit'])).m  #m: Convert to a floating point number
    inventory[heating_p] = abs((heating).to(heating_p['unit'])).m
    inventory[power_p] = abs((power).to(power_p['unit'])).m
    return inventory

def unit_lci (heat_utilities, power_utility):   
    INC=InventoryConstructor()
    inventory = {}
    activity_lst=[cooling_p, heating_p, power_p] = [INC.hx_cooling, INC.hx_heating, INC.electricity]
    cooling, heating, power = amount(heat_utilities, power_utility)
    activity_str = list(map(lambda x: (x.get('name') + ' (' 
                                       + x.get('unit') +', ' 
                                       + x.get('location') + ') '), activity_lst))
    [cooling_str, heating_str, power_str] = activity_str
    inventory[cooling_str] = abs((cooling).to(cooling_p['unit'])).m  #m: Convert to a floating point number
    inventory[heating_str] = abs((heating).to(heating_p['unit'])).m
    inventory[power_str] = abs((power).to(power_p['unit'])).m
    df = pd.DataFrame(inventory.items())   
#        df.style.set_properties(**{'text-align': 'right'})
    pd.options.display.max_colwidth = 100
    return df

ia_methods =[
        ('TRACI', 'environmental impact', 'acidification'),
        ('TRACI', 'environmental impact', 'ecotoxicity'),
        ('TRACI', 'environmental impact', 'eutrophication'),
        ('TRACI', 'environmental impact', 'global warming'),
        ('TRACI', 'environmental impact', 'ozone depletion'),
        ('TRACI', 'environmental impact', 'photochemical oxidation'),
        ('TRACI', 'human health', 'carcinogenics'),
        ('TRACI', 'human health', 'non-carcinogenics'),
        ('TRACI', 'human health', 'respiratory effects, average')
        ]
    
def unit_lca(heat_utilities, 
             power_utility, method=ia_methods):
 #            method=[('TRACI', 'environmental impact', 'global warming')]):
    inventory = _unit_lci_as_dict(heat_utilities, power_utility)
    MultiLCA(inventory).set_ia_methods (method)
    results = MultiLCA(inventory).scores()
    unclassified= [sum(results[i]) for i in results.keys()]
    unclassified_sum=dict(zip(results.keys(),unclassified))
    return unclassified_sum

#class EnergyInventory:
#
##    Parameters
##    ----------
##    ID='' : str, defaults to a unique ID
##        A unique identification. If ID is None, unit will not be
##        registered in flowsheet.
#    
#    def __init__(self, heat_utilities, power_utility ):
#        self.heat_utilities = heat_utilities
#        self.power_utility = power_utility
#
#    def demand_per_hr(self):
#        """Return a dictionary of power utilities and heat utilities for each unit process."""
#        util_demand = {}
#        power = 0
#        if self.heat_utilities:
#            for index,util in enumerate (self.heat_utilities):
##                demand = util.duty
##                hx_demand.append(demand)
##                ut_demand = {'Hx':hx_demand, 'Power':power_demand}
##                return ut_demand###
#                if util.duty < 0 :
#                    cooling_utilities = [i for i in self.heat_utilities]
#                    cooling_demand = sum([i.duty for i in cooling_utilities])*ureg.kJ
#                    #Cooling['unit'] = 'kJ/hr'
#                    util_demand['Cooling_energy']=cooling_demand
#                elif util.ID in HeatUtility.heating_agents.keys():
#                    heating_demand = util.duty*ureg.kJ
#                    util_demand['Heating_energy']=heating_demand
#                    #Cooling['unit'] = 'kJ/hr'      
#        if self.power_utility:
#            power+= self.power_utility.rate
#            power_demand = power*ureg.kWh
#            util_demand['Power']=power_demand
#        return util_demand
#        #Power['unit']= 'kWh/h'
#
#    def amount(self):
#        demand=self.demand_per_hr()
#        cooling= demand.get('Cooling_energy',0*ureg.kJ) #get cooling energy, if for units have no cooling, return 0
#        heating = demand.get('Heating_energy',0*ureg.kJ)
#        power = demand.get('Power',0*ureg.kWh)
#        return cooling, heating, power
#
#    def unit_lci(self):
#        inventory = {}  
#        activity_lst=[cooling_p, heating_p, power_p] = [INC.hx_cooling, INC.hx_heating, INC.electricity]
#        cooling, heating, power = self.amount()
#        activity_str = list(map(lambda x: (x.get('name') + ' (' 
#                                           + x.get('unit') +', ' 
#                                           + x.get('location') + ') '), activity_lst))
#        [cooling_str, heating_str, power_str] = activity_str
#        inventory[cooling_str] = abs((cooling).to(cooling_p['unit'])).m  #m: Convert to a floating point number
#        inventory[heating_str] = abs((heating).to(heating_p['unit'])).m
#        inventory[power_str] = abs((power).to(power_p['unit'])).m
#        df = pd.DataFrame(inventory.items())   
##        df.style.set_properties(**{'text-align': 'right'})
#        pd.options.display.max_colwidth = 100
#        return df
#
#    def unit_lca(self):
#        inventory =  self.unit_lci()
#        MultiLCA(inventory).set_ia_methods ([('TRACI', 'environmental impact', 'global warming')])
#        results = MultiLCA(inventory).run()
#        return results
##baseGHG is now removed from biorefinery unit simulation.
##def unit_EF(heat_utilities,power_utility):
##
##    cooling, heating, power = num_only(heat_utilities,power_utility)
###    GHG['Process emission'] = GHG_process_emission = {}
##    GHG_process_emission = {}
##    #convert unit of utility demand to match the unit of EF factors being imported
###    if not cooling ==0:
##    cooling_cvt= abs((cooling).to(flow.hx_cooling_e()['unit'])).m
###    else:
###        cooling_cvt=cooling
###    if not heating ==0:
##    heating_cvt= abs((heating).to(flow.natural_gas_e()['unit'])).m 
###    else:
###        heating_cvt = heating
##    if heating or cooling:
##        GHG_process_emission ['Thermal']= (cooling_cvt*  flow.hx_cooling_e()['emission(g CO2eq)']+heating_cvt*(flow.natural_gas_e()['emission(g CO2eq)'])*1.25)
##        #applied 1.25 to the emission factor of NG, accoridng to GREET Model, 1.25mmBTU produces 1mmBTU steam. See sheet Hydrogen. 
##    if power:
##        power_cvt= (power.to(flow.electricity_e()['unit'])).m 
##        GHG_process_emission['Power']= (power_cvt* flow.electricity_e()['emission(g CO2eq)']) 
##    return GHG_process_emission
###    self._GHGs =GHG
###    self._totalGHG = [sum(GHG_construction_emission.values()), sum(GHG_process_emission.values())]
