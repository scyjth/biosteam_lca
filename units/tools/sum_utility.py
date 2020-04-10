# -*- coding: utf-8 -*-
"""
Created on Thu Mar 7 16:12:21 2019

@author: cyshi
"""
from construction_assumption import *
from biosteam import HeatUtility
from biosteam_lca.flow import *
from biosteam_lca.multilca import MultiLCA
import pint

class Utility:  
    """
    Summary of power utilities and heat utilities consumptions for each unit process.
    """
#    power_utility = self._power_utility
#    heat_utilities = self.heat_utilities
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
        return ut_demand
  
    def utility_lci (self,heat, power =None):
        EI=self.utility_demand()
        self.Power= EI['Power']
        self.HX = EI['Hx']
    
    def u_sum_per_hr(self):
        heat_utilities=self.heat_utilities
        power_utility=self.power_utility
        ureg = pint.UnitRegistry()
        Q_ = ureg.Quantity
    
        power_demand = 0
        if heat_utilities:
            Cooling= {}
            Heating={}
            for index,util in enumerate (heat_utilities):
                if util.ID in HeatUtility.cooling_agents.keys():
                    Cooling['demand'] = util.duty*ureg.kJ
                    #Cooling['unit'] = 'kJ/hr'
                elif util.ID in HeatUtility.heating_agents.keys():
                    Heating['demand'] = util.duty*ureg.kJ
                    #Cooling['unit'] = 'kJ/hr'      
        if power_utility:
            Power ={}
            power_demand += power_utility.rate
            Power['demand'] = power_demand*ureg.kWh
            #Power['unit']= 'kWh/h'
    
    #    return Cooling, Heating, Power
    #
    #def u_lci()
        inventory = {}       
        cl_p = hx_cooling()
        ht_p = hx_heating()
        power_p = electricity()
        if Cooling:
            inventory[cl_p] = abs((Cooling['demand']).to(cl_p['unit'])).m  
        if Heating:
            inventory[ht_p] = abs((Heating.get('demand',"doesn't exsit")).to(ht_p['unit'])).m
        if Power:
            inventory[power_p] = abs((Power.get('demand',"doesn't exsit")).to(power_p['unit'])).m
        #inventory = {electricity(): power_demand, hx_cooling(): abs((Cooling['demand'])), hx_heating(): abs((Heating.get('demand',"0")))}
    #    return inventory
        multi_lca = MultiLCA(inventory).multi_calc()
        return multi_lca 

#def u_sum_per_hr(heat_utilities, _power_utility ):
#    ureg = pint.UnitRegistry()
#    Q_ = ureg.Quantity
#
#    power_demand = 0
#    if heat_utilities:
#        Cooling= {}
#        Heating={}
#        for index,util in enumerate (heat_utilities):
#            if util.ID in HeatUtility.cooling_agents.keys():
#                Cooling['demand'] = util.duty*ureg.kJ
#                #Cooling['unit'] = 'kJ/hr'
#            elif util.ID in HeatUtility.heating_agents.keys():
#                Heating['demand'] = util.duty*ureg.kJ
#                #Cooling['unit'] = 'kJ/hr'      
#    if _power_utility:
#        Power ={}
#        power_demand += _power_utility.rate
#        Power['demand'] = power_demand*ureg.kWh
#
#        #Power['unit']= 'kWh/h'
#
##    return Cooling, Heating, Power
##
##def u_lci()
#    inventory = {}       
#    cl_p = hx_cooling()
#    ht_p = hx_heating()
#    power_p = electricity()
#    if Cooling:
#        inventory[cl_p] = abs((Cooling['demand']).to(cl_p['unit'])).m  
#    if Heating:
#        inventory[ht_p] = abs((Heating.get('demand',"doesn't exsit")).to(ht_p['unit'])).m
#    if Power:
#        inventory[power_p] = abs((Power.get('demand',"doesn't exsit")).to(power_p['unit'])).m
#    #inventory = {electricity(): power_demand, hx_cooling(): abs((Cooling['demand'])), hx_heating(): abs((Heating.get('demand',"0")))}
##    return inventory
#    multi_lca = MultiLCA(inventory).multi_calc()
#    return multi_lca 
##    
#    
    
#class UtilityEmission(SumUtility):
#    """
#    A method that calculates the GHG emisssion using default emission factors in the builtin inventory.
#    * 'Construction': (g CO2eq)
#    * 'Process': (g CO2eq)
#    """
#    def utility_emission(self):
#        GHG={}
#        results = self.results
#        self.results['Energy inputs'] =SumUtility.utility_demand
#        Design = results['Design']
#        N = Design['Number of reactors']
#        W = Design['Weight of reactor (lb)']
#        Power= self.results['Energy inputs']['Power']
#        HX = self.results['Energy inputs']['Hx']
#        #emission factor
#        EF_steel =  EF.steel['emission']
#        EF_power = EF.electricity['emission']
#        EF_thermal_cooling = EF.hx_cooling['emission']
#        EF_thermal_heating = EF.natural_gas['emission']
#        #Calculate GHG
#        GHG['Construction emission (g CO2eq)'] = '%.2e' %(W *N * EF_Steel *0.0005/self.total_hr) #convert W(lb) to ton
#        GHG['Process emission (g CO2eq)'] ={}
#        GHG['Process emission (g CO2eq)']['power']= '%.2e' %(Power* EF_power)
#        GHG['Process emission (g CO2eq)'] ['thermal']= '%.2e' %((abs(HX [0])* EF_EF_thermal_cooling)+(abs(HX [1])* EF_EF_thermal_heating))
#        self.results['GHG'] =GHG