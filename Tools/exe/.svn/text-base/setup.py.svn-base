#python Tools/exe/setup.py py2exe 
from distutils.core import setup
import py2exe

import sys
import glob

sys.path.append(r'.')
sys.path.append(r'Tools\exe\vcr')
print sys.path

datafiles = [(r'.', glob.glob(r'Tools\exe\vcr\*.*')),
             (r'.', [r'cent.pyd',]),
             (r'.', [r'localOptions.yaml',]),
             (r'.', [r'ogre.cfg',]),
             (r'.', [r'OgreMain.dll',]),
             (r'config', glob.glob(r'config\*.*')),
             (r'plugins\nt', glob.glob(r'plugins\nt\*.*')),
             ]

import os
import shutil
src = os.path.join(os.getcwd(), os.path.join('Tools', os.path.join('exe', os.path.join('dlls', 'OgreMain.dll'))))

shutil.copy2(src, os.getcwd())
print "Copying data dir"
svnPatternFunction = shutil.ignore_patterns(r'.svn')
dataDir = os.path.join(os.getcwd(), 'data')
dataDst = os.path.join(os.getcwd(), os.path.join('dist', 'data'))

if os.path.exists(dataDst):
    shutil.rmtree(dataDst) # fresh copy
shutil.copytree(r'data', r'dist\data', ignore=svnPatternFunction)

setup(
    data_files = datafiles, 
    console=['main.py'],
    )

distDst = os.path.join('Tools', os.path.join('exe', 'ecslent'))
if os.path.exists(distDst):
    shutil.rmtree(distDst)
shutil.copytree(r'dist', distDst)


# import zipfile
# with zipfile.ZipFile(os.path.join(distDst, "ecslent.zip"), 'w', zipfile.ZIP_DEFLATED) as zf:
#     for root, dirs, files in os.walk(dstDst):
#         for file in files:
#             zf.write(os.path.join(root, file), os.path.join(root, file))

            

