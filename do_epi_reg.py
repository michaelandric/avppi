# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 16:33:00 2015

@author: andric
"""

import os
import procs as pr

if __name__ == '__main__':
    # subj_list = range(1, 19)
    subj_list = [1]

    for ss in subj_list:
        decon_dir = os.path.join(os.environ['avp'], 'nii', 'deconvolve_outs')
        vol_dir_pref = 'nii/%s_CNR.anat' % ss
        anat_dir = os.path.join(os.environ['avp'], vol_dir_pref)
        wholet1 = os.path.join(anat_dir, 'T1_biascorr.nii.gz')
        extrt1 = os.path.join(anat_dir, 'T1_biascorr_brain.nii.gz')
        premat = os.path.join(anat_dir, '%s_3.2mprage.mat' % ss)
        for i in range(1, 5):
            epi_pref = 'decon_out.mion.%d_%d.Powered.cleanEPI' % (ss, i)
            epi_nii_pref = os.path.join(decon_dir, epi_pref)
            pr.converttoNIFTI(decon_dir, '%s+orig' % epi_nii_pref,
                              epi_nii_pref)
            in_fl = os.path.join(decon_dir, '%s.nii.gz' % epi_nii_pref)
            out_fl = os.path.join(decon_dir, '%s_flirted' % epi_nii_pref)
            pr.applywarpFLIRT(ss, decon_dir, in_fl, extrt1,
                              out_fl, premat)

            fn_coef = os.path.join(anat_dir,
                                   'T1_to_MNI_nonlin_coeff.nii.gz')
            in_fn = '%s.nii.gz' % out_fl
            out_fn = os.path.join(decon_dir,
                                  '%s_fnirted_MNI2mm' % epi_nii_pref)
            pr.applywarpFNIRT(ss, decon_dir, in_fn, out_fn, fn_coef)
