# @andric
# do 3dANOVA*
# June 6 2016
# =====================

"""Doing 3dANOVA2 for more traditional analysis.

Named 'do_anova_group_trad.py' because trying an anova in a
way that is more traditional (but not as powerful) as what
I did in 3dMEMA.

Note:
    # corresponds to sub-briks in REML out
    # 4: ALowVLow; 7: ALowVHigh; 10: AHighVLow; 13:AHighVHigh
"""

import os
from setlog import setup_log
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


def afni_anova(log, subj_list, outname):
    """Run AFNI 3dANOVA3."""
    log.info('Doing 3dANOVA2')

    ameans, dsets = build_anova_input(log, subj_list)
    cmdargs = split('3dANOVA2 -type 3 -alevels 4 -blevels %d \
                    %s -fa all_fstat %s -fab intxn_fstat -mask %s \
                    -acontr -1 -1 1 1 AHigh \
                    -acontr -1 1 -1 1 VHigh \
                    -bucket %s' %
                    (len(subj_list), dsets, ameans,
                     os.path.join(os.environ['FSLDIR'], 'data/standard',
                                  'MNI152_T1_2mm_brain_mask_dil1.nii.gz'),
                     outname))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def build_anova_input(log, subj_list):
    """Build the input list for afni_anova."""
    log.info('Doing build_anova_input...')
    f_suffx = 'Powered.cleanEPI_REML_fnirted_MNI2mm.nii.gz'
    decondir = os.path.join(os.environ['avp'], 'nii',
                            'deconvolve_outs_concat_dec')
    dsets = []
    ameans = []
    conditions = ['ALowVLow', 'ALowVHigh', 'AHighVLow', 'AHighVHigh']
    sb = [4, 7, 10, 13]
    d = dict(zip(conditions, sb))
    for i, cond_name in enumerate(conditions):
        ameans.append('-amean %d %s_mean' % (i+1, cond_name))
        for j, ss in enumerate(subj_list):
            dset_name = 'decon_out.mion.%s_concat.%s' % (ss, f_suffx)
            dsets.append("-dset %d %d '%s[%d]'" %
                         (i+1, j+1, os.path.join(decondir, dset_name),
                          d[cond_name]))

    ameans = ' '.join(ameans)
    dsets = ' '.join(dsets)
    return (ameans, dsets)


def main():
    """Execute afni_anova."""
    subjectlist = [s for s in range(1, 20)]
    subjectlist.remove(3)
    subjectlist.remove(11)

    workdir = os.path.join(os.environ['avp'], 'nii/group_effects_trad')
    logfile = setup_log(os.path.join(workdir, 'do_anova_grouptrad'))
    logfile.info('Doing main call')
    outname = os.path.join(workdir, 'anova2_grouptrad')
    afni_anova(logfile, subjectlist, outname)


if __name__ == '__main__':
    main()
