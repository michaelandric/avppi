# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 19:54:37 2015

@author: andric
"""

import os
from subprocess import PIPE
from subprocess import STDOUT
from subprocess import call
from setlog import setup_log


def bucket(log, outpref, infile):
    """Bucket data from sub brik."""
    log.info("Do 3dbucket %s \n", outpref)

    bucketargs = "3dbucket -prefix %s %s" % (outpref, infile)
    log.info("Bucket args: \n%s", bucketargs)
    call(bucketargs, stdout=PIPE, stderr=STDOUT)


def dictionary_set():
    """Build dictionary with condition names and sub brik."""
    conditions = ['ALowVLow_rampdown', 'ALowVLow_rampup',
                  'ALowVHigh_rampdown', 'ALowVHigh_rampup',
                  'AHighVLow_rampdown', 'AHighVLow_rampup',
                  'AHighVHigh_rampdown', 'AHighVHigh_rampup']

    coef = range(4, 26, 3)
    tstat = range(5, 27, 3)
    cond_dict = dict(zip(conditions, zip(coef, tstat)))
    return cond_dict


def main():
    """Call functions."""
    subj_list = [s for s in range(1, 20)]
    subj_list.remove(3)
    subj_list.remove(11)

    logfile = setup_log(os.path.join(os.environ['avp'], 'logs',
                                     'bucket'))
    dat_dir = os.path.join(os.environ['avp'], 'nii',
                           'deconvolve_outs_ramps')
    condition_dict = dictionary_set()

    for subj in subj_list:
        fname_sufx = 'Powered.cleanEPI_REML_fnirted_MNI2mm.nii.gz'
        fname = 'decon_out.ramps_wav.%s_concat.%s' % (subj, fname_sufx)
        for condition in condition_dict:
            for i, subbrk in enumerate(['coef', 'tstat']):
                in_file = os.path.join(dat_dir, "%s'[%d]'" %
                                       (fname, condition_dict[condition][i]))
                out_pref = os.path.join(dat_dir,
                                        '%s_%s_%s' % (condition, subbrk, subj))
                bucket(logfile, out_pref, in_file)


if __name__ == '__main__':
    main()
