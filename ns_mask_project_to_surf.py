# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 16:58:24 2015

@author: andric
"""

import os
import subprocess
import setLog
import procs as pr
from shlex import split

class mask_to_surface:

    def __init__(self, infile, logf):
        self.input = infile
        self.logf = logf

    def mask_neurosynth_file(self, outfile):
        """
        Get the values as mask
        from the neurosynth result
        """
        lg = setLog._log(self.logf)
        lg.info('Doing mask_neurosynth_file')
        cmd = split("3dcalc -a %s -expr 'step(a)' \
                    -prefix %s " % (self.input, outfile))
        lg.info("Command: \n%s" % cmd)
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lg.info(p.stdout.decode("utf-8", "strict"))
        lg.info("Done with mask_neurosynth_file")


if __name__ == '__main__':

    workdir = os.path.join('/Users/andric/Documents/workspace',
                           'AVPPI', 'nii', 'group_effects_dec')
    ns_masks = ['lateral_occipital_pFgA_z_FDR_0.01', 'mt_pFgA_z_FDR_0.01']
    logs = os.path.join(workdir, 'mask_to_surface')

    for f in ns_masks:
        ms = mask_to_surface(os.path.join(workdir, '%s.nii.gz' % f), logs)
        outmask = os.path.join(workdir, 'stepmask_%s' % f)
        ms.mask_neurosynth_file(outmask)

        pn = 1.0
        for hemi in ['lh', 'rh']:
            outname = '%s_%s_pn%s_MNI_N27.1D' % (outmask, hemi, pn)
            pr.vol2surf_mni(workdir, 'max_abs', hemi,
                            '%s+tlrc' % outmask, pn, outname, logs, local=True)