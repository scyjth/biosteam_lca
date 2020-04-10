# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 22:56:08 2019

@author: cyshi
"""
from biosteam.units import MagneticSeparator
from biosteam_lca import flow
from biosteam_lca import demand
from biosteam_lca.units.tools import fix_results

base_design = MagneticSeparator._design

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
    W = self._Design['Weight of MagneticSeparator (lb)']
    GHG['Construction emission'] = {}
    if W:
        GHG['Construction emission']['MagneticSeparator'] = (W *flow.steel_e()['emission(g CO2eq)'] *0.0005)
    self._GHGs =GHG
    self._totalGHG = [sum(GHG['Process emission'].values()), sum(GHG['Construction emission'].values())]
    return GHG

def multiLCA(self):
    return demand.unit_lca(self._heat_utilities,self._power_utility)
# %% Replace functioins
MagneticSeparator.energy_inputs=energy_inputs
MagneticSeparator.baseLCA =baseLCA
MagneticSeparator._GHG_units = {'Process emission': 'g CO2eq/hr',
                           'Construction emission': 'g CO2eq'} 
MagneticSeparator.multiLCA = multiLCA