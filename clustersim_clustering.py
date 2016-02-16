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
    mask = os.path.join(os.environ['FSLDIR'], 'data/standard',
                        'MNI152_T1_2mm_brain_mask_dil1.nii.gz')
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
                 -2thresh -%s %s -savemask %s_mask \
                 -dxyz=1 1.44 %s %s') %
                 (outname, thr, thr, outname, clst_size, infile))
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lg.info(p.stdout.decode("utf-8", "strict"))
    lg.info('cluster is done.')


if __name__ == '__main__':
#    fwhmx = np.array((8.054140, 8.238027, 8.247797))
    fwhm_d = {20: [8.84498176, 8.98884216, 9.00245],
              15: [8.91003216, 9.06582647, 9.03423882],
 10: [8.8977802, 9.07431745, 9.00935118]}
    for block in fwhm_d:
        fwhmx = np.array(fwhm_d[block])
        outdir = os.path.join(os.environ['avp'], 'nii',
                              'group_effects_%sblk' % block)
        estimate_clustersizes(fwhmx, outdir)
    
        effects = ['Aentr', 'Ventr', 'Aentr_intxn']
        for ef in effects:
            infile = os.path.join(outdir, '%s_flt2_msk_mema+tlrc.HEAD' % ef)
            outname = os.path.join(outdir, 'clust_%s_flt2_msk_mema_p.005' % ef)
#            cluster(outdir, 3.25, 146, infile, outname)
