# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:03:24 2015

@author: andric
"""

import os
import time
from shlex import split
from subprocess import call, STDOUT


def applywarp(workdir, input, extrt1, out, premat, interp=None):
    """
    general procedure for applywarp
    """
    print 'Doing applywarp'
    stdoutdir = os.path.join(workdir, 'stdout_files')
    if not os.path.exists(stdoutdir):
        os.makedirs(stdoutdir)
    f = open('%s/stdout_from_applywarp.txt' % stdoutdir, 'w')
    if interp is None:
        cmdargs = split('applywarp -i %s -r %s -o %s --premat=%s' %
                        (input, extrt1, out, premat))
    else:
        cmdargs = split('applywarp -i %s -r %s -o %s --premat=%s \
        --interp=%s' % (input, extrt1, out, premat, interp))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def applywarpFLIRT(ss, work_dir, input, extrt1, out, premat, interp=None):
    """
    Warp via linear transformation via fsl FLIRT
    """
    print 'doing applywarpFLIRT for %s -- ' % ss+time.ctime()
    stdout_dir = os.path.join(work_dir, 'stdout_files')
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_applywarpFLIRT.txt' % stdout_dir, 'w')
    if interp is None:
        cmdargs = split('applywarp -i %s -r %s -o %s --premat=%s' %
                        (input, extrt1, out, premat))
    else:
        cmdargs = split('applywarp -i %s -r %s -o %s --premat=%s --interp=%s' %
                        (input, extrt1, out, premat, interp))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def applywarpFNIRT(ss, work_dir, input, out, coeff, interp=None):
    """
    Warp via nonlinear transformation via fsl FNIRT
    """
    print 'Doing applywarpFNIRT for %s -- ' % ss+time.ctime()
    stdout_dir = os.path.join(work_dir, 'stdout_files')
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_applywarp.txt' % stdout_dir, 'w')
    if interp is None:
        cmdargs = split('applywarp -i %s \
                        -r %s/data/standard/MNI152_T1_2mm.nii.gz \
                        -o %s -w %s' %
                        (input, os.environ['FSLDIR'], out, coeff))
    else:
        cmdargs = split('applywarp -i %s \
                        -r %s/data/standard/MNI152_T1_2mm.nii.gz \
                        -o %s -w %s --interp=%s' %
                        (input, os.environ['FSLDIR'], out, coeff, interp))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def converttoNIFTI(work_dir, brain, prefix=None):
    """
    convert AFNI file to NIFTI
    """
    print 'Doing converttoNIFTI for %s -- ' % brain+time.ctime()
    stdout_dir = os.path.join(work_dir, 'stdout_files')
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_converttoNIFTI' % stdout_dir, 'w')
    if prefix is None:
        cmdargs = split('3dAFNItoNIFTI %s' % brain)
    elif prefix:
        cmdargs = split('3dAFNItoNIFTI -prefix %s %s' % (prefix, brain))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def fwhm_est(input_data, outname, mask=None):
    """
    Estiamte FWHM of data
    Will return FWHM
    """
    print 'Doing fwhm_est -- %s' % time.ctime()
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s_fwhm_est_out.txt' % input_data, 'w')
    if mask is None:
        cmdargs = split('3dFWHMx -input %s -out %s' %
                        (input_data, outname))
    else:
        cmdargs = split('3dFWHMx -mask %s -input %s -out %s' %
                        (mask, input_data, outname))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def clustsim(fwhm, outdir, mask=None):
    """
    Find the size of clusters by chance
    """
    print 'Running clustsim -- %s' % time.ctime()
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/ClustSim_FWHM_%f_%f_%f_out.txt' %
             (outdir, fwhm[0], fwhm[1], fwhm[2]), 'w')
    if mask is None:
        cmdargs = split('3dClustSim -NN 123 -fwhmxyz %f %f %f' %
                        (fwhm[0], fwhm[1], fwhm[2]))
    else:
        cmdargs = split('3dClustSim -NN 123 -mask %s -fwhmxyz %f %f %f' %
                        (mask, fwhm[0], fwhm[1], fwhm[2]))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def mean_epi(ss, infile, work_dir, outpref):
    """
    Average across TS mean brain to get one mean image.
    YOU SHOULD FIRST HAVE AN AVERAGE OF TS (MANY IMAGES)
    THIS IS WHAT YOU MAKE MEAN (ONE IMAGE).
    Serves registration purposes.
    :param ss: Subject identifier
    Writes to file AFNI mean brain (one image)
    """
    print 'Doing mean_epi for %s -- ' % ss
    print time.ctime()
    stdout_dir = os.path.join(work_dir, 'stdout_files')
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_mean_epi.txt' % stdout_dir, 'w')
    cmdargs = split('3dTstat -prefix %s -mean %s' % (outpref, infile))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()
