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

import time

from aspect import Aspect
from control import ManualControl
import command
from mathlib import *
from units   import *
from collections import deque
from vector import vector3


SPEED_TOLERANCE = 0.1
HEADING_TOLERANCE = mathlib.pi/360.0
LAG_LENGTH = 5


class NetAspect(Aspect):
    ''' Store information about networked ent
    '''

    def initNetworking(self, id, status):
        self.id = id
        self.statusData = status
        # for now --> this should go away as soon as Mike changes the 
        # rotational speed to be math.halfpi - rotationalSpeed in the Daemon
        self.lerpRot = self.lerpECSLRot
        self.lerpPos = self.lerpECSLPos

        self.remotePos = vector3(self.statusData.pos[0], self.statusData.pos[1], self.statusData.pos[2])
        self.ent.pos = self.remotePos
        import netMgr
        if netMgr.gMoveCameraToEntPos == self.ent and self.engine.cameraSystem.cameraCenterPos:
            self.engine.cameraSystem.lookAt(self.ent)
            netMgr.gMoveCameraToEntPos = None

        self.newPos  = self.ent.pos
        self.ent.yaw = self.statusData.yaw 
        self.remoteVel = vector3(self.statusData.vel[0], self.statusData.vel[1], self.statusData.vel[2])
        self.ent.speed = self.remoteVel.length()
        self.ent.desiredHeading, self.ent.desiredSpeed = (self.statusData.dh, self.statusData.ds)

        self.oldTime = 0
        self.latency = 0
        self.ent.updateQueue = deque(maxlen=LAG_LENGTH)

        self.netCommand  = None
        self.squelchCommand = None

        # let us create all local vars here
        self.dh, self.ds = (0.0, 0.0)

        # for interpolation
        self.nSteps        = 0
        self.nextRemotePos = None
        self.diffPos       = None
        self.diffPosFrac   = None
        self.remoteQuat    = None
        self.destOrie      = None
        self.srcOrie       = None
        self.rotFactor     = 0
        self.rotProgress   = 1.0


    def crosslink(self):
        self.netMgr = self.engine.netMgr
        self.controlAspect = self.ent.findAspect(ManualControl)
    
    def tick(self, dtime):
        self.updateEcslent(dtime)
        if self.ent.UnitAI.state == self.ent.UnitAI.State.AI or self.ent.UnitAI.state == self.ent.UnitAI.State.STOP:
            self.updateServer(self.ent.UnitAI.helmDesiredSpeed, self.ent.UnitAI.helmDesiredHeading)
        elif self.ent.UnitAI.state == self.ent.UnitAI.State.MANUAL_CONTROL:
            self.updateServer(self.controlAspect.desiredSpeed, self.controlAspect.desiredHeading)

    def lerpECSLPos(self):
        self.remoteVel = vector3(self.statusData.vel[0], self.statusData.vel[1], self.statusData.vel[2])
        self.remotePos = vector3(self.statusData.pos[0], self.statusData.pos[1], self.statusData.pos[2])
        self.nextRemotePos = self.remotePos + (self.remoteVel * self.latency)
        self.nextPos = self.ent.pos + (self.ent.velocity * self.latency)
        self.diffPos = self.nextPos - self.nextRemotePos
        self.diffPosFrac = self.diffPos/self.nSteps

    def lerpECSLRot(self):
        self.remoteQuat  = pitchYawRoll(0, toDegrees(self.statusData.yaw), 0)
        self.destOrie = self.remoteQuat * pitchYawRoll(0, toDegrees(self.statusData.rSpeed * self.latency), 0)
        self.srcOrie  = pitchYawRoll(0, toDegrees(self.ent.yaw), 0)
        self.finalDestOrie = self.destOrie * self.srcOrie
        if self.destOrie.equals(self.srcOrie, HEADING_TOLERANCE): # this is critical
            self.rotFactor  = 1.0
            self.rotProgress = 1.0
        else:
            self.rotFactor  = 1.0/self.nSteps
            self.rotProgress = self.rotFactor


    def updateEcslent(self, dtime):
        if self.engine.selectionSystem.forceMovingEnts: #handle forced moves
            if self.ent in self.engine.selectionSystem.forceMovingEnts:
                return
        if self.ent.updateQueue: # handle served position, orientation
            self.statusData = self.ent.updateQueue.popleft() #get the latest throw out the rest
            self.ent.updateQueue.clear()
            self.nSteps = 0
            if self.statusData.time > self.oldTime:
                self.latency = (self.statusData.time - self.oldTime)/1000.0 # VShip time is in milliseconds
                self.oldTime = self.statusData.time
                self.nSteps = self.latency/dtime

                self.lerpPos() # these are function pointers set in initNetworking
                self.lerpRot() # these are function pointers set in initNetworking

                #self.ent.speed = self.remoteVel.length()

                self.ent.desiredSpeed = self.statusData.ds #does vship send ds in knots? NO
                self.ent.desiredHeading = self.statusData.dh
            else:
                self.rotProgress = 1.0
                self.nSteps = 0

        if self.nSteps > 0:
            self.ent.pos -= self.diffPosFrac
            if(self.rotProgress < 1.0):
                self.qDelta = quat.Slerp(self.rotProgress, self.srcOrie, self.destOrie, True)
                self.deltaYaw = self.qDelta.getYaw().valueRadians()
                self.ent.yaw = self.deltaYaw
                self.rotProgress += self.rotFactor

            self.nSteps -= 1

    def withinSpeedTolerance(self, a, b):
        return math.fabs(a - b) < SPEED_TOLERANCE

    def withinHeadingTolerance(self, a, b):
        return math.fabs(a - b) < HEADING_TOLERANCE

    def squelch(self):
        if self.ent.hasSquad:
            self.ent.squad.SquadAI.commands = [command.NetSlave(self.engine)]

    def squelchOthers(self):
        self.squelchCommand = self.netMgr.squelch.pack(self.id)
        self.netMgr.addSquelch(self.squelchCommand)
        #self.msg = self.netMgr.header.pack(self.netMgr.SquelchCommand, int(self.netMgr.simTimeMilli()), 1, self.netMgr.squelch.size) + self.squelchCommand
        #self.netMgr.send(self.msg)

    def updateServer(self, newDS, newDH):
        ''' Called ONLY if unitAI is in State.AI or State.Manual_Control
        '''
        if self.withinSpeedTolerance(self.ds, newDS) and self.withinHeadingTolerance(self.dh, newDH):
            pass # don't send any message
        else:
            self.ds = newDS
            self.dh = newDH
            #print "Potential command: ", str(self.ent), self.id, self.ent.UnitAI.state
            #print "Potential command limits: ", -math.pi, self.dh, math.pi, self.ent.maxSpeed, self.ds,  
            if self.dh >= -math.pi and self.dh <= math.pi and self.ds <= self.ent.maxSpeed + 1 and self.ds >= -0.1:
                #print "Commanding: ", str(self.ent), self.id, self.ent.UnitAI.state, self.ds, self.dh
                self.netCommand = self.netMgr.command.pack(self.id, self.dh, self.ds)
                self.netMgr.addCommand(self.netCommand)
                self.squelchOthers()
