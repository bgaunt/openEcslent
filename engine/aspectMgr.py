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

from mgr import Mgr
class AspectMgr(Mgr):
    types = []
    aspects = {}

    def initialize(self):
        """Register all our various aspect types
        """
      #  import physics
     #   import helmsman
     #   import renderable
       # self.registerType(physics.RBPhysics25d)
        #self.registerType(helmsman.Helmsman)
     #   self.registerType(renderable.Renderable)
        pass

    def crosslink(self):
        pass

    def registerType(self, type):
        self.types.append(type)

    def registerAspect(self, aspect):
        self.aspects.setdefault(aspect.__class__, []).append(aspect)

