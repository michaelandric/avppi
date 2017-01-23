# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 19:54:37 2015

@author: andric
"""

import os
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from shlex import split
from setlog import setup_log


def cluster(log, thresh, clstsize, outpref, infile):
    """Cluster the data."""
    log.info('Do cluster for %s', outpref)
    clustcmd = split("3dclust -prefix %s -1Dformat -1dindex 1 -1tindex 1 \
                     -2thresh -%s %s -savemask %s_mask \
                     -dxyz=1 1.44 %s %s" %
                     (outpref, thresh, thresh, outpref, clstsize, infile))
    proc = Popen(clustcmd, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def main():
    """Call to functions for cluster."""
    logfile = setup_log(os.path.join(os.environ['avp'], 'logs',
                                     'do_cluster'))

    for ramp in ['rampup', 'rampdown']:
        for condition in ["A", "V", "Intxn"]:
            fpref = '%s_%s_mema_out' % (condition, ramp)
            inname = os.path.join(os.path.join(os.environ['avp'], 'nii',
                                               'ramp_effects'),
                                  '%s+tlrc' % fpref)
            outname = os.path.join(os.path.join(os.environ['avp'], 'nii',
                                                'ramp_effects'),
                                   'clust_%s' % fpref)
            cluster(logfile, 2.92, 212, outname, inname)


if __name__ == '__main__':
    main()
