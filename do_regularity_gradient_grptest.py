# -*- coding: utf-8 -*-
"""
Created Jul 19 2016.

(AFNI doesn't work in 3+)
@author: andric
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from setlog import setup_log


def mema(log, level, subjectlist, outname_mema):
    """Model effects with AFNI's 3dMema."""
    mask = os.path.join(os.environ['avp'], 'nii', 'regularity_gradient',
                        'MNI152_T1_2mm_brain_mask_dil1+tlrc.BRIK.gz')
    diff_set_list = []
    for subject in subjectlist:
        dat_dir = os.path.join(os.environ['avp'], 'nii',
                               'ss{}_effects_dec'.format(subject))
        coeff = os.path.join(dat_dir, '{}_grad_ss{}_coef+tlrc'.format(
            level, subject))
        tstatf = os.path.join(dat_dir, '{}_grad_ss{}_tstat+tlrc'.format(
            level, subject))
        diff_set_list.append('{} {} {}'.format(subject, coeff, tstatf))
    diff_set = ' '.join(diff_set_list)
    mema_args = split('3dMEMA -jobs 20 -prefix {} \
                      -mask {} -set {} {} -missing_data 0 \
                      -residual_Z'.format(
                          outname_mema, mask, level, diff_set))
    log.info('args for 3dMEMA: \n%s', mema_args)
    proc = Popen(mema_args, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def main():
    """Wrap method to execute in main.

    high/high - mean(high/low, low/high)
    mean(high/low, low/high) - low/low
    """
    subj_list = [s for s in range(1, 20)]
    subj_list.remove(3)
    subj_list.remove(11)

    logfile = setup_log(os.path.join(os.environ['avp'], 'logs',
                                     'do_regularity_gradient_grptest'))
    logfile.info('Doing regularity_gradient_grptest.')
    logfile.info('Doing 3dMEMA.')
    for lvl in ['high', 'low']:
        mema_out = os.path.join(os.environ['avp'], 'nii',
                                'regularity_gradient',
                                '{}_grad_flt2_msk_mema'.format(lvl))
        mema(logfile, lvl, subj_list, mema_out)


if __name__ == '__main__':
    main()
