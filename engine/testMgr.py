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

import pdb
import random
import math

import mathlib
import boat
from vector import vector3
from units import knots, degrees
from mgr import Mgr
from desiredState import StoppedAtPosition, MaintainingRelativeToEnt
import command
from netAspect import NetAspect

import entMgr

class TestMgr(Mgr):
    """
    Only runs on server
    """

    additionalAspects = []
    def loadLevel(self):
        if self.engine.localOptions.networkingOptions.enableNetworking and not self.engine.localOptions.networkingOptions.server:
            return
        if self.engine.localOptions.networkingOptions.server:
            self.additionalAspects = []
        self.test = self.engine.localOptions.gameOptions.testToRun
        print 'TestMgr.loadLevel', self.test
        if self.test == 0:
            self.setupOpenOceanEmptyScenario()
        elif self.test == 1:
            self.setupAvoidanceTest0()
        elif self.test == 2:
            self.setupAvoidanceTest1()
        elif self.test == 3:
            self.setupAvoidanceTest2()
        elif self.test == 4:
            self.setupAvoidanceTest3()
        elif self.test == 5:
            self.setupCarrierApproach(20)
        elif self.test == 6:
            self.setupCarrierApproach(100)
        elif self.test == 7:
            self.setupRightAngleAvoidanceTest()
        elif self.test == 8:
            self.setupBoatComparison()
        elif self.test == 9:
            self.setupNetTest(2)
        elif self.test == 10:
            self.setupKrakenNet(2)
        elif self.test == 11:
            self.multiPlayerNetTest(5)

    def setupKrakenNet(self, boatCount):
        """

        """
        boatTypes =  [boat.DDG51, boat.CVN68, boat.SPEEDBOAT]
        x = -100 * len(boatTypes)
        z = -100 * boatCount
        nextYaw  = 0
        for boatType in boatTypes:
            for i in range(boatCount):
                ent = self.engine.entMgr.createEntity(self.engine.entMgr.createHandle(), boatType)
                ent.pos.x = x
                ent.pos.z = z
                x += 200
                cmd = command.Stop(self.engine, 0)
                ent.squad.SquadAI.commands = [cmd]
                ent.yaw = random.choice([math.pi/2, -math.pi/2, math.pi]);


            
    def setupNetTest(self, boatCount):
        """

        """
        x = -100 * len(self.engine.entMgr.types)
        z = -50 * boatCount
        for boatType in [boat.DDG51, boat.CVN68, boat.SPEEDBOAT]:
            for i in range(boatCount):
                ent = self.engine.entMgr.createEntity(self.engine.entMgr.createHandle(), boatType)
                ent.pos.x = x
                ent.pos.z = z
                z += 100
                cmd = command.Stop(self.engine, 0)
                ent.squad.SquadAI.commands = [cmd]
            x += 200
            z = -50 * boatCount

            
    def setupOpenOceanEmptyScenario(self):
        pass

    def setupAvoidanceTest0(self):
        self.createSampleEntities([boat.CIGARETTE])
        self.createObstactleCourseEntities(1)

    def setupAvoidanceTest1(self):
        self.createSampleEntities([boat.DDG51])
        self.createObstactleCourseEntities(5)

    def setupAvoidanceTest2(self):
        """
        Lets do a basic cross between two ddgs moving towards each other
        """
        ent1 = self.engine.entMgr.createEntity(self.engine.entMgr.createHandle(), boat.DDG51, additionalAspects = self.additionalAspects)
        ent1.pos.x = 0
        ent1.yaw = -mathlib.halfpi
        ent1.pos.z = -1000 
        desiredState = StoppedAtPosition(vector3(0, 0, +1000))
        cmd = command.MoveTo(self.engine, desiredState)
        ent1.squad.SquadAI.commands = [cmd]

        ent2 = self.engine.entMgr.createEntity(self.engine.entMgr.createHandle(), boat.DDG51, additionalAspects = self.additionalAspects)
        ent2.pos.x = 0
        ent2.pos.z = +1000 
        ent2.yaw = mathlib.halfpi
        desiredState = StoppedAtPosition(vector3(0, 0, -1000))
        cmd = command.MoveTo(self.engine, desiredState)
        ent2.squad.SquadAI.commands = [cmd]

    def setupRightAngleAvoidanceTest(self):
        """
        The one case we could never get well with lagoon
        Two ddg's at right angles
        """
        ent1 = self.engine.entMgr.createEntity(self.engine.entMgr.createHandle(), boat.DDG51, additionalAspects = self.additionalAspects)
        ent1.pos.x = 0
        ent1.yaw = -mathlib.halfpi
        ent1.pos.z = -1000 
        desiredState = StoppedAtPosition(vector3(0, 0, +1000))
        cmd = command.MoveTo(self.engine, desiredState)
        ent1.squad.SquadAI.commands = [cmd]

        ent2 = self.engine.entMgr.createEntity(self.engine.entMgr.createHandle(), boat.DDG51, additionalAspects = self.additionalAspects)
        ent2.pos.x = -1000
        ent2.pos.z = 0 
        ent2.yaw = 0.0
        desiredState = StoppedAtPosition(vector3(1000, 0, 0))
        cmd = command.MoveTo(self.engine, desiredState)
        ent2.squad.SquadAI.commands = [cmd]

    def setupAvoidanceTest3(self):
        self.createObstactleCourseEntities(5)
        for i in range(3):
            ent = self.engine.entMgr.createEntity(self.engine.entMgr.createHandle(), boat.DDG51, additionalAspects = self.additionalAspects)
            ent.pos = mathlib.randomVectorSquare(500) + vector3(0, 0, 500)
            #ent.yaw = random.uniform(0, mathlib.twopi)
            ent.yaw = math.radians(90)
            desiredState = StoppedAtPosition(vector3(0, 0, -2000))
            cmd = command.MoveTo(self.engine, desiredState)
            ent.squad.SquadAI.commands = [cmd]

    def setupCarrierApproach(self, numSpeedBoats):
        spawnCarrier = True

        if spawnCarrier:
            carrier = self.engine.entMgr.createEntity(self.engine.entMgr.createHandle(), boat.CVN68, additionalAspects = self.additionalAspects)
            carrier.pos.x = 5
            carrier.pos.z = 12
            carrier.yaw = mathlib.halfpi
            desiredState = StoppedAtPosition(vector3(0, 0, -5000))
            cmd = command.MoveTo(self.engine, desiredState, desiredSpeed=knots(10))
            #carrier.squad.strategicData.commands = [cmd]
            carrier.squad.SquadAI.commands = [cmd]

        startPositionCenters        = [vector3(2000,0,-1000), vector3(2000,0,1000)]
        targetOffsets               = [vector3(50,0,150)]#, vector3(-50,0,150)]
        kStartPosSize               = 600
        kApproachRadiusSizeMinMax   = (300, 500)
        for i in range(numSpeedBoats):
            startPosCenter = startPositionCenters[i % len(startPositionCenters)]
            offset = mathlib.randomVectorSquare(kStartPosSize)
            startPos = startPosCenter + offset

            smallBoat = self.engine.entMgr.createEntity(self.engine.entMgr.createHandle(), boat.SPEEDBOAT, additionalAspects = self.additionalAspects)
            smallBoat.pos.x = startPos.x
            smallBoat.pos.z = startPos.z
            smallBoat.yaw = mathlib.pi
            assert carrier

            #offset = targetOffsets[i % len(targetOffsets)]
            offset = mathlib.randomVectorCircular(*kApproachRadiusSizeMinMax)
            desiredState = MaintainingRelativeToEnt(carrier, offset)
            cmd = command.MoveTo(self.engine, desiredState)
            smallBoat.squad.SquadAI.commands = [cmd]

    def setupBoatComparison(self):
        boatSpacing = 200
        z = 0
        for boatType in self.engine.entMgr.types:
            ent = self.engine.entMgr.createEntity(self.engine.entMgr.createHandle(), boatType, additionalAspects = self.additionalAspects)
            ent.pos.z = z
            z += boatSpacing

    def createSampleEntities(self, types = None):
        if types is None:
            types = self.types
        x = 0
        for type in types:
            ent = self.engine.entMgr.createEntity(self.engine.entMgr.createHandle(), type, additionalAspects = self.additionalAspects)
            ent.pos.x = x
            #self.giveRandomMoveToOrderToEnt(ent)
            #self.makeMoveToOtherSideOfObstacles(ent)
            x -= type.length


    def createObstactleCourseEntities(self, width):
        x = 0
        z = 1000

        type = boat.DDG51
        for i in range(width / 2 - width + 1, width / 2 + 1):
            x = i * type.length 
            print x
            for zcoef in [-1]:
                ent = self.engine.entMgr.createEntity(self.engine.entMgr.createHandle(), type, additionalAspects = self.additionalAspects)
                ent.pos.x = x
                ent.pos.z = z * zcoef

    def giveRandomMoveToOrderToEnt(self, ent):
        #desiredState = desiredState.Location(mathlib.randomVectorSquare(500))
        #cmd = cmd.MoveTo(self.engine, desiredState)
        cmd = command.MoveRandomly(self.engine, 1000)
        ent.squad.SquadAI.commands = [cmd]

    def makeMoveToOtherSideOfObstacles(self, ent):
        ent.yaw = degrees(90)
        desiredState = StoppedAtPosition(vector3(0, 0, -2000))
        cmd = command.MoveTo(self.engine, desiredState)
        ent.squad.SquadAI.commands = [cmd]


    def multiPlayerNetTest(self, numSpeedBoats):
        spawnCarrier = True

        if spawnCarrier:
            carrier = self.engine.entMgr.createEntity(self.engine.entMgr.createHandle(), boat.CVN68, additionalAspects = self.additionalAspects, playerInfo = entMgr.Player(entMgr.Side.BLUE, 0))
            carrier.pos.x = 5
            carrier.pos.z = 12
            carrier.yaw = mathlib.halfpi
            desiredState = StoppedAtPosition(vector3(0, 0, -5000))
            cmd = command.MoveTo(self.engine, desiredState, desiredSpeed=knots(10))
            #carrier.squad.strategicData.commands = [cmd]
            carrier.squad.SquadAI.commands = [cmd]

        startPositionCenters        = [vector3(2000,0,-1000), vector3(2000,0,1000)]
        targetOffsets               = [vector3(50,0,150)]#, vector3(-50,0,150)]
        kStartPosSize               = 600
        kApproachRadiusSizeMinMax   = (300, 500)
        for i in range(numSpeedBoats):
            startPosCenter = startPositionCenters[i % len(startPositionCenters)]
            offset = mathlib.randomVectorSquare(kStartPosSize)
            startPos = startPosCenter + offset

            smallBoat = self.engine.entMgr.createEntity(self.engine.entMgr.createHandle(), boat.SPEEDBOAT, additionalAspects = self.additionalAspects, playerInfo = entMgr.Player(entMgr.Side.RED, 1))
            smallBoat.pos.x = startPos.x
            smallBoat.pos.z = startPos.z
            smallBoat.yaw = mathlib.pi
            assert carrier

            #offset = targetOffsets[i % len(targetOffsets)]
            offset = mathlib.randomVectorCircular(*kApproachRadiusSizeMinMax)
            desiredState = MaintainingRelativeToEnt(carrier, offset)
            cmd = command.MoveTo(self.engine, desiredState)
            smallBoat.squad.SquadAI.commands = [cmd]

