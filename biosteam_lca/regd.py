# -*- coding: utf-8 -*-
"""
Created on Thu Mar 7 16:12:21 2019

@author: cyshi
"""

import pint
import os
from decimal import Decimal

ureg = pint.UnitRegistry()

#Register new units of inventory inputs
dir_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'setup')
file_name='units_registration.txt'
unit_path=os.path.join(dir_path,file_name)
ureg.load_definitions(unit_path)

Q_ = ureg.Quantity
