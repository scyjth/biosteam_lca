# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 00:12:20 2019

@author: cyshi
"""
from biosteam import Species, Stream
from hx_utility_e import HXutility
Stream.species = Species('Water', 'Ethanol')

# Simulate heat exchanger
feed = Stream('feed', Water=200, Ethanol=200)
hx = HXutility('hx', ins=feed, outs='product', T=50+273.15,
               rigorous=False) # Ignore VLE
hx.simulate()
