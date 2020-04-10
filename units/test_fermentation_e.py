# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 17:02:39 2019

@author: cyshi
"""
#from biosteam import Stream#, Fermentation
#from fermentation_LCA import Fermentation
#from lipidcane import ethanol_species
##%% Set up species
#Stream.species = ethanol_species
##Water = Chemical('Water')        
##CO2 = Gas('CO2')
##Ethanol = Chemical('Ethanol')
##glucose = DissolvedCompound('Glucose', '492-61-5', MW=180.156, rho=1540.000)
##sucrose = DissolvedCompound('Sucrose', '57-50-1', MW=342.2965, rho=1540.000)
##dry_yeast = DissolvedCompound('DryYeast', 'Yeast', MW=1)
##phosphoric_acid = DissolvedCompound('H3PO4', '7664-38-2', MW=97.994, rho=10**8)
##Octane = Chemical('Octane')
##ethanol_species = sp = Species.as_species((CO2, Ethanol, Water, glucose, sucrose, phosphoric_acid, Octane, dry_yeast))
##Stream.species = Species.as_species((CO2, Ethanol, Water, glucose, sucrose, phosphoric_acid, Octane, dry_yeast))
#


#from lipidcane import ethanol_species 
from biosteam.biorefineries.lipidcane import species

ethanol_species = species.ethanol_species
from biosteam import Stream
#from biosteam.units import Fermentation
from fermentation_e import Fermentation
#
Stream.species = ethanol_species
#
# Simulate Fermentor
feed = Stream('feed',
              Water=1.20e+05,
              Glucose=1.89e+03,
              Sucrose=2.14e+04,
              DryYeast=1.03e+04,
              units='kg/hr',
              T=32+273.15)

#Fermentation.autoselect_N = True
F1 = Fermentation('F1', ins=feed, outs=('CO2', 'product'), tau=8, efficiency=0.6, N=8)
F1.simulate()
#
## Show results
#F1.show()
#F1.baseLCA()
#F1.inventory()
#results=F1.results()