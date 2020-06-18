# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 18:06:46 2019

@author: cyshi
"""
import numpy as np
from biosteam import find, System
from lipidcane.biodiesel_sys import *
from lipidcane.ethanol_sys import *


def coproduct_finder(sys):
    """ look for the streams that has coproducts outputs"""
    #streams ={}
    # return sys.products
    
    streams=np.array([])
    if not isinstance(sys, System):
        raise TypeError(f"Argument, 'sys', must be type System, not {type(sys).__name__}")
    if sys == biodiesel_sys:
        #print ('Coproducts producing in the biodiesel system:')
        biodiesel_sys._converge()
    elif sys == EtOH_sys:
        EtOH_sys._converge()
    else:
        raise Warning ("Please select a sytem that yields coproducts")
        
    for s in filter(lambda s: not s.sink[0] and s.source[0], sys.streams):
        stream = str(s)
        find(stream).show()
        streams=np.append(streams,stream)
    return streams

def coproduct_sum(sys):

    """kwarg takes the name of the system, such as biodiesel_sys, or EoTH_sys"""
    
    streams=coproduct_finder(sys)
    BD_mass=0
    Glycerol_mass=0
    products = {}
    for i in streams:
        if i == 'Waste':
            pass
        else:
            mass = find(i).mass
            BD_index=find(i).get_index('Biodiesel')
            Glycerol_index=find(i).get_index('Glycerol')
            BD = mass[BD_index]
            Glycerol = mass[Glycerol_index]
            BD_mass = BD_mass+ BD
            Glycerol_mass = Glycerol_mass + Glycerol
            products = {'Biodiesel (kg/hr)':BD_mass, 'Glycerol (kg/hr)': Glycerol_mass}
    return products

def allocation_factor(sys, method):
    products=coproduct_sum(sys)
    print (products)
    """
    "Mass" represents mass allocation factor. "Energy" represents energy allocation factor. "Market" represents market value allocation factor
    """
    if method == 'mass':
        AF = (products['Biodiesel (kg/hr)'])/(products['Biodiesel (kg/hr)']+products['Glycerol (kg/hr)'])
    if method == 'energy':
        # energy content of biodiesel and glycerol was taken from GREET Model
        AF = (products['Biodiesel (kg/hr)'] * 16134.17668)/(products['Biodiesel (kg/hr)']*16134.17668 +products['Glycerol (kg/hr)']*7979)
    if method == 'market':
        # market value of biodiesel and glycerol was taken from GREET Model
        AF = (products['Biodiesel (kg/hr)'] * 0.547)/(products['Biodiesel (kg/hr)']*0.547 +products['Glycerol (kg/hr)']*0.25)
    return AF

#find('d108').sink
#find('d108').source
