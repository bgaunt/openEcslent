#---------------------------------------------------------------------------
# Copyright 2010, 2011 Sushil J. Louis and Christopher E. Miles, 
# Evolutionary Computing Systems Laboratory, Department of Computer Science 
# and Engineering, University of Nevada, Reno. 
#
# This file is part of OpenECSLENT 
#
#    OpenECSLENT is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    OpenECSLENT is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with OpenECSLENT.  If not, see <http://www.gnu.org/licenses/>.
#---------------------------------------------------------------------------
#-------------------------End Copyright Notice------------------------------

import os
from distutils.core import setup, Extension

cEntFilename = os.path.join(os.path.join('engine', 'CEnt'), 'cent.cpp')

dynLibPath = 'build\lib.win32-2.6\cent.pyd'
dynLibFilename = 'cent.pyd'
if os.name == 'posix':
    dynLibPath = 'build/lib.linux-i686-2.6/cent.so'
    dynLibFilename = 'cent.so'

#try:
     #os.utime(cEntFilename, None)
#except:
    #pass

#setup(name='cent',
      #version='1.0',
      #ext_modules=[Extension('cent', [cEntFilename],
                             #libraries = [])
                   #],
      #)

import fnmatch
pyFiles = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if fnmatch.fnmatch(file, '*.py'):
            pyFiles.append(os.path.relpath(os.path.join(root, os.path.splitext(file)[0])))

print pyFiles
from glob import glob
data_files = [("Microsoft.VC90.CRT", glob(r'c:\dev\ms-vc-runtime\*.*'))]

setup(name='cent',
        version='1.0',
        ext_modules=[Extension('cent', [cEntFilename], libraries=[])],
        py_modules=pyFiles,
    data_files=data_files,
)
print pyFiles
#setup(name='IA',
       #version='2.0',
       #py_modules=pyFiles,
#)

#try:
    #os.unlink(dynLibFilename)
#except:
    #pass

#print "os.rename('build\lib.win32-2.6\cent.pyd', 'cent.pyd')"
#print "os.rename(",dynLibPath, dynLibFilename, ")"
#os.rename(dynLibPath, dynLibFilename)
#os.rename('build\lib.win32-2.6\cent.pyd', 'cent.pyd')

#import test
