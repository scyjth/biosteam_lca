# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 17:02:39 2019

@author: cyshi
"""
from centrifuge_e import Centrifuge_LLE
from biosteam import Stream
#from biosteam.units import Centrifuge_LLE
from lipidcane import biodiesel_species

# Set up stream
Stream.species = biodiesel_species
feed = Stream(Lipid=1, Methanol=51, Glycerol= 9, Biodiesel=27, T=333.15)

# Set up centrifuge
C1 = Centrifuge_LLE('C1',
                    ins = feed,
                    outs = ('light', 'heavy'),
                    species_IDs=('Lipid', 'Methanol', 'Biodiesel'),
                    split=(1, 0.5, 1),
                    solvents=('Glycerol',),
                    solvent_split=(0.05,))

# Run all methods
C1.simulate()


