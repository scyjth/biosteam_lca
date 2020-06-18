# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 00:12:20 2019

@author: cyshi
"""
from biosteam.units import * 

from biosteam_lca.units.energy_inventory import demand_per_hr, unit_lci, unit_lca

def energy_inputs(self):
    """ summary of all power utilities and heat utilities for the unit process."""
    return ('Energy inputs per hour:{}'.format(demand_per_hr(self.heat_utilities, self.power_utility)))

def energy_inventory(self):
    """ returns a dict of inventory flows and amounts"""
    return unit_lci(self.heat_utilities, self.power_utility)

def multiLCA(self):
    return unit_lca(self.heat_utilities, self.power_utility)

classes = [
    LLECentrifuge, 
    Flash, 
    ConveyingBelt, 
    CrushingMill, 
    Shredder, 
    Clarifier, 
    RotaryVacuumFilter, 
    LiquidsSplitCentrifuge, 
    SolidsCentrifuge, 
    VentScrubber, 
    BinaryDistillation, 
    SplitFlash, 
    MultiEffectEvaporator,
    HXutility,
    Pump, 
    Transesterification, 
    VibratingScreen, 
    EnzymeTreatment, 
    StorageTank, 
    MixTank, 
    MagneticSeparator, 
    MolecularSieve 
    ]




for i in classes:
    setattr(i, 'energy_inventory', energy_inventory)
    setattr(i, 'multiLCA', multiLCA)
#setattr(LLECentrifuge, 'multiLCA', energy_inventory)


