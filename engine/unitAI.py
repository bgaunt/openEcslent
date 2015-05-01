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
import math
import random
import cent

import timer
import command
from aspect import Aspect
from control import ManualControl

from vector import vector2, vector3
from units import degrees, knots, toKnots
import mathlib
import desiredState



kCEntInvalidFloat = cent.getInvalidFloat()[0]

class Voters:
    MAINTAIN_HEADING = 0
    TOWARDS_DEST = 1
    AVOID_COLLISIONS = 2
    NUM = 3


class UnitAI(Aspect):
    """
    Maintains individual level control of a unit 
    This class ALWAYS works in tandem with a squad ent / ai
    """
    class State:
        AI = 0
        NET_SLAVE = 1
        MANUAL_CONTROL = 2
        STOP = 3

    updateFrequency = 1.0
    commandsDirty = False
    def init(self):
        self.ent.squad = None
        self.destination = None

        self.ddContextLong = self.engine.debugDrawSystem.getContext()

        self._commands = []
        self.updateTimer = timer.Timer(self.updateFrequency, fireFirstCheck=True)

        self.cent = cent.CEnt(self.ent.maxSpeed, 
                self.ent.maxSpeed * -.5, 
                self.ent.accelSpeed, 
                self.ent.rotationalSpeed, 
                self.ent.avoidanceSize.x, 
                self.ent.avoidanceSize.z,
                self.ent.collisionLookAheadTime,
                self.ent.maxDistanceForFullStop,
                self.ent.minDistanceForFullStop,
                self.ent.crampDistance,
                self.ent.collisionClass
        )

        self.ent.desiredHeading = 0
        self.ent.desiredSpeed = 0
        self.ent.speed = 0
        self.ent.velocity = vector3(0,0,0)
        #self.helmDesiredSpeed   = 0
        #self.helmDesiredHeading = 0

        self.ent.uiDesiredSpeed = kCEntInvalidFloat

        self.ddContext = self.engine.debugDrawSystem.getContext()
        self.updateCounter = 0
        self.state = self.State.AI
        self.stopAtDestination = True

    def crosslink(self):
        self.cent.register()
        self.controlAspect = self.ent.findAspect(ManualControl)

    lastSelectionState = None
    def tick(self, dtime):
        if self.commandsDirty or self.updateTimer.check(dtime):
            """
            Translate our desiredState into world coordinates, and let the low level c api do all the work
            """
            self.commandsDirty = False
            self.ddContextLong.clear()
            current = self.command
            if current is None:
                self.ent.hasDestination = False
                return

            elif type(current) == command.MoveTo:
                currentWP = current.desiredState.calcWorldPos(self.ent)
                if len(self.commands) > 1:
                    #we are an interimittent move - if we have a next point see if we rae hitting this one and then mvoe on
                    vecToGoal = self.ent.pos - currentWP
                    distanceToGoal = vecToGoal.length()
                    if distanceToGoal < self.ent.moveToReachedTolerance:
                        del self.commands[0]
                    self.stopAtDestination = False
                else:
                    self.stopAtDestination = True

                self.state = self.State.AI
                self.destination = currentWP

                if current.desiredSpeed is None:
                    self.navDesiredSpeed = self.ent.uiDesiredSpeed
                else:
                    self.navDesiredSpeed = current.desiredSpeed

                if type(current.desiredState) == desiredState.MaintainingRelativeToEnt:
                    self.cent.inRamMode = current.desiredState.offset.length() < 50.0
                    if self.ent.isSelected:
                        self.engine.debugDrawSystem.drawLine(self.ddContextLong, current.desiredState.ent.pos, currentWP)
                else:
                    self.cent.inRamMode = False

                if self.ent.isSelected:
                    p = self.ent.pos
                    for c in self._commands:
                        p2 = c.desiredState.calcWorldPos(self.ent)
                        self.engine.debugDrawSystem.drawLine(self.ddContextLong, p, p2)
                        p = p2
                    self.engine.debugDrawSystem.drawCircle(self.ddContextLong, self.destination, 100.0)
                    if self.cent.inRamMode:
                        import colors
                        self.engine.debugDrawSystem.drawCircle(self.ddContextLong, self.destination, 110.0, color=colors.RED)

            elif type(current) == command.Stop:
                self.state = self.State.STOP
                self.ent.hasDestination = False
                self.destination = None

            elif type(current) == command.NetSlave:
                self.state = self.State.NET_SLAVE
                self.ent.hasDestination = False
                self.destination = None

            elif type(current) == command.ManualControl:
                self.state = self.State.MANUAL_CONTROL
                self.ent.hasDestination = False
                self.destination = None

            else:
                raise Exception('Not Implemented %s' % current)

        if self.state == self.State.AI:
            self.cent.posX = self.ent.pos.x
            self.cent.posY = self.ent.pos.z
            self.cent.yaw  = self.ent.yaw

            #pass control data down to cent land
            if self.destination:
                self.cent.destinationX = self.destination.x
                self.cent.destinationY = self.destination.z
                self.cent.stopAtDestination = self.stopAtDestination
