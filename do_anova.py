# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 14:54:25 2015

@author: andric
"""

import os
from shlex import split
from subprocess import call, STDOUT
from itertools import product, combinations


def afni_anova3(decon_dir, ss_list):
    """
    analysis of variance
    with mixed effects
    2 x 2 within participants
    factor A: Modality (audio/visual aka A/V)
    factor B: entropy (High/Low)
    THIS IS NOT REALLY PROPER BCS
    THE DESIGN IS NOT REALLY 2x2
    IT IS 1x4. THERE IS ALWAYS A and V.
    """
    os.chdir(decon_dir)
    print os.getcwd()
    l1 = list(product(*[range(1, 3), range(1, 3)]))
    # corresponds to sub-briks in REML out
    # 4: ALowVLow; 7: ALowVHigh; 10: AHighVLow; 13:AHighVHigh
    l2 = [4, 7, 10, 13]
    d = dict(zip(l1, l2))
    f_suffx = 'Powered.cleanEPI_REML_fnirted_MNI2mm.nii.gz'
    dset_form_lvls = list(product(*[range(1, 3), range(1, 3),
                                    range(1, len(ss_list)+1)]))
    dsets = []
    for lv in dset_form_lvls:
        """
        a: Aud/Vis
        b: High/Low
        c: subject
        """
        a, b, c = lv
        f_name = 'decon_out.mion.%s_concat.%s' % (ss_list[c-1], f_suffx)
        sub_brk = d[a, b]
        dsets.append("-dset %d %d %d '%s[%d]'" % (a, b, c, f_name, sub_brk))
    dsets = ' '.join(dsets)

    conds = ['A', 'V']
    amp = ['Low', 'High']
    ameans = []
    bmeans = []
    for i in range(1, 3):
        ameans.append('-amean %d %s' % (i, conds[i-1]))
        bmeans.append('-bmean %d %s' % (i, amp[i-1]))
    ameans = ' '.join(ameans)
    bmeans = ' '.join(bmeans)

    aa = '3dANOVA3 -type 4 -alevels 2 -blevels 2 -clevels %d %s \
        -fa %s_fstat -fb %s_fstat -fab %s_intrxn %s %s \
        -adiff 1 2 AudvsVis -bdiff 1 2 HighvsLow \
        -bucket anova2_out.mion_concat.nii.gz' % \
        (len(ss_list), dsets, ''.join(conds), ''.join(amp),
         ''.join([''.join(conds), ''.join(amp)]), ameans, bmeans)
    f = open('stdout_from_anova.txt', 'w')
    print aa
    call(aa, shell=True)
    f.close()


def anova2(stdoutdir, ss_list):
    decondir = os.path.join(os.environ['avp'], 'nii', 'deconvolve_outs_concat')
    f_suffx = 'Powered.cleanEPI_REML_fnirted_MNI2mm.nii.gz'
    dsets = []
    ameans = []
    cond_list = ['ALowVLow', 'ALowVHigh', 'AHighVLow', 'AHighVHigh']
    sb = [4, 7, 10, 13]
    d = dict(zip(cond_list, sb))
    for i, cond_name in enumerate(cond_list):
        ameans.append('-amean %d %s_mean' % (i+1, cond_name))
        for j, ss in enumerate(ss_list):
            dset_name = 'decon_out.mion.%s_concat.%s' % (ss, f_suffx)
            dsets.append("-dset %d %d '%s[%d]'" %
                         (i+1, j+1, os.path.join(decondir, dset_name),
                          d[cond_name]))

    ameans = ' '.join(ameans)
    dsets = ' '.join(dsets)
    f = open('%s/stdout_from_3dANOVA2.txt' % stdoutdir, 'w')
    cmdargs = '3dANOVA2 -type 3 -alevels 4 -blevels %d \
              %s -fa all_fstat %s -mask %s \
              -acontr -1 -1 1 1 AHigh \
              -acontr -1 1 -1 1 VHigh \
              -bucket %s/anova2_out' % \
              (len(ss_list), dsets, ameans,
               os.path.join(os.environ['FSLDIR'], 'data/standard',
                            'MNI152_T1_2mm_brain_mask_dil1.nii.gz'), stdoutdir)
    call(cmdargs, stdout=f, stderr=STDOUT, shell=True)
    f.close()


if __name__ == '__main__':
    subj_list = range(1, 20)
    subj_list.remove(11)
    subj_list.remove(19)
    decondir = os.path.join(os.environ['avp'], 'nii', 'deconvolve_outs_concat')
    grp_eff_dir = os.path.join(os.environ['avp'], 'nii', 'group_effects')
#    afni_anova3(decondir, subj_list)
    anova2(grp_eff_dir, subj_list)
