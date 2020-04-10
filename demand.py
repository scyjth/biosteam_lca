# -*- coding: utf-8 -*-
"""
Created on Thu Mar 7 16:12:21 2019

@author: cyshi
"""
from biosteam_lca.construction_assumption import *
from biosteam import HeatUtility
from biosteam_lca import flow
from biosteam_lca.regd import ureg
from biosteam_lca.multilca import MultiLCA
#from decimal import Decimal

class SumUtility():  
    """
    Summary of power utilities and heat utilities consumptions for each unit process.
    """
#    def __init__(self):
#        self._power_utility = Unit._power_utility
#        self._heat_utilities= Unit._heat_utilities     
    def utility_demand(self):                
        hx_demand = []
        power_demand = 0
        if self._power_utility:
            power_demand += self._power_utility.rate
        
        if self._heat_utilities:
            for index, util in enumerate(self._heat_utilities):
                demand = util.duty
                hx_demand.append(demand)
        ut_demand = {'Hx':hx_demand, 'Power':power_demand}
        return ut_demand###
#getting "AttributeError: 'Fermentation' object has no attribute '_num_only'"


def utility_per_hr(heat_utilities,power_utility):
#    def utility_per_hr(self):
#    heat_utilities=self._heat_utilities
#    power_utility=self._power_utility
    util_demand = {}
    power = 0
    if heat_utilities:
        for index,util in enumerate (heat_utilities):
            if util.ID in HeatUtility.cooling_agents.keys():
                cooling_demand = util.duty*ureg.kJ
                #Cooling['unit'] = 'kJ/hr'
                util_demand['Cooling_energy']=cooling_demand
            elif util.ID in HeatUtility.heating_agents.keys():
                heating_demand = util.duty*ureg.kJ
                util_demand['Heating_energy']=heating_demand
                #Cooling['unit'] = 'kJ/hr'      
    if power_utility:
        power+= power_utility.rate
        power_demand = power*ureg.kWh
        util_demand['Power']=power_demand
    return util_demand
        #Power['unit']= 'kWh/h'
#        return self.Cooling, self.Heating, self.Power
def num_only(heat_utilities,power_utility):
    total=utility_per_hr(heat_utilities,power_utility)
    cooling= total.get('Cooling_energy',0*ureg.kJ) #get cooling energy, if for units have no cooling, return 0
    heating = total.get('Heating_energy',0*ureg.kJ)
    power = total.get('Power',0*ureg.kWh)
    return cooling, heating, power

def unit_EF(heat_utilities,power_utility):

    cooling, heating, power = num_only(heat_utilities,power_utility)
#    GHG['Process emission'] = GHG_process_emission = {}
    GHG_process_emission = {}
    #convert unit of utility demand to match the unit of EF factors being imported
#    if not cooling ==0:
    cooling_cvt= abs((cooling).to(flow.hx_cooling_e()['unit'])).m
#    else:
#        cooling_cvt=cooling
#    if not heating ==0:
    heating_cvt= abs((heating).to(flow.natural_gas_e()['unit'])).m 
#    else:
#        heating_cvt = heating
    if heating or cooling:
        GHG_process_emission ['Thermal']= (cooling_cvt*  flow.hx_cooling_e()['emission(g CO2eq)']+heating_cvt*(flow.natural_gas_e()['emission(g CO2eq)'])*1.25)
        #applied 1.25 to the emission factor of NG, accoridng to GREET Model, 1.25mmBTU produces 1mmBTU steam. See sheet Hydrogen. 
    if power:
        power_cvt= (power.to(flow.electricity_e()['unit'])).m 
        GHG_process_emission['Power']= (power_cvt* flow.electricity_e()['emission(g CO2eq)']) 
    return GHG_process_emission
#    self._GHGs =GHG
#    self._totalGHG = [sum(GHG_construction_emission.values()), sum(GHG_process_emission.values())]

def unit_lci(heat_utilities,power_utility):
    inventory = {}  
    cooling_p = flow.hx_cooling()
    heating_p = flow.hx_heating()
    power_p = flow.electricity()
    cooling, heating, power = num_only(heat_utilities,power_utility)
#    if cooling:
    inventory[cooling_p] = abs((cooling).to(cooling_p['unit'])).m  
#    if heating:
    inventory[heating_p] = abs((heating).to(heating_p['unit'])).m
#    if power:
    inventory[power_p] = abs((power).to(power_p['unit'])).m
#        #inventory = {electricity(): power_demand, hx_cooling(): abs((Cooling['demand'])), hx_heating(): abs((Heating.get('demand',"0")))}
    return inventory

def unit_lca(heat_utilities,power_utility):
    inventory =  unit_lci(heat_utilities,power_utility)
    multi_lca = MultiLCA(inventory).run()#lcia_methods =[('TRACI', 'environmental impact', 'global warming')])
