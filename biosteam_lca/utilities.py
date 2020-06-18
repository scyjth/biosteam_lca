85# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:31:45 2019

@author: cyshi
"""

#from biosteam.biorefineries.sugarcane import system
import system
from system import sugarcane_sys
from biosteam import find
from biosteam_lca.regd import ureg
from biosteam_lca import setting_flow

#system=sugarcane_sys

def heatutilprop_getter(system, ID, attr, name=None):
    heatutils = sum([i._heat_utilities for i in system._costunits if i._heat_utilities], [])
    heatutils = [i for i in heatutils if i.ID==ID]
    def get_heatutilprop(): return sum([getattr(i, attr) for i in heatutils])
    return get_heatutilprop

BT=system.BT
power_utils = ([i._power_utility for i in sugarcane_sys.units if (i._power_utility and i is not BT)])
excess_electricity = [0]
def get_consumed_electricity():
    electricity_generated = -BT._power_utility.rate
    consumed_electricity = sum([i.rate for i in power_utils])
    excess_electricity[0] = electricity_generated - consumed_electricity
    return consumed_electricity   

def sys_utility(sys_name):
    get_excess_electricity = lambda: excess_electricity[0]
    get_cooling_prop = heatutilprop_getter(find(sys_name), "Cooling water", "duty")
    get_chilled_prop = heatutilprop_getter(find(sys_name), "Chilled water", "duty")
    get_heating_prop = heatutilprop_getter(find(sys_name), "Low pressure steam", "duty")
    get_power_prop = heatutilprop_getter(find(sys_name), "Consumed electricity", "duty")
    get_excess_electricity = heatutilprop_getter(find(sys_name), "excess_electricity", "duty")
    
    cooling=get_cooling_prop()
    chilled=get_chilled_prop()
    #convert unit to be aligh ith unit of inventory inputs
    total_cooling = (cooling +chilled)*ureg.kJ
    total_heating = (get_heating_prop())*ureg.kJ
    total_power = get_power_prop()*ureg.kWh
    excess_power = get_excess_electricity()
#    return total_cooling, total_heating, total_power, excess_power

def lci(sys_name): 
    inventory={}
    cooling_p = setting_flow.hx_cooling()
    heating_p = setting_flow.hx_heating()
    power_p = setting_flow.electricity()
    inventory[cooling_p] = abs((total_cooling).to(cooling_p['unit'])).m 
    inventory[heating_p] = abs((total_heating).to(heating_p['unit'])).m
    inventory[power_p] =abs((total_power).to(power_p['unit'])).m
#        #inventory = {electricity(): power_demand, hx_cooling(): abs((Cooling['demand'])), hx_heating(): abs((Heating.get('demand',"0")))}
    return inventory
