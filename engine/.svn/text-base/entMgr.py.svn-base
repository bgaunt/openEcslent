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
import boat
import timer

import command
from netAspect import NetAspect

from player import Player
from player import Side

class EntMgr(Mgr):
    types = []
    _ents = {}
    
    nEnts = 0
    entMap = {}
    """
    Owns all the entities
    """
    def initEngine(self):
        def registerEntType(type):
            self.types.append(type)

        import boat
        registerEntType(boat.DDG51)
        registerEntType(boat.SLEEK)
        registerEntType(boat.ALIENBOAT)
        registerEntType(boat.SAILBOAT)
        registerEntType(boat.CVN68)
        registerEntType(boat.SPEEDBOAT)
        registerEntType(boat.CIGARETTE)


    def crosslink(self):
        import ogre.io.OIS as OIS
        import inputSystem
        self.engine.inputSystem.registerHandler(inputSystem.InputEvent.KEY_PRESSED, OIS.KC_N, self.dump)
        self.player = Player(self.engine.localOptions.playerOptions.side, self.engine.localOptions.playerOptions.playerId)

    def createEntity(self, handle, type, createSquad=True, additionalAspects=[], playerInfo = None):
        """
        Create a new entity of whatever type. 
        """
        ent = type(self.engine, handle, playerInfo)
        self._ents[handle] = ent
        ent.createAspects(additionalAspects)

        if ent.hasSquad and createSquad:
            squad = self.createEntity(self.createHandle(), boat.Squad)
            squad.SquadAI.squadMembers.append(ent)
            ent.squad = squad

        if ent.hasSquad:
            ent.squad.SquadAI.commands = [command.Stop(self.engine, 0)] # stop for 0 seconds
            ent.id = self.nEnts
            self.entMap[self.nEnts] = ent
            self.nEnts += 1

        netAspect = ent.findAspect(NetAspect)
        if netAspect:
            ent.squad.SquadAI.commands = [command.NetSlave(self.engine)]
            print "Net slave", str(ent)

        return ent

    dumpTimer = timer.Timer(60.0)
    def tick(self, dtime):
        for ent in self._ents.values():
            ent.tick(dtime)
        #if self.dumpTimer.check(dtime):
            #self.dump()

    def dump(self):
        print '--------------------------------------------------------------------------------'
        print 'EntMgr.Dump'
        print '--------------------------------------------------------------------------------'
        for ent in self._ents.values():
            if ent.isNormal:
                ent.dump()

    handleCounter = 0
    def createHandle(self):
        self.handleCounter = int(self.handleCounter + 1)
        return (self.engine.executionHandle, self.handleCounter)

    @property
    def ents(self):
        pass

    @ents.getter
    def ents(self):
        return self._ents.values()

    def findEntFromHandle(self, handle):
        return self._ents[handle]
