# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 16:24:02 2015

@author: andric
"""

import os
from shlex import split
from subprocess import call, STDOUT


def ttest(stdoutdir, ss_list):
    """
    direct tests on comaprisons
    """
    effects = ['Aentr', 'Ventr', 'Aentr_intxn', 'Ventr_intxn']
    for ef in effects:
        a_sets = []
        for ss in ss_list:
            dat_dir = os.path.join(os.environ['avp'], 'nii',
                                   'ss%s_effects' % ss)
            coeff = os.path.join(dat_dir, '%s_ss%s_coef+tlrc' % (ef, ss))
            a_sets.append(coeff)
        a_sets = ' '.join(a_sets)
        f = open('%s/stdout_from_3dttest++_%s.txt' % (stdoutdir, ef), 'w')
        args = split('3dttest++ -setA %s -labelA %s \
                     -mask %s/MNI152_T1_2mm_brain_mask_dil1.nii.gz \
                     -prefix %s/ttest_%s' %
                     (a_sets, ef,
                      os.path.join(os.environ['FSLDIR'], 'data/standard'),
                      stdoutdir, ef))
        call(args, stdout=f, stderr=STDOUT)
        f.close()


if __name__ == '__main__':
    subj_list = range(1, 20)
    subj_list.remove(11)
    subj_list.remove(19)
    grp_eff_dir = os.path.join(os.environ['avp'], 'nii', 'group_effects')
    ttest(grp_eff_dir, subj_list)
