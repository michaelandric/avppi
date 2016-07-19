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


def calc_subt(log, file_a, file_b, outname_contr):
    """Setup contrast via 3dcalc."""
    log.info('Doing contrast %s - %s', file_a, file_b)
    cmdargs = split("3dcalc -a {} -b {} -expr 'a-b' -prefix {}".format(
        file_a, file_b, outname_contr))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def calc_mean(log, file_a, file_b, outname_mean):
    """Calcuate mean of the two."""
    log.info('Get mean of %s and %s', file_a, file_b)
    cmdargs = split("3dMean -prefix {} '{}' '{}'".format(
        outname_mean, file_a, file_b))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def make_subbrck_dict(vartype):
    """Make dictionary specifying sub brick correspondence."""
    conds = ['ALowVLow', 'ALowVHigh', 'AHighVLow', 'AHighVHigh']
    if vartype is 'coef':
        subbrk = [4, 7, 10, 13]
    elif vartype is 'tstat':
        subbrk = [5, 8, 11, 14]
    subbrk_cond_dict = dict(zip(conds, subbrk))
    return subbrk_cond_dict


def main():
    """Wrap methods in this main call.

    high/high - mean(high/low, low/high)
    mean(high/low, low/high) - low/low
    """
    subj_list = [s for s in range(1, 20)]
    subj_list.remove(3)
    subj_list.remove(11)
    decondir = os.path.join(os.environ['avp'], 'nii',
                            'deconvolve_outs_concat_dec')
    f_suffx = 'Powered.cleanEPI_REML_fnirted_MNI2mm.nii.gz'
    for vvar in ['coef', 'tstat']:
        cond_dict = make_subbrck_dict(vvar)

        for subj in subj_list:
            inpref = 'decon_out.mion.{}_concat'.format(subj)
            infile_a = os.path.join(decondir, '{}.{}[{}]'.format(
                inpref, f_suffx, cond_dict['AHighVLow']))
            infile_b = os.path.join(decondir, '{}.{}[{}]'.format(
                inpref, f_suffx, cond_dict['ALowVHigh']))
            fx_dir = os.path.join(os.environ['avp'], 'nii',
                                  'ss{}_effects_dec'.format(subj))
            mean_outname = os.path.join(fx_dir,
                                        'crossd_avg_ss{}_{}'.format(
                                            subj, vvar))
            logfile = setup_log(os.path.join(os.environ['avp'], 'logs',
                                             'calc_mean'))
            logfile.info('Doing calc_mean.')
            calc_mean(logfile, infile_a, infile_b, mean_outname)

            logfile = setup_log(os.path.join(os.environ['avp'], 'logs',
                                             'calc_subt'))
            logfile.info('Doing calc_subt.')
            hh_file = os.path.join(decondir, '{}.{}[{}]'.format(
                inpref, f_suffx, cond_dict['AHighVHigh']))
            hhout_contr = os.path.join(fx_dir, 'high_grad_ss{}_{}'.format(
                subj, vvar))
            calc_subt(logfile, hh_file, '{}+tlrc'.format(mean_outname),
                      hhout_contr)

            ll_file = os.path.join(decondir, '{}.{}[{}]'.format(
                inpref, f_suffx, cond_dict['ALowVLow']))
            llout_contr = os.path.join(fx_dir, 'low_grad_ss{}_{}'.format(
                subj, vvar))
            calc_subt(logfile, '{}+tlrc'.format(mean_outname), ll_file,
                      llout_contr)


if __name__ == '__main__':
    main()
