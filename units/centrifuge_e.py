# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 00:12:20 2019

@author: cyshi
"""
from biosteam.units import Centrifuge_LLE
import numpy as np
from biosteam_lca import demand
from units.fix import fix_results
from construction_assumption import *
# %% Wrappers for Fermentation
if __name__ == '__main__':
    import centrifuge_e
    raise Exception('Successfully imported Biosteam :-)')
old_design = Centrifuge_LLE._design

def simulate(self):
    super().simulate()
# %% additional design for LCA   
def _design(self):
    old_design(self)
    results = self._results
    Design = results['Design']
    Design['Weight of centrifuge (lb)'] = _calc_Weight (self.rho_M)
    return Design

def _calc_Weight(rho_M: 'Density of material (lb/in^3)') -> 'W (lb)':
        
        """Return the weight of the pump     
        """
        w= 0 # place holder, Rachael is working on the mass caluclation of pump
        return w
    
def energy_inputs (self):
    """ Returns the summary of all power utilities and heat utilities for the unit process."""
    return SumUtility.utility_demand(self)

#%%            
def baseLCA(self, location=None):
    """
    * 'Construction': (g CO2eq)
    * 'Process': (g CO2eq)
    """
    GHG={}
    results = self._results
    Design = results['Design']
    EI = energy_inputs(self)
    self.Power= EI['Power']
    
#    GHG={}
#    self.results['Energy inputs'] =energy_inputs(self)
#    Design = self.results['Design']
#    self.Power= self.results['Energy inputs']['Power']
    W = Design['Weight of centrifuge (lb)']
    GHG['Construction emission (g CO2eq)'] = '%.2e' %(W * EF.steel["emission"] *0.0005)
    GHG['Process emission (g CO2eq)'] = '%.2e' %(self.Power * EF.electricity["emission"] )
    self._results['GHG'] =GHG
    return GHG

def multiLCA(self):
    return demand.unit_lca(self._heat_utilities,self._power_utility)
# %% Replace functioins
Centrifuge_LLE.rho_M = construction.rho_vessel
Centrifuge_LLE._design = _design
Centrifuge_LLE.baseLCA = baseLCA
Centrifuge_LLE._GHG_units = {'Process emission': 'g CO2eq/hr',
                           'Construction emission': 'g CO2eq'} 
Centrifuge_LLE.multiLCA = multiLCA
