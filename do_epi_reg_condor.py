# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 16:33:00 2015

@author: andric
"""

import os
import sys
import procs as pr
from setlog import setup_log


def epi_reg(logf, decon_dir, subj):
    """Register epi to the group template."""
    anat_dir = os.path.join(os.environ['avp'], 'nii/%s_CNR.anat' % subj)
    epi_pref = 'decon_out.ramps_wav.%s_concat.Powered.cleanEPI_REML' % subj
    epi_nii_pref = os.path.join(decon_dir, epi_pref)
    pr.converttoNIFTI(decon_dir,
                      '%s+orig' % epi_nii_pref,
                      epi_nii_pref)

    in_fl = os.path.join(decon_dir, '%s.nii.gz' % epi_nii_pref)
    out_fl = os.path.join(decon_dir, '%s_flirted' % epi_nii_pref)
    pr.applywarpFLIRT(subj,
                      decon_dir,
                      in_fl,
                      os.path.join(anat_dir, 'T1_biascorr_brain.nii.gz'),
                      out_fl,
                      os.path.join(anat_dir, '%s_3.2mprage.mat' % subj))

    out_fn = os.path.join(decon_dir, '%s_fnirted_MNI2mm' % epi_nii_pref)
    pr.applywarpFNIRT(subj,
                      '%s.nii.gz' % out_fl,
                      out_fn,
                      os.path.join(anat_dir, 'T1_to_MNI_nonlin_coeff.nii.gz'),
                      log=logf)


def main():
    """Wrap and call functions.

    Require subject ID as command arg 1.
    """
    decon_outdir = os.path.join(os.environ['avp'],
                                'nii', 'deconvolve_outs_ramps')
    logfile = setup_log(os.path.join(os.environ['avp'], 'logs',
                                     'do_epi_reg_%s' % sys.argv[1]))
    epi_reg(logfile, decon_outdir, sys.argv[1])


if __name__ == '__main__':
    main()
