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
    A means of conducting life cycle assessment calculations with multiple inventory 
    inputs profiles, life cycle impact assessment methods, and variable amounts 
    inherited from each unit. Pre-selection of database is required, if not specify, 
    default database would be chosen. 
   
    Attributes
    ----------

    inventory_inputs: dict 

        Inventory profile and amount for process inputs. 

    Note
    -----
    
    Call `.run ()` to generate results. Results return a numpy array with multiple 
    impact results, calculate up to 800+ impact categories for each unit simultaneously. 
    Call``.timer ()`` to see simulation time.

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
        """A @classmethod to set user defined impact assessment method(s).

        Parameters
        ----------

        set_methods : 

            The methods to be set to `ia_methods`.

        Returns
        -------

        cls.ia_methods : dict

            The newly set `ia_methods`. 
        """
        cls.ia_methods = set_methods
        return cls.ia_methods
    
    def scores(self, timer=False, table=False, method=None):
        """A method to run multi impact LCA calculation by taking inputs, methods and 
        amounts of each input. 

        Parameters
        ----------

        timer : boolean, optional

            Set to `True` to print() time taken to process. Default is `False`. 

        table : boolean, optional

            Set to `True` to print tabulated results.

        method : tuple, optional

            LCIA Method; e.g. `('TRACI', 'human health', 'carcinogenics')`

        Returns
        -------

        results_dic : dict

            A dict containing numpy arrays with multiple impact results.

        Note
        ----

        User can choose one or more impact categories. If 
        not specified, `IPCC glowbal warming potencial` is the default method.
        """
        lcia_methods = self.ia_methods
        if not isinstance(lcia_methods , list):
            raise ("method must be a valid method lists")
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
#         return (output, lcia_methods)
# #        #return multi_score
        # for row, flow in enumerate(flows):
        #     for col, method in enumerate(lcia_methods):
        #         self.results = np.zeros((len(flows), len(lcia_methods)))
        #         self.results[row, col] = results_dic [method]
        
        return results_dic
     
    def multi_process_calc(self, activities, single_impact):
        """A method to calculate the impact score of multiple process using selected 
        lcia method. 

        Parameters
        ----------

        activities : list

            The activities to apply.

        single_impact :

            The single impact to consider.
        
        Returns
        -------
        multi_process_calc_result : tuple

            A tuple containing a numpy array of impact scores for each input. 
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
        multi_process_calc_result = (single_impact, output)
        return multi_process_calc_result
    
    def multi_process(self, single_impact):
        """A method to calculate the impact score of multiple process using selected 
        lcia method. 

        Parameters
        ----------

        simgle_impact :

            The single impact to consider.

        Returns
        ------- 
        
        multi_process_result : tuple

            A tuple containing numpy array of impact scores for each input. 

        Raises
        ------

        ValueError

            If flow is not a dict.

        ValueError

            If flow dict is empty.
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
        multi_process_result = (single_impact, output)
        return multi_process_result
    
    @staticmethod
    def multi_impact (flow, amount, methods, factorize=False,table=False):
        """A method to calculate the life cycle impact assessment results for selected 
        processes and multiple methods. 
        
        Parameters
        ----------

        flow : dict

            The flow to apply.

        amount :

            

        methods :

            The methods to apply.

        factorize : bool, optional

            Factorize results. Default is `False`.

        table : bool, optional

            Return results in tabular form. Default is `False`.

        Returns
        -------
        
        multi_impact_result : tuple

            The flow, and its associated scoresum.

        Notes
        -----

        LCIAmethods is an inclusive list of all candidate LCIA methods that need to be tested. 
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
            multi_impact_result = (flow,scoresum)
            return multi_impact_result
            
    def timer (self):
        """A method to record the time of running analysis

        Returns
        -------

        end_time : float

            The difference between the start time and the end time of the process 
            as expressed in seconds.
        """
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
    """A method to export inventory input matrix to excel.

    Parameters
    ----------

    row_names : list

        A list of the row names to write to the Excel sheet.

    col_names : list

        The column names to write to the Excel sheet.

    matrix :

        The matrix from which to write.

    filepath : str, optional

        The name of the file to write to. Default value is `export.xlsx`.

    sheetname : str, optional

        The name of the Excel sheet. Default value is `Export`.
    """
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