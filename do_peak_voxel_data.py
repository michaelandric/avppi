# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 15:56:44 2016

@author: andric
"""

import os
import setLog
import pandas as pd
from shlex import split
import subprocess


def mask_dump_peak(clust, coords, subj):
    dat = os.path.join(os.environ['avp'], 'nii', 'ss%s_effects_dec' % subj,
                       '%s_ss%s_coef+tlrc.' % (clust, subj))
    cmd = split('3dmaskdump -noijk -dbox %s %s' % (coords, dat))
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return float(p.stdout.decode("utf-8", "strict"))



if __name__ == '__main__':
    
    stdoutdir = os.path.join(os.environ['avp'], 'nii', 'peak_vox_from_clust')
    lg = setLog._log('%s/do_peak_voxel_data' % stdoutdir)

    clust_coords = {'Aentr': ('-38.0 26.0 44.0', '34.0 -50.0 30.0'),
                    'Ventr': ('32.0 -32.0 28.0', '-26.0 -8.0 46.0'),
 'Aentr_intxn': ('-42.0 56.0 -12.0', '34.0 58.0 -16.0', '-26.0 -14.0 28.0')}

    bad_subjs = [3, 11]
    subj_list = [s for s in range(1, 20) if s not in bad_subjs]
    clust_col_names = []

    clust_dat = pd.Series()
    for clust in clust_coords:
        ncl  = len(clust_coords[clust])
        for cl in range(ncl):
            L = []
            c_name = '%s_%s' % (clust, cl)
            clust_col_names.append(c_name)
            coords = clust_coords[clust][cl]
            for ss in subj_list:
                lg.info('get peak for Clust %s, subj %s' % (clust, ss))
                L.append(mask_dump_peak(clust, coords, ss))
            clust_dat = clust_dat.append(pd.Series(L))

    out_dat = pd.DataFrame(clust_dat.reshape(7, 17).T, columns=clust_col_names)
    outname = os.path.join(stdoutdir, 'peak_voxel_data.csv')
    out_dat.to_csv(outname, index=False)

lg.info(print(out_dat.corr()))


# Doing the tests
import itertools
import scipy.stats

conds = []
stats = []
for combo in itertools.combinations(range(out_dat.shape[1]), 2):
    conds.append(list([out_dat.columns[combo[0]], out_dat.columns[combo[1]]]))
    stats.append(list(scipy.stats.pearsonr(out_dat.iloc[:, combo[0]], out_dat.iloc[:, combo[1]])))

corr_res = pd.concat([pd.DataFrame(conds), pd.DataFrame(stats)], axis=1)
col_heads = ['condition1', 'condition2', 'rvalue', 'pvalue']
corr_res.columns = col_heads
outname_corr = os.path.join(stdoutdir, 'corr_tests_on_peak_voxel_data.csv')
corr_res.to_csv(outname_corr, index=False)