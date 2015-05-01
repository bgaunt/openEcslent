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


from aspect import Aspect

import inputSystem
from inputSystem import JoyAxes

from vector import vector3
import mathlib
import random
import colors

from timer import Timer
import ogre.io.OIS as OIS

import command

class ManualControl(Aspect):
    ''' Control with right stick of xbox gamepad
    '''
    turnDelta = 1.0


    def init(self):
        self.ddContext = self.engine.debugDrawSystem.getContext()
        self.timer = Timer(0.01)
        self.desiredSpeed = 0.0
        self.desiredHeading = 0.0

    def crosslink(self):
        if self.engine.inputSystem.joystick:
            self.gamepad = self.engine.inputSystem.joystick
        self.keyboard = self.engine.inputSystem.keyboard
        self.engine.inputSystem.registerHandler(inputSystem.InputEvent.KEY_PRESSED, OIS.KC_SPACE, self.spacebar)
        self.engine.inputSystem.registerHandler(inputSystem.InputEvent.KEY_PRESSED, OIS.KC_BACK, self.setToNetSlave)


    def spacebar(self):
        if self.ent.isSelected:
            if self.ent.UnitAI.state == self.ent.UnitAI.State.AI:
                self.setToManual()
            elif self.ent.UnitAI.state == self.ent.UnitAI.State.MANUAL_CONTROL:
                if self.engine.localOptions.networkingOptions.enableNetworking:
                    self.setToNetSlave()
                else:
                    self.setToStop()
            elif self.ent.UnitAI.state == self.ent.UnitAI.State.NET_SLAVE:
                self.setToManual()
            elif self.ent.UnitAI.state == self.ent.UnitAI.State.STOP:
                self.setToManual()
            else:
                print "Unknown state transition"

    def setToNetSlave(self):
        self.ent.squad.SquadAI.commands = [command.NetSlave(self.engine)] 

    def setToStop(self):
        self.ent.squad.SquadAI.commands = [command.Stop(self.engine, 0)] 

    def setToManual(self):
        self.ent.squad.SquadAI.commands = [command.ManualControl(self.engine)] 
        self.desiredSpeed = self.ent.desiredSpeed
        self.desiredHeading = self.ent.yaw


    def turnRight(self, dh, dtime):
        dh -= self.turnDelta*dtime
        while dh < -mathlib.pi:
            dh += mathlib.twopi
        return dh

    def turnLeft(self, dh, dtime):
        dh += self.turnDelta*dtime
        while dh > mathlib.pi:
            dh -= mathlib.twopi
        return dh
    
    def speedUp(self, ds, ms):
        return mathlib.clamp(ds + ms/100.0, 0, ms)


    def slowDown(self, ds, ms):
        return mathlib.clamp(ds - ms/100.0, 0, ms)


    def tick(self, dtime):
        self.ddContext.clear()        
        if self.ent.isSelected:
            if self.ent.UnitAI.state == self.ent.UnitAI.State.MANUAL_CONTROL:

                if self.engine.inputSystem.joystick:
                    joyState = self.gamepad.getJoyStickState()
                    if joyState.mAxes[JoyAxes.LEFT_LEFTRIGHT].abs > 10000: #right
                        self.desiredHeading = self.turnRight(self.desiredHeading, dtime)
                    if joyState.mAxes[JoyAxes.LEFT_LEFTRIGHT].abs < -10000: #left
                        self.desiredHeading = self.turnLeft(self.desiredHeading, dtime)
                    if joyState.mAxes[JoyAxes.LEFT_UPDOWN].abs > 10000:  #slower
                        self.desiredSpeed = self.slowDown(self.desiredSpeed, self.ent.maxSpeed)
                    if joyState.mAxes[JoyAxes.LEFT_UPDOWN].abs < -10000:   #faster
                        self.desiredSpeed = self.speedUp(self.desiredSpeed, self.ent.maxSpeed)

                # in any case you can use keyboard arrow control

                if self.keyboard.isKeyDown(OIS.KC_LEFT): 
                    self.desiredHeading = self.turnLeft(self.desiredHeading, dtime)
                if self.keyboard.isKeyDown(OIS.KC_RIGHT): 
                    self.desiredHeading = self.turnRight(self.desiredHeading, dtime)
                if self.keyboard.isKeyDown(OIS.KC_UP): 
                    self.desiredSpeed = self.speedUp(self.desiredSpeed, self.ent.maxSpeed)
                if self.keyboard.isKeyDown(OIS.KC_DOWN): 
                    self.desiredSpeed = self.slowDown(self.desiredSpeed, self.ent.maxSpeed)

                if self.timer.check(dtime):
                    v = vector3(self.ent.avoidanceSize.x/2.0 *  self.desiredSpeed, 0, 0)
                    sv = mathlib.yawwedVector(v, self.ent.yaw)
                    offset = mathlib.yawwedVector(v, self.desiredHeading)
                    self.engine.debugDrawSystem.drawRay(self.ddContext, self.ent.pos, offset, color = colors.BLUE)
