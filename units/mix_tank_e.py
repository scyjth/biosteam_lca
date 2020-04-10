# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 17:02:39 2019

@author: cyshi
"""
from biosteam import MixTank, Distillation
import numpy as np
from biosteam_lca import flow
from biosteam_lca import demand
from biosteam_lca.units.tools import fix_results
from .construction_assumption import construction
from biosteam_lca.multilca import MultiLCA
import pint
ureg = pint.UnitRegistry()
Q_ = ureg.Quantity
# %% Wrappers for tank in Biosteam
if __name__ == '__main__':
    import mix_tank_LCA
    raise Exception('Successfully imported Biosteam :-)')
base_design = MixTank._design

#%%
def simulate(self):
    super().simulate()
      
def _design(self):
    base_design(self)
    Design = self._Design
    V = Design['Total volume']
    a = self.aspect_ratio
    D = _calc_Diameter(V, a)
    L = _calc_Height (D, a)
    Di = 12 *D # ft to inch
    Li = 12 *L # ft to inch
    Po = self.outs[0].P
    Design['Diameter (in)'] = _calc_Diameter(V,a)
    Design['Height (in)'] = _calc_Height(D,a)
    Design['Wall thickness (in)'] = tv = Distillation._calc_WallThickness(Po, Di, Li, S=15000, E=None)
    Design['Weight of tank (lb)'] = _calc_Weight (Di, Li, tv, self.rho_M)
    return Design

def _calc_Diameter(V:'Volume',
                   a: 'Aspect ration (a=L/D)'):
    
    """Return diameter based on volume.
    :math:`V = \frac{\pi a D^3}{4}`
    """
    return 4*V/(np.pi*a)**(1/3)*3.28084  # m To ft


def _calc_Height (D, a):
    #Vh = 4/3*pi*(D/2)**2*(0.8*D/2), Volume of the vessel head
    return a *D +0.8*D  #0.8D accounts for the two heads

    
def _calc_Weight(Di:'Diameter(ft)',
                     L: 'Length(ft)',
                     tv: 'shell thickness (in)',
                     rho_M: 'Density of material (lb/in^3)') -> 'W (lb)':
        
        """Return the weight of the reactor assuming 2:1 elliptical head."""
        #return np.pi*(Di*12 + tv)*(L*12 + 0.8*Di*12)*tv*rho_M
        return np.pi*(Di + tv)*(L + 0.8*Di)*tv*rho_M
def energy_inputs (self):
    """ summary of all power utilities and heat utilities for the unit process."""
    return ('Energy inputs per hour:{}'.format(sum_utility.utility_per_hr(self._heat_utilities,self._power_utility)))

def baseLCA(self, location=None):
    """
    * 'Construction': (g CO2eq)
    * 'Process': (g CO2eq)
    """
    GHG={}
    #calculate process GHG
    GHG['Process emission'] = sum_utility.unit_process_EF(self._heat_utilities,self._power_utility)
    #calculate construction GHG
    W = self._Design['Weight of tank (lb)']
    GHG['Construction emission'] = GHG_construction_emission = {}
    GHG_construction_emission['Tank'] = ((W*ureg.lb).to(flow.steel_e()['unit']).m *flow.steel_e()['emission(g CO2eq)'] *0.0005)
    
    self._GHGs =GHG
    self._totalGHG = [sum(GHG['Process emission'].values()),sum(GHG_construction_emission.values())]
    return GHG
#%%
def multiLCA(self):
    return demand.unit_lca(self._heat_utilities,self._power_utility)
# %% Replace functioins
MixTank.rho_M = construction.rho_vessel
MixTank.aspect_ratio = construction.aspect_ratio
MixTank._design = _design
MixTank.baseLCA = baseLCA
MixTank.energy_inputs=energy_inputs
MixTank._GHG_units = {'Process emission': 'g CO2eq/hr',
                           'Construction emission': 'g CO2eq'} 
MixTank.multiLCA = multiLCA

