# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 18:31:04 2016
This version does different block lengths
by using censor files

@author: andric
"""

import os
import sys
from shlex import split
from subprocess import call, STDOUT


def deconv(stdoutdir, inputset, seq, censorf, wmfile, ventfile, outpref):
    """
    3dDeconvolve with multiple inputs
    There are 4 inputs
    because per subject there are 4 runs
    """
    tdir = '/mnt/lnif-storage/urihas/AVaudvisppi/timing'
    sf_list = []
    for i in range(6):
        sf_list.append(os.path.join(tdir,
                                    'concat_stim_times_cond%s.txt' % i))
    f = open('%s/stdout_from_deconv.txt' % stdoutdir, 'w')
    deconargs = split("3dDeconvolve -jobs 2 -input %s \
                      -force_TR 1.5 -polort A \
                      -censor %s \
                      -nodmbase -num_stimts 8 \
                      -stim_times 1 %s 'GAM' \
                      -stim_label 1 fixate \
                      -stim_times 2 %s 'MION(30)' \
                      -stim_label 2 ALowVLow \
                      -stim_times 3 %s 'MION(30)' \
                      -stim_label 3 ALowVHigh \
                      -stim_times 4 %s 'MION(30)' \
                      -stim_label 4 AHighVLow \
                      -stim_times 5 %s 'MION(30)' \
                      -stim_label 5 AHighVHigh \
                      -stim_times 6 %s 'GAM' \
                      -stim_label 6 catch \
                      -stim_file 7 %s \
                      -stim_label 7 WM \
                      -stim_file 8 %s \
                      -stim_label 8 VENT \
                      -gltsym 'SYM: +ALowVLow' -glt_label 1 ALowVLow_glt \
                      -gltsym 'SYM: +ALowVHigh' -glt_label 2 ALowVHigh_glt \
                      -gltsym 'SYM: +AHighVLow' -glt_label 3 AHighVLow_glt \
                      -gltsym 'SYM: +AHighVHigh' -glt_label 4 AHighVHigh_glt \
                      -gltsym 'SYM: +AHighVHigh +AHighVLow \
                      -ALowVHigh -ALowVLow' -glt_label 5 AHigh \
                      -gltsym 'SYM: +AHighVHigh +ALowVHigh \
                      -AHighVLow -ALowVLow' -glt_label 6 VHigh \
                      -fout -tout -errts %s_errts -bucket %s -x1D %s.xmat.1D" %
                      (inputset, censorf, sf_list[0], sf_list[1], sf_list[2],
                       sf_list[3], sf_list[4], sf_list[5],
                       wmfile, ventfile, outpref, outpref, outpref))
    call(deconargs, stdout=f, stderr=STDOUT)
    f.close()

    rf = open('%s/stdout_from_reml.txt' % stdoutdir, 'w')
    reml = split('3dREMLfit -matrix %s.xmat.1D \
                 -input "%s" \
                 -fout -tout -Rbuck %s_REML -Rvar %s_REMLvar \
                 -Rerrts %s_errts_REML -verb' %
                 (outpref, inputset, outpref, outpref, outpref))
    call(reml, stdout=rf, stderr=STDOUT)
    rf.close()


if __name__ == '__main__':
    ss = sys.argv[1]
    inputs = []
    for seq in range(1, 5):
        infname = 'v8.%s_%s.Powered.cleanEPI.uncensored.nii.gz' % (ss, seq)
        infile = os.path.join(os.environ['avp'], 'nii', infname)
        inputs.append(infile)
    inputs = ' '.join(inputs)

    sfx = 'Powered.cleanEPI.uncensored.txt'
    wm_name = 'wm_v8.%s_all.%s' % (ss, sfx)
    wm_file = os.path.join(os.environ['avp'], 'nii',
                           '%s_CNR.anat' % ss, wm_name)
    vent_name = 'vent_v8.%s_all.%s' % (ss, sfx)
    vent_file = os.path.join(os.environ['avp'], 'nii',
                             '%s_CNR.anat' % ss, vent_name)
    for block in [20, 15, 10]:
        cf = os.path.join('/mnt/lnif-storage/urihas/AVaudvisppi/timing',
                          'all_ts.block%s.%s.Powered.censor.1D' % (block, ss))
        outpref = 'decon_out.mion.%s_concat.Powered.cleanEPI_%sblk' % (ss, block)
        decon_outdir = os.path.join(os.environ['avp'], 'nii',
                                    'deconvolve_outs_concat_%sblk' % block)
        outfile = os.path.join(decon_outdir, outpref)
        deconv(decon_outdir, inputs, seq, cf, wm_file, vent_file, outfile)
