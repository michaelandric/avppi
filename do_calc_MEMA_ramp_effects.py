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


def calc_conds(log, subj, rmp, tt):
    """
    Calculate difference maps and interaction.

    arg: rmp
        This is for the ramp type: 'rampup' or 'rampdown'
    arg: tt
        This is 'coef' or 'tstat
    """
    log.info("Calculate condition differences.")
    os.chdir(os.path.join(os.environ['avp'], 'nii', 'deconvolve_outs_ramps'))
    A_ef = split("3dcalc -a %s -b %s -c %s -d %s \
                 -expr '(a+b)-(c+d)' -prefix %s" %
                 ('AHighVHigh_%s_%s_%d+tlrc' % (subj, tt, rmp),
                  'AHighVLow_%s_%s_%d+tlrc' % (subj, tt, rmp),
                  'ALowVHigh_%s_%s_%d+tlrc' % (subj, tt, rmp),
                  'ALowVLow_%s_%s_%d+tlrc' % (subj, tt, rmp),
                  os.path.join(os.environ['avp'], 'nii', 'ramp_effects',
                               'A_%s_%s_%d' % (rmp, tt, subj))))
    log.info("Args: \n%s", A_ef)
    proc = Popen(A_ef, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())

    V_ef = split("3dcalc -a %s -b %s -c %s -d %s \
                 -expr '(a+b)-(c+d)' -prefix %s" %
                 ('AHighVHigh_%s_%s_%d+tlrc' % (subj, tt, rmp),
                  'ALowVHigh_%s_%s_%d+tlrc' % (subj, tt, rmp),
                  'AHighVLow_%s_%s_%d+tlrc' % (subj, tt, rmp),
                  'ALowVLow_%s_%s_%d+tlrc' % (subj, tt, rmp),
                  os.path.join(os.environ['avp'], 'nii', 'ramp_effects',
                               'V_%s_%s_%d' % (rmp, tt, subj))))
    log.info("Args: \n%s", V_ef)
    proc = Popen(V_ef, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())

    Intxn_ef = split("3dcalc -a %s -b %s -c %s -d %s \
                     -expr '(a-b)-(c-d)' -prefix %s" %
                     ('AHighVHigh_%s_%s_%d+tlrc' % (subj, tt, rmp),
                      'ALowVHigh_%s_%s_%d+tlrc' % (subj, tt, rmp),
                      'AHighVLow_%s_%s_%d+tlrc' % (subj, tt, rmp),
                      'ALowVLow_%s_%s_%d+tlrc' % (subj, tt, rmp),
                      os.path.join(os.environ['avp'], 'nii',
                                   'ramp_effects',
                                   'Intxn_%s_%s_%d' % (rmp, tt, subj))))
    log.info("Args: \n%s", Intxn_ef)
    proc = Popen(Intxn_ef, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def mema_ef(log, subj_list, cond, rmp, outpref, mask=None):
    """Do MEMA analysis on calculated effects."""
    log.info('Doing mema ------------ \n')
    dat_dir = os.path.join(os.environ['avp'], 'nii',
                           'ramp_effects')

    d_set = []
    for subj in subj_list:
        d_set.append("%d %s %s" % (subj,
                                   os.path.join(dat_dir, "%s_%s_coef_%d+tlrc" %
                                                (cond, rmp, subj)),
                                   os.path.join(dat_dir, "%s_%s_tstat_%d+tlrc" %
                                                (cond, rmp, subj))))
    mema_args = split("3dMEMA -jobs 10 -prefix %s \
                      -mask %s -set %s %s -missing_data 0 -residual_Z" %
                      (outpref, mask, cond, ' '.join(d_set)))
    log.info('args for 3dMEMA: \n%s', mema_args)
    proc = Popen(mema_args, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())
    log.info('3dMEMA done.')


def main():
    """Wrap and call functions for 3dcalc and MEMA."""
    subj_list = [s for s in range(1, 20)]
    subj_list.remove(3)
    subj_list.remove(11)
    logfile = setup_log(os.path.join(os.environ['avp'], 'logs',
                                     'calc_MEMA_ramp_effects'))
    mask = os.path.join(os.environ['avp'], 'nii', 'group_effects_dec',
                        'MNI152_T1_2mm_brain_mask_dil1+tlrc.BRIK.gz')

    for ramp in ['rampup', 'rampdown']:
        for subject in subj_list:
            for stat in ['coef', 'tstat']:
                calc_conds(logfile, subject, ramp, stat)

        for condition in ["A", "V", "Intxn"]:
            outname = os.path.join(os.path.join(os.environ['avp'], 'nii',
                                                'ramp_effects'),
                                   '%s_%s_mema_out' % (condition, ramp))
            mema_ef(logfile, subj_list, condition, ramp, outname, mask)


if __name__ == '__main__':
    main()
