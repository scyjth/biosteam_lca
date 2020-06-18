85# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:31:45 2019

@author: cyshi
"""

#from biosteam.biorefineries.sugarcane import system
from system import sugarcane_sys, BT, enzyme, H3PO4, lime, polymer, \
    ethanol, yeast, sugar_cane, R301, C202, makeup_water
from biosteam.evaluation.evaluation_tools import triang
from biosteam_lca.inventory_constructor import InventoryConstructor
from biosteam_lca.multilca import MultiLCA
from biosteam.evaluation import Model, Metric

ethanol_density_kgL = 0.789 # kg/L
liter_per_gallon = 3.78541
ethanol_cost = 2.15 # USD/gal
ethanol_density_kggal = liter_per_gallon * ethanol_density_kgL # kg/gal


# Raw material price (USD/kg)
INC = InventoryConstructor()

#system=sugarcane_sys
get_ethanol_production = ethanol.F_mass
get_steam_demand = BT.steam_demand.F_mass
pws = [i.power_utility for i in sugarcane_sys.units
       if i.power_utility and i is not BT]
get_excess_electricity = (-BT.power_utility.rate - sum([i.rate for i in pws]))/1e3
get_acid_input = float(H3PO4.imass['H3PO4'])
get_lime_input = lime.F_mass #sanme as lime.imass['Substance']
get_yeast_input = float(yeast.imass['DryYeast'])
get_polymer_input = float(polymer.imass['Flocculant'])
get_makeup_water = float(makeup_water.imass['Water'])

#def heatutilprop_getter(system, ID, attr, name=None):
#    heatutils = sum([i._heat_utilities for i in system._costunits if i._heat_utilities], [])
#    heatutils = [i for i in heatutils if i.ID==ID]
#    def get_heatutilprop(): return sum([getattr(i, attr) for i in heatutils])
#    return get_heatutilprop

def cooling_duty_biorefinery():
    heat_utilities = sum([i.heat_utilities for i in sugarcane_sys.units if i._N_heat_utilities], ())
    cooling_utilities = [i for i in heat_utilities if i.duty < 0]
    return sum([i.duty for i in cooling_utilities])  

biomass_IDs = ('Glucose',
 'Lignin',
 'Solids',
 'Ash',
 'Sucrose',
 'Cellulose',
 'Hemicellulose',
 'Water')

total_biomass = sugar_cane.imass[biomass_IDs].sum()
get_combusted_mass = (sum([i.imass[biomass_IDs].sum() for i in BT.ins[0:1]]))
get_combusted_biomass_ratio = (sum([i.imass[biomass_IDs].sum() for i in BT.ins[0:1]]))/total_biomass

#biomass combustion emission from GREET Model
boiler_combustion_emission= {
    'sugarcane bagesse': 1.724474126, #kg/kg
    'cornstover':1.75E+00,
    'miscanthus':1.78E+00,
    'switchgrass':1.74E+00,
    'forage sorgum':1.56E+00}


inventory_inputs = {INC.electricity:get_excess_electricity,
                    INC.fresh_water: get_makeup_water,
                    INC.lime:get_lime_input,
                    INC.yeast:get_yeast_input,
                    INC.sulfuric_acid:get_acid_input}

class SugarcaneLCA(MultiLCA):
    
    
    # def __init__(self):
    #     super().__init__()
    
    # @property
    def system_impact(self):
        self._system_impact= super().scores()
        impact_value= [sum(self._system_impact[i]) for i in self._system_impact.keys()]
        self.impact_sum=dict(zip(self._system_impact.keys(),impact_value))
        return self.impact_sum


    def impact_fn(self):
        """impact by functional unit"""
        total=self.system_impact()
        ethanol_kg=int(ethanol.F_mass)
        for key in total:    
            total[key] *=  (1/ethanol_kg)
        # total=total.update((x, y/ethanol_kg) for x, y in total.items())
        return total
#def sys_utility(sys_name):
#    get_cooling_prop = heatutilprop_getter(find(sys_name), "Cooling water", "duty")
#    get_chilled_prop = heatutilprop_getter(find(sys_name), "Chilled water", "duty")
#    get_heating_prop = heatutilprop_getter(find(sys_name), "Low pressure steam", "duty")
#    get_power_prop = heatutilprop_getter(find(sys_name), "Consumed electricity", "duty")
#    get_excess_electricity = heatutilprop_getter(find(sys_name), "excess_electricity", "duty")
#    
#    cooling=get_cooling_prop()
#    chilled=get_chilled_prop()
#    #convert unit to be aligh ith unit of inventory inputs
#    total_cooling = (cooling +chilled)*ureg.kJ
#    total_heating = (get_heating_prop())*ureg.kJ
#    total_power = get_power_prop()*ureg.kWh
#    excess_power = get_excess_electricity()
#    return total_cooling, total_heating, total_power, excess_power
#
#def energy_lci(sys_name): 
#    inventory={}
#    cooling_p = INC().hx_cooling
#    heating_p = INC().hx_heating()
#    power_p = INC().electricity()
#    utilities = sys_utility(sys_name)
#    inventory[cooling_p] = abs((utilities[0]).to(cooling_p['unit'])).m 
#    inventory[heating_p] = abs((utilities[1]).to(heating_p['unit'])).m
#    inventory[power_p] =abs((utilities[2]).to(power_p['unit'])).m
##        #inventory = {electricity(): power_demand, hx_cooling(): abs((Cooling['demand'])), hx_heating(): abs((Heating.get('demand',"0")))}
#    return inventory

## thermo should include all possible chemicals
#all_feeds = Stream(thermo=None)
#for feed in sugarcane_sys.feeds:
#    if 'water' in str(feed):
#        pass
#    else:
#        IDs = feed.chemicals.IDs
#        all_feeds.imass[IDs] = feed.mass
#        print (feed, IDs)
#        