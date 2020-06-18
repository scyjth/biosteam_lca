# -*- coding: utf-8 -*-
"""
Created on Fri May 10 14:17:14 2019

@author: cyshi
"""

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def calc_correlation (LCA_scores, coefficient = 'Kendall'):
    """ A method to calculate correlations of the calculated LCA scores using multiple impact assessment methods"""
    num_methods = LCA_scores.shape[1]
    correlations = np.zeros((num_methods, num_methods))

    for row in range(num_methods):
        for col in range(num_methods):
            if col <= row:
                continue                               
            dataset1 = LCA_scores[:, row]
            dataset2 = LCA_scores[:, col]
            masking = (dataset1 != 0) * (dataset2 != 0) #Set masking crateria
            dataset1= dataset1[masking] #Array masking to exclude zero scores
            dataset2 = dataset2[masking]
            if coefficient.lower() == 'kendall':
               tau, p_value = stats.kendalltau(dataset1, dataset2)
               corr = tau
            elif coefficient.lower() == 'spearman':
                rho, p_value = stats.spearmanr(dataset1,dataset2)
                corr = rho
            elif coefficient.lower() == 'pearson':
                r, p_value = stats.pearsonr(dataset1,dataset2)
                corr = r
            if np.isnan(corr):
                correlations[row, col] = 0
            else:
                correlations[row, col] = corr
    # Drop zeros
    mask = correlations.sum(axis=0) != 0   # Drop rows of zeros
    correlations = correlations[:, mask]
    mask = correlations.sum(axis=1) != 0   # Drop columns of zeros
    correlations = correlations[mask, :]
    return correlations

def plot_correlation (LCA_scores):
    correlation_matrix = calc_correlation (LCA_scores)
    masked_correlation = np.ma.array(correlation_matrix, mask=correlation_matrix == 0).T
    sns.set(style="white")
    corr = masked_correlation
    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    f, ax = plt.subplots(figsize=(12, 12))
    plt.axis('off')
    plt.ylim(None, correlation_matrix.shape[1] - 1)
    plt.xlim(None, correlation_matrix.shape[0] - 1)
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    #fig = plt.gcf()
    #fig.set_size_inches(12, 12)
    #plt.pcolor(masked_correlation, cmap=plt.cm.cubehelix_r)
    #plt.colorbar()
    #plt.ylim(None, correlation_data.shape[1] - 1)
    #plt.xlim(None, correlation_data.shape[0] - 1)

def min_correlation(correlation_matrix):
    min_correlation = correlation_matrix.min()
    min_correlation_index = np.unravel_index(np.argmin(correlation_matrix), correlation_matrix.shape)
    return "Minimium correlation is: {}, which indice in the results array is {} ".format(min_correlation, min_correlation_index)

#        assert hasattr(self, "characterized_inventory"), "Must do LCIA calculation first"



