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

import cent
from vector import vector3
import mathlib

class DesiredState(cent.CDesiredState):
    """A DesiredState is a smart / hybrid position thing
    Which can be relative to a number of things, along a variable number of axis
    What this class really does is convert the lowlevel c interface into something pythonic for the upper universes to interact with
    """
    class Type:
        """
        IMPORTANT: keep synced with CEnt\CDesiredState.CDesiredStateType
        """
        INVALID = 0
        STOPPED_AT_POSITION = 1
        MAINTAINING_RELATIVE_TO_ENT = 2

    def __init__(self, type):
        cent.CDesiredState.__init__(self, type)

    @property
    def pos(self):
        pass

    @pos.getter
    def pos(self):
        return vector3(self.posX, 0, self.posY)

    @pos.setter
    def pos(self, value):
        self.posX = value.x
        self.posY = value.z

    @property
    def offset(self):
        pass

    @offset.getter
    def offset(self):
        return vector3(self.offsetX, 0, self.offsetY)

    @offset.setter
    def offset(self, value):
        self.offsetX = value.x
        self.offsetY = value.z

    def calcWorldPos(self, ent):
        return self.pos

    def __getstate__(self):
        return {
            'type' : self.type,
            'pos' : (self.posX, self.posY),
            'offset' : (self.offsetX, self.offsetY),
        }

    def __setstate__(self, state):
        self.type                  = state['type']
        self.posX, self.posY       = state['pos']
        self.offsetX, self.offsetY = state['offset']

    def connectToEngine(self, engine):
        pass

class StoppedAtPosition(DesiredState):
    def __init__(self, pos):
        DesiredState.__init__(self, self.Type.STOPPED_AT_POSITION)
        self.pos = pos

class MaintainingRelativeToEnt(DesiredState):
    def __init__(self, ent, offset):
        DesiredState.__init__(self, self.Type.MAINTAINING_RELATIVE_TO_ENT)
        self.ent = ent
        self.targetID = ent.UnitAI.cent.id
        self.offset = offset
        self.entHandle = None

    def calcWorldPos(self, ent):
        offset = mathlib.yawwedVector(self.offset, self.ent.yaw)
        return self.ent.pos + offset

    def __getstate__(self):
        state = DesiredState.__getstate__(self)
        state['entHandle'] = self.entHandle or self.ent.handle
        return state

    def __setstate__(self, state):
        self.entHandle = state['entHandle']
        state = DesiredState.__setstate__(self, state)

    def connectToEngine(self, engine):
        if self.entHandle:
            self.ent = engine.entMgr.findEntFromHandle(self.entHandle)
            self.entHandle = None

