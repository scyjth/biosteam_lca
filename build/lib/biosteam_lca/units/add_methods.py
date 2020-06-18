# -*- coding: utf-8 -*-
"""
Created on Thu May  7 16:29:24 2020

@author: cyshi
"""

from functools import wraps # This func preserves name and docstring

def add_method(cls):
    def decorator(func):
        @wraps(func) 
        def wrapper(self, *args, **kwargs): 
            return func(self,*args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        return func # returning func means func can still be used normally
    return decorator