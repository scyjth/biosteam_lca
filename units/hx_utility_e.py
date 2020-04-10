# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 00:12:20 2019

@author: cyshi
"""
from biosteam import HXutility
import numpy as np
from biosteam_lca import flow
from biosteam_lca import sum_utility
from biosteam_lca.units.tools import fix_results
from construction_assumption import construction
from biosteam_lca.multilca import MultiLCA

base_design = HXutility._design

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
    return sum_utility.unit_lca(self._heat_utilities,self._power_utility)
# %% Replace functioins
HXutility._design = _design
HXutility.energy_inputs=energy_inputs
HXutility.baseLCA =baseLCA
HXutility._GHG_units = {'Process emission': 'g CO2eq/hr',
                           'Construction emission': 'g CO2eq'} 
HXutility.multiLCA = multiLCA
        
       


