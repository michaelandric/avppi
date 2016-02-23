# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 17:20:57 2016

@author: andric
"""

import os
from itertools import combinations

def filterbyvalue(seq, value):
    for i, el in enumerate(seq):
        if el == value: yield i

def reader(infile, val):
    with open(infile) as f:
        newf = list(map(int, f.readlines()))
        return list(filterbyvalue(newf, val))

def dicer(filename_list, effect_type, inds):
    sets2 = []
    for i in range(4):
        sets2.append(reader(filenames[i], ind[i]))
    
    outdices = []
    outlogs = []
    for g in combinations(range(4), 2):
        num = len(set(sets2[g[0]]).intersection(set(sets2[g[1]])))*2
        den = len(sets2[g[0]]) + len(sets2[g[1]])
        dice = num / den
        print ('Dice similarity score for \n{} \n{} \n{:.5f}'.format(filenames[g[0]], filenames[g[1]], dice))
        outlogs.append('Dice similarity score for \n{} \n{} \n{:.5f}\n'.format(filenames[g[0]], filenames[g[1]], dice))
        outdices.append(dice)
    
    outflogs = os.path.join(os.environ['avp'], 'nii', 'dice_coefs',
                            'out_dice_{}.log'.format(effect_type))
    with open(outflogs, 'w') as f:
        for ol in outlogs:
            print(ol, file=f)
    
    outfdices = os.path.join(os.environ['avp'], 'nii', 'dice_coefs',
                             'out_dice_{}.scores'.format(effect_type))
    with open(outfdices, 'w') as f:
        for od in outdices:
            print(od, file=f)


effects = ['Aentr', 'Ventr', 'Aentr_intxn']
ind = [1, 1, 2, 1]   # corresponds to the cluster number in Aentr_intxn
filenames = []
pref = 'clust_Aentr_intxn_flt2_msk_mema_mask+tlrc.txt'
clstfile = os.path.join(os.environ['avp'], 'nii', 'group_effects_dec',
                        pref)
filenames.append(clstfile)
for block in [20, 15, 10]:
    pref = 'clust_Aentr_intxn_flt2_{}blk_msk_mema_mask+tlrc.txt'.format(block)
    clstfile = os.path.join(os.environ['avp'], 'nii',
                            'group_effects_{}blk'.format(block), pref)
    filenames.append(clstfile)

dicer(filenames, 'Aentr_intxn', ind)