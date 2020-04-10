# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 16:56:48 2019

@author: cyshi
"""
from biosteam import Flash
from default_EF import *
from construction_assumption import *
from sum_utility import SumUtility
# %% Wrappers for flash
if __name__ == '__main__':
    import flash_LCA
    raise Exception('Executed after Biosteam :-)')
design = Flash._design

def simulate(self):
    super().simulate()

def energy_inputs (self):
    """ Returns the summary of all power utilities and heat utilities for the unit process."""
    return SumUtility.utility_demand(self)

def simpleLCA(self, location=None):
    """
    * 'Construction': (g CO2eq)
    * 'Process': (g CO2eq)
    """
    GHG={}
    results = self.results
    self.results['Energy inputs'] =energy_inputs(self)
    Design = results['Design']
    Weight = Design['Weight']
    Power= self.results['Energy inputs']['Power']
    HX = self.results['Energy inputs']['Hx']
    #Calculate GHG
    GHG['Construction emission (g CO2eq)'] = '%.2e' %(Weight * EF.steel['emission'] *0.0005/construction.total_hr) #convert W(lb) to ton
    GHG['Process emission (g CO2eq)'] ={}
    GHG['Process emission (g CO2eq)']['power'] = '%.2e' %(Power* EF.electricity['emission'])
    GHG['Process emission (g CO2eq)'] ['thermal']= '%.2e' %(abs(HX [0])* EF.natural_gas['emission'])
    self.results['GHG'] =GHG
    return GHG
# %% Replace functioins
Flash.simpleLCA = simpleLCA
Flash.energy_inputs=energy_inputs