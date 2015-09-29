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
