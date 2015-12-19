# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 15:09:52 2015

@author: andric
"""

import os
import sys
import procs as pr

if __name__ == '__main__':
    ss = int(sys.argv[1])

    anat_dir = os.path.join(os.environ['avp'], 'nii', '%s_CNR.anat' % ss)
    fn_coef = os.path.join(anat_dir,
                           'T1_to_MNI_nonlin_coeff.nii.gz')
    in_fn = os.path.join(anat_dir, 'T1_subcort_seg.nii.gz')
    out_fn = os.path.join(anat_dir,
                          '%s_T1_subcort_seg_fnirted_MNI2mm' % ss)
    logfile = os.path.join(anat_dir, 'applywarpFNIR.log')
    pr.applywarpFNIRT(ss, in_fn, out_fn, fn_coef, 'nn', logfile)
