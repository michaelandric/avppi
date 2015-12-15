# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 18:32:23 2015

@author: andric
"""

import os
import procs as pr

if __name__ == '__main__':

    outdir = os.path.join(os.environ['avp'], 'nii', 'group_effects_dec')

    logf = os.path.join(outdir, 'project_to_surf')

    effects = ['Aentr', 'Ventr', 'Aentr_intxn']

    pn_list = ['0.2', '0.3', '1.0', '2.0']
    mapping = 'max_abs'

    for ef in effects:
        parent_pref = os.path.join(outdir, 'clust_%s_flt2_msk_mema' % ef)
        for hemi in ['lh', 'rh']:
            outname = '%s_%s_no_pn_MNI_N27.1D' % (parent_pref, hemi)
            pr.vol2surf_mni_no_pn(outdir, mapping, hemi,
                                  '%s+tlrc' % parent_pref, outname, logf)
            for pn in pn_list:
                outname = '%s_%s_pn%s_MNI_N27.1D' % (parent_pref, hemi, pn)
                pr.vol2surf_mni(outdir, mapping, hemi,
                                '%s+tlrc' % parent_pref, pn, outname, logf)
