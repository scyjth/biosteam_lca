# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 00:12:20 2019

@author: cyshi
"""
#from setuptools import setup,find_packages
#setup(name='biosteam_lca',packages=find_packages(),)

from biosteam.units import VentScrubber
import numpy as np
from biosteam_lca import flow
from biosteam_lca import demand
from biosteam_lca.units.tools import fix_results
from biosteam_lca.multilca import MultiLCA

base_design = VentScrubber._design

def simulate(self):
    super().simulate()
  
def _design(self):
    base_design(self)
    Design = self._Design
    Design['Weight of Vent Scrubber (lb)'] = 0 # place holder, Karen is working on the mass caluclation of pump
    return Design

def energy_inputs (self):
    """ summary of all power utilities and heat utilities for the unit process."""
    return ('Energy inputs per hour:{}'.format(demand.utility_per_hr(self._heat_utilities,self._power_utility)))

def baseLCA(self, location=None):
    """
    * 'Construction': (g CO2eq)
    * 'Process': (g CO2eq)
    """
    GHG={}
    GHG['Process emission'] = demand.unit_process_EF(self._heat_utilities,self._power_utility)
    W = self._Design['Weight of Vent Scrubber (lb)']
    GHG['Construction emission'] = {}
    if W:
        GHG['Construction emission']['Vent Scrubber'] = (W *flow.steel_e()['emission(g CO2eq)'] *0.0005)
    self._GHGs =GHG
    self._totalGHG = [sum(GHG['Process emission'].values()), sum(GHG['Construction emission'].values())]
    return GHG

def multiLCA(self):
    return demand.unit_lca(self._heat_utilities,self._power_utility)
# %% Replace functioins
VentScrubber._design = _design
VentScrubber.energy_inputs=energy_inputs
VentScrubber.baseLCA =baseLCA
VentScrubber._GHG_units = {'Process emission': 'g CO2eq/hr',
                           'Construction emission': 'g CO2eq'} 
VentScrubber.multiLCA = multiLCA
