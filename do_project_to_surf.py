# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 18:32:23 2015

@author: andric
"""

import os
import setLog
import subprocess
from shlex import split
import procs as pr

if __name__ == '__main__':

    outdir = os.path.join(os.environ['avp'], 'nii', 'group_effects_dec')

    logf = os.path.join(outdir, 'project_to_surf')

    effects = ['Aentr', 'Ventr', 'Aentr_intxn']

    pn = '1.0'
    for hemi in ['lh', 'rh']:
        for ef in effects:
            parent_pref = os.path.join(outdir, 'clust_%s_flt2_msk_mema' % ef)
            outname = '%s_%s_pn%s_MNI_N27.1D' % (parent_pref, hemi, pn)
            pr.vol2surf_mni(outdir, hemi, '%s+tlrc' % parent_pref,
                            pn, outname, logf)
