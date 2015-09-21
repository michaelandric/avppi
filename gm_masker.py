# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 12:50:43 2015

@author: andric
"""

import os
import time
from shlex import split
from subprocess import call, STDOUT

class Masker(object):

    def __init__(self, master_ref, ss, stdout_dir):
        print 'Initializing... '+time.ctime()
        self.ref = master_ref
        self.subjid = ss
        self.stdoutdir = stdout_dir

    def get_gm(self, pve, outpref):
        print '3dcalc to get gm segmentation'
        f = open('%s/stdout_from_gm_seg.txt' % self.stdoutdir, 'w')
#        calcargs = split("3dcalc -a %s -expr 'equals(a, 2) -prefix %s" %
#        (fast_seg, outpref))
        calcargs = split("3dcalc -a %s -expr 'step(a-.3)' -prefix %s" %
        (pve, outpref))
        call(calcargs, stdout=f, stderr=STDOUT)
        f.close()

    def mask_calc(self, subcort_frc, gm_frc, outpref):
        print 'Doing mask_calc'
        f = open('%s/stdout_from_mask_calc.txt' % self.stdoutdir, 'w')
        mask_args = split("3dcalc -a %s -b %s -expr 'step(a+b)' -prefix %s" %
        (subcort_frc, gm_frc, outpref))
        call(mask_args, stdout=f, stderr=STDOUT)
        f.close()

    def applywarp_reorient(self, input, outname, premat, interp):
        print 'Reorient to epi space'
        f = open('%s/stdout_from_reorient.txt' % self.stdoutdir, 'w')
        cmdargs = split('applywarp -i %s -r %s -o %s \
                        --premat=%s --interp=%s' % 
                        (input, self.ref, outname, premat, interp))
        call(cmdargs, stdout=f, stderr=STDOUT)
        f.close()


if __name__ == '__main__':
#    subj_list = range(1, 20)
    subj_list = [19]
    for ss in subj_list:
        anat_dir = os.path.join(os.environ['avp'], 'nii',
                                '%s_CNR.anat' % ss)
        ref_brain = os.path.join(anat_dir, '%s_1.vol8.nii.gz' % (ss))
        msk = Masker(ref_brain, ss, anat_dir)

        pve_seg = os.path.join(anat_dir, 'T1_fast_pve_1.nii.gz')
        gm_out_pref = os.path.join(anat_dir, 'pve_gm_seg.%s.nii.gz' % (ss))
        msk.get_gm(pve_seg, gm_out_pref)

        pre_mat = os.path.join(anat_dir, 'mprage2.%s_1.mat' % (ss))
        gm_reor_pref = os.path.join(anat_dir,
                                    'pve_gm_seg_epispace.%s.nii.gz' % ss)
        msk.applywarp_reorient(gm_out_pref, gm_reor_pref, pre_mat, 'nn')

        subcort = os.path.join(anat_dir, 'T1_subcort_seg.nii.gz')
        subcort_reor_pref = os.path.join(anat_dir,
                                         'subcort_seg_epispace.%s.nii.gz' % ss)
        msk.applywarp_reorient(subcort, subcort_reor_pref, pre_mat, 'nn')

        mask_out_pref = os.path.join(anat_dir,
                                     'gm_mask_epispace.%ss.nii.gz' % ss)
        msk.mask_calc(subcort_reor_pref, gm_reor_pref, mask_out_pref)
