# -*- coding: utf-8 -*-
"""
Big update for maskdump proc on Jan 30 2017

@author: andric
"""

import os
import procs as pr
from setlog import setup_log


def call_maskdump_decon(log, mask, cond, workdir, subj):
    """Call maskdump for deconvolve data."""
    log.info('Maskdump in: %s', workdir)
    inname = os.path.join(workdir, '%s_coef_%s+tlrc' % (cond, subj))
    outname = os.path.join(workdir, '%s_coef_%s.txt' % (cond, subj))
    pr.maskdump(workdir, mask, inname, outname)


def call_maskdump_effects(log, mask, workdir, effect):
    """Call maskdump for effect data.

    arg: effect
        This takes the form, e.g., 'A_rampdown'
    """
    log.info('maskdump_effects in %s', workdir)
    inname = os.path.join(workdir, 'clust_%s_mema_out_mask+tlrc' % effect)
    outname = os.path.join(workdir, 'clust_%s_mema_out_mask.txt' % effect)
    if os.path.exists('%s.HEAD' % inname):
        pr.maskdump(workdir, mask, inname, outname)


def main():
    """Execute function for maskdumps."""
    logfile = setup_log(os.path.join(os.environ['avp'], 'logs',
                                     'do_procs_maskdumps'))
    subj_list = [s for s in range(1, 20)]
    subj_list.remove(3)
    subj_list.remove(11)
    mask = os.path.join(os.environ['FSLDIR'], 'data/standard',
                        'MNI152_T1_2mm_brain_mask_dil1.nii.gz')

    conditions = ['ALowVLow_rampdown', 'ALowVLow_rampup',
                  'ALowVHigh_rampdown', 'ALowVHigh_rampup',
                  'AHighVLow_rampdown', 'AHighVLow_rampup',
                  'AHighVHigh_rampdown', 'AHighVHigh_rampup']
    for subject in subj_list:
        for condition in conditions:
            call_maskdump_decon(logfile, mask, condition,
                                os.path.join(os.environ['avp'], 'nii',
                                             'deconvolve_outs_ramps'),
                                subject)

    for ramp in ['rampup', 'rampdown']:
        for condition in ["A", "V", "Intxn"]:
            call_maskdump_effects(logfile, mask,
                                  os.path.join(os.environ['avp'], 'nii',
                                               'ramp_effects'),
                                  '%s_%s' % (condition, ramp))


if __name__ == '__main__':
    main()
