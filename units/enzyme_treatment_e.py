# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 22:56:08 2019

@author: cyshi
"""
from biosteam.units import EnzymeTreatment
import numpy as np
from biosteam_lca import flow
from biosteam_lca import demand
from biosteam_lca.units.tools import fix_results
from .construction_assumption import construction


base_design = EnzymeTreatment._design


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
    GHG['Process emission'] = demand.unit_process_EF(self._heat_utilities,self._power_utility)
    GHG['Construction emission'] = {}
    self._GHGs =GHG
    self._totalGHG = [sum(GHG['Process emission'].values()), sum(GHG['Construction emission'].values())]
    return GHG

def multiLCA(self):
    return demand.unit_lca(self._heat_utilities,self._power_utility)

# %% Replace functioins
EnzymeTreatment.energy_inputs=energy_inputs
EnzymeTreatment.baseLCA =baseLCA
EnzymeTreatment._GHG_units = {'Process emission': 'g CO2eq/hr',
                           'Construction emission': 'g CO2eq'} 
EnzymeTreatment.multiLCA = multiLCA
