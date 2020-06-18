# -*- coding: utf-8 -*-
"""
Created on Sun May  3 00:12:20 2020

@author: cyshi
"""

from biosteam.units import Fermentation
from biosteam_lca.units.energy_inventory import demand_per_hr, unit_lci, unit_lca
from biosteam_lca.units.add_methods import add_method

@add_method(Fermentation)
def energy_inputs(self):
    """ summary of all power utilities and heat utilities for the unit process."""
    return ('Energy inputs per hour:{}'.format(demand_per_hr(self.heat_utilities, self.power_utility)))

@add_method(Fermentation)
def energy_inventory(self):
    """ returns a dict of inventory flows and amounts"""
    return unit_lci(self.heat_utilities, self.power_utility)

@add_method(Fermentation)
def multiLCA(self):
    return unit_lca(self.heat_utilities, self.power_utility)

#below are old scripts.##notes 05-07-2020: if wrap BioSTEAM design and register new designs, it has to increase the recursion limit. So , use the new method instead. 
#from biosteam_lca.units.energy_inventory import EnergyInventory as EINV
#Rui: hestitate to set this higher recursion depth but This was only to solve the constant occuring RecursionError:"maximum recursion depth exceeded"
#import sys
#sys.setrecursionlimit(3000) # by default, sys.getrecursionlimit() was 3000

#base_design = Fermentation._design
#def simulate(self):
#    super().simulate()
 
#def _design(self):
#    """include additional designs for LCA pcalculation"""
#    base_design(self)
#    #results = self._results
#    #Design = results['Design']
#    Design = self._design
##    V = Design['Reactor volume']
##    a = self.aspect_ratio=construction.aspect_ratio
##    D = calc_Diameter(V, a)
##    L = calc_Height (D, a)
##    Di = 12 *D # ft to inch
##    Li = 12 *L # ft to inch
##    Po = self.outs[0].P
##    Design['Diameter (in)'] = calc_Diameter(V,a)
##    Design['Reactor height (in)'] = calc_Height(D,a)
##    Design['Wall thickness (in)'] = tv = BinaryDistillation._calc_WallThickness(Po, Di, Li, S=15000, E=None)
##    Design['Weight of reactor (lb)'] = calc_Weight (Di, Li, tv, self.rho_M)
#    return Design
#
#def calc_Diameter(V: 'Reactor volume',
#                   a: 'Aspect ration (a=L/D)'):
#    
#    """Return diameter based on volume.
#    :math:`V = \frac{\pi a D^3}{4}`
#    """
#    return (4*V/(np.pi*a))**(1/3)*3.28084  # m To ft
#
#def calc_Height (D, a):
#    """Return the height of each reactor"""
#    #Vh = 4/3*pi*(D/2)**2*(0.8*D/2), Volume of the vessel head
#    return a *D +0.8*D  #0.8D accounts for the two heads
#    
#def calc_Weight(Di:'Diameter(ft)',
#                     L: 'Length(ft)',
#                     tv: 'shell thickness (in)',
#                     rho_M: 'Density of material (lb/in^3)') -> 'W (lb)':
#        
#        """Return the weight of the reactor assuming 2:1 elliptical head."""
#        #return np.pi*(Di*12 + tv)*(L*12 + 0.8*Di*12)*tv*rho_M
#        return np.pi*(Di + tv)*(L + 0.8*Di)*tv*rho_M

#def energy_inputs (self):
#    """ summary of all power utilities and heat utilities for the unit process."""
#    return ('Energy inputs per hour:{}'.format(self.e_inv.demand_per_hr()))
# 
#def inventory(self):
#    """ returns a dict of inventory flows and amounts"""
#    self.e_inv = EINV(self.heat_utilities,self.power_utility)   
#    return  self.e_inv.unit_lci()
###%% default emission factor on the greenhouse gas emissions, using GREET Model and e-grid
###def baseLCA(self, location=None):
###    """
###    * 'Construction': (g CO2eq)
###    * 'Process': (g CO2eq)
###    """
###    GHG={}
###    #calculate process GHG
###    GHG['Process emission'] = demand.unit_EF(self._heat_utilities,self._power_utility)
###    #calculate construction GHG
###    W = self._Design['Weight of reactor (lb)']
###    #N = self._Design['Number of reactors']
###    N =self._N
###    GHG['Construction emission'] = GHG_construction_emission = {}
###    #GHG_construction_emission['Reactor'] = ((W*ureg.lb).to(flow.steel_e()['unit']).m *N*flow.steel_e()['emission(g CO2eq)'])
###    self._GHGs =GHG
###    self._totalGHG = [sum(GHG['Process emission'].values()),sum(GHG_construction_emission.values())]
###    return GHG
###%%
#def multiLCA(self):
#    return self.e_inv.unit_lca()
## %% Replace functioins
##Fermentation._design = _design
##Fermentation._GHG_units = {'Process emission': 'g CO2eq/hr',
##                           'Construction emission': 'g CO2eq'} 
#Fermentation.inventory = inventory
#Fermentation.energy_inputs = energy_inputs
#Fermentation.multiLCA = multiLCA