# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 17:02:39 2019

@author: cyshi
"""
from biorefineries.lipidcane.chemicals import lipidcane_chemicals
from biosteam import settings, Stream
from biosteam_lca.units import Flash

settings.set_thermo(['Water', 'Glycerol'])
feed = Stream('feed', Glycerol=300, Water=1000)
bp = feed.bubble_point_at_P() # Feed at bubble point T
feed.T = bp.T
F1 = Flash('F1',
            ins=feed,
            outs=('vapor', 'crude_glycerin'),
            P=101325, # Pa
            T=410.15) # K
F1.simulate()
F1.show(T='degC', P='atm')
