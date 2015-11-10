# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 19:54:37 2015

@author: andric
"""

import os
from subprocess import call, STDOUT
from shlex import split


def calc3d_4cond(stdoutdir, ss, input):
    """
    Get difference measures
    ------------
    A1: Auditory Entropy
    (AHighVHigh + AHighVLow) vs. (ALowVHigh + ALowVLow)
    ------------
    V1: Visual Entropy
    (AHighVHigh + ALowVHigh) vs. (ALowVLow + AHighVLow)
    ------------
    Interactions
    (AHighVHigh - ALowVHigh) - (AHighVLow - ALowVLow)
    (AHighVHigh - ALowVLow) - (AHighVLow - ALowVHigh)
    """
    conds = ['ALowVLow', 'ALowVHigh', 'AHighVLow', 'AHighVHigh']
    for tt in ['coef', 'tstat']:
        if tt is 'coef':
            sb = [4, 7, 10, 13]
        elif tt is 'tstat':
            sb = [5, 8, 11, 14]
        d = dict(zip(conds, sb))
        print 'doing Subj %s -- %s... \n' % (ss, tt)
        f = open('%s/stdout_from_3dcalc.txt' % stdoutdir, 'w')
        A_ef_args = "3dcalc -a '%s[%d]' -b '%s[%d]' -c '%s[%d]' -d '%s[%d]' \
                    -expr '(a+b)-(c+d)' -prefix %s/Aentr_ss%s_%s" % \
                    (input, d['AHighVHigh'], input, d['AHighVLow'],
                     input, d['ALowVHigh'], input, d['ALowVLow'],
                     stdoutdir, ss, tt)
        V_ef_args = "3dcalc -a '%s[%d]' -b '%s[%d]' -c '%s[%d]' -d '%s[%d]' \
                    -expr '(a+b)-(c+d)' -prefix %s/Ventr_ss%s_%s" % \
                    (input, d['AHighVHigh'], input, d['ALowVHigh'],
                     input, d['AHighVLow'], input, d['ALowVLow'],
                     stdoutdir, ss, tt)
        A_intxn_args = "3dcalc -a '%s[%d]' -b '%s[%d]' -c '%s[%d]' -d '%s[%d]' \
                       -expr '(a-b)-(c-d)' -prefix %s/Aentr_intxn_ss%s_%s" % \
                       (input, d['AHighVHigh'], input, d['ALowVHigh'],
                        input, d['AHighVLow'], input, d['ALowVLow'],
                        stdoutdir, ss, tt)
        V_intxn_args = "3dcalc -a '%s[%d]' -b '%s[%d]' -c '%s[%d]' -d '%s[%d]' \
                       -expr '(a-b)-(c-d)' -prefix %s/Ventr_intxn_ss%s_%s" % \
                       (input, d['AHighVHigh'], input, d['AHighVLow'],
                        input, d['ALowVHigh'], input, d['ALowVLow'],
                        stdoutdir, ss, tt)

        call(['echo', 'Doing A main effects ...'], stdout=f, stderr=STDOUT)
        call(A_ef_args, stdout=f, stderr=STDOUT, shell=True)
        call(['echo', 'Doing A main effects ...'], stdout=f, stderr=STDOUT)
        call(V_ef_args, stdout=f, stderr=STDOUT, shell=True)
        call(['echo', 'Doing interaction ...'], stdout=f, stderr=STDOUT)
        call(A_intxn_args, stdout=f, stderr=STDOUT, shell=True)
        call(['echo', 'Doing interaction ...'], stdout=f, stderr=STDOUT)
        call(V_intxn_args, stdout=f, stderr=STDOUT, shell=True)
        f.close()


def mema(stdoutdir, ss_list):
    """
    AFNI's 3dMema
    """
    effects = ['Aentr', 'Ventr', 'Aentr_intxn', 'Ventr_intxn']
    for ef in effects:
        diff_set = []
        for s in ss_list:
            dat_dir = os.path.join(os.environ['avp'], 'nii',
                                   'ss%s_effects' % s)
            coeff = os.path.join(dat_dir, '%s_ss%s_coef+tlrc' % (ef, s))
            tstatf = os.path.join(dat_dir, '%s_ss%s_tstat+tlrc' % (ef, s))
            diff_set.append('%d %s %s' %
                            (s, coeff, tstatf))
        diff_set = ' '.join(diff_set)
        f = open('%s/stdout_from_3dmema_%s.txt' % (stdoutdir, ef), 'w')
        mema_args = '3dMEMA -jobs 4 -prefix %s/%s_mema \
                    -set %s %s -missing_data 0' % \
                    (stdoutdir, ef, ef, diff_set)
        print ''.join(mema_args)
        call(['echo', ' '.join(mema_args)], stdout=f)
        call(mema_args, stdout=f, stderr=STDOUT, shell=True)
        f.close()


def mema2(stdoutdir, ss_list):
    """
    AFNI's 3dMema
    """
    effects = ['Aentr', 'Ventr', 'Aentr_intxn', 'Ventr_intxn']
    for ef in effects:
        diff_set = []
        for s in ss_list:
            dat_dir = os.path.join(os.environ['avp'], 'nii',
                                   'ss%s_effects' % s)
            coeff = os.path.join(dat_dir, '%s_ss%s_coef+tlrc' % (ef, s))
            tstatf = os.path.join(dat_dir, '%s_ss%s_tstat+tlrc' % (ef, s))
            diff_set.append('%d %s %s' %
                            (s, coeff, tstatf))
        diff_set = ' '.join(diff_set)
        f = open('%s/stdout_from_3dmema_%s.txt' % (stdoutdir, ef), 'w')
        mema_args = '3dMEMA -jobs 4 -prefix %s/%s_mema2 \
                    -set %s %s -max_zeros 0.25 \
                    -model_outliers -residual_Z' % \
                    (stdoutdir, ef, ef, diff_set)
        print ''.join(mema_args)
        call(['echo', ''.join(mema_args)], stdout=f)
        call(mema_args, stdout=f, stderr=STDOUT, shell=True)
        f.close()


if __name__ == '__main__':
    subj_list = range(1, 20)
    subj_list.remove(11)
    subj_list.remove(19)

    decondir = os.path.join(os.environ['avp'], 'nii', 'deconvolve_outs_concat')
#    conds = ['ALowVLow', 'ALowVHigh', 'AHighVLow', 'AHighVHigh']
    f_suffx = 'Powered.cleanEPI_REML_fnirted_MNI2mm.nii.gz'
    for ss in subj_list:
        inpref = 'decon_out.mion.%s_concat' % ss
        infile = os.path.join(decondir, '%s.%s' % (inpref, f_suffx))
        fx_dir = os.path.join(os.environ['avp'], 'nii', 'ss%s_effects' % ss)
        if not os.path.exists(fx_dir):
            os.makedirs(fx_dir)
#        calc3d_4cond(fx_dir, ss, infile)

    groupdir = os.path.join(os.environ['avp'], 'nii', 'group_effects')
#    mema(groupdir, subj_list)
    mema2(groupdir, subj_list)
