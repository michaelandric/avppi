# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 18:32:23 2015

@author: andric
"""

import os
import procs as pr
from setlog import setup_log


def project_to_surf(logf, hh, pn):
    """Project functional to surface."""
    workdir = os.path.join(os.environ['avp'], 'nii', 'ramp_effects')
    for ramp in ['rampup', 'rampdown']:
        for condition in ["A", "V", "Intxn"]:
            if condition is "Intxn" and ramp is "rampup":
                continue
            fpref = 'clust_%s_%s_mema_out' % (condition, ramp)
            pr.vol2surf_mni(os.path.join(os.environ['avp'], 'nii',
                                         'ramp_effects'),
                            'max_abs',
                            hh,
                            os.path.join(workdir, '%s+tlrc' % fpref),
                            pn,
                            os.path.join(workdir, '%s_%s_%s_MNI_N27.1D' %
                                         (fpref, hh, pn)),
                            log=logf)


def main():
    """Call project_to_surf."""
    logfile = setup_log(os.path.join(os.environ['avp'], 'logs',
                                     'project_to_surf'))
    for hemi in ['lh', 'rh']:
        project_to_surf(logfile, hemi, '1.0')


if __name__ == '__main__':
    main()
