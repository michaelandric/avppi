# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 17:01:06 2015

@author: andric

Estimated fwhm from residuals via 3dMEMA.
Now get clustering sizes and clustering

Can use this to estimate and/or cluster.

"""

import os
import setLog
import subprocess
import numpy as np
from shlex import split


def estimate_clustersizes(fwhmx, outdir):
    """
    Already derived estimate of fwhmx via residuals
    fwhmx: x y z of fwhm estimate
    """
    lg = setLog._log('%s/clustersize_estimates' % outdir)
    lg.info('Doing estimate_clustersizes ---- ')
    lg.info('FWHMx is: %s' % fwhmx)
#    mask = os.path.join(os.environ['FSLDIR'], 'data/standard',
#                        'MNI152_T1_2mm_brain_mask_dil1+tlrc.BRIK.gz')
    mask = os.path.join(os.environ['avp'], 'nii', 'group_effects_wmvnt_incl',
                        'MNI152_T1_2mm_brain_mask_dil1+tlrc.BRIK')    
    cmd = split('3dClustSim -mask %s -fwhmxyz %f %f %f' % (mask, fwhmx[0], fwhmx[1], fwhmx[2]))
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lg.info(p.stdout.decode("utf-8", "strict"))
    f = open('%s/clustSim_resZ_fwhmx_%f_%f_%f_out.txt' %
             (outdir, fwhmx[0], fwhmx[1], fwhmx[2]), 'w')
    f.write(p.stdout.decode("utf-8", "strict"))
    f.close()
    lg.info('estimate_clustersizes done.')

def cluster(outdir, thr, clst_size, infile, outname):
    """
    Doing clustering
    """
    lg = setLog._log('%s/clustering' % outdir)
    lg.info('Doing cluster ---- ')
    cmd = split(('3dclust -prefix %s -1Dformat -nosum -1dindex 1 -1tindex 1 \
                 -2thresh -%s %s \
                 -dxyz=1 1.44 %s %s -savemask %s_mask') %
                 (outname, thr, thr, clst_size, infile, outname))
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lg.info(p.stdout.decode("utf-8", "strict"))
    lg.info('cluster is done.')


if __name__ == '__main__':
    fwhmx = np.array((8.054140, 8.238027, 8.247797))
    outdir = os.path.join(os.environ['avp'], 'nii', 'group_effects_dec')
#    estimate_clustersizes(fwhmx, outdir)

    effects = ['Aentr', 'Ventr', 'Aentr_intxn']
    for ef in effects:
        infile = os.path.join(outdir, '%s_flt2_msk_mema+tlrc.HEAD' % ef)
        outname = os.path.join(outdir, 'clust_%s_flt2_msk_mema_p.005' % ef)
        cluster(outdir, 3.25, 146, infile, outname)
