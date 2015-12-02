# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 17:50:42 2015

@author: andric
"""

import os
import sys
import logging
from shlex import split
from subprocess import call, Popen, PIPE
import numpy as np
import pandas as pd


class masker(object):
    """
    set of AFNI calls and functions to make
    seeds from ventricles and white matter
    """
    def __init__(self, subj_id, workdir):
        self.ss = subj_id
        self.workdir = workdir

    def applywarp(self):
        """
        This is done to get the fast segmentations in epi space
        """
        cmd = split("applywarp -v --ref=%s_3.vol8.nii.gz \
                    --in=T1_fast_seg.nii.gz --postmat=mprage2.%s_3.mat \
                    --out=%s_fast_seg_2epi \
                    --interp=nn" % (self.ss, self.ss, self.ss))
        call(cmd)

    def get_msk(self):
        """
        This is to get the values in the fast seg
        """
        cmd = split('3dmaskdump -noijk \
                    -mask %s/%s_fast_seg_2epi.nii.gz \
                    %s/%s_fast_seg_2epi.nii.gz' %
                    (self.workdir, self.ss, self.workdir, self.ss))
        proc = Popen(cmd, stdout=PIPE)
        output = proc.communicate()[0].splitlines()
        seg = pd.Series(np.array(output, dtype=np.float64))

        cmd2 = split('3dmaskdump -noijk \
                     -mask %s/%s_fast_seg_2epi.nii.gz \
                     %s/%s_3.T12epi.nii.gz' %
                     (self.workdir, self.ss, self.workdir, self.ss))
        proc = Popen(cmd2, stdout=PIPE)
        output = proc.communicate()[0].splitlines()
        vol = pd.Series(np.array(output, dtype=np.float64))

        wm_thr = vol[seg==3].quantile(.66)
        vent_thr = vol[seg==1].quantile(.33)
        wm_msk = pd.Series(np.zeros(len(vol)))
        wm_msk[vol > wm_thr] = 1
        wm_msk = wm_msk.astype('int')
        vent_msk = pd.Series(np.zeros(len(vol)))
        vent_msk[vol < vent_thr] = 1
        vent_msk = vent_msk.astype('int')

        cmd3 = split('3dmaskdump -noijk \
                     -mask %s/%s_fast_seg_2epi.nii.gz \
                     %s/%s_3.T12epi.nii.gz' %
                     (self.workdir, self.ss, self.workdir, self.ss))
        proc = Popen(cmd3, stdout=PIPE)
        output = proc.communicate()[0].splitlines()
        xcol = np.empty(len(output))
        ycol = np.empty(len(output))
        zcol = np.empty(len(output))
        for i, line in enumerate(output):
            x, y, z, v = line.split()
            xcol[i] = x
            ycol[i] = y
            zcol[i] = z
        xyz = np.column_stack((xcol, ycol, zcol))
        
        wm_msk = pd.DataFrame(np.column_stack((xyz, wm_msk)))
        wm_msk.to_csv('%s/wm_mask_seed.txt' % self.workdir,
                      sep=' ', header=False, index=False)
        vent_msk = pd.DataFrame(np.column_stack((xyz, vent_msk)))
        vent_msk.to_csv('%s/vent_mask_seed.txt' % self.workdir,
                        sep=' ', header=False, index=False)
        
    def undump(self):
        for n in ['wm', 'vent']:
            cmd = split('3dUndump -prefix %s/%s_mask_seed.nii.gz \
                        -ijk -datum short \
                        -master %s/%s_3.T12epi.nii.gz %s/%s_mask_seed.txt' %
                        (self.workdir, n, self.workdir, self.ss,
                         self.workdir, n))
            call(cmd)


def maskave(workdir, mask, ts, outfile):
    cmd = split('3dmaskave -mask %s %s' % (workdir))
    f = open(outfile, 'w')
    call(cmd, stdout=f)
    f.close()


if __name__ == '__main__':
    subj_list = range(1, 20)
    subj_list = [1]
    for ss in subj_list:
        workdir = os.path.join(os.environ['avp'], 'nii', '%s_CNR.anat' % ss)
        logging.basicConfig(filename='%s/seed_masks.log' % workdir,
                            level=logging.DEBUG)
        logging.StreamHandler(sys.stdout)

        m = masker(ss, workdir)
        m.applywarp()
        m.get_msk()
        m.undump()

        sfx = 'Powered.cleanEPI.uncensored.txt'
        for r in range(1, 5):
            ts_name = 'v8.%s_%s.Powered.cleanEPI.uncensored.nii.gz' % (ss, r)
            ts_file = os.path.join(os.environ['avp'], 'nii', ts_name)
            for n in ['wm', 'vent']:
                outmasktsname = '%s_v8.%s_%s.%s' % (n, ss, r, sfx)
                outf = os.path.join(os.environ['avp'], 'nii',
                                    '%s_CNR.anat' % ss, outmasktsname)
                mask = os.path.join(workdir, '%s_mask_seed.nii.gz' % n)
                maskave(workdir, mask, ts_file, outf)
        