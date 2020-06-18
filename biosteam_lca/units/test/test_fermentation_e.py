# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 17:02:39 2019

@author: cyshi
"""

from biorefineries.lipidcane.chemicals import ethanol_chemicals
# from biosteam.units import Fermentation
from biosteam_lca.units.fermentation_e import Fermentation
from biosteam import Stream, settings
settings.set_thermo(ethanol_chemicals)
feed = Stream('feed',
               Water=1.20e+05,
               Glucose=1.89e+03,
               Sucrose=4.14e+04,
               DryYeast=1.03e+04,
               units='kg/hr',
               T=32+273.15)
F1 = Fermentation('F1',ins=feed, outs=('CO2', 'product'),tau=8, efficiency=0.90, N=8)
F1.simulate()
F1.show()

#import numpy as np
#results = []
#for i in np.arange(0.7, 0.9, 0.01): 
#    feed = Stream('feed',
#               Water=1.20e+05,
#               Glucose=1.89e+03,
#               Sucrose=4.14e+04,
#               DryYeast=1.03e+04,
#               units='kg/hr',
#               T=32+273.15)
#    F1 = Fermentation('F1',ins=feed, outs=('CO2', 'product'),tau=8, efficiency=i, N=8)
#    F1.simulate()
#    F1.show()
##    results.append(F1.mass_out[2])
#    results.append(F1.purchase_cost/F1.mass_out[2])