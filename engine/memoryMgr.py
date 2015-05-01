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

import timer
from misc import EasyLog1
class MemoryMgr(object):
    def __init__(self, engine):
        self.engine = engine
        self.counts = {}

    def crosslink(self):
        import ogre.io.OIS as OIS
        import inputSystem
        self.engine.inputSystem.registerHandler(inputSystem.InputEvent.KEY_PRESSED, OIS.KC_M, self.dump)

    def initObject(self, obj):
        n = obj.__class__.__name__
        self.counts.setdefault(n, 0)
        self.counts[n] += 1

    def delObject(self, obj):
        n = obj.__class__.__name__
        self.counts[n] -= 1

    dumpTimer = timer.Timer(60.0)
    def tick(self, dtime):
        pass
        #if self.dumpTimer.check(dtime):
            #self.dump()

    def dump(self):
        print 'MemoryManager.dump'
        for name, count in self.counts.items():
            print '    %6i:%s' % (count, name)

