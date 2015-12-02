# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 18:38:22 2015

@author: andric
"""

import os
from subprocess import call
from shelx import split

def concat(filelist, outname):
    files =  ' '.join(filelist)
    cmd = split('cat %s > %s' % (files, outname))
    call(cmd)

if __name__ == '__main__':
    subj_list = range(1, 20)
    for ss in subj_list:
        workdir = os.path.join(os.environ['avp'], 'nii', '%s_CNR.anat' % ss)
        for n in ['wm', 'vent']:
            inputs = []
            for r in range(1, 5):
                f = '%s_v8.%s_%s.Powered.cleanEPI.uncensored.txt' % (n, ss, r)
                inputs.append(os.path.join(workdir, f))
            outn = '%s_v8.%s_all.Powered.cleanEPI.uncensored.txt' % (n, ss)
            outf = os.path.join(workdir, outn)
            concat(inputs, outf)