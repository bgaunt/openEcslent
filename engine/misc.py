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

import sys, os
def EasyLog(f):
    def new_f():
        #print "<%s>" % f.__name__
        f()
        #print "</%s>" % f.__name__
    new_f.__name__ = f.__name__
    return new_f

def EasyLog1(f):
    def new_f(a1):
        #print "<%s(%s)>" % (f.__name__, a1)
        f(a1)
        #print "</%s(%s)>" % (f.__name__, a1)
    new_f.__name__ = f.__name__
    return new_f

@EasyLog
def setupPaths():
    pyDirs = set()
    pyFiles = set()
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                pyDirs.add(root)
                pyFiles.add(file)
    pyDirs.remove('.')
    sys.path.extend(pyDirs)

#@EasyLog
def importAll():
    pyFiles = set()
    for root, dirs, files in os.walk('.'):
        if root.endswith('Deprecated'):
            continue
        for file in files:
            if file.endswith('.py'):
                pyFiles.add(file)

    doNotImportList = set()
    doNotImportList.add('__init__.py')
    doNotImportList.add('setup.py')
    pyFiles = pyFiles.difference(doNotImportList)

    for file in pyFiles:
        fileShort = os.path.splitext(file)[0]
        print 'import', fileShort
        __import__(fileShort, globals())


#@EasyLog
def erasePycFiles():
    return
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                path = os.path.join(root, file)
                os.unlink(path)