#####get the desired heading and speed
                self.desiredHeading = math.atan2((self.ent.pos.z- self.destination.z), -1*(self.ent.pos.x - self.destination.x))
                if(self.desiredHeading > math.pi):
                    self.desiredHeading -= 2*math.pi
                elif(self.desiredHeading < -(math.pi)):
                    self.desiredHeading += 2*math.pi
                self.cent.helmDesiredHeading = self.desiredHeading

                #get desired speed
                self.distance = pow((self.destination.x - self.ent.pos.x),2) + pow((self.destination.z - self.ent.pos.z),2)
                if(self.distance > 15000):
                    self.desiredSpeed = self.ent.maxSpeed
                else:
                    self.desiredSpeed = 0
                self.cent.helmDesiredSpeed = self.desiredSpeed


            self.cent.tick(dtime)

            self.ent.pos.x = self.cent.posX
            self.ent.pos.z = self.cent.posY
            self.ent.yaw = self.cent.yaw
            self.ent.speed = self.cent.speed
            self.ent.velocity = vector3(self.cent.velX, 0, self.cent.velY)

            #self.helmDesiredSpeed   = self.cent.helmDesiredSpeed   #To tell VShip
            #self.helmDesiredHeading = self.cent.helmDesiredHeading

            #take all my c debugging requests and pass them up to python debug drawer
            if self.ent.isSelected:
                if self.updateCounter != self.cent.updateCounter:
                    self.ddContext.clear()
                    self.updateCounter = self.cent.updateCounter
                    debugLines = self.cent.getDebugLines()
                    for cdebugline in self.cent.getDebugLines():
                        self.engine.debugDrawSystem.drawLine(self.ddContext,
                                                             vector3(cdebugline[0], 0, cdebugline[1]),
                                                             vector3(cdebugline[2], 0, cdebugline[3])
                        )
            else:
                self.ddContext.clear()

        elif self.state == self.State.MANUAL_CONTROL:
            
            self.cent.posX = self.ent.pos.x
            self.cent.posY = self.ent.pos.z
            self.cent.yaw  = self.ent.yaw
            
            self.cent.helmDesiredSpeed = self.controlAspect.desiredSpeed     # keyboard or joystick
            self.cent.helmDesiredHeading = self.controlAspect.desiredHeading

            self.cent.helmTick(dtime);

            self.ent.pos.x = self.cent.posX
            self.ent.pos.z = self.cent.posY
            self.ent.yaw = self.cent.yaw
            self.ent.speed = self.cent.speed            
            self.ent.velocity = vector3(self.cent.velX, 0, self.cent.velY)
            
        elif self.state == self.State.STOP:

            self.cent.posX = self.ent.pos.x
            self.cent.posY = self.ent.pos.z
            self.cent.yaw  = self.ent.yaw
            
            self.cent.helmDesiredSpeed   = 0.0
            self.cent.helmDesiredHeading = self.ent.yaw

            self.cent.helmTick(dtime);

            self.ent.pos.x = self.cent.posX
            self.ent.pos.z = self.cent.posY
            self.ent.yaw = self.cent.yaw
            self.ent.speed = self.cent.speed            
            self.ent.velocity = vector3(self.cent.velX, 0, self.cent.velY)


        else: #state == NET_SLAVE
            self.cent.posX = self.ent.pos.x
            self.cent.posY = self.ent.pos.z
            self.cent.yaw  = self.ent.yaw
            
            self.cent.helmDesiredSpeed = self.ent.desiredSpeed     # from network or keyboard or joystick
            self.cent.helmDesiredHeading = self.ent.desiredHeading
            #print "UnitAI: DS, DH: ", self.ent.desiredSpeed, self.ent.desiredHeading
            self.cent.helmTick(dtime);

            self.ent.pos.x = self.cent.posX
            self.ent.pos.z = self.cent.posY
            self.ent.yaw = self.cent.yaw
            self.ent.speed = self.cent.speed            

            self.ent.velocity = vector3(self.cent.velX, 0, self.cent.velY)


    @property
    def helmDesiredSpeed(): 
        pass

    @property
    def helmDesiredHeading(): 
        pass

    @helmDesiredSpeed.setter
    def helmDesiredSpeed(self, value):
        self.cent.helmDesiredSpeed = value

    @helmDesiredSpeed.getter
    def helmDesiredSpeed(self):
        return self.cent.helmDesiredSpeed

    @helmDesiredHeading.setter
    def helmDesiredHeading(self, value):
        self.cent.helmDesiredHeading = value

    @helmDesiredHeading.getter
    def helmDesiredHeading(self):
        return self.cent.helmDesiredHeading

    @property
    def navDesiredSpeed(): 
        pass

    @property
    def navDesiredHeading(): 
        pass

    @navDesiredSpeed.setter
    def navDesiredSpeed(self, value):
        self.cent.navDesiredSpeed = value

    @navDesiredSpeed.getter
    def navDesiredSpeed(self):
        if self.cent.navDesiredSpeed == kCEntInvalidFloat:
            return self.ent.maxSpeed
        else:
            return self.cent.navDesiredSpeed

    @navDesiredHeading.setter
    def navDesiredHeading(self, value):
        self.cent.navDesiredHeading = value

    @navDesiredHeading.getter
    def navDesiredHeading(self):
        return self.cent.navDesiredHeading


    @property 
    def command(self):
        pass

    @command.getter
    def command(self):
        return self._commands and self._commands[0] or None

    @property 
    def commands(self):
        return self._commands

    @commands.setter
    def commands(self, commands):
        self._commands = commands
        self.commandsDirty = True
