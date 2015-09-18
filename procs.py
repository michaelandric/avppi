# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:03:24 2015

@author: andric
"""

import os
from shlex import split
from subprocess import call, STDOUT


def applywarp(workdir, input, extrt1, out, premat, interp=None):
    """
    general procedure for applywarp
    """
    print 'Doing applywarp'
    stdoutdir = os.path.join(workdir, 'stdout_files')
    if not os.path.exists:
        os.makedirs(stdoutdir)
    f = open('%s/stdout_from_applywarp.txt' % stdoutdir, 'w')
    if interp is None:
        cmdargs = split('applywarp -i %s -r %s -o %s --premat=%s' %
        (input, extrt1, out, premat))
    else:
        cmdargs = split('applywarp -i %s -r %s -o %s --premat=%s \
        --interp=%s' % (input, extrt1, out, premat, interp))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()
