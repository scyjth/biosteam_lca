# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 15:36:43 2019

@author: cyshi
"""
import pandas
from os import path, makedirs
from stats_arrays import *
from stats_arrays import NormalUncertainty
import csv

#%%
#df = pandas.read_excel(r'C:\Users\cyshi\Documents\LCA Documents\ecoinvent 3.1-3.2.xlsx')
import os

FOLDER_PATH=os.getcwd()
def listDir(dir):
    fileNames=os.listdir(dir)
    for fileName in fileNames:
        print('File Name:' + fileName)
        print('Folder Path:' +os.path.abspath(os.path.join(dir,fileName)),sep ='\n')

if __name__ == '__main__':
    listDir(FOLDER_PATH)
    

def calculate_lcas(selected_methods, selected_activities):
    tic = time.clock()
    if not selected_methods:
        raise ValueError ('Please add at least one valid method first.')
    elif not selected_activities:
        raise ValueError ('Please add at least one activity flow first.')
    else:
        lca_scores, methods, activities = \
            self.lcaData.multi_lca(self.selected_activities, self.selected_methods)
        self.results.update({
            'lca_scores': lca_scores,
            'methods': methods,
            'activities': activities,
        })
        print (activities)
        print (methods)
        print (lca_scores)
        self.signal_status_bar_message.emit('Done in {:.2f} seconds.'.format(time.clock()-tic))

#    def save_results(self):
#        activity_names = [' // '.join(filter(None, [self.lcaData.getActivityData(key)['product'],
#                                                    self.lcaData.getActivityData(key)['name'],
#                                                    self.lcaData.getActivityData(key)['location']]))
#                          for key in self.results['activities']]
#        methods = [', '.join(method) for method in self.results['methods']]  # excelwrite does not support tuples
#        matrix_lca_scores = self.results['lca_scores']
#        file_types = "Excel (*.xlsx);;"
#        filepath = str(QtGui.QFileDialog.getSaveFileName(self, 'Save File', self.PATH_MULTI_LCA, file_types))
#        if filepath:
#            try:
#                export_matrix_to_excel(activity_names, methods, matrix_lca_scores, filepath, sheetname='Multi-LCA-Results')
#                self.signal_status_bar_message.emit('Multi-LCA Results saved to: '+filepath)
#            except IOError:
#                self.signal_status_bar_message.emit('Could not save to file.')