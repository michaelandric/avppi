# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 18:09:33 2015

@author: andric
"""

import os
import numpy as np

if __name__ == '__main__':
    subj_list = range(1, 20)
    censor_array = np.zeros(shape=(len(subj_list), 5))
    for i, ss in enumerate(subj_list):
        censor_array[i, 0] = ss
        for seq in range(1, 5):
            cf = os.path.join(os.environ['avp'], 'nii',
                              '%s_preproc/%s_%s/%s_%s.Powered.censor.1D' %
                              (ss, ss, seq, ss, seq))
            censor = np.loadtxt(cf)
            blanks = len(np.where(censor == 0)[0])
            censor_array[i, seq] = blanks
    outname = 'censor_numbers.txt'
    outf = os.path.join(os.environ['avp'], 'nii', outname)
    np.savetxt(outf, censor_array, fmt='%d')
