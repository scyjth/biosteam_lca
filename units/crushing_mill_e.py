# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 22:14:01 2018

@author: cyshi
"""
from biosteam.units import CrushingMill
from biosteam_lca import flow
from biosteam_lca import demand
from biosteam_lca.units.tools import fix_results
from .construction_assumption import construction

base_design = CrushingMill._design

def simulate(self):
    super().simulate()

def energy_inputs (self):
    """ summary of all power utilities and heat utilities for the unit process."""
    return ('Energy inputs per hour:{}'.format(demand.utility_per_hr(self._heat_utilities,self._power_utility)))

def baseLCA(self, location=None):
    """
    * 'Construction': (g CO2eq)
    * 'Process': (g CO2eq)
    """
    GHG={}
    #calculate process GHG
    GHG['Process emission'] = demand.unit_process_EF(self._heat_utilities,self._power_utility)
    W = self._Design['Weight of Crushing Mill (lb)']
    GHG['Construction emission'] = {}
    if W:
        GHG['Construction emission']['Crushing Mill'] = (W *flow.steel_e()['emission(g CO2eq)'] *0.0005)
    self._GHGs =GHG
    self._totalGHG = [sum(GHG['Process emission'].values()), sum(GHG['Construction emission'].values())]
    return GHG

def multiLCA(self):
    return demand.unit_lca(self._heat_utilities,self._power_utility)
# %% Replace functioins
CrushingMill.rho_M = construction.rho_vessel
CrushingMill.energy_inputs=energy_inputs
CrushingMill.baseLCA =baseLCA
CrushingMill._GHG_units = {'Process emission': 'g CO2eq/hr',
                           'Construction emission': 'g CO2eq'} 
CrushingMill.multiLCA = multiLCA