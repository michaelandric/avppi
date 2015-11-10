# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 16:17:02 2015

@author: andric
"""

import os
import numpy as np
import general_procedures as gp
from shlex import split
from subprocess import Popen, PIPE


def get_fwhm(input):
    """
    Will return x, y, z as floats
    """
    cmds = split('3dFWHMx -automask -input %s' % (input))
    p = Popen(cmds, stdout=PIPE).communicate()
    return map(float, p[0].split())


subj_list = range(1, 19)
xyz_mat = np.zeros(len(subj_list)*3).reshape(len(subj_list), 3)
decon_dir = os.path.join(os.environ['avp'],
                         'nii', 'deconvolve_outs_concat')
suff = 'Powered.cleanEPI_errts_REML_mean_fnirted_MNI2mm'
for i, ss in enumerate(subj_list):
    fpref = 'decon_out.mion.%s_concat.%s' % (ss, suff)
    input_pref = os.path.join(decon_dir, fpref)
    x, y, z = get_fwhm('%s.nii.gz' % input_pref)
    xyz_mat[i, :] = [x, y, z]

avg_fwhm = np.mean(xyz_mat, axis=0)
print 'FWHM is:'
print avg_fwhm
out_pref = 'decon_out.mion.group_.%s_fwhm_est_out' % suff
out_name = os.path.join(decon_dir, out_pref)
np.savetxt(out_name, avg_fwhm.reshape(1, 3), fmt='%.4f %.4f %.4f')

mask = os.path.join(os.environ['FSLDIR'], 'data/standard',
                    'MNI152_T1_2mm_brain_mask_dil1.nii.gz')
gp.clustsim(avg_fwhm, decon_dir, mask)
