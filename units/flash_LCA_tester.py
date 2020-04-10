# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 16:56:48 2019

@author: cyshi
"""

#from biosteam import Species, Stream
#from flash_LCA import Flash
## Set up feed
#Stream.species = Species('Glycerol', 'Water')
#feed = Stream('feed', flow=(100, 600))
#feed.T = feed.bubble_point()[0]
#
## Simulate flash drum
#F1 = Flash('F1',
#           ins=feed,
#           outs=('vapor', 'crude glycerin'),
#           P=101325, # Pa
#           T=410.15) # K
#F1.simulate()

from biosteam import Species, Stream, Flash
# Set up feed
Stream.species = Species('Glycerol', 'Water')
feed = Stream('feed', flow=(100, 600))
feed.T = feed.bubble_point()[0]

# Simulate flash drum
F1 = Flash('F1',
           ins=feed,
           outs=('vapor', 'crude glycerin'),
           P=101325, # Pa
           T=410.15) # K
F1.simulate()