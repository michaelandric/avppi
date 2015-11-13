# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 18:09:48 2015

@author: andric
"""

import os
import procs as pr

if __name__ == '__main__':
    subj_list = range(1, 19)
    subj_list.remove(11)
#    subj_list = [19]

#    effects = ['Aentr', 'Ventr', 'Aentr_intxn']
    conds = ['ALowVLow', 'ALowVHigh', 'AHighVLow', 'AHighVHigh']
    sb = [4, 7, 10, 13]
    d = dict(zip(conds, sb))
    decon_dir = os.path.join(os.environ['avp'], 'nii',
                             'deconvolve_outs_concat')
    mask = os.path.join(os.environ['FSLDIR'], 'data/standard',
                        'MNI152_T1_2mm_brain_mask_dil1.nii.gz')
    suff = 'Powered.cleanEPI_REML_fnirted_MNI2mm'
    for ss in subj_list:
        ef_dir = os.path.join(os.environ['avp'], 'nii', 'ss%s_effects' % ss)
        for cn in conds:
            in_image = "'%s/decon_out.mion.%s_concat.%s.nii.gz[%d]'" % \
                (decon_dir, ss, suff, d[cn])
            out_txt = "%s/%s_coef_%s_concat.%s.txt" % \
                (decon_dir, cn, ss, suff)
            pr.maskdump(ef_dir, mask, in_image, out_txt)
