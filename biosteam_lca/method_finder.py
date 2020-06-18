# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 14:23:21 2019

@author: cyshi
"""
from __future__ import unicode_literals
import os 
from .setup import methods, Database
#from .setup.util import get_activity
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

def get_activity(key):
    try:
        return Database(key[0]).get(key[1])
    except TypeError:
        raise Exception ("Key {} cannot be understood as an activity"
                            " or `(database, code)` tuple.")
#        raise UnknownObject("Key {} cannot be understood as an activity"
#                            " or `(database, code)` tuple.")

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
#        asmethod=[]
#        for method in filter(lambda x: search_string in x[0], methods):
#            asmethod.append(method)

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
    
    _metadata = methods
#    validator_ia
#    numpy_string = lambda x: bytes(x) if sys.version_info < (3, 0) else x
#    dtype_fields = [(numpy_string('flow'), np.uint32),
#                    (numpy_string('geo'), np.uint32),
#                    (numpy_string('row'), np.uint32),
#                    (numpy_string('col'), np.uint32),]

    def __init__(self, name):
        self.name = name

    def _write(self, data, process=True):
        """From bw2; Serialize intermediate data to disk. Sets the metadata key ``num_cfs`` automatically."""
        self.metadata[u"num_cfs"] = len(data)
        self._metadata.flush()
        super(Method, self).write(data)
        
    def characterization_factor(self):
        """A method to find characterization factors of a lcia method"""
        CFs=[]
        for key, cf in super(Method, self).load():
            try:
                activity= Database(key[0]).get(key[1])
            except TypeError as err:
                print (err)
            CFs.append((activity, cf))
        return CFs
            
    def description(self):
        """get brieft description of the impact assessment method"""
        return self.metadata.get('description')
    
    def unit(self):
        """get unit of the impact assessment score"""
        return self.metadata.get('unit')

#    def get_abbreviation(self):
#        """Retrieve the abbreviation of the method identifier."""
#        self.register()
#        return self.metadata["abbreviation"]
        
    def __str__(self):
        return "Impact assessment %s: %s in BioSteam.LCA" % (self.__class__.__name__, self.name)             
      
Methods = MethodsConstructor

#CANDIDATES = [
# (u'CML 2001', u'acidification potential', u'average European'),
# (u'CML 2001', u'climate change', u'GWP 100a'),
# (u'CML 2001', u'eutrophication potential', u'average European'),
# (u'CML 2001', u'freshwater aquatic ecotoxicity', u'FAETP 100a'),
# (u'CML 2001', u'human toxicity', u'HTP 100a'),
# (u'CML 2001', u'land use', u'competition'),
# (u'CML 2001', u'marine aquatic ecotoxicity', u'MAETP infinite'),
# (u'CML 2001', u'resources', u'depletion of abiotic resources'),
# (u'CML 2001', u'stratospheric ozone depletion', u'ODP 25a'),
# (u'EDIP2003', u'ecotoxicity', u'in sewage treatment plants'),
# (u'EDIP2003', u'eutrophication', u'terrestrial eutrophication'),
# (u'EDIP2003', u'renewable resources', u'wood'),
# (u'EDIP2003', u'stratospheric ozone depletion', u'ODP total'),
# (u'EPS 2000', u'total', u'abiotic stock resources'),
# (u'EPS 2000', u'total', u'emissions into soil'),
# (u'EPS 2000', u'total', u'emissions into water'),
# (u'EPS 2000', u'total', u'land occupation'),
# (u'IMPACT 2002+ (Endpoint)', u'ecosystem quality', u'land occupation'),
# (u'IMPACT 2002+ (Endpoint)', u'human health', u'ozone layer depletion'),
# (u'IMPACT 2002+ (Endpoint)', u'resources', u'mineral extraction'),
# (u'IMPACT 2002+ (Endpoint)', u'resources', u'non-renewable energy'),
# (u'IMPACT 2002+ (Midpoint)', u'ecosystem quality', u'aquatic acidification'),
# (u'IPCC 2001', u'climate change', u'GWP 100a'),
# (u'ReCiPe Endpoint (H,A)',
#  u'ecosystem quality',
#  u'agricultural land occupation'),
# (u'ReCiPe Endpoint (H,A)',
#  u'ecosystem quality',
#  u'freshwater eutrophication'),
# (u'ReCiPe Endpoint (H,A)',
#  u'ecosystem quality',
#  u'natural land transformation'),
# (u'ReCiPe Endpoint (H,A)',
#  u'ecosystem quality',
#  u'terrestrial acidification'),
# (u'ReCiPe Endpoint (H,A)', u'ecosystem quality', u'urban land occupation'),
# (u'ReCiPe Endpoint (H,A)', u'human health', u'particulate matter formation'),
# (u'ReCiPe Endpoint (H,A)', u'resources', u'fossil depletion'),
# (u'TRACI', u'environmental impact', u'acidification'),
# (u'TRACI', u'environmental impact', u'eutrophication'),
# (u'TRACI', u'environmental impact', u'global warming'),
# (u'TRACI', u'environmental impact', u'ozone depletion'),
# (u'TRACI', u'human health', u'respiratory effects, average'),
# (u'cumulative energy demand', u'total'),
# (u'cumulative exergy demand',  u'total'),
# (u'eco-indicator 99, (H,A)',
#  u'ecosystem quality',
#  u'acidification & eutrophication'),
# (u'eco-indicator 99, (H,A)', u'ecosystem quality', u'ecotoxicity'),
# (u'eco-indicator 99, (H,A)', u'ecosystem quality', u'land occupation'),
# (u'eco-indicator 99, (H,A)', u'human health', u'carcinogenics'),
# (u'eco-indicator 99, (H,A)', u'human health', u'climate change'),
# (u'eco-indicator 99, (H,A)', u'human health', u'ozone layer depletion'),
# (u'eco-indicator 99, (H,A)', u'resources', u'fossil fuels'),
# (u'eco-indicator 99, (H,A)', u'resources', u'mineral extraction'),
# (u'ecological footprint', u'total', u'CO2'),
# (u'ecological footprint', u'total', u'land occupation'),
# (u'ecological footprint', u'total', u'nuclear'),
# (u'ecological scarcity 2006', u'total', u'deposited waste'),
# (u'ecological scarcity 2006', u'total', u'emission into groundwater'),
# (u'ecological scarcity 2006', u'total', u'energy resources'),
# (u'ecological scarcity 2006', u'total', u'natural resources'),
# (u'ecosystem damage potential', u'total', u'linear, land occupation'),
# (u'ecosystem damage potential', u'total', u'linear, land transformation'),
#]

