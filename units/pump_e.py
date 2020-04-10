# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 15:53:14 2019

@author: cyshi
"""
from biosteam.units import Pump
import numpy as np
from biosteam_lca import flow
from biosteam_lca import demand
from biosteam_lca.units.tools import fix_results
from .construction_assumption import construction
from biosteam_lca.multilca import MultiLCA
# %% Wrappers for Pump
if __name__ == '__main__':
    import pump_e
    raise Exception('Successfully imported Biosteam :-)')
base_design = Pump._design

def simulate(self):
    super().simulate()
    
def _design(self):
    base_design(self)
    Design = self._Design
    Design['Weight of pump (lb)'] = _calc_Weight (self.rho_M)
    return Design

def _calc_Weight(rho_M: 'Density of material (lb/in^3)') -> 'W (lb)':
        
        """Return the weight of the pump     
        """
        w= 0 # place holder, Rachael is working on the mass caluclation of pump
        return w
#%%
def energy_inputs (self):
    """ summary of all power utilities and heat utilities for the unit process."""
    return ('Energy inputs per hour:{}'.format(sum_utility.utility_per_hr(self._heat_utilities,self._power_utility)))
#%%            
def baseLCA(self, location=None):
    """
    * 'Construction': (g CO2eq)
    * 'Process': (g CO2eq)
    """
    GHG={}
    #calculate process GHG
    GHG['Process emission'] = sum_utility.unit_process_EF(self._heat_utilities,self._power_utility)
    W = self._Design['Weight of pump (lb)']
    GHG['Construction emission'] = {}
    if W:
        GHG['Construction emission']['Pump'] = (W *flow.steel_e()['emission(g CO2eq)'] *0.0005)
    self._GHGs =GHG
    self._totalGHG = [sum(GHG['Process emission'].values()), sum(GHG['Construction emission'].values())]
    return GHG
#%%
def multiLCA(self):
    return demand.unit_lca(self._heat_utilities,self._power_utility)
# %% Replace functioins
Pump.rho_M = construction.rho_vessel
Pump._design = _design
Pump.energy_inputs=energy_inputs
Pump.baseLCA =baseLCA
Pump._GHG_units = {'Process emission': 'g CO2eq/hr',
                           'Construction emission': 'g CO2eq'} 
Pump.multiLCA = multiLCA
