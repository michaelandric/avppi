# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 13:12:19 2015

@author: andric
"""

import os
import sys
from shlex import split
from subprocess import call, STDOUT


def deconv(stdoutdir, input, seq, censorf, outpref):
    """
    deconvolve
    """
    tdir = '/mnt/lnif-storage/urihas/AVaudvisppi/timing'
    sf_list = []
    for i in range(6):
        sf_list.append(os.path.join(tdir,
                                    'decon_seq%s_cond%s.txt' % (seq, i)))
    f = open('%s/stdout_from_deconv.txt' % stdoutdir, 'w')
    deconargs = split("3dDeconvolve -input %s \
                      -force_TR 1.5 -polort A \
                      -censor %s \
                      -nodmbase -num_stimts 6 \
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
                      -gltsym 'SYM: +ALowVLow' -glt_label 1 ALowVLow_glt \
                      -gltsym 'SYM: +ALowVHigh' -glt_label 2 ALowVHigh_glt \
                      -gltsym 'SYM: +AHighVLow' -glt_label 3 AHighVLow_glt \
                      -gltsym 'SYM: +AHighVHigh' -glt_label 4 AHighVHigh_glt \
                      -gltsym 'SYM: +AHighVHigh +AHighVLow \
                      -ALowVHigh -ALowVLow' -glt_label 5 AHigh \
                      -gltsym 'SYM: +AHighVHigh +ALowVHigh \
                      -AHighVLow -ALowVLow' -glt_label 6 VHigh \
                      -fout -tout -errts %s_errts -bucket %s -x1D %s.xmat.1D" %
                      (input, censorf, sf_list[0], sf_list[1], sf_list[2],
                       sf_list[3], sf_list[4], sf_list[5],
                       outpref, outpref, outpref))
    call(deconargs, stdout=f, stderr=STDOUT)
    f.close()


if __name__ == '__main__':
    ss = sys.argv[1]
    for seq in range(1, 5):
        infname = 'v8.%s_%s.Powered.cleanEPI.uncensored.nii.gz' % (ss, seq)
        infile = os.path.join(os.environ['avp'], 'nii', infname)
        decon_outdir = os.path.join(os.environ['avp'],
                                    'nii', 'deconvolve_outs')
        outpref = 'decon_out.mion.%s_%s.Powered.cleanEPI' % (ss, seq)
        cf = os.path.join(os.environ['avp'], 'nii',
                          '%s_preproc/%s_%s/%s_%s.Powered.censor.1D' %
                          (ss, ss, seq, ss, seq))
        outfile = os.path.join(decon_outdir, outpref)
        deconv(decon_outdir, infile, seq, cf, outfile)
