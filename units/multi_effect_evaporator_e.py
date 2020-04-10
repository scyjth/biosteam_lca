# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 22:56:08 2019

@author: cyshi
"""
from biosteam import MultiEffectEvaporator
import numpy as np
from biosteam_lca import flow
from biosteam_lca import demand
from biosteam_lca.units.tools import fix_results
from biosteam_lca.multilca import MultiLCA

if __name__ == '__main__':
    import MultiEffectEvaporator_e
    raise Exception('Succesfully Imported :-)')
    
base_design = MultiEffectEvaporator._design

def simulate(self):
    super().simulate()

def _design(self):
    base_design(self)
    Design = self._Design
    Design['Weight (lb)'] = 0 #Karen to add later 
    return Design

def energy_inputs (self):
    """ summary of all power utilities and heat utilities for the unit process."""
    return ('Energy inputs per hour:{}'.format(sum_utility.utility_per_hr(self._heat_utilities,self._power_utility)))

def baseLCA(self, location=None):
    """
    * 'Construction': (g CO2eq)
    * 'Process': (g CO2eq)
    """
    GHG={}
    GHG['Process emission'] = sum_utility.unit_process_EF(self._heat_utilities,self._power_utility)
    GHG['Construction emission'] = {}
    self._GHGs =GHG
    self._totalGHG = [sum(GHG['Process emission'].values()), sum(GHG['Construction emission'].values())]
    return GHG

def multiLCA(self):
    return demand.unit_lca(self._heat_utilities,self._power_utility)
# %% Replace functioins
MultiEffectEvaporator._design = _design
MultiEffectEvaporator.energy_inputs=energy_inputs
MultiEffectEvaporator.baseLCA =baseLCA
MultiEffectEvaporator._GHG_units = {'Process emission': 'g CO2eq/hr',
                           'Construction emission': 'g CO2eq'} 
MultiEffectEvaporator.multiLCA = multiLCA