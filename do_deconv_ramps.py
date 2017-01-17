# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 14:42:18 2015

This differs from do_deconvMION_condory.py
because here users multiple input datasets

@author: andric
"""

import os
import sys
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from setlog import setup_log


def deconv(log, stdoutdir, inputset, deconv_fnames):
    """3dDeconvolve with multiple inputs.

    arg: inputset
        This is a list of inputfile. They follow the '-input' flag.
        There are 4 inputs in inputset because per subject there are 4 runs.
    arg: deconv_fnames
        This is a dictionary that holds other various files, e.g., regressors
        and the outputprefix
    """
    log.info('Deconvolve ramps.')
    log.info('Outpref: %s', deconv_fnames['outpref'])
    tdir = '/mnt/lnif-storage/urihas/AVaudvisppi/timing'
    sf_list = []
    for i in range(6):
        sf_list.append(os.path.join(tdir,
                                    'concat_stim_times_cond%s.txt' % i))

    deconargs = split("3dDeconvolve -jobs 2 -input %s \
                      -force_TR 1.5 -polort A \
                      -censor %s \
                      -nodmbase -num_stimts 12 \
                      -stim_times 1 %s 'GAM' \
                      -stim_label 1 fixate \
                      -stim_times 2 %s 'WAV(0,2,0,12,0,0)' \
                      -stim_label 2 ALowVLow_rampdown \
                      -stim_times 3 %s 'WAV(0,2,12,0,0,0)' \
                      -stim_label 3 ALowVLow_rampup \
                      -stim_times 4 %s 'WAV(0,2,0,12,0,0)' \
                      -stim_label 4 ALowVHigh_rampdown \
                      -stim_times 5 %s 'WAV(0,2,12,0,0,0)' \
                      -stim_label 5 ALowVHigh_rampup \
                      -stim_times 6 %s 'WAV(0,2,0,12,0,0)' \
                      -stim_label 6 AHighVLow_rampdown \
                      -stim_times 7 %s 'WAV(0,2,12,0,0,0)' \
                      -stim_label 7 AHighVLow_rampup \
                      -stim_times 8 %s 'WAV(0,2,0,12,0,0)' \
                      -stim_label 8 AHighVHigh_rampdown \
                      -stim_times 9 %s 'WAV(0,2,12,0,0,0)' \
                      -stim_label 9 AHighVHigh_rampup \
                      -stim_times 10 %s 'GAM' \
                      -stim_label 10 catch \
                      -stim_file 11 %s \
                      -stim_label 11 WM \
                      -stim_file 12 %s \
                      -stim_label 12 VENT \
                      -gltsym 'SYM: +ALowVLow_rampdown +ALowVHigh_rampdown \
                      +AHighVLow_rampdown +AHighVHigh_rampdown \
                      -ALowVLow_rampup -ALowVHigh_rampup -AHighVLow_rampup \
                      -AHighVHigh_rampup' -glt_label 1 rampdown_vs_rampup \
                      -fout -tout -errts %s_errts -bucket %s -x1D %s.xmat.1D" %
                      (inputset, deconv_fnames['cf'], sf_list[0],
                       sf_list[1], sf_list[1], sf_list[2], sf_list[2],
                       sf_list[3], sf_list[3], sf_list[4], sf_list[4],
                       sf_list[5],
                       deconv_fnames['wm_file'], deconv_fnames['vent_file'],
                       deconv_fnames['outpref'], deconv_fnames['outpref'],
                       deconv_fnames['outpref']))
    proc = Popen(deconargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())

    reml = split('3dREMLfit -matrix %s.xmat.1D \
                 -input "%s" \
                 -fout -tout -Rbuck %s_REML -Rvar %s_REMLvar \
                 -Rerrts %s_errts_REML -verb' %
                 (deconv_fnames['outpref'], inputset, deconv_fnames['outpref'],
                  deconv_fnames['outpref'], deconv_fnames['outpref']))
    proc = Popen(reml, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def set_inputs(subj):
    """Set file names for this run."""
    inputs = []
    for seq in range(1, 5):
        infname = 'v8.%s_%s.Powered.cleanEPI.uncensored.nii.gz' % (subj, seq)
        infile = os.path.join(os.environ['avp'], 'nii', infname)
        inputs.append(infile)
    inputfiles = ' '.join(inputs)

    return inputfiles


def set_fnames(subj, decondir):
    """Create dictionary with names."""
    fnames = dict()
    outpref = 'decon_out.ramps_wav.%s_concat.Powered.cleanEPI' % subj
    sfx = 'Powered.cleanEPI.uncensored.txt'
    wm_name = 'wm_v8.%s_all.%s' % (subj, sfx)
    fnames['wm_file'] = os.path.join(os.environ['avp'], 'nii',
                                     '%s_CNR.anat' % subj, wm_name)
    vent_name = 'vent_v8.%s_all.%s' % (subj, sfx)
    fnames['vent_file'] = os.path.join(os.environ['avp'], 'nii',
                                       '%s_CNR.anat' % subj, vent_name)
    fnames['cf'] = os.path.join(os.environ['avp'], 'nii',
                                'all_ts.%s.Powered.censor.1D' % subj)
    fnames['outpref'] = os.path.join(decondir, outpref)

    return fnames


def main():
    """Call methods for main execution."""
    decon_outdir = os.path.join(os.environ['avp'],
                                'nii', 'deconvolve_outs_ramps')
    logfile = setup_log(os.path.join(os.environ['avp'], 'logs',
                                     'do_deconv_ramps_%s' % sys.argv[1]))

    deconv(logfile, decon_outdir, set_inputs(sys.argv[1]),
           set_fnames(sys.argv[1], decon_outdir))


if __name__ == '__main__':
    main()
