# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 16:56:48 2019

@author: cyshi
"""
from biosteam.units import Distillation
import numpy as np
from biosteam_lca import flow
from biosteam_lca import demand
from biosteam_lca.units.tools import fix_results
from .construction_assumption import construction
from biosteam_lca.multilca import MultiLCA
import pint
ureg = pint.UnitRegistry()
Q_ = ureg.Quantity
#import sys, os
#sys.path.insert(0, os.path.realpath('./'))

#dir_path = os.path.dirname(os.path.realpath(__file__)) + '\\'
# %% Wrappers for distillation
if __name__ == '__main__':
    import distillation_e
    raise Exception('Succesfully Imported :-)')

def simulate(self):
    super().simulate()
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
    is_divided = self.is_divided
    Design = self._Design
    GHG={}
#    try:
#        EI = energy_inputs = SumUtility.utility_demand(self)
#        Power = self.Power= EI['Power']
#        HX=self.HX = EI['Hx']
#    except ValueError:
#        print("Please check your calculation for energy inputs")

    GHG['Process emission'] = sum_utility.unit_process_EF(self._heat_utilities,self._power_utility)

    GHG['Construction emission'] = GHG_construction_emission = {}
    GHG_construction_emission['Foundation'] = 0 #Karen to add later
    if is_divided:
        Weight_R = (((Design['Rectifier weight'])*ureg.lb).to(flow.steel_e()['unit'])).m 
        Weight_S = (((Design['Stripper weight'])*ureg.lb).to(flow.steel_e()['unit'])).m 
        GHG_construction_emission['Rectifier'] = (Weight_R * flow.steel_e()['emission(g CO2eq)']) #convert W(lb) to ton
        GHG_construction_emission['Stripper'] = (Weight_S *flow.steel_e()['emission(g CO2eq)']) #convert W(lb) to ton
    else:
        Weight = ((Design['Weight']*ureg.lb).to(flow.steel_e()['unit'])).m 
        GHG_construction_emission['Column'] = (Weight * flow.steel_e()['emission(g CO2eq)'])

    self._GHGs =GHG
    self._totalGHG = [sum(GHG['Process emission'].values()),sum(GHG_construction_emission.values())]
    return GHG

def multiLCA(self):
    return demand.unit_lca(self._heat_utilities,self._power_utility)
# %% Replace functioins
Distillation.energy_inputs=energy_inputs
Distillation.baseLCA = baseLCA
Distillation._GHG_units = {'Process emission': 'g CO2eq/hr',
                           'Construction emission': 'g CO2eq'} 
Distillation.multiLCA = multiLCA

