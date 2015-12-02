# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 17:50:42 2015

@author: andric
"""

import os
import logging
from shlex import split
from subprocess import call, STDOUT

logging.basicConfig(filename='seed_masks.log', level=logging.DEBUG)
def make_vent_seed(outlocation):
    Vseed = '-8 13 19\n8 13 19\n'
    file = open('%s/vent.seed.tal.1D' % outlocation,'w')
    file.write(Vseed)
    file.close()

class masker(object):
    """
    set of AFNI calls and functions to make
    seeds from ventricles and white matter
    """
    def __init__(self, workdir, initial_vol):
        self.workdir = workdir
        self.initial_vol = initial_vol
        volname = initial_vol.split('.')
        self.vol_pref = '_'.join(volname.split('.')[:-1])
        self.iniital_vol_pref

    def calc_aroundvent_val(self, fast_seg):
        f = open('%s/stdout_from_aroundvent_preblur.txt' % self.workdir, 'w')
        cmd = split("3dcalc -a %s -b %s \
                    -expr '100*step(b)*iszero(amongst(a,1,0))' \
                    -prefix %s_aroundvent_preblur" %
                    (fast_seg, self.initial_vol))
        call(cmd, stdout=f, stderr=STDOUT)
        f.close()
    
    def vecwarp(self, transformmat, ventseed, ventseed_in_orig):
        """
        transformmat: This gives the transform from MNI to linear T1 space
        ventseed: the ventricle seed in MNI
        ventseed_in_orig: the ventricle seed in original space
        """
        f = open('%s/stdout_from_vecwarp.txt' % self.workdir, 'w')
        cmd = split("Vecwarp -matvec %s -forward -input %s \
                    -output %s" % (transformmat, ventseed, ventseed_in_orig))
        call(cmd, stdout=f, stderr=STDOUT)
        f.close()
        


"""
os.system("3dcalc -a "+self.options.loc+"/volume."+self.options.id+"_seg.nii.gz -b "+frac_mask+" -expr '100*step(b)*iszero(amongst(a,1,0))' -prefix "+self.options.loc+"/volume.aroundVent.preblur."+self.options.id)  ## mask around the ventricle

os.system("Vecwarp -matvec "+self.options.loc+"/volume.tal."+self.options.id+".1D -forward -input vent.seed.tal.1D -output "+self.options.loc+"/vent.seed.1D")
        print "<<<<<<<< 3dUndump to get ventricles seed >>>>>>>>>>>>> "+time.ctime()
        os.system("3dUndump -xyz -orient RAI -prefix "+self.options.loc+"/vent.seed."+self.options.id+" -master "+frac_mask+" -srad 8 "+self.options.loc+"/vent.seed.1D")

"""