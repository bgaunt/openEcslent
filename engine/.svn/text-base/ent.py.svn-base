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

from copy import copy
from mgr import EngineObject
from player import Player, Side

class Ent(EngineObject):
    """
    Base class for all kinds of things
    Really not much to it in python
    Just keeps a list of aspects that it initializes, and passes down func calls to
    """
    hasSquad = False
    selectable = False
    isNormal = False

    def __init__(self, engine, handle, playerInfo = None):
        EngineObject.__init__(self, engine)
        self.isClosestEntToMouse = False
        self.isUnderMouse = False
        self.isSelected = False
        self.tickCount = 0
        self.handle = handle
        if playerInfo:
            self.player = playerInfo
        else:
            self.player = Player(Side.NEUTRAL, -1)

    def createAspects(self, additionalAspects):
        self.aspectClasses = self.aspects + additionalAspects
        self.aspects = []
        for aspectClass in self.aspectClasses:
            aspect = aspectClass(self.engine, self)
            self.aspects.append(aspect)
            setattr(self, aspect.__class__.__name__, aspect)

        for aspect in self.aspects:
            aspect.init()

        for aspect in self.aspects:
            aspect.crosslink()

    def tick(self, dtime):
        for aspect in self.aspects:
            aspect.preTick(dtime)
        for aspect in self.aspects:
            aspect.tick(dtime)
        self.tickCount += 1

    def dump(self):
        print 'Ent.Dump(%s)' % self
        for name, val in self.__dict__.items():
            print '    %20s:%20s' % (name, val)

    def findAspect(self, t):
        for aspect in self.aspects:
            if type(aspect) == t:
                return aspect
        return None
    
    def attachAspect(self, aspect):
        if not aspect in self.aspects:
            self.aspects.append(aspect)
