# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 18:32:23 2015

@author: andric
"""

import os
import setLog
import subprocess
from shlex import split

if __name__ == '__main__':
    logf = os.path.join(os.environ['hel'], 'nii', 'group_effects_dec',
                        'project_to_surf')

    for hemi in ['lh', 'rh']:
        lg.info('Doing hemi %s' % hemi)
        parent_pref
        