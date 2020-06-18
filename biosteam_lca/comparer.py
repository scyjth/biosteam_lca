# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 12:00:00 2019

@author: cyshi
"""
import numpy as np
from matplotlib import pyplot as plt
from .setup import static_calc


def multi_activity_tester (flows,LCIAmethod, amount=1, plot=False):
    """
    Calculate the impact scores for many processes using one method. 
    **Args:
        *name: is the name of the processes needs to be tested, i
        *flows: is a list include all candidate processes in selected database. 
    """
    print("There are {} processes to test using method{}".format(len(flows),LCIAmethod))
    
    outputsum=[]
    for index, flow_name in enumerate(flows):
        output = static_calc (flow_name, amount, LCIAmethod)
        outputsum.append(output)
        results = (index, flow_name,output) 
    if plot ==True:
        plt.figure(figsize=(15, 10), dpi=80)
        plt.subplot(1, 1, 1)
        index = np.arange(len(flows))
        p1 = plt.bar(index, outputsum, width=0.7, label="Impact score", color = 'yellow')
        plt.xlabel('Process name')
        plt.ylabel('Impact score')
        plt.title('Multi processes using LCIA method:\n {}'.format(LCIAmethod))
        
        # Split description in tick label 
        xlabels = []
        for f in flows:
            label = str(f).replace("' (", '\n(')
            xlabels.append(label)
        plt.xticks(index, (xlabels), rotation=80, fontsize=9)
        plt.yticks(np.arange(0, 5.0, 0.5), fontsize= 6)
        plt.subplots_adjust(bottom=0.45)
        plt.legend(loc="upper right")  
        # For each bar: Place a label
        rects = p1.patches
        def addlabel(rects):
            for r in rects:
                height = r.get_height()
                plt.text(r.get_x()+ r.get_width()/2., 1.01*height, '%.2f'%(height),
                         ha='center', va='bottom')
        addlabel(rects)
        plt.show()
    else: 
        pass
    return results

def multi_method_tester(flow, LCIAmethods, amount=1, plot=False):
    """
    Calculate the impact scores for selected processes with multiple method. LCIAmethods is a list include All candidate LCIA methods that needs to be tested. 
    """
    print("There are {} methods to test for process{}".format(len(LCIAmethods),flow))
    methodsum =[]
    outputsum=[]
    resultsum=[]
    #output_t = np.zeros((1, len(candidate_method)))
    for index, method_name in enumerate(LCIAmethods):                                  
        #lca.decompose_technosphere()               # Keep the LU factorized matrices for faster calculations                                 
        output= static_calc (flow, amount, method_name)
        methodsum.append(method_name)
        outputsum.append(output)
        result = (index, method_name, output)
        resultsum.append(result)
        #print (result)        
    #Plot  method comparison results
    if plot ==True:
        plt.figure(figsize=(10, 10), dpi=80)
        plt.subplot(1, 1, 1)
        index = np.arange(len(LCIAmethods))
        p1 = plt.bar(index, outputsum, width=0.8, label="Impact score")
        plt.xlabel('LCIA method', ha='left')
        plt.ylabel('Impact score')
        plt.title('Multi LCIA Methods for process:\n {}'.format(flow))
        plt.xticks(index, (methodsum), rotation=80, fontsize=9)
        plt.yticks(np.arange(0, 1.6, 0.1))
        plt.subplots_adjust(bottom=0.47)
        plt.legend(loc="upper right")  
        # For each bar: Place a label
        rects = p1.patches
        def addlabel(rects):
            for r in rects:
                height = r.get_height()
                plt.text(r.get_x()+ r.get_width()/2., 1.01*height, '%.2f'%(height),
                         ha='center', va='bottom')
        addlabel(rects)
        plt.show()
    else: 
        pass
    return resultsum



