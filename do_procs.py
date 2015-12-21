# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 18:09:48 2015

@author: andric
"""

import os
import procs as pr

if __name__ == '__main__':

    subj_list = [s for s in range(1, 20)]
    
    mask = os.path.join(os.environ['FSLDIR'], 'data/standard',
                        'MNI152_T1_2mm_brain_mask_dil1.nii.gz')

    for ss in subj_list:
        anat_dir = os.path.join(os.environ['avp'], 'nii',
                                '%s_CNR.anat' % ss)
        inpref = '%s_T1_subcort_seg_fnirted_MNI2mm' % ss
        in_image = os.path.join(anat_dir, '%s.nii.gz' % inpref)
        out_txt = os.path.join(anat_dir, '%s.txt' % inpref)
        pr.maskdump(anat_dir, mask, in_image, out_txt)