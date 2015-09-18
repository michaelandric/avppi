# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 18:09:48 2015

@author: andric
"""

import os
import procs as pr


if __name__ == '__main__':
#    subj_list = range(1, 20)
    subj_list = [19]
    for ss in subj_list:
        for i in range(1, 5):
            anat_dir = os.path.join(os.environ['avp'], 'nii',
                                    '%s_CNR.anat' % ss)
            in_anat = os.path.join(anat_dir, 'T1_subcort_seg.nii.gz')
            ref = os.path.join(anat_dir, '%s_%s.vol8.nii.gz' % (ss, i))
            outf = os.path.join(anat_dir,
                                '%s_%s.T1_subcort_seg.2epi.nii.gz' % (ss, i))
            mat = os.path.join(anat_dir, 'mprage2.%s_%s.mat' % (ss, i))
            pr.applywarp(anat_dir, in_anat, ref, outf, mat, 'spline')