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
    mask = os.path.join(os.environ['FSLDIR'], 'data/standard',
                        'MNI152_T1_2mm_brain_mask_dil1.nii.gz')

    for block in [20, 15, 10]:
        outdir = os.path.join(os.environ['avp'], 'nii',
                              'group_effects_%sblk' % block)
        for ef in effects:
            ef_pref = os.path.join(outdir,
                                   'clust_%s_flt2_%sblk_msk_mema_mask+tlrc' %
                                   (ef, block))
            ef_file = '%s.BRIK.gz' % ef_pref
            if os.path.exists('%s.BRIK.gz' % ef_pref):
                clust_image = ef_file
                out_txt = os.path.join(outdir, '%s.txt' % ef_pref)
                pr.maskdump(outdir, mask, clust_image, out_txt)
