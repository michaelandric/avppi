# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 18:09:48 2015

@author: andric
"""

import os
import procs as pr

if __name__ == '__main__':
    subj_list = [s for s in range(1, 20)]

    effects = ['Aentr', 'Ventr', 'Aentr_intxn']
    conds = ['ALowVLow', 'ALowVHigh', 'AHighVLow', 'AHighVHigh']
    sb = [4, 7, 10, 13]
    d = dict(zip(conds, sb))
    decon_dir = os.path.join(os.environ['avp'], 'nii',
                             'deconvolve_outs_concat_dec')
    mask = os.path.join(os.environ['FSLDIR'], 'data/standard',
                        'MNI152_T1_2mm_brain_mask_dil1.nii.gz')
    """
    suff = 'Powered.cleanEPI_REML_fnirted_MNI2mm'
    for ss in subj_list:
        ef_dir = os.path.join(os.environ['avp'], 'nii', 'ss%s_effects_dec' % ss)
        for cn in conds:
            in_image = "'%s/decon_out.mion.%s_concat.%s.nii.gz[%d]'" % \
                (decon_dir, ss, suff, d[cn])
            out_txt = "%s/%s_coef_%s_concat.%s.txt" % \
                (decon_dir, cn, ss, suff)
            pr.maskdump(ef_dir, mask, in_image, out_txt)
    """
    for ss in subj_list:
        ef_dir = os.path.join(os.environ['avp'], 'nii', 'ss%s_effects_dec' % ss)
        for ef in effects:
            inpref = '%s_ss%s_coef+tlrc' % (ef, ss)
            clust_image = os.path.join(ef_dir, inpref)
            out_txt = os.path.join(ef_dir, '%s.txt' % inpref)
            pr.maskdump(ef_dir, mask, clust_image, out_txt)