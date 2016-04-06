# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 15:56:44 2016

@author: andric
"""

import os
import setLog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


dat = pd.read_csv('peak_voxel_data.csv')
datcorr = dat.corr()
datarr = np.array(datcorr)
np.fill_diagonal(datarr, 0)
msk_datarr = np.ma.masked_where(datarr == 0, datarr)
plt.pcolormesh(msk_datarr, cmap=plt.cm.jet, vmin=-1, vmax=1)
plt.colorbar()
outname = 'cluster_cross_corrmat.pdf'
plt.savefig('cluster_cross_corrmat.pdf', dpi=300, transparent=True)
plt.close()

