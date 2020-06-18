# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 15:36:43 2019

@author: cyshi
"""
import sys
from scipy import stats
from multiprocessing import Pool, cpu_count
import time
import brightway2 as bw2
import numpy as np
from tabulate import tabulate
from xlsxwriter import Workbook
import multiprocessing
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping
import warnings
#import pandas as pd

def static_calc (flow, amount, methods, factorize=False):
    """Establish static lca basis. By default no factorization."""
    if not isinstance(flow, Mapping):
            raise ValueError("Flow must be a dictionary")
    for key in flow:
        if not key:
            raise ValueError("Invalid dictionary")
    lca = bw2.LCA({flow: amount}, method=methods) 
    lca.lci()
    if factorize:
        lca.decompose_technosphere()
    lca.lcia()                                   
    return lca.score  

class MultiLCA:
    """
    Conducting life cycle assessment calculations with multiple inventory inputs profiles, life cycle impact assessment methods, 
    and variable amounts inherited from each unit. Pre-selection of database is required, if not specify, default database would be chosen. 
   
    ***Initilization parameter:
        **inventory_inputs:** [dict] Create a dictionary with selected inventory profile and amount for process inputs. 
    
    Call ``.run ()`` to generate results. Results return a numpy array with multiple impact results, calculate up to 800+ 
    impact categories for each unit simultaneously. Call``.timer ()`` to see simulation time.

    """
    ia_methods =[
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
    
    def __init__(self, inventory_inputs):
        self.inventory_inputs = inventory_inputs
    
    @classmethod
    def set_ia_methods(cls, set_methods):
        """set user defined impact assessment method/methods"""
        try:
            assert isinstance(set_methods, list)
        except:
            raise ("method must be a valid method lists")
        cls.ia_methods = set_methods
        return cls.ia_methods
    
    def scores(self, timer=False, table = False):
        
        """
        Run multi impact LCA calculation by taking inputs, methods and amounts of each input. 
        User can choose one impact category or multiple. If doesn't specify, IPCC glowbal warming potencial would be the default method.
        
        **Kwargs:
            * *method* (tuple, optional): LCIA Method tuple, e.g. ``('TRACI', 'human health', 'carcinogenics')``.

        **Returns:
            numpy array with multiple impact results.
        """
        lcia_methods = self.ia_methods
        start_time = time.clock()
        inventory_inputs = self.inventory_inputs
        flows = list(self.inventory_inputs.keys())
        num_flow = len(inventory_inputs.keys())
        num_methods= len(lcia_methods)
        output = np.zeros((num_flow,num_methods)) # to store calculated results
        assert len(lcia_methods) != 0, "Please select at least one valid life cycle impact assessment method"
        if isinstance (lcia_methods, tuple):
            # if there is only one lcia method, the method is shown as a tuple. For example, ('TRACI', 'environmental impact', 'acidification')
            multi_score = self.multi_process(inventory_inputs)#,lcia_methods)
            multi_score = dict([multi_score])
            output = multi_score[lcia_methods]
        else:
            if (num_flow) * (num_methods) > 10:
                print ('using multi pool')
            # When the iteration is large, use The multiprocessing pool for paralle processing. 
            # For small numbers of LCA iterations, a for-loop is faster. 
                try:
                    pool = Pool(processes=multiprocessing.cpu_count())
                    jobs = [pool.apply_async(
                        self.multi_process_calc,                 # Function
                        (flows,method)) for method in lcia_methods]
                    pool.close()
                    pool.join()
                    multi_score = dict([job.get() for job in jobs])
                except OSError:
                        sys.exit()
            else:   
                multi_score = []
                lcia_methods = sorted(lcia_methods) # Sort to make sure order is always the same
                for i in lcia_methods:
                    multi_score.append(self.multi_process(i))  
            for index, method in enumerate(lcia_methods):
                try:
                    results_dic = dict(multi_score)
                    output[:, index] = results_dic[method]
                except:
                    warnings.warn("Please revisit your lca calculation")
        if timer ==True:
            print ('MultiLCA done in {:.2f} seconds.'.format(time.clock()-start_time))
        headers = ['Impact Category', 'Impact Score']
        if table == True:
            print (tabulate(multi_score, headers=headers, tablefmt='grid'))   
        return (output, lcia_methods)
#        #return multi_score
#        return results_dic
     
    def multi_process_calc(self, activities, single_impact):
        """ 
        Calculate the impact score of multiple process using selected lcia method. Returns a numpy array of impact scores for each input. 
        """
        amounts = list(self.inventory_inputs.values())
        output = np.zeros((len(activities),))                              # Load method data
        for index, (flow, amount) in enumerate(zip(activities, amounts)):
            if not isinstance(flow, Mapping):
                raise ValueError("Flow must be a dictionary")
            for key in flow:
                if not key:
                    raise ValueError("Invalid dictionary")
            score = static_calc (flow, amount, single_impact)
            output[index] = score
        return (single_impact, output)  
    
    def multi_process(self, single_impact):
        """ 
        Calculate the impact score of multiple process using selected lcia method. Returns a numpy array of impact scores for each input. 
        """
        flows = list(self.inventory_inputs.keys())
        amounts = list(self.inventory_inputs.values())
        output = np.zeros((len(flows),))                              # Load method data
        for index, (flow, amount) in enumerate(zip(flows, amounts)):
            if not isinstance(flow, Mapping):
                raise ValueError("Flow must be a dictionary")
            for key in flow:
                if not key:
                    raise ValueError("Invalid dictionary")
            score = static_calc (flow, amount, single_impact)
            output[index] = score
        return (single_impact, output)  
    
    @staticmethod
    def multi_impact (flow, amount, methods, factorize=False,table = False):
        """
        Calculate the life cycle impact assessment results for selected processes and multiple method. Returns multiple LCA scores. 
        LCIAmethods is a list include All candidate LCIA methods that needs to be tested. 
        """
        methodsum =[]
        scoresum = []
        output = np.zeros(len(methods))
        for index, method in enumerate(methods):
            output[index]= static_calc (flow,amount,method,factorize)
            methodsum.append(method)
            scoresum.append((index, method, output[index]))
        headers = ['No.', 'Category', 'Impact Score']
        if table == True:
            print (tabulate(scoresum, headers=headers, tablefmt='grid'))            
        else:
            return (flow,scoresum)
            
    def timer (self):
        """Record the time of running analysis"""
        start_time = time.time()
        self.multi_calc(self.lcia_methods)
        end_time = time.time() - start_time
        return end_time

#def work_log(work_data):
#    print(" Process %s waiting %s seconds" % (work_data[0], work_data[1]))
#    time.sleep(int(work_data[1]))
#    print(" Process %s Finished." % work_data[0])

#{'cooling energy, from natural gas, at cogen unit with absorption chiller 100kW' (megajoule, RoW, None): 10531.536537658454,
# 'steam production, as energy carrier, in chemical industry' (megajoule, RoW, None): 0.0,
# 'market for electricity, medium voltage' (kilowatt hour, US-FRCC, None): 11.609127275005434}

def export_matrix_to_excel(row_names, col_names, matrix, filepath='export.xlsx', sheetname='Export'):
    """Export inventory input matrix to excel"""
    workbook = Workbook(filepath)
    ws = workbook.add_worksheet(sheetname)
    # formatting border
    format_border = workbook.add_format()
    format_border.set_border(1)
    format_border.set_font_size(9)
    # border + text wrap
    format_border_text_wrap = workbook.add_format()
    format_border_text_wrap.set_text_wrap()
    format_border_text_wrap.set_border(1)
    format_border_text_wrap.set_font_size(9)
    # set column width
    ws.set_column(0, 1, width=15, cell_format=None)
    ws.set_column(1, 50, width=9, cell_format=None)
    # write data
    for i, p in enumerate(col_names):  # process names
        ws.write(0, i+1, p, format_border_text_wrap)
    for i, p in enumerate(row_names):  # product names
        ws.write(i+1, 0, p, format_border)
    for i, row in enumerate(range(matrix.shape[0])):  # matrix
        ws.write_row(i+1, 1, matrix[i, :], format_border)
    workbook.close()
    
#def calculate_lcas(selected_methods, selected_activities):
#    tic = time.clock()
#    if not selected_methods:
#        raise ValueError ('Please add at least one valid method first.')
#    elif not selected_activities:
#        raise ValueError ('Please add at least one activity flow first.')
#    else:
#        lca_scores, methods, activities = \
#            self.lcaData.multi_lca(self.selected_activities, self.selected_methods)
#        self.results.update({
#            'lca_scores': lca_scores,
#            'methods': methods,
#            'activities': activities,
#        })
#        print (activities)
#        print (methods)
#        print (lca_scores)
#        self.signal_status_bar_message.emit('Done in {:.2f} seconds.'.format(time.clock()-tic))