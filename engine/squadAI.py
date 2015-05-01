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

import math
import random

import timer
from aspect import Aspect
from vector import vector3
from mathlib import differenceBetweenAngles, clamp
import command

kUpdateStrategyFrequency = 0.1

class SquadAI(Aspect):
    """
    Maintains group level control over a set of units
    """
    class LongTermData(object):
        """
        Ultimate goal / long term for this squad
        Input from the strategic AI / HumanPlayer goes in here
        """
        def __init__(self):
            self.commands = []

    class MediumTermData(object):
        def __init__(self):
            pass

    class ImmediateData(object):
        def __init__(self):
            pass

    def init(self):
        self.squadMembers = []
        self.longTermUpdateTimer = timer.Timer(kUpdateStrategyFrequency, fireFirstCheck=True)

        self.immediateData = self.ImmediateData()
        self.mediumTermData = self.MediumTermData()
        self.longTermData = self.LongTermData()

        self.immediateData.ddContext = self.engine.debugDrawSystem.getContext()
        self.mediumTermData.ddContext = self.engine.debugDrawSystem.getContext()
        self.longTermData.ddContext = self.engine.debugDrawSystem.getContext()

    def tick(self, dtime):
        if self.longTermUpdateTimer.check(dtime):
            self.longTermUpdate()

    @property 
    def command(self):
        pass

    @command.getter
    def command(self):
        return self.longTermData.commands and self.longTermData.commands[0] or None

    @property 
    def commands(self):
        return self.longTermData.commands

    @commands.setter
    def commands(self, commands):
        self.longTermData.commands = commands

    def longTermUpdate(self):
        """The squad is not particularly used at the moment, - since we aren't doing any real coordination
        so most of this is just pass through
        """
        if not self.commands:
            return

        current = self.commands[0]
        if type(current) == command.MoveTo:
            for squadMember in self.squadMembers:
                squadMember.UnitAI.commands = self.commands

        elif type(current) == command.NetSlave:
            for squadMember in self.squadMembers:
                squadMember.UnitAI.commands = self.commands

        elif type(current) == command.ManualControl:
            for squadMember in self.squadMembers:
                squadMember.UnitAI.commands = self.commands

        elif type(current) == command.Stop:
            for squadMember in self.squadMembers:
                squadMember.UnitAI.commands = self.commands


        else:
            raise Exception('not yet implemented')
