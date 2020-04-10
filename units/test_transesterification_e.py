# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 17:06:06 2019

@author: cyshi
"""
from biosteam import Stream
from transesterification_e import Transesterification
from lipidcane import biodiesel_species

# From USDA Biodiesel model
x_cat = 0.01064 # Catalyst molar fraction in reactor

Stream.species = biodiesel_species
lipid = Stream('lipid', Lipid=10)
methanol = Stream('methanol',Methanol=5)

R1 = Transesterification('R1',
                         ins = (lipid, methanol),
                         outs = Stream('product'),
                         efficiency=0.90,
                         r=6, # Methanol ratio
                         T=273.15+60,
                         catalyst_molfrac=0.11)
R1.simulate()
results=R1.baseLCA()
#%% ester 2
#Stream.species = biodiesel_species
#R1=Transesterification('example', outs=('Biodiesel','Glycerol'))
#feed = Stream('feed', Lipid=100, Water=400)  
#fresh_Methanol = 5
#R1.ins = (feed, fresh_Methanol)
#
#R1.simulate()
