# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 16:04:31 2019

@author: cyshi
"""

import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates
import matplotlib.ticker as mtick
 

# Scaling attribute values to avoid few outiers
data=pd.read_excel('uncertainty_file_copy.xlsx',sheet_name='parallel')

#cols = ['Acidification',	'Ecotoxicity',	'Eutrophication']
#subset_df = data[cols]


fig, ax = plt.subplots(1,1,figsize=(12,6))
parallel_coordinates(data, 'Names', colormap=plt.get_cmap("Set2"))
xlabels=['Acidification','Ecotoxicity','Eutrophication','Global warming','Ozone depletion','Photochemical oxidation','Carcinogenics','Non-carcinogenics','Respiratory effects']
ax.legend(loc='center left', bbox_to_anchor= (1,0.5))
ax.set_xticklabels(xlabels, rotation=40, horizontalalignment="right")

plt.show()


fig, ax = plt.subplots(1,1,figsize=(12,6))
parallel_coordinates(data, 'Names', color=['#79bf82','#60c1cf' , '#90918e', '#f98f60', '#a280b9'])
xlabels=['Acidification','Ecotoxicity','Eutrophication','Global warming','Ozone depletion','Photochemical oxidation','Carcinogenics','Non-carcinogenics','Respiratory effects']
ax.legend(loc='center left', bbox_to_anchor= (1,0.5))
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_xticklabels(xlabels, rotation=90, horizontalalignment="left")
ax.grid(axis='y')
plt.show()

fig, ax = plt.subplots(1,1,figsize=(12,6))
parallel_coordinates(data, 'Names', color=['#79bf82','#60c1cf' , '#90918e', '#f98f60', '#a280b9',], use_columns=False,alpha=0.02, axvlines=False)
xlabels=['Acidification','Ecotoxicity','Eutrophication','Global warming','Ozone depletion','Photochemical oxidation','Carcinogenics','Non-carcinogenics','Respiratory effects']
ax.legend(loc='center left', bbox_to_anchor= (1,0.5))
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_xticklabels(xlabels, rotation=90, horizontalalignment="left")
ax.grid(axis='y')
plt.show()

#from sklearn.preprocessing import StandardScaler
#
#ss = StandardScaler()
#
#
#
#scaled_df = ss.fit_transform(subset_df)
#
#scaled_df = pd.DataFrame(scaled_df, columns=cols)
#
#final_df = pd.concat([scaled_df, data['Units Type']], axis=1)
#
#final_df.head()
#
#
#
# plot parallel coordinates

from pandas.plotting import parallel_coordinates

pc = parallel_coordinates(final_df, 'Units Type', color=('#FFE888', '#FF9999'))