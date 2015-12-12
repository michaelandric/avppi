# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 16:24:02 2015

@author: andric
"""

import os
import setLog
from shlex import split
import subprocess


def ttest(stdoutdir, ss_list, ef, outpref):
    """
    direct tests on comaprisons
    """
    lg = setLog._log('ttest')
    lg.info('Doing ttest in %s' % stdoutdir)

    a_sets = []
    for ss in ss_list:
        dat_dir = os.path.join(os.environ['avp'], 'nii',
                               'ss%s_effects' % ss)
        coeff = os.path.join(dat_dir, '%s_ss%s_coef+tlrc' % (ef, ss))
        a_sets.append(coeff)
    a_sets = ' '.join(a_sets)
    args = split('3dttest++ -setA %s -labelA %s \
                 -mask %s/MNI152_T1_2mm_brain_mask_dil1.nii.gz \
                 -prefix %s' %
                 (a_sets, ef,
                  os.path.join(os.environ['FSLDIR'], 'data/standard'),
                  outpref))
    lg.info('args: \n%s' % args)
    p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    lg.info(p.stderr.decode("utf-8", "strict"))
    lg.info('ttest done')


if __name__ == '__main__':
    subj_list = [s for s in range(1, 20)]
    subj_list.remove(3)
    subj_list.remove(11)

    grp_eff_dir = os.path.join(os.environ['avp'], 'nii', 'group_effects')
    effects = ['Aentr', 'Ventr', 'Aentr_intxn', 'Ventr_intxn']
    for ef in effects:
        outn = os.path.join(grp_eff_dir, 'ttest_flt2_%s' % ef)
        ttest(grp_eff_dir, subj_list, ef, outn)
