# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 16:08:25 2015

@author: andric
"""

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
    """
#    This is old alternative to make lvls:
#    lvls = []
#    for s in range(1, 19):
#        for c in ['A', 'V']:
#            for l in ['High', 'Low']:
#                lvls.append([c, l, s])
#    lvls = list(product(*[modal, amp, range(1, 20)]))
    l1 = list(product(*[range(1, 3), range(1, 3)]))
    # corresponds to sub-briks in REML out
    # 4: ALowVLow; 7: ALowVHigh; 10: AHighVLow; 13:AHighVHigh
    l2 = [4, 7, 10, 13]
    d = dict(zip(l1, l2))
    f_suffx = 'Powered.cleanEPI_REML_fnirted_MNI2mm.nii.gz'
    dset_form_lvls = list(product(*[range(1, 3), range(1, 3), ss_list]))
    dsets = []
    for lv in dset_form_lvls:
        """
        a: Aud/Vis
        b: High/Low
        c: subject
        """
        a, b, c = lv
        f_pref = 'decon_out.mion.%s_concat.%s' % (c, f_suffx)
        f_name = os.path.join(decon_dir, f_pref)
        sub_brk = d[a, b]
#        dsets.append('-dset %s %s %s \"%s[%d]\"' % (a, b, c, f_name, sub_brk))
        dsets.append("-dset %s %s %s '%s[%d]'" % (a, b, c, f_name, sub_brk))
    dsets = ' '.join(dsets)

    conds = ['A', 'V']
    amp = ['Low', 'High']
#    cond_names = []
#     cond_names = ['ALowVLow', 'ALowVHigh', 'AHighVLow', 'AHighVHigh']
#    for cc in list(combinations((product(*[conds, amp])), 2)):
#        if cc[0][0] is not cc[1][0]:
#            cond_names.append(''.join([''.join(cc[0]), ''.join(cc[1])]))
    ameans = []
    bmeans = []
    for i in range(1, 3):
        ameans.append('-amean %d %s' % (i, conds[i-1]))
        bmeans.append('-bmean %d %s' % (i, amp[i-1]))
    ameans = ' '.join(ameans)
    bmeans = ' '.join(bmeans)

    aa = '3dANOVA3 -type 4 -alevels 2 -blevels 2 -clevels %s %s %s %s -adiff 1 2 AudvsVis -bdiff 1 2 HighvsLow -bucket %s/anova_out.mion_concat' % (len(ss_list), dsets, ameans, bmeans, decon_dir)

    anova_args = split('3dANOVA3 -type 4 -alevels 2 -blevels 2 \
                       %s %s %s -adiff 1 2 AudvsVis -bdiff 1 2 HighvsLow \
                       -bucket %s/anova_out.mion_concat' %
                       (dsets, ameans, bmeans, decon_dir))
    f = open('%s/stdout_from_anova.txt' % decon_dir, 'w')
    print aa
    call(aa, shell=True)
#    call(anova_args, stdout=f, stderr=STDOUT)
    f.close()


if __name__ == '__main__':
    subj_list = range(1, 20)
    subj_list.remove(11)
    subj_list.remove(19)
    decondir = os.path.join(os.environ['avp'], 'nii', 'deconvolve_outs_concat')
    afni_anova3(decondir, subj_list)
