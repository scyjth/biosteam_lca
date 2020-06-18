# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 17:02:39 2019

@author: cyshi
"""
from biorefineries.lipidcane.chemicals import lipidcane_chemicals
from biosteam import settings, Stream
from units_e import LLECentrifuge

settings.set_thermo(lipidcane_chemicals)
feed = Stream('feed', T=333.15,
              Lipid=0.996, Biodiesel=26.9,
              Methanol=32.9, Glycerol=8.97)
C1 = LLECentrifuge('C1', ins=feed, outs=('light', 'heavy'))
C1.simulate()
C1.show()
