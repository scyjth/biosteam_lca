# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 13:37:36 2019

@author: cyshi
"""
from biosteam.units import Transesterification, Distillation
import numpy as np
from flow import EF, Inv
from demand import SumUtility
from units.fix import fix_results
from construction_assumption import *
from pprint import pprint
from decimal import Decimal
from multilca import MultiLCA
# %% Wrappers
if __name__ == '__main__':
    import transesterification_e
    raise Exception('Successfully imported :-)')
old_design = Transesterification._design


def simulate(self):
    super().simulate()
   
def _design(self):
    old_design(self)

    results = self._results
    Design = results['Design']
    V = Design['Volume']
    a = self.aspect_ratio=construction.aspect_ratio
    D = _calc_Diameter(V, a)
    L = _calc_Height (D, a)
    Di = 12 *D # ft to inch
    Li = 12 *L # ft to inch
    Po = self.outs[0].P
    Design['Diameter (in)'] = _calc_Diameter(V,a)
    Design['Reactor height (in)'] = _calc_Height(D,a)
    Design['Wall thickness (in)'] = tv = Distillation._calc_WallThickness(Po, Di, Li, S=15000, E=None)
    Design['Weight of reactor (lb)'] = _calc_Weight (Di, Li, tv, self.rho_M)
    return Design
# %% Additional functions for design of reactor
def _calc_Diameter(V:'Volume',
                   a: 'Aspect ration (a=L/D)') -> 'ft':
    
    """Return diameter based on volume.
    :math:`V = \frac{\pi a D^3}{4}`
    """
    return 4*V/(np.pi*a)**(1/3)*3.28084  # m To ft

def _calc_Height (D, a) -> 'ft':
    #Vh = 4/3*pi*(D/2)**2*(0.8*D/2), Volume of the vessel head
    return a *D +0.8*D  #0.8D accounts for the two heads
  
def _calc_Weight(Di:'Diameter(ft)',
                     L: 'Length(ft)',
                     tv: 'shell thickness (in)',
                     rho_M: 'Density of material (lb/in^3)') -> 'W (lb)':
        
        """Return the weight of the reactor assuming 2:1 elliptical head. Material is made by carbon steel.     
        """
        rho_M=construction.rho_vessel
        return np.pi*(Di+tv)*(L+0.8*Di)*tv*rho_M
#%%Energy inputs
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
    EI = energy_inputs(self)
    Design = results['Design']
    W = Design['Weight of reactor (lb)']
    self.Power= EI['Power']
    self.HX = EI['Hx']
    
    #calculate GHG
    GHG['Construction emission'] = GHG_construction_emission = {}
    GHG_construction_emission['Foundation'] = 0 #Karen to add later
    GHG_construction_emission['Reactor'] = (W * EF.steel['emission'] *0.0005)
    GHG['Process emission'] = GHG_process_emission = {}
    GHG_process_emission['Power']= (self.Power* EF.electricity['emission'])
    GHG_process_emission ['Thermal_cooling']= (abs(self.HX [0])*  EF.hx_cooling['emission'])
    self._results['GHG'] =GHG
    self._totalGHG = [sum(GHG_construction_emission.values()), sum(GHG_process_emission.values())]
    return GHG

def multiLCA(self):
    inventory = {Inv.electricity: self.Power, Inv.natural_gas: abs(self.HX[0])}
    multi_lca = MultiLCA(inventory).multi_calc()
    return multi_lca
# %% Replace functioins
Transesterification.rho_M = construction.rho_vessel
Transesterification._design =_design
Transesterification.baseLCA = baseLCA
Transesterification._GHG_units = {'Process emission': 'g CO2eq/hr',
                           'Construction emission': 'g CO2eq'} 
Transesterification.multiLCA = multiLCA