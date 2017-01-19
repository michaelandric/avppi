# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 19:54:37 2015

@author: andric
"""

import os
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from shlex import split
from setlog import setup_log


def mema(log, subj_list, cond, outpref, mask=None):
    """Do AFNI's 3dMema."""
    log.info('Doing mema ------------ \n')
    dat_dir = os.path.join(os.environ['avp'], 'nii',
                           'deconvolve_outs_ramps')

    d_set = []
    for subj in subj_list:
        d_set.append("%d %s %s" % (subj,
                                   os.path.join(dat_dir, "%s_coef_%d+tlrc" %
                                                (cond, subj)),
                                   os.path.join(dat_dir, "%s_tstat_%d+tlrc" %
                                                (cond, subj))))
    mema_args = split("3dMEMA -jobs 10 -prefix %s \
                      -mask %s -set %s %s -missing_data 0 -residual_Z" %
                      (outpref, mask, cond, ' '.join(d_set)))
    log.info('args for 3dMEMA: \n%s', mema_args)
    proc = Popen(mema_args, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())
    log.info('3dMEMA done.')


def main():
    """Wrap an call functions for MEMA."""
    subj_list = [s for s in range(1, 20)]
    subj_list.remove(3)
    subj_list.remove(11)

    logfile = setup_log(os.path.join(os.environ['avp'], 'logs',
                                     'MEMA_ramps'))
    conditions = ['ALowVLow_rampdown', 'ALowVLow_rampup',
                  'ALowVHigh_rampdown', 'ALowVHigh_rampup',
                  'AHighVLow_rampdown', 'AHighVLow_rampup',
                  'AHighVHigh_rampdown', 'AHighVHigh_rampup']
    mask = os.path.join(os.environ['avp'], 'nii', 'group_effects_dec',
                        'MNI152_T1_2mm_brain_mask_dil1+tlrc.BRIK.gz')

    for cc in conditions:
        outdir = os.path.join(os.environ['avp'], 'nii',
                              'deconvolve_outs_ramps')
        mema(logfile, subj_list, cc,
             os.path.join(outdir, '%s_mema_out' % cc),
             mask)


if __name__ == '__main__':
    main()
