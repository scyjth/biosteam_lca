# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 00:12:20 2019

@author: cyshi
"""
#from setuptools import setup,find_packages
#setup(name='biosteam_lca',packages=find_packages(),)

from biosteam.units import MolecularSieve
import numpy as np
from biosteam_lca import flow
from biosteam_lca import demand
from biosteam_lca.units.tools import fix_results
from .construction_assumption import construction
from biosteam_lca.multilca import MultiLCA

base_design = MolecularSieve._design

def simulate(self):
    super().simulate()
#%% additional design for LCA   
def _design(self):
    base_design(self)
    Design = self._Design
    Design['Weight of Molecular Sieve (lb)'] = _calc_Weight (self.rho_M)
    return Design

def _calc_Weight(rho_M: 'Density of material (lb/in^3)') -> 'W (lb)':
        
        """Return the weight of the pump     
        """
        w= 0 # place holder, Rachael is working on the mass caluclation of pump
        return w

def energy_inputs (self):
    """ summary of all power utilities and heat utilities for the unit process."""
    return ('Energy inputs per hour:{}'.format(demand.utility_per_hr(self._heat_utilities,self._power_utility)))
#%% default life cycle analysis on the greenhouse gas emissions
def baseLCA(self, location=None):
    """
    * 'Construction': (g CO2eq)
    * 'Process': (g CO2eq)
    """
    GHG={}
    #calculate process GHG
    GHG['Process emission'] = demand.unit_process_EF(self._heat_utilities,self._power_utility)
    W = self._Design['Weight of Molecular Sieve (lb)']
    GHG['Construction emission'] = {}
    if W:
        GHG['Construction emission']['Molecular Sieve'] = (W *flow.steel_e()['emission(g CO2eq)'] *0.0005)
    self._GHGs =GHG
    self._totalGHG = [sum(GHG['Process emission'].values()), sum(GHG['Construction emission'].values())]
    return GHG

def multiLCA(self):
    return demand.unit_lca(self._heat_utilities,self._power_utility)
# %% Replace functioins
MolecularSieve.rho_M = construction.rho_vessel
MolecularSieve._design = _design
MolecularSieve.energy_inputs=energy_inputs
MolecularSieve.baseLCA =baseLCA
MolecularSieve._GHG_units = {'Process emission': 'g CO2eq/hr',
                           'Construction emission': 'g CO2eq'} 
MolecularSieve.multiLCA = multiLCA
