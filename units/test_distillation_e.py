# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 00:12:20 2019

@author: cyshi
"""
##import unittest
#from biosteam import Species, Stream
#from distillation_e import Distillation
#
## Set up stream
#Stream.species = Species('Water', 'Methanol', 'Glycerol')
#feed = Stream('feed', flow=(80, 100, 25))
#feed.T = feed.bubble_T()[0] # Feed at bubble point T
#
## Set up column
#D1 = Distillation('D1', ins=feed,
#                  LHK=('Methanol', 'Water'),
#                  y_top=0.99, x_bot=0.01, k=2)
#D1.is_divided = True
#D1.simulate()



from biosteam import Species, Stream
#from biosteam.units import Distillation
from distillation_e import Distillation

# Set up stream
Stream.species = Species('Water', 'Methanol', 'Glycerol')
feed = Stream('feed', flow=(80, 100, 25))
feed.T = feed.bubble_T()[0] # Feed at bubble point T

# Set up column
D1 = Distillation('D1', ins=feed,
                  LHK=('Methanol', 'Water'),
                  y_top=0.99, x_bot=0.01, k=2)
D1.is_divided = True
D1.simulate()

# See all results
#D1.diagram()
D1.show(T='degC', P='atm', fraction=True)