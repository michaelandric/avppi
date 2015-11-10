# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 18:09:48 2015

@author: andric
"""

import os
import procs as pr

if __name__ == '__main__':
    subj_list = range(1, 19)
#    subj_list = [19]

    decon_dir = os.path.join(os.environ['avp'], 'nii',
                             'deconvolve_outs_concat')
    insuff = 'Powered.cleanEPI_errts_REML+orig.'
    outsuff = 'Powered.cleanEPI_errts_REML_mean'
    for ss in subj_list:
        fpref = 'decon_out.mion.%s_concat' % ss
        fname = '%s.%s' % (fpref, insuff)
        infile = os.path.join(decon_dir, fname)
        outfname = '%s.%s' % (fpref, outsuff)
        outfile = os.path.join(decon_dir, outfname)
        pr.mean_epi(ss, infile, decon_dir, outfile)
