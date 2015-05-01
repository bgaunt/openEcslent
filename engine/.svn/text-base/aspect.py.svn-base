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

from mgr import EngineObject
class Aspect(EngineObject):
    def __init__(self, engine, ent):
        EngineObject.__init__(self, engine)
        self.ent = ent
        self.engine.aspectMgr.registerAspect(self)

    def init(self):
        pass

    def crosslink(self):
        pass

    def preTick(self, dtime):
        pass

    def tick(self, dtime):
        print '%s.tick %f' % (self.__class__, dtime)
        pass

    def render():
        pass
