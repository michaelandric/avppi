# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 02:32:29 2015

@author: andric
"""

import os
import setLog
import numpy as np
import procs as pr
from shlex import split
from subprocess import Popen, PIPE

import itertools


subj_list = [s for s in range(1, 20)]
subj_list.remove(3)
subj_list.remove(11)

ones = list([it for it in itertools.repeat([1, -1], 17)])
perm_ones = [it for it in itertools.product(*ones)]

n_perms = 1000
np.random.randint(0, len(perm_ones)/2., size=n_perms)


lg = setLog._log('calc_pos_neg')

def do_calc():
    lg.info("Doing 3dcalc for pos neg")