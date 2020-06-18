# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 15:33:39 2019

@author: cyshi
"""
# This class will be completed when Karen finishes her design on all biorefinary constructiosn, including all deirect and indirects inputs related to coast and emission.

class Construction:
    """A summary of all construction related assumptions been adopted in the process deisgn and calculation"""
    
    rho_Mdict = {'Carbon steel': 0.284 ,
    'Low-alloy steel': None,
    'Stainless steel 304': None,
    'Stainless steel 316': None,
    'Carpenter 20CB-3': None,
    'Nickel-200': None,
    'Monel-400': None,
    'Inconel-600': None,
    'Incoloy-825': None,
    'Titanium': None}
    
    h_a = 1.5 # assume aspect ratio of vessel is 1.5
    day = 100
    year = 20
    
    @property
    def rho_vessel(self, material=None):
        """ returns the density of the material used for all pressure vessels on site, such as fermentor, transesterification reactor, storage tanks, etc."""
        if material:
            rho = self.rho_Mdict[material]
        else:
            rho = self.rho_Mdict['Carbon steel'] 
        return rho
    
    @property
    def aspect_ratio(self):
        """returns the aspect ratio of the pressure vessel"""
        return self.h_a 
    
#    @property
#    def total_hr(self):
#        """return the total running hours for the entire biorefinary life"""
#        return self.day*self.year*24
    
    
construction = Construction()