# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 16:13:28 2016

@author: andric
"""

from shlex import split
import os
import subprocess
import setLog
import numpy as np



def get_fwhm(mask, input):
    """
    Will return x, y, z as floats
    """
    lg.info('Doing get_fwhm')
    cmds = split('3dFWHMx -mask %s -input %s' % (mask, input))
    p = subprocess.run(cmds, stdout=subprocess.PIPE)
    lg.info(p.stdout.decode("utf-8", "strict"))
    return list(map(float, p.stdout.decode("utf-8", "strict").split()))


subj_list = [s for s in range(1, 20)]
subj_list.remove(3)
subj_list.remove(11)
effects = ['Aentr', 'Ventr', 'Aentr_intxn']
mask = os.path.join(os.environ['FSLDIR'], 'data/standard',
                    'MNI152_T1_2mm_brain_mask_dil1.nii.gz')

for block in [20, 15, 10]:
    workdir = os.path.join(os.environ['avp'], 'nii',
                           'group_effects_%sblk' % block)
    lg = setLog._log('%s/fwhm_estimation' % workdir)
    block_mat = np.empty(len(effects)*3).reshape(len(effects), 3)
    for (n, ef) in enumerate(effects):
        xyz_mat = np.empty(len(subj_list)*3)
        xyz_mat = xyz_mat.reshape(len(subj_list), 3)
        infile = os.path.join(os.environ['avp'], 'nii/group_effects_%sblk' % block,
                              '%s_flt2_%sblk_msk_mema_resZ+tlrc' % (ef, block))
        for (i, ss) in enumerate(subj_list):
            x, y, z = get_fwhm(mask, '%s\[%d]' % (infile, i))
            xyz_mat[i, :] = [x, y, z]
        avg_fwhm = xyz_mat.mean(axis=0)
        block_mat[n, :] = avg_fwhm
        lg.info('%s block %s averages: %s' % (ef, block, avg_fwhm))
    block_avg = block_mat.mean(axis=0)
    lg.info('block average: %s' % block_avg)
    out_pref = 'fwhm_est_%sblk.out' % block
    out_name = os.path.join(workdir, out_pref)
    np.savetxt(out_name, block_mat, fmt='%.4f')
