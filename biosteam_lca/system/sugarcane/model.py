85# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:31:45 2019

@author: cyshi
"""

#from biosteam.biorefineries.sugarcane import system
from system import sugarcane_sys, BT, enzyme, H3PO4, lime, polymer, \
    ethanol, yeast, sugar_cane, R301, C202, makeup_water
from tea import sugarcane_tea
from biosteam.evaluation.evaluation_tools import triang
from biosteam_lca.inventory_constructor import InventoryConstructor as INC
from biosteam.evaluation import Model, Metric

ethanol_density_kgL = 0.789 # kg/L
liter_per_gallon = 3.78541
ethanol_cost = 2.15 # USD/gal
ethanol_density_kggal = liter_per_gallon * ethanol_density_kgL # kg/gal

#system=sugarcane_sys

get_MESP = lambda: sugarcane_tea.solve_price(ethanol) * ethanol_density_kggal

#get_coproduct_credit = lambda: sum([i._utility_cost_cached for i in sugarcane_tea.TEAs])
get_ethanol_production = lambda: ethanol.F_mass
get_steam_demand = lambda: BT.steam_demand.F_mass
pws = [i.power_utility for i in sugarcane_sys.units
       if i.power_utility and i is not BT]
get_excess_electricity = lambda: (-BT.power_utility.rate - sum([i.rate for i in pws]))/1e3

get_acid_innput = lambda: float(H3PO4.imass['H3PO4'])
get_lime_input = lambda: lime.F_mass #sanme as lime.imass['Substance']
get_yeast_input = lambda: float(yeast.imass['DryYeast'])
get_polymer_input = lambda: float(polymer.imass['Flocculant'])
get_makeup_water = lambda: float(makeup_water.imass['Water'])

#def heatutilprop_getter(system, ID, attr, name=None):
#    heatutils = sum([i._heat_utilities for i in system._costunits if i._heat_utilities], [])
#    heatutils = [i for i in heatutils if i.ID==ID]
#    def get_heatutilprop(): return sum([getattr(i, attr) for i in heatutils])
#    return get_heatutilprop

def cooling_duty_biorefinery():
    heat_utilities = sum([i.heat_utilities for i in sugarcane_sys.units if i._N_heat_utilities], ())
    cooling_utilities = [i for i in heat_utilities if i.duty < 0]
    return lambda: sum([i.duty for i in cooling_utilities])  

biomass_IDs = ('Glucose',
 'Lignin',
 'Solids',
 'Ash',
 'Sucrose',
 'Cellulose',
 'Hemicellulose',
 'Water')

total_biomass = sugar_cane.imass[biomass_IDs].sum()
get_combusted_mass = lambda: (sum([i.imass[biomass_IDs].sum() for i in BT.ins[0:1]]))
get_combusted_biomass_ratio = lambda: (sum([i.imass[biomass_IDs].sum() for i in BT.ins[0:1]]))/total_biomass

#metrics for LCA
metrics =[
#          Metric('Fixed capital investment', get_FCI, 'USD'),
          Metric('Minimum ethanol selling price', get_MESP, 'USD/gal'),
#          Metric('Co-product credit', get_coproduct_credit, 'USD/yr'),
          Metric('Ethanol production', get_ethanol_production, 'kg/hr'),
          Metric('Steam demand', get_steam_demand, 'kg/hr'),
          Metric('Excess electricity', get_excess_electricity, 'MW'),
          Metric('Cooling duty', cooling_duty_biorefinery(), 'KJ/hr'),
          Metric('H2SO4 input',get_acid_innput, 'kg/hr'),
          Metric('Lime_input',get_lime_input, 'kg/hr'),
          Metric('Polymer_input', get_polymer_input, 'kg/hr'),
          Metric('Yeast_input',get_yeast_input, 'kg/hr'),
          Metric('Makeup_water',get_makeup_water, 'kg/hr'),
          Metric('Biomass goes to combustion', get_combusted_mass, 'kg/hr'),
          Metric('Share of total biomass goes to combustion', get_combusted_biomass_ratio, '100&')
          ]

sugarcane_model = Model(sugarcane_sys, metrics)
sugarcane_model.load_default_parameters(sugar_cane, operating_days=False)
param = sugarcane_model.parameter


# Fermentation efficiency
fermentation = R301
baseline = fermentation.efficiency
@param(element=fermentation, distribution=triang(baseline),
       baseline=baseline,
       kind='coupled')
def set_fermentation_efficiency(efficiency):
    fermentation.efficiency= efficiency
    
# Boiler efficiency
baseline = BT.boiler_efficiency
@param(element=BT, distribution=triang(baseline),
       baseline=baseline)
def set_boiler_efficiency(boiler_efficiency):
    BT.boiler_efficiency = boiler_efficiency

# Turbogenerator efficiency
baseline = BT.turbogenerator_efficiency
@param(element=BT, distribution=triang(baseline),
       baseline=baseline)
def set_turbogenerator_efficiency(turbo_generator_efficiency):
    BT.turbo_generator_efficiency = turbo_generator_efficiency
    
# RVF separation
rvf = C202
baseline = rvf.isplit['Lignin']
@param(element=rvf, distribution=triang(baseline), baseline=baseline,
        kind='coupled')
def set_rvf_solids_retention(solids_retention):
    rvf.isplit['Lignin', 'CaO', 'Ash', 'Cellulose', 'Hemicellulose'] = solids_retention
    
    
#from biorefineries.cornstover.model import cornstover_model as model_cs
#
N_samples = 1000
rule = 'L'
samples = sugarcane_model.sample(N_samples, rule)
sugarcane_model.load_samples(samples)
sugarcane_model.evaluate()
sugarcane_model.table.to_excel('Monte Carlo sugarcane.xlsx')

#metrics = (model_cs.metrics[0],)
#spearman = model_cs.spearman(metrics)
#spearman.to_excel("Spearman correlation cornstover.xlsx")    

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