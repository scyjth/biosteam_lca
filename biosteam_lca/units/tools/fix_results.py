# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 20:42:58 2019

@author: cyshi
"""
from biosteam import Unit
results = Unit.results
def results_wt_LCA(self):
    try:
        self.baseLCA()
    except:
        pass
    return results(self)


Unit.results = results_wt_LCA
