 # -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 22:51:13 2019

@author: cyshi
"""
import inspect
from biosteam_lca.activity_builder import ActivityBuilder as AB
from pint import UnitRegistry
import pandas as pd
import numpy as np
from biosteam_lca.multilca import MultiLCA
from biosteam_lca.ef_finder import BuitInEF
from biosteam_lca.monte_carlo import MultiMonteCarlo as MMC
ureg = UnitRegistry()


#"""
#weight = 42 * ureg.pound
#x= weight.to(ureg.kg)
#Collection of emission factors of materials and energy inputs for biorefinary unit processes. By default, the emission factor is taken from the CABBI inventory profile.
#The default emission factor is used by each unit module as the built in emission factor for simpleLCA. 
#""" 
#    dir_path = os.path.dirname(os.path.realpath(__file__)) + '\\'
#    inventory = EmisssionFactorFinder(dir_path+'CABBI_Inventory_Database.xlsx', sheetname='Sheet1')

# def steel_ef(location=None):
#     "emission factor of steel in BioSTEAM.LCA customized database"
#     return BuitInEF('Average Steel',location).show()


# def electricity_ef(location='US'):
#     "emission factor of electricity in BioSTEAM.LCA customized database, varies along different locations selected by user"
#     return BuitInEF('Electricity',location).show()

# def natural_gas_ef(location=None):
#     "emission factor of natural gas in BioSTEAM.LCA customized database"
#     return BuitInEF('Natural Gas as Stationary Fuels',location).show() #an additional factor of 1.25 will be applied for EF of steam. 

# def hx_cooling_ef(location=None):
#     "emission factor of industrial cooling tower water in BioSTEAM.LCA customized database"
#     return BuitInEF('HX_cooling',location).show()
    

keys_lst = ['comment',
             'classifications',
             'activity type',
             'activity',
             'database',
             'filename',
             'location',
             'name',
             'parameters',
             'authors',
             'type',
             'reference product',
             'flow',
             'unit',
             'production amount',
             'code']

class InventoryConstructor:
    """ Set inventory flows for unit process inputs at biorefinery if not otherwise provided by the default inventory process flow
            
   **References**
  
        [1] ISO 14044. ISO 14044: Environmental management--Life cycle assessment--Requirements and guidelines. International Organization for Standardization; Switzerland: 2006. 
        
        [2] Edelen, A., Ingwersen, W. W., Rodríguez, C., Alvarenga, R. A., de Almeida, A. R., & Wernet, G. (2018). Critical review of elementary flows in LCA data. The international journal of life cycle assessment, 23(6), 1261-1273.
        
    """
    
    def __init__(self, system_name=None):
        self.system_name=system_name
        assert system_name in {None, 'sugarcane_sys', 
                               'cornstover_sys',
                               'lipidcane_sys'}, "define the system first"

        
    @property
    def electricity(self):
        return AB('"market for electricity, medium" "US-FRCC"').flow
    @property  
    def hx_heating (self):
        return AB('"steam production, as energy carrier, in chemical industry""ROW"').flow
    @property  
    def hx_cooling (self):
        return AB('"cooling energy" "ROW"').flow
    @property
    def sulfuric_acid (self):
        return AB('"Sulfuric acid production" "Row"').flow
    @property
    def phosphoric_acid (self):
        return AB('"Phosphoric acid production" "RoW"').flow
    @property
    def ammonia (self):
        return AB('"ammonia production, steam reforming, liquid" "Row"').flow           
    @property
    def DAP(self):
        return AB('"diammonium phosphate production" "Row"').flow       
    @property
    def lime(self):
        return AB('"lime production, milled, packed" "Row"').flow   
    @property
    def yeast(self):
        return AB('"enzyme production" "Row"').flow   
    @property
    def concrete(self):
          return AB('"concrete production, for civil engineering, with cement CEM I" "RoW"').flow
    @property
    def fresh_water(self):
        return AB('"tap water production, underground water without treatment""RoW"').flow
