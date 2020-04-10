# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 22:56:08 2019

@author: cyshi
"""
from biosteam.units import RVF
from biosteam_lca import flow
from biosteam_lca import demand
from biosteam_lca.units.tools import fix_results
from .construction_assumption import construction

base_design = RVF._design

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
    W = self._Design['Weight of RVF (lb)']
    GHG['Construction emission'] = {}
    if W:
        GHG['Construction emission']['RVF'] = (W *flow.steel_e()['emission(g CO2eq)'] *0.0005)
    self._GHGs =GHG
    self._totalGHG = [sum(GHG['Process emission'].values()), sum(GHG['Construction emission'].values())]
    return GHG

def multiLCA(self):
    return demand.unit_lca(self._heat_utilities,self._power_utility)
# %% Replace functioins
RVF.rho_M = construction.rho_vessel
RVF.energy_inputs=energy_inputs
RVF.baseLCA =baseLCA
RVF._GHG_units = {'Process emission': 'g CO2eq/hr',
                           'Construction emission': 'g CO2eq'} 
RVF.multiLCA = multiLCA