# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 14:23:21 2019

@author: cyshi
"""
from __future__ import unicode_literals
import os 
from .setup import methods, Database
from .setup.util import get_activity
import operator
import sys
from tabulate import tabulate
from bw2data.ia_data_store import ImpactAssessmentDataStore

PY3 = sys.version_info > (3,)
if PY3:
    dt = ";"
else:
    dt = b";"

dirpath = os.path.dirname(__file__)

class MethodsConstructor():
    """Search and analyze impact assessment methods.
    **Initialization parameters**
            * *methods_name*: List of candidate impact assessment methods
    """    
    
    def __init__(self, methods_name = None):
        self.methods_namee = methods_name

    def search (self, exclude = None, length =None):
        """   
         A method to lookup life cycle impact assessment method (LCIA) by method name or impact category, such as:'IPCC 2007', or 'ReCiPe Endpoint (H,A)'
         By tradition, LCIA method is understood as a set of LCIA impact catergories, it need to be selected before caulcating LCA results for product, system, or projectis.
         Returns all methods for which the search string is part of. If no mthod is specified, will return US EPA TRACI.
         Certain methods will be exclude if exclude string is specified.  
         If length is specified, results are reduced to those that have a length of x, i.e. x parts in the method tuple.
        """
        search_string = self.methods_namee
        self.asmethod = []
        if search_string == None:
            self.asmethod = [
                ('TRACI', 'environmental impact', 'acidification'),
                 ('TRACI', 'environmental impact', 'ecotoxicity'),
                 ('TRACI', 'environmental impact', 'eutrophication'),
                 ('TRACI', 'environmental impact', 'global warming'),
                 ('TRACI', 'environmental impact', 'ozone depletion'),
                 ('TRACI', 'environmental impact', 'photochemical oxidation'),
                 ('TRACI', 'human health', 'carcinogenics'),
                 ('TRACI', 'human health', 'non-carcinogenics'),
                 ('TRACI', 'human health', 'respiratory effects, average')]        
        elif search_string == 'all':
            self.asmethod = list(methods)
        else:
            #asmethod = [method for method in methods if search_string in method[0] ]
            for method in methods:
                for name in method:
                    if search_string.lower() in name.lower() :
                        self.asmethod.append(method)
        if exclude:
           self.asmethod = [op for op in self.asmethod if exclude not in [sth for sth in op]]
        if length:
            self.asmethod = [op for op in self.asmethod if len(op) == length]
        if not self.asmethod:
            raise ValueError("No methods matches your searching criteria. Please select a valide life cycle impact assessment method")   
        return self.asmethod

#o3_method = [m for m in methods if 'ILCD' in str(m)
#                                and 'human health' in str(m)
#                                and 'ozone layer depletion' in str(m)
#                                and 'no LT' in str(m)][0]
        
    def categories(self,asmethods=None):
        """ summarize impact assessment categories"""
        asmethods = self.asmethods
        if asmethods == None:
            asmethods = methods
        ct_dict={}
        am=[method[1] for method in asmethods]
        for i in am:
            am.count(i)
            ct_dict[i]=am.count(i)
        sorted_ct = sorted(ct_dict.items(), key=operator.itemgetter(1))
        return sorted_ct
    

    def tools(self): 
        """summerize total approaches. 
        Note that Eco-Indicator 99, EPS Method, LIME, and Impact 2002+ include potential impacts from future extractions in the impact assessment, \
        whereas Recipe assumes assumes impacts have been included in the inventory analysis.
        ReCipe method includes eighteen midpoint indicators and three endpoint indicators
        
        **Args**
            * *asmethods* (list): List of candidate impact assessment methods
        """
        t_methods = self.search()
        tm=[method[0] for method in t_methods]
        tools_lst = list(dict.fromkeys(tm))
        return tools_lst, ("Number of methods: {}".format(len(tools_lst)))
    
    def negtive_cf(self):

        """Looks throught all flows that has impact to the selected LCIA methods find the negative values of Chracterization Fators of ia method, negative values represents the process is benificial to the environment under the current impact categories,
        which implied that they are good for the environment
        **Kwargs**    
            **method_name** : [str] name of the method tool, for exmaple-- ('ReCiPe Midpoint (I) V1.13')
        **return
            A dictionary of negtive CFs of selected method. For exmaple-- 
            ('ReCiPe Midpoint (I) V1.13','photochemical oxidant formation','POFP'):\ 
                [('Benzaldehyde' (kilogram, None, ('air',)),-0.155),
                ('Benzaldehyde' (kilogram, None, ('air', 'urban air close to ground')), -0.155)]
        """
        negtive_cf_dict={}
        if self.asmethods is not None:
            method_lst= list(filter(lambda x: x[0] == self.asmethods, methods))
        else:
            method_lst=methods
        for method in method_lst:
            CFs ={}
            #CFs=[]
            for key, cfs in Method(method).load():
                if cfs < 0:
#                    CFs.append((get_activity(key), cfs))
                    CFs[(Database('biosphere3').get(key[1]))] = cfs
            if CFs:
                negtive_cf_dict[method]= CFs
#        workbook = openpyxl.Workbook()
#        sheet = workbook.active
#        row = 1
#        for key,values in negtive_cf_dict.items():
#            sheet.cell(row=row, column=1, value=str(key))
#            column = 2
#            for element in values:
#                sheet.cell(row=row, column=column, value=str(element))
#                column += 1
#                row += 1
#        workbook.save(filename="ncf2.xlsx")
        return negtive_cf_dict
        
    def random(self):
        return methods.random()

    def __str__(self):
        return "%s" % (self.__class__.__name__) 
           
class Method (ImpactAssessmentDataStore):

    def __init__(self, method_name):
        self.method_namee = method_name
        
    def characterization_factor(self, table=True):
        """Quick overview of characterization factors of a certain lcia method"""
        CFs=[]
        for key, cf in super(Method, self).load():
            try:
                activity= get_activity(key)
            except TypeError as err:
                print (err)
            CFs.append((activity, cf))
        headers = ['Substance', 'Characterization Factor']
        if table == True:
            print (tabulate(CFs, headers=headers, tablefmt='grid'))   
        return CFs
    
    def get_abbreviation(self):
        """Retrieve the abbreviation of the method identifier."""
        self.register()
        return self.metadata["abbreviation"]
            
    def description(self):
        return self.metadata.get('description')
    
    def unit(self):
        return self.metadata.get('unit')
        
    def __str__(self):
        return "Impact Assessment %s: %s in BioSteam.LCA" % (self.__class__.__name__, self.name)            
      
Methods = MethodsConstructor