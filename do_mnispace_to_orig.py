# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 12:51:36 2015

@author: andric
"""

import os
import logging
import procs as pr

if __name__ == '__main__':
    subj_list = [1]
    for ss in subj_list:
        logfilename = '%s_makeinvmat.log' % ss
        vol_dir_pref = '%s_CNR.anat' % ss
        anat_dir = os.path.join(os.environ['avp'], 'nii', vol_dir_pref)
        logging.basicConfig(filename=os.path.join(anat_dir, logfilename))
        stdout_dir = os.path.join(anat_dir, 'stdout_files')
        for r in range(1, 4):
            matfile = os.path.join(anat_dir,
                                   '%s_%s.2mprage.mat' % (ss, r))
            inv_mat = os.path.join(anat_dir,
                                   '%s_%s.2mprage_inv.mat' % (ss, r))
            pr.convert_inversemat(matfile, inv_mat)