#
    def lci_name_lst(self):
        """Obtain a list of all inventory flow names built in the class"""
        pronames = [p for p in dir(InventoryConstructor) if isinstance(getattr(InventoryConstructor,p),property)]
        return pronames
    
    @classmethod
    def lci_lst(self):
        def isprop(v):
            return isinstance(v, property)
        #use inspect module allows getting all properties also from inherited class.
        propnames = [name for (name, value) in inspect.getmembers(InventoryConstructor, isprop)]
        self.lcis = [getattr(InventoryConstructor(), x) for x in propnames]
        return self.lcis    
        
    def add_lci(self, unit_process):

        if unit_process not in self.lcis:
            self.lcis.append (unit_process)
            
    def remov_lci(self, unit_process):
        if unit_process in self.lcis:
            self.lcis.remove (unit_process)
            
    def print_lcis(self):
        for lci in self.lcis:
            print ('-->', lci.get('parameters'))
    
    def impact(self):
        self.inv=sorted(self.lcis)  # Sort to make sure order is always the same
        self.inputs_name=sorted (self.lci_name_lst()) # Sort to make sure order is always the same
        # activity_str = list(map(lambda x: (x.get('name') + ' (' 
        #                            + x.get('unit') +', ' 
        #                            + x.get('location') + ') '), self.inv))
        unit_inv = dict((act,1) for act in self.inv)
        objs=MultiLCA(unit_inv)
        methods =objs.ia_methods
        output = np.zeros((len(self.inv),len(methods)))
        results = objs.scores()
        for index, method in enumerate(methods):
            output[:, index] = results[method]
        # unclassified= [sum(results[i]) for i in results.keys()]
        # unclassified_sum=dict(zip(results.keys(),unclassified))
        score_dict_by_impact={}
        for i in output:
            for j in self.inputs_name:
                x=dict(zip(methods,i))
                score_dict_by_impact[str(j)] = x
        #df=pd.DataFrame(data=score_dict_by_impact.items())
        return score_dict_by_impact

# class InventoryConstructor(BuitInInventory):
#
#     def __init__(self, unit_processes = None):
#         if unit_processes  is None:
#             while True:
#                 self.lcis = self.lci_lst()
#         else:
#             self.lcis = unit_processes 

#     def add_lci(self, unit_process):
#         if unit_process not in self.lcis:
#             self.lcis.append (unit_process)
            
#     def remov_lci(self, unit_process):
#         if unit_process in self.lcis:
#             self.lcis.remove (unit_process)
            
#     def print_lcis(self):
#         for lci in self.lcis:
#             print ('-->', lci.get('parameters'))
    

class MMC_InventoryConstructor(InventoryConstructor):
    #lcia_method = np.array[
    #        ('TRACI', 'environmental impact', 'acidification'),
    #        ('TRACI', 'environmental impact', 'ecotoxicity'),
    #        ('TRACI', 'environmental impact', 'eutrophication'),
    #        ('TRACI', 'environmental impact', 'global warming'),
    #        ('TRACI', 'environmental impact', 'ozone depletion'),
    #        ('TRACI', 'environmental impact', 'photochemical oxidation'),
    #        ('TRACI', 'human health', 'carcinogenics'),
    #        ('TRACI', 'human health', 'non-carcinogenics'),
    #        ('TRACI', 'human health', 'respiratory effects, average')]

    lcia_method = [('TRACI', 'environmental impact', 'global warming')]
#    def lci_lst(self):
#        def isprop(v):
#            return isinstance(v, property)
#        #use inspect module allows getting all properties also from inherited class.
#        propnames = [name for (name, value) in inspect.getmembers(InventoryConstructor, isprop)]
#        get_lci_lst = [getattr(InventoryConstructor(), x) for x in propnames]
#        return get_lci_lst
    
    @classmethod
    def set_lcia_method(cls, ia_method):
        cls.lcia_method = ia_method  
    
    def parameterize(self,ifplot=False):
        """run monte carlo analysis for all unit process inputs set in the InventoryConstructer class"""
        self.lcis = self.lci_lst()
        MMC_lcis = [MMC(lci, self.lcia_method).uncertainty(plot=ifplot) for lci in self.lcis] 
        lcis_as_list=[str(lci) for lci in self.lcis]
        self.as_dict = dict(zip(lcis_as_list, MMC_lcis))
        # df = pd.DataFrame(data=self.as_dict.items())
        return self.as_dict
    
    def export_MMC_lci(self):
        """export montecarlo results for inventories to excel"""  
        writer = pd.ExcelWriter('monte_carlo_lci.xlsx', engine = 'xlsxwriter')
        for lci in self.lcis:
            pd.DataFrame(lci).to_excel(writer, sheet_name = str(lci))
        # pd.DataFrame(mc_hx_heating).to_excel(writer, sheet_name = 'mc_hx_cooling')
        # pd.DataFrame(mc_hx_cooling).to_excel(writer, sheet_name = 'mc_hx_heating')
        writer.save()
        writer.close()    

