# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 17:55:42 2015

@author: andric
"""

import numpy as np
import os

os.chdir('/mnt/lnif-storage/urihas/AVaudvisppi/timing/')

seq_list = []
for i in range(1, 5):
    seq_list.append('seq%s' % i)

for seq in seq_list:
    for c in range(6):
        dat = np.loadtxt('%s.txt' % seq)
        o = dat[np.where(dat[:, 0] == c), 2]
        np.savetxt('decon_%s_cond%s.txt' % (seq, c), o, fmt='%.1f')
