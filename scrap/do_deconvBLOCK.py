# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 13:12:19 2015

@author: andric
"""

import os
from shlex import split
from subprocess import call, STDOUT


def deconv(stdoutdir, input, seq, outpref):
    """
    deconvolve
    """
    tdir = '/mnt/lnif-storage/urihas/AVaudvisppi/timing'
    sf_list = []
    for i in range(6):
        sf_list.append(os.path.join(tdir,
                                    'decon_seq%s_cond%s.txt' % (seq, i)))
    f = open('%s/stdout_from_deconv.txt' % stdoutdir, 'w')
    deconargs = split("3dDeconvolve -input %s -polort A \
                      -nodmbase -num_stimts 6 \
                      -stim_times 1 %s 'GAM' \
                      -stim_label 1 fixate \
                      -stim_times 2 %s 'BLOCK(30,1)' \
                      -stim_label 2 cond1 \
                      -stim_times 3 %s 'BLOCK(30,1)' \
                      -stim_label 3 cond2 \
                      -stim_times 4 %s 'BLOCK(30,1)' \
                      -stim_label 4 cond3 \
                      -stim_times 5 %s 'BLOCK(30,1)' \
                      -stim_label 5 cond4 \
                      -stim_times 6 %s 'GAM' \
                      -stim_label 6 catch \
                      -gltsym 'SYM: +cond1' -glt_label 1 cond1glt \
                      -gltsym 'SYM: +cond2' -glt_label 2 cond2glt \
                      -gltsym 'SYM: +cond3' -glt_label 3 cond3glt \
                      -gltsym 'SYM: +cond4' -glt_label 4 cond4glt \
                      -fout -tout -errts %s_errts -bucket %s -x1D %s.xmat.1D" %
                      (input, sf_list[0], sf_list[1], sf_list[2], sf_list[3],
                       sf_list[4], sf_list[5], outpref, outpref, outpref))
    call(deconargs, stdout=f, stderr=STDOUT)
    f.close()


if __name__ == '__main__':
    # ss_list = range(1, 20)
    ss_list = [10]
    for ss in ss_list:
        for seq in range(1, 5):
            infname = 'v8.%s_%s.Powered.cleanEPI.nii.gz' % (ss, seq)
            infile = os.path.join(os.environ['avp'], 'nii', infname)
            decon_outdir = os.path.join(os.environ['avp'],
                                        'nii', 'deconvolve_outs')
            outpref = 'decon_out.%s_%s.Powered.cleanEPI' % (ss, seq)
            outfile = os.path.join(decon_outdir, outpref)
            deconv(decon_outdir, infile, seq, outfile)
