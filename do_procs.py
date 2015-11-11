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

    group_dir = os.path.join(os.environ['avp'], 'nii',
                             'group_effects')
    effects = ['Aentr', 'Ventr', 'Aentr_intxn']
    for ef in effects:
        inpref = 'Clust_ttest_%s_mask+tlrc' % ef
        clust_image = os.path.join(group_dir, inpref)
        out_txt = os.path.join(group_dir, '%s.txt' % inpref)
        pr.maskdump(group_dir, clust_image, clust_image, out_txt, 'False')
