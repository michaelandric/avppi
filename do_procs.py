# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 18:09:48 2015

@author: andric
"""

import os
import procs as pr

if __name__ == '__main__':
    subj_list = [s for s in range(1, 20)]

    group_dir = os.path.join(os.environ['avp'], 'nii',
                             'group_effects_dec')

    """Doing p < .005. There are no Ventr clusters"""
    effects = ['Aentr', 'Aentr_intxn']
    mask = os.path.join(os.environ['FSLDIR'], 'data/standard',
                        'MNI152_T1_2mm_brain_mask_dil1.nii.gz')
    for ef in effects:
        inpref = 'clust_%s_flt2_msk_mema_p.005_mask+tlrc' % ef
        clust_image = os.path.join(group_dir, inpref)
        out_txt = os.path.join(group_dir, '%s.txt' % inpref)
        pr.maskdump(group_dir, mask, clust_image, out_txt)
