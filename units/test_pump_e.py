# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 16:56:48 2019

@author: cyshi
"""
from biosteam import Species, Stream
from pump_e import Pump
Stream.species = Species('Water', 'Ethanol')

# Simulate pump
feed = Stream('feed', Water=200, T=350)
P1 = Pump('P1', ins=feed, outs='out')
P1.simulate()
