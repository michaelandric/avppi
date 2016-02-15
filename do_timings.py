# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 15:18:26 2016

@author: andric
"""

import os

def filterbyvalue(seq, value):
    for i, el in enumerate(seq):
        if el == value: yield i

def reader(infile):
    with open(infile) as f:
        ff = list(map(int, f.readlines()))
        return list(filterbyvalue(ff, 0))     

def make_censor(infile, blockTRs):
    """
    blockTRs: block length in TRs
    """
    timing_dir = '/mnt/lnif-storage/urihas/AVaudvisppi/timing'
    timings = []
    for i in range(1, 5):
        concat_stim_times = os.path.join(timing_dir,
                                         'concat_stim_times_cond%d.txt' % i)
        with open(concat_stim_times) as f:
            for n, line in enumerate(f.read().split('\n')[:4]):
                for l in list(map(float, line.split())):
                    timings.append(round(l/1.5)+(n*343))
    
    timings.sort()
    
    censor_list = [1]*1372
    for v in reader(infile):
        censor_list[v]=0
    
    # 30 s blocks / 1.5 TR = 20 TRs per block
    ends = [t+20 for t in timings]
    starts = [t+blockTRs for t in timings]
            
    for (st, en) in zip(starts, ends):
        for i in range(st, en+1):
            censor_list[i] = 0

    return censor_list


# Main call
subj_list = [s for s in range(1, 20)]
subj_list.remove(3)
subj_list.remove(11)
for ss in subj_list:
    infile = os.path.join(os.environ['avp'], 'nii',
                          'all_ts.%s.Powered.censor.1D' % ss)
    for block in [20, 15, 10]:
        outcensor = make_censor(infile, round(block/1.5))
        outf = os.path.join('/mnt/lnif-storage/urihas/AVaudvisppi/timing',
                            'all_ts.block%s.%s.Powered.censor.1D' % (block, ss))
        out = open(outf, 'w')
        out.write('\n'.join(map(str, outcensor)))
        out.close()