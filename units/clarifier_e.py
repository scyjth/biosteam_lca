# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 22:56:08 2019

@author: cyshi
"""
import numpy as np
from biosteam.units import Clarifier
from biosteam_lca import demand
from biosteam_lca.units.tools import fix_results
from .construction_assumption import construction

base_design = Clarifier._design

if __name__ == '__main__':
    import clarifier_e
    raise Exception('Succesfully Imported :-)')

def simulate(self):
    super().simulate()

def _design(self):
    
    """
    Walls  of  clarifiers  shall  extend  at  least  six  (6)  inches  above  the  surrounding 
    **References**
    
        [1] Oliveira, Samuel C., et al. "Discrimination between ethanol inhibition models in a continuous alcoholic fermentation process using flocculating yeast." Applied biochemistry and biotechnology 74.3 (1998): 161-172.
    
    ground surface and shall provide not less than twelve (12) inches of freeboard.
    """
    base_design(self)
    Design = self._Design
    overflow = self.ins[0]
    SetArea = Design['Settling area']
    diameter = np.sqrt(SetArea*4/np.pi)
    self.W = Design['Weight of reactor (lb)'] = 0 # Karen to add the weight calculation algorithm
    Design['Diameter (in)'] = diameter

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
Clarifier.rho_M = construction.rho_vessel
Clarifier._design = _design
Clarifier.baseLCA = baseLCA
Clarifier._GHG_units = {'Process emission': 'g CO2eq/hr',
                           'Construction emission': 'g CO2eq'} 
Clarifier.multiLCA = multiLCA

#    

#    def _calc_energy(self, SetArea):
#        # Finding diameter of the tank in ft
#        diameter = np.sqrt(SetArea*4/np.pi)
#        # Energy assuming quadratic relationship in hp
#        Energy = 16 * (diameter/200)**2
#        return Energy