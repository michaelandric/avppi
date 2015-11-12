# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 18:09:48 2015

@author: andric
"""

import os
import procs as pr

if __name__ == '__main__':
    subj_list = range(1, 19)
#    subj_list = [19]

    effects = ['Aentr', 'Ventr', 'Aentr_intxn']
    mask = os.path.join(os.environ['FSLDIR'], 'data/standard',
                        'MNI152_T1_2mm_brain_mask_dil1.nii.gz')
    for ss in subj_list:
        ef_dir = os.path.join(os.environ['avp'], 'nii', 'ss%s_effects' % ss)
        for ef in effects:
            inpref = '%s_ss%s_coef+tlrc' % (ef, ss)
            clust_image = os.path.join(ef_dir, inpref)
            out_txt = os.path.join(ef_dir, '%s.txt' % inpref)
            pr.maskdump(ef_dir, mask, clust_image, out_txt)
