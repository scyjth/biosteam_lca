# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 22:14:01 2018

@author: cyshi
"""
from biosteam.units import ConveyingBelt
from biosteam_lca import flow
from biosteam_lca import demand
from biosteam_lca.units.tools import fix_results
from .construction_assumption import construction

base_design = ConveyingBelt._design

if __name__ == '__main__':
    import ConveyingBelt_e
    raise Exception('Succesfully Imported :-)')

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
    W = self._Design['Weight of Conveying Belt (lb)']
    GHG['Construction emission'] = {}
    if W:
        GHG['Construction emission']['Conveying Belt'] = (W *flow.steel_e()['emission(g CO2eq)'] *0.0005)
    self._GHGs =GHG
    self._totalGHG = [sum(GHG['Process emission'].values()), sum(GHG['Construction emission'].values())]
    return GHG

def multiLCA(self):
    return demand.unit_lca(self._heat_utilities,self._power_utility)
# %% Replace functioins
ConveyingBelt.rho_M = construction.rho_vessel
ConveyingBelt.energy_inputs=energy_inputs
ConveyingBelt.baseLCA =baseLCA
ConveyingBelt._GHG_units = {'Process emission': 'g CO2eq/hr',
                           'Construction emission': 'g CO2eq'} 
ConveyingBelt.multiLCA = multiLCA