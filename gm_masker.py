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

    def get_gm(self, fast_seg, outpref):
        print '3dcalc to get gm segmentation'
        f = open('%s/stdout_from_gm_seg.txt' % self.stdoutdir, 'w')
        calcargs = split("3dcalc -a %s -expr 'equals(a, 2)' -prefix %s" %
        (fast_seg, outpref))
        call(calcargs, stdout=f, stderr=STDOUT)
        f.close()

    def fractionize(self, input, outpref):
        print 'Doing fractionize for %s' % outpref
        f = open('%s/stdout_from_fractionize.txt' % self.stdoutdir, 'w')
        frcargs = split('3dfractionize -template %s -input %s \
                        -prefix %s -clip 0.3' % (self.ref, input, outpref))
        call(frcargs, stdout=f, stderr=STDOUT)
        f.close()

    def mask_calc(self, subcort_frc, gm_frc, outpref):
        print 'Doing mask_calc'
        f = open('%s/stdout_from_mask_calc.txt' % self.stdoutdir, 'w')
        mask_args = split("3dcalc -a %s -b %s -expr 'a+b' -prefix %s" %
        (subcort_frc, gm_frc, outpref))
        call(mask_args, stdout=f, stderr=STDOUT)
        f.close()

    def reorient(self, input, outname, premat, interp):
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
        for i in range(1, 5):
            anat_dir = os.path.join(os.environ['avp'], 'nii',
                                    '%s_CNR.anat' % ss)
            ref_brain = os.path.join(anat_dir, '%s_%s.vol8.nii.gz' % (ss, i))
            msk = Masker(ref_brain, ss, anat_dir)

            fast_seg = os.path.join(anat_dir, 'T1_fast_seg.nii.gz')
            gm_out_pref = os.path.join(anat_dir, '%s_%s.fast_seg_gm.nii.gz' %
            (ss, i))
            msk.get_gm(fast_seg, gm_out_pref)

            gm_frac_pref = os.path.join(anat_dir,
                                        '%s_%s.fast_seg_gm_frac.nii.gz' %
                                        (ss, i))
            subcort = os.path.join(anat_dir, 'T1_subcort_seg.nii.gz')
            subcort_frac_pref = os.path.join(anat_dir,
                                             '%s_s.subcort_seg_frac.nii.gz')
            msk.fractionize(fast_seg, gm_frac_pref)
            msk.fractionize(subcort, subcort_frac_pref)
            mask_pref = os.path.join(anat_dir,
                                     '%s_%s.gm_mask_T1space.nii.gz' % (ss, i))
            msk.mask_calc(subcort_frac_pref, gm_frac_pref, mask_pref)
            reorient_pref = os.path.join(anat_dir,
                                         '%s_%s.gm_mask_epi.nii.gz' % (ss, i))
            pre_mat = os.path.join(anat_dir, 'mprage2.%s_%s.mat' % (ss, i))
            msk.reorient(mask_pref, reorient_pref, pre_mat, 'spline')
