# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:03:24 2015

@author: andric
"""

import os
import time
import logging
import setLog
from shlex import split
from subprocess import call, STDOUT
import subprocess


def applywarp(workdir, input, extrt1, out, premat, interp=None):
    """
    general procedure for applywarp
    """
    print ('Doing applywarp')
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
    print ('doing applywarpFLIRT for %s -- ' % ss+time.ctime())
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


def applywarpFNIRT(ss, input, out, coeff, interp=None, logf=None):
    """
    Warp via nonlinear transformation via fsl FNIRT
    """
    if logf:
        lg = setLog._log(logf)
    lg.info('Doing applywarpFNIRT for %s -- ' % ss)
    if interp is None:
        cmd = split('applywarp -i %s \
                        -r %s/data/standard/MNI152_T1_2mm.nii.gz \
                        -o %s -w %s' %
                        (input, os.environ['FSLDIR'], out, coeff))
    else:
        cmd = split('applywarp -i %s \
                        -r %s/data/standard/MNI152_T1_2mm.nii.gz \
                        -o %s -w %s --interp=%s' %
                        (input, os.environ['FSLDIR'], out, coeff, interp))
    lg.info("Command: \n%s" % cmd)
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lg.info(p.stdout.decode("utf-8", "strict"))
    lg.info("Done with applywarpFNIRT")


def converttoNIFTI(work_dir, brain, prefix=None):
    """
    convert AFNI file to NIFTI
    """
    print ('Doing converttoNIFTI for %s -- ' % brain+time.ctime())
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
    print ('Doing fwhm_est -- %s' % time.ctime())
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
    print ('Running clustsim -- %s' % time.ctime())
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/ClustSim_FWHM_%f_%f_%f_fwhm_orig_out.txt' %
             (outdir, fwhm[0], fwhm[1], fwhm[2]), 'w')
    if mask is None:
        cmdargs = split('3dClustSim -NN 123 -fwhmxyz %f %f %f' %
                        (fwhm[0], fwhm[1], fwhm[2]))
    else:
        cmdargs = split('3dClustSim -NN 123 -mask %s -fwhmxyz %f %f %f' %
                        (mask, fwhm[0], fwhm[1], fwhm[2]))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()

def clustsim_acf(acf, outdir, mask=None):
    """
    Find the size of clusters by chance
    """
    print ('Running clustsim -- %s' % time.ctime())
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/ClustSim_FWHM_%f_%f_%f_acf_orig_out.txt' %
             (outdir, acf[0], acf[1], acf[2]), 'w')
    if mask is None:
        cmdargs = split('3dClustSim -NN 123 -acf %f %f %f' %
                        (acf[0], acf[1], acf[2]))
    else:
        cmdargs = split('3dClustSim -NN 123 -mask %s -acf %f %f %f' %
                        (mask, acf[0], acf[1], acf[2]))
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
    print ('Doing mean_epi for %s -- ' % ss)
    print (time.ctime())
    stdout_dir = os.path.join(work_dir, 'stdout_files')
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_mean_epi.txt' % stdout_dir, 'w')
    cmdargs = split('3dTstat -prefix %s -mean %s' % (outpref, infile))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def maskdump(work_dir, mask, in_pref, out_pref, noijk=True):
    stdout_dir = os.path.join(work_dir, 'stdout_files')
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    outf = open(out_pref, 'w')
    f = open('%s/stdout_from_maskdump.txt' % stdout_dir, 'w')
    if noijk is True:
        cmdargs = split('3dmaskdump -mask %s -noijk %s' % (mask, in_pref))
    else:
        cmdargs = split('3dmaskdump -mask %s %s' % (mask, in_pref))
    call(cmdargs, stdout=outf, stderr=f)
    outf.close()
    f.close()

def convert_inversemat(matfile, outfile, stdf=None):
    if stdf is not None:
        stdout_dir = 'stdout_files'
        if not os.path.exists(stdout_dir):
            os.makedirs(stdout_dir)
    cmdargs = split('convert_xfm -omat %s -inverse %s' % (outfile, matfile))
    if stdf is not None:
        f = open(stdf, 'w')
        call(cmdargs, stdout=f, stderr=STDOUT)
        f.close()
    else:
        call(cmdargs)

def mnispace_to_origspace(stdout, matfile, invmat,
                          rev_fnirt, flirtd_brain,
                          region_msk, coeff,
                          region_msk_out_flirt, region_msk_out_orig,
                          msk_frac_bin_orig, final_msk_outpref):
    """
    1. convert flirt mat to inverse
    2. use invwarp to get inverse of warp (fnirt'd)
    3. applywarp
    """
    convert_inversemat(matfile, invmat)
    f = open('%s/stdout_from_mnispace_to_origspace.txt' % stdout, 'w')
#    inv_args = split('invwarp --ref=%s --warp=%s --out=%s' %
#                     (flirtd_brain, coeff, rev_fnirt))
#    call(inv_args, stdout=f, stderr=STDOUT)
    cmdargs1 = split('applywarp --ref=%s --in=%s --warp=%s \
                    --out=%s --interp=nn' %
                     (flirtd_brain, region_msk, rev_fnirt,
                      region_msk_out_flirt))
    call(cmdargs1, stdout=f, stderr=STDOUT)
    cmdargs2 = split('applywarp --ref=%s --in=%s --postmat=%s \
                     --out=%s --interp=nn' %
                     (msk_frac_bin_orig, region_msk_out_flirt,
                      invmat, region_msk_out_orig))
    call(cmdargs2, stdout=f, stderr=STDOUT)
    maskdump(stdout, msk_frac_bin_orig, region_msk_out_orig, final_msk_outpref)
    f.close()

def vol2surf_mni(work_dir, mapfunc, hemi, parent, pn, outname, logf=None):
    """
    Project to MNI surf.
    Make sure 'suma_dir' is set right
    """
    if logf:
        lg = setLog._log(logf)
    lg.info("vol2surf_mni starting")
    suma_dir = '/mnt/lnif-storage/urihas/software/AFNI2015/suma_MNI_N27'
    spec_fname = 'MNI_N27_%s.spec' % hemi
    spec = os.path.join(suma_dir, spec_fname)
    surf_a = '%s.smoothwm.gii' % hemi
    surf_b = '%s.pial.gii' % hemi
    surfvol_name = 'MNI_N27_SurfVol.nii'
    sv = os.path.join(suma_dir, surfvol_name)
    cmdargs = split('3dVol2Surf -spec %s \
                    -surf_A %s -surf_B %s \
                    -sv %s -grid_parent %s \
                    -map_func %s -f_steps 10 -f_index voxels \
                    -f_p1_fr -%s -f_pn_fr %s \
                    -outcols_NSD_format -oob_index -1 -oob_value 0.0 \
                    -out_1D %s' % (spec, surf_a, surf_b, sv,
                                   parent, mapfunc, pn, pn, outname))
    lg.info("Command: \n%s" % cmdargs)
    p = subprocess.run(cmdargs, stderr=subprocess.PIPE)
    lg.info(p.stderr.decode("utf-8", "strict"))
    lg.info("Done with vol2surf_mni")

def vol2surf_mni_no_pn(work_dir, mapfunc, hemi, parent, outname, logf=None):
    """
    Project to MNI surf.
    Make sure 'suma_dir' is set right
    """
    if logf:
        lg = setLog._log(logf)
    lg.info("vol2surf_mni starting")
    suma_dir = '/mnt/lnif-storage/urihas/software/AFNI2015/suma_MNI_N27'
    spec_fname = 'MNI_N27_%s.spec' % hemi
    spec = os.path.join(suma_dir, spec_fname)
    surf_a = '%s.smoothwm.gii' % hemi
    surf_b = '%s.pial.gii' % hemi
    surfvol_name = 'MNI_N27_SurfVol.nii'
    sv = os.path.join(suma_dir, surfvol_name)
    cmdargs = split('3dVol2Surf -spec %s \
                    -surf_A %s -surf_B %s \
                    -sv %s -grid_parent %s \
                    -map_func %s -f_steps 10 -f_index voxels \
                    -outcols_NSD_format -oob_index -1 -oob_value 0.0 \
                    -out_1D %s' % (spec, surf_a, surf_b, sv,
                                   parent, mapfunc, outname))
    lg.info("Command: \n%s" % cmdargs)
    p = subprocess.run(cmdargs, stderr=subprocess.PIPE)
    lg.info(p.stderr.decode("utf-8", "strict"))
    lg.info("Done with vol2surf_mni")

def cluster(vx_thr, clst_thr, infile, outpref, logf=None):
    """
    do 3dclust
    """
    if logf:
        lg = setLog._log(logf)
    lg.info("doing cluster (3dclust): \n%s" % infile)
    cmd = split("3dclust -prefix %s -1Dformat -nosum \
                -1dindex 1 -1tindex 1 -2thresh -%s %s \
                -dxyz=1 1.44 %s %s" %
                (outpref, vx_thr, vx_thr, clst_thr, infile))
    lg.info("Command: \n%s" % cmd)
    p = subprocess.run(cmd, stderr=subprocess.PIPE)
    lg.info(p.stderr.decode("utf-8", "strict"))
    lg.info("Done with cluster (3dclust).")