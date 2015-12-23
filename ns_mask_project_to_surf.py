# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 16:58:24 2015

@author: andric
"""

import os
import subprocess
import setLog
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
    ns_masks = ['lateral_occipital_pFgA_z_FDR_0.01.nii.gz']
    logs = os.path.join(workdir, 'mask_to_surface')

    for f in ns_masks:
        ms = mask_to_surface(os.path.join(workdir, f), logs)
        outmask = os.path.join(workdir, 'stepmask_%s' % f)
        ms.mask_neurosynth_file(outmask)
