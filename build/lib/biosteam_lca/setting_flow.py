 # -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 22:51:13 2019

@author: cyshi
"""
from biosteam_lca.inventory_finder import BuiltInInventory
from biosteam_lca.inventory_constructor import LCI
from pint import UnitRegistry
from biosteam_lca.static import method
import pandas as pd
from .monte_carlo import MultiMonteCarlo as MMC
ureg = UnitRegistry()
#weight = 42 * ureg.pound
#x= weight.to(ureg.kg)



"""
Collection of emission factors of materials and energy inputs for biorefinary unit processes. By default, the emission factor is taken from the CABBI inventory profile.
The default emission factor is used by each unit module as the built in emission factor for simpleLCA. 
""" 
#    dir_path = os.path.dirname(os.path.realpath(__file__)) + '\\'
#    inventory = InventoryFinder(dir_path+'CABBI_Inventory_Database.xlsx', sheetname='Sheet1')
    

def steel_ef(location=None):
    "emission factor of steel in BioSTEAM.LCA customized database"
    return BuiltInInventory('Average Steel',location).show()


def electricity_ef(location='US'):
    "emission factor of electricity in BioSTEAM.LCA customized database, varies along different locations selected by user"
    return BuiltInInventory('Electricity',location).show()

def natural_gas_ef(location=None):
    "emission factor of natural gas in BioSTEAM.LCA customized database"
    return BuiltInInventory('Natural Gas as Stationary Fuels',location).show() #an additional factor of 1.25 will be applied for EF of steam. 


def hx_cooling_ef(location=None):
    "emission factor of industrial cooling tower water in BioSTEAM.LCA customized database"
    return BuiltInInventory('HX_cooling',location).show()
    
    #def methanol_GHG(location = None):
    

def steel(p): 
    selected_steel = LCI().flow(p)
    return selected_steel

def electricity(p= '"market for electricity, medium" "US-FRCC"'):
    return LCI().flow(p)[0]
  
def hx_heating (p= '"steam production, as energy carrier, in chemical industry""ROW"'):
    return LCI().flow(p)[0]
   
def hx_cooling(p='"cooling energy" "ROW"'):
    return LCI().flow(p)[0] 

def concrete(concrete_P='concrete production'):
    return LCI().flow(concrete_P)[-1]
    

#def methods_array():
#
#    return ([('CML 2001', 'acidification potential', 'average European'),
#             ('CML 2001', 'climate change', 'GWP 100a')])

methods_array=np.array[ 
        ('TRACI', 'environmental impact', 'acidification'),
        ('TRACI', 'environmental impact', 'ecotoxicity'),
        ('TRACI', 'environmental impact', 'eutrophication'),
        ('TRACI', 'environmental impact', 'global warming'),
        ('TRACI', 'environmental impact', 'ozone depletion'),
        ('TRACI', 'environmental impact', 'photochemical oxidation'),
        ('TRACI', 'human health', 'carcinogenics'),
        ('TRACI', 'human health', 'non-carcinogenics'),
        ('TRACI', 'human health', 'respiratory effects, average')
        ]


def get_MC_lci (ifplot=False):
    """run monte calro analysis for each inventory inputs"""
    _electricity = electricity()
    _hx_heating = hx_heating()
    _hx_cooling = hx_cooling()
    mc_electricity=MMC(_electricity,methods_array).uncertainty(plot=ifplot)
    mc_hx_heating=MMC(_hx_heating,methods_array).uncertainty(plot=ifplot)
    mc_hx_cooling=MMC(_hx_cooling,methods_array).uncertainty(plot=ifplot)
    
    writer = pd.ExcelWriter('monte_carlo_lci.xlsx', engine = 'xlsxwriter')
    pd.DataFrame(mc_electricity).to_excel(writer, sheet_name = 'mc_electricity')
    pd.DataFrame(mc_hx_heating).to_excel(writer, sheet_name = 'mc_hx_cooling')
    pd.DataFrame(mc_hx_cooling).to_excel(writer, sheet_name = 'mc_hx_heating')
    writer.save()
    writer.close()    
#    
CANDIDATES = [
 (u'CML 2001', u'acidification potential', u'average European'),
 (u'CML 2001', u'climate change', u'GWP 100a'),
 (u'CML 2001', u'eutrophication potential', u'average European'),
 (u'CML 2001', u'freshwater aquatic ecotoxicity', u'FAETP 100a'),
 (u'CML 2001', u'human toxicity', u'HTP 100a'),
 (u'CML 2001', u'land use', u'competition'),
 (u'CML 2001', u'marine aquatic ecotoxicity', u'MAETP infinite'),
 (u'CML 2001', u'resources', u'depletion of abiotic resources'),
 (u'CML 2001', u'stratospheric ozone depletion', u'ODP 25a'),
 (u'EDIP2003', u'ecotoxicity', u'in sewage treatment plants'),
 (u'EDIP2003', u'eutrophication', u'terrestrial eutrophication'),
 (u'EDIP2003', u'renewable resources', u'wood'),
 (u'EDIP2003', u'stratospheric ozone depletion', u'ODP total'),
 (u'EPS 2000', u'total', u'abiotic stock resources'),
 (u'EPS 2000', u'total', u'emissions into soil'),
 (u'EPS 2000', u'total', u'emissions into water'),
 (u'EPS 2000', u'total', u'land occupation'),
 (u'IMPACT 2002+ (Endpoint)', u'ecosystem quality', u'land occupation'),
 (u'IMPACT 2002+ (Endpoint)', u'human health', u'ozone layer depletion'),
 (u'IMPACT 2002+ (Endpoint)', u'resources', u'mineral extraction'),
 (u'IMPACT 2002+ (Endpoint)', u'resources', u'non-renewable energy'),
 (u'IMPACT 2002+ (Midpoint)', u'ecosystem quality', u'aquatic acidification'),
 (u'IPCC 2001', u'climate change', u'GWP 100a'),
 (u'ReCiPe Endpoint (H,A)',
  u'ecosystem quality',
  u'agricultural land occupation'),
 (u'ReCiPe Endpoint (H,A)',
  u'ecosystem quality',
  u'freshwater eutrophication'),
 (u'ReCiPe Endpoint (H,A)',
  u'ecosystem quality',
  u'natural land transformation'),
 (u'ReCiPe Endpoint (H,A)',
  u'ecosystem quality',
  u'terrestrial acidification'),
 (u'ReCiPe Endpoint (H,A)', u'ecosystem quality', u'urban land occupation'),
 (u'ReCiPe Endpoint (H,A)', u'human health', u'particulate matter formation'),
 (u'ReCiPe Endpoint (H,A)', u'resources', u'fossil depletion'),
 (u'TRACI', u'environmental impact', u'acidification'),
 (u'TRACI', u'environmental impact', u'eutrophication'),
 (u'TRACI', u'environmental impact', u'global warming'),
 (u'TRACI', u'environmental impact', u'ozone depletion'),
 (u'TRACI', u'human health', u'respiratory effects, average'),
 (u'cumulative energy demand', u'total'),
 (u'cumulative exergy demand',  u'total'),
 (u'eco-indicator 99, (H,A)',
  u'ecosystem quality',
  u'acidification & eutrophication'),
 (u'eco-indicator 99, (H,A)', u'ecosystem quality', u'ecotoxicity'),
 (u'eco-indicator 99, (H,A)', u'ecosystem quality', u'land occupation'),
 (u'eco-indicator 99, (H,A)', u'human health', u'carcinogenics'),
 (u'eco-indicator 99, (H,A)', u'human health', u'climate change'),
 (u'eco-indicator 99, (H,A)', u'human health', u'ozone layer depletion'),
 (u'eco-indicator 99, (H,A)', u'resources', u'fossil fuels'),
 (u'eco-indicator 99, (H,A)', u'resources', u'mineral extraction'),
 (u'ecological footprint', u'total', u'CO2'),
 (u'ecological footprint', u'total', u'land occupation'),
 (u'ecological footprint', u'total', u'nuclear'),
 (u'ecological scarcity 2006', u'total', u'deposited waste'),
 (u'ecological scarcity 2006', u'total', u'emission into groundwater'),
 (u'ecological scarcity 2006', u'total', u'energy resources'),
 (u'ecological scarcity 2006', u'total', u'natural resources'),
 (u'ecosystem damage potential', u'total', u'linear, land occupation'),
 (u'ecosystem damage potential', u'total', u'linear, land transformation'),
]


"""
References

ISO 14044. ISO 14044: Environmental management--Life cycle assessment--Requirements and guidelines. International Organization for Standardization; Switzerland: 2006. 

Edelen, A., Ingwersen, W. W., Rodríguez, C., Alvarenga, R. A., de Almeida, A. R., & Wernet, G. (2018). Critical review of elementary flows in LCA data. The international journal of life cycle assessment, 23(6), 1261-1273.

"""