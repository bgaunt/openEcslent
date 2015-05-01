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

"""
an EngineObject is something that is owned within the engine, that lives within its memory and is tracked
it keeps apointer to the engine, which is were we get all our singleton references
we also do some basic id counting so that 
"""
class EngineObject(object):
    ids = {}
    def __init__(self, engine):
        self.engine = engine
        self.engine.memoryMgr.initObject(self)
        t = type(self)
        self.ids.setdefault(t, 0)
        self.ids[t] += 1
        self.typeId = self.ids[t]

    def __del__(self):
        self.engine.memoryMgr.delObject(self)

    def __str__(self):
        return '%s%i' % (type(self).__name__, self.typeId)

    def __repr__(self):
        return self.__str__()



"""
A system is a managed singleton that subscribes to the execution level
    which allows it to acquire / release resources
"""
class System(EngineObject):
    def __init__(self, engine):
        EngineObject.__init__(self, engine)
    def initialize(self):
        pass
    def crosslink(self):
        pass
    def initEngine(self):
        pass
    def initEnginePost(self):
        pass
    def initMenu(self):
        pass
    def loadLevel(self):
        pass
    def releaseLevel(self):
        pass
    def releaseEngine(self):
        pass
    def tick(self, dtime):
        pass
    def render(self):
        pass


"""
A mgr is a descendent of a system, that owns a category of objects, such as entity or aspects
Really the distinction is just in name
and rael
"""
class Mgr(System):
    pass
