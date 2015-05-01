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

from engineExceptions import NotImplementedException
from mgr import EngineObject
import desiredState

class Command(EngineObject):
    """A command is a high level thing you can tell a squad (and boat by extension) to do
    These should be treated as basic structs (they contain data, but do not have methods associated with them
    """
    def __init__(self, engine):
        EngineObject.__init__(self, engine)

    def uiStr(self):
        return ''
    
class Stop(Command):
    def __init__(self, engine, duration):
        Command.__init__(self, engine)
        self.duration = duration
        self.desiredState = None

    def uiStr(self):
        return 'Stop:'

class MoveTo(Command):
    def __init__(self, engine, desiredState, desiredSpeed=None):
        Command.__init__(self, engine)
        self.desiredState = desiredState
        self.desiredSpeed = desiredSpeed

    def uiStr(self):
        if self.desiredState.type == desiredState.DesiredState.Type.MAINTAINING_RELATIVE_TO_ENT:
            answer = 'Maintain:%s' % str(self.desiredState)
        else:
            answer = 'Move:%s' % str(self.desiredState)
        if self.desiredSpeed is not None:
            answer += '@%0.2f' % self.desiredSpeed
        return answer

class NetSlave(Command):
    def __init__(self, engine):
        Command.__init__(self, engine)
        self.desiredState = None

    def uiStr(self):
        return 'NetSlave:'

class ManualControl(Command):
    def __init__(self, engine):
        Command.__init__(self, engine)
        self.desiredState = None

    def uiStr(self):
        return 'ManualControl:'

