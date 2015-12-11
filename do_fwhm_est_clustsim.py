# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 16:17:02 2015

@author: andric
"""

import os
import setLog
import numpy as np
import procs as pr
from shlex import split
from subprocess import Popen, PIPE


def get_fwhm(input):
    """
    Will return x, y, z as floats
    """
    cmds = split('3dFWHMx -automask -input %s' % (input))
    p = Popen(cmds, stdout=PIPE).communicate()
    return map(float, p[0].split())

def get_fwhm_acf(input):
    """
    Will return x, y, z as floats
    """
    cmds = split('3dFWHMx -input %s -ACF' % (input))
    p = Popen(cmds, stdout=PIPE).communicate()
    return map(float, p[0].split('\n')[3].split())

subj_list = [s for s in range(1, 20)]
subj_list.remove(3)
subj_list.remove(11)
xyz_mat = np.zeros(len(subj_list)*3).reshape(len(subj_list), 3)
abc_mat = np.zeros(len(subj_list)*4).reshape(len(subj_list), 4)
decon_dir = os.path.join(os.environ['avp'],
                         'nii', 'deconvolve_outs_concat_dec')
suff = 'Powered.cleanEPI_errts_REML_mean_fnirted_MNI2mm'
lg = setLog._log('%s/acf_est_clustsim' % decon_dir)
lg.info('Doing get_fwhm')
for i, ss in enumerate(subj_list):
    lg.info('subj %s' % ss)
    fpref = 'decon_out.mion.%s_concat.%s' % (ss, suff)
    input_pref = os.path.join(decon_dir, fpref)
#    x, y, z = get_fwhm('%s.nii.gz' % input_pref)
#    xyz_mat[i, :] = [x, y, z]
    a, b, c, cmb_fwhm = get_fwhm_acf('%s.nii.gz' % input_pref)
    lg.info('a b c and fwhm: %s %s %s %s' % (a, b, c, cmb_fwhm))
    abc_mat[i, :] = [a, b, c, cmb_fwhm]
lg.info('get_fwhm done.')

#avg_fwhm = np.mean(xyz_mat, axis=0)
avg_acf = np.mean(abc_mat, axis=0)
lg.info('averages: %s' % avg_acf)
avg_acf = avg_acf[:3]
#lg.info('FWHM is: %s' % avg_fwhm)
out_pref = 'fwhm_est_decon_out.mion.group.%s_acf_out' % suff
out_name = os.path.join(decon_dir, out_pref)
#np.savetxt(out_name, avg_fwhm.reshape(1, 3), fmt='%.4f %.4f %.4f')
np.savetxt(out_name, avg_acf.reshape(1, 3), fmt='%.4f %.4f %.4f')
lg.info('saved FWHM to %s' % out_name)

mask = os.path.join(os.environ['FSLDIR'], 'data/standard',
                    'MNI152_T1_2mm_brain_mask_dil1.nii.gz')

lg.info('Doing clustsim')
#pr.clustsim(avg_fwhm, decon_dir, mask)
pr.clustsim_acf(avg_acf, decon_dir, mask)
lg.info('clustsim done.')