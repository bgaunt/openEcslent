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

import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

from misc import EasyLog1

import mgr 
import time
import command
import mathlib
from vector import vector2, vector3
import inputSystem
import actionMgr

from vector import vector2, vector3
from units import knots, degrees

from inputSystem import MouseEvent, MouseButton, Modifier

class SpeedHandle(object):
    def __init__(self):
        self.worldPos = None
        self.underMouse = False

class SelectedData(object):
    """
    Entities that are selected will have one of these classes attached to them
    Which we can use to store UI interaction data
    """
    def __init__(self):
        self.speedHandle = SpeedHandle()

class SelectionSystem(mgr.System):
    kSpeedHandleMouseOverTolerance = 0.10
    kSpeedSliderLength = 300.0
    kSpeedSliderWidth = 2.0
    kSpeedSliderBarWidth = 25.0
    kSpeedSliderBarThickness = 3.0

    @property 
    def selectedEnts(self):
        return list(self._selectedEnts)

    @property
    def primaryEnt(self):
        for a in self._selectedEnts:
            return a
        return None

    def __init__(self, engine):
        mgr.System.__init__(self, engine)
        self.selectionDDContext = self.engine.debugDrawSystem.getContext()
        #self.setSpeedDDContext = self.engine.debugDrawSystem.getContext()
        #self.rudderDisplayNodes = []
        #self.adjustSpeedHandleInputLock = None
        #self.adjustingSpeedHandleForEnt = None
        self.forceMovingEnts = None
        self.forceMovingEntMousePos = None
        self.forceMovingEntLock = None

    def initialize(self):
        self._selectedEnts = set()

    def crosslink(self):
        self.engine.inputSystem.registerMouseHandler(MouseEvent.MOUSE_MOVED,    None,               self.handleMouseMoved)
        self.engine.inputSystem.registerMouseHandler(MouseEvent.MOUSE_PRESSED,  MouseButton.LEFT,   self.handleMousePressed)
        self.engine.inputSystem.registerMouseHandler(MouseEvent.MOUSE_RELEASED, MouseButton.LEFT,   self.handleMouseReleased)

    def loadlevel(self):
        #self.entUnderMouse = None
        self._selectedEnts = set()

    def releaseLevel(self):
        #self.entUnderMouse = None
        self._selectedEnts = set()

    def selectEnts(self, newSelectedEnts):
        newSelectedEnts = set(newSelectedEnts)

        #cant believe it took me so long to think to use set functions for this..duh
        for ent in newSelectedEnts.difference(self._selectedEnts):
            ent.isSelected = True
            ent.selectionData = SelectedData()
        for ent in self._selectedEnts.difference(newSelectedEnts):
            ent.isSelected = False
            del ent.selectionData

        self._selectedEnts = newSelectedEnts

    def render(self):
        #move / place our UI square thing to display rudder setting
        return
        #rudder = 1.0
        #i = 0
        #for ent in self._selectedEnts:
            #while i >= len(self.rudderDisplayNodes):
                #print 'creating rudder node'
                #gent = self.engine.gfxSystem.sceneManager.createEntity('RudderGEnt%i' % i, 'RudderDisc.mesh')
                #gent = self.engine.gfxSystem.sceneManager.createEntity('RudderGEnt%i' % i, 'SquareX.mesh')
                #node = self.engine.gfxSystem.sceneManager.getRootSceneNode().createChildSceneNode('RudderNode%i' % i, vector3(0,0,0))
                #node.attachObject(gent)
                #node.setVisible(True)
                #self.rudderDisplayNodes.append(node)

                #print 'showing unitOverlay %i' % i
                #node = self.rudderDisplayNodes[i]
                #node.setVisible(True)
                #r = ent.selectionCircleRadius or ent.avoidanceSize.x
                #r *= 1.2
                #node.setPosition(ent.pos + vector3(0, 1, 0))
                #node.setScale(r, r, r)
                #node.resetOrientation()
                #node.yaw(ent.yaw - degrees(60))
                #print 'pos', self.rudderDisplayNodes[i].position, 'scale', self.rudderDisplayNodes[i].scale
                #i += 1

        #while i < len(self.rudderDisplayNodes):
            #print 'hiding unitOverlay %i' % i
            #self.rudderDisplayNodes[i].setVisible(False)
            #i += 1

    def tick(self, dtime):
        pass
        #self.setSpeedDDContext.clear()
        '''
        for ent in self._selectedEnts:
            if ent.UnitAI.destination: #ent.isClosestEntToMouse and 
                v = ent.UnitAI.destination - ent.pos
                sliderLength = self.kSpeedSliderLength #min(v.length() - ent.selectionCircleRadius, self.kSpeedSliderLength)
                v.normalise()
                cross = v.crossProduct(vector3(0,1,0))
                p0 = ent.pos + v * ent.selectionCircleRadius
                p1 = ent.pos + v * (ent.selectionCircleRadius + (ent.UnitAI.navDesiredSpeed / ent.maxSpeed) * sliderLength)

                coef = 1.0
                if ent.selectionData.speedHandle.underMouse:
                    coef = 2.0

                #draw the 5 lines that compose the speed handle
                self.engine.debugDrawSystem.drawLine(self.setSpeedDDContext, p0 + cross * self.kSpeedSliderWidth * coef, p1 + cross * self.kSpeedSliderWidth * coef)
                self.engine.debugDrawSystem.drawLine(self.setSpeedDDContext, p0 - cross * self.kSpeedSliderWidth * coef, p1 - cross * self.kSpeedSliderWidth * coef)
                self.engine.debugDrawSystem.drawLine(self.setSpeedDDContext, p1 - cross * self.kSpeedSliderBarWidth * coef, p1 + cross * self.kSpeedSliderBarWidth * coef)
                self.engine.debugDrawSystem.drawLine(self.setSpeedDDContext, p1 - cross * self.kSpeedSliderBarWidth * coef - v * self.kSpeedSliderBarThickness, p1 + cross * self.kSpeedSliderBarWidth * coef - v * self.kSpeedSliderBarThickness)
                self.engine.debugDrawSystem.drawLine(self.setSpeedDDContext, p1 - cross * self.kSpeedSliderBarWidth * coef + v * self.kSpeedSliderBarThickness, p1 + cross * self.kSpeedSliderBarWidth * coef + v * self.kSpeedSliderBarThickness)

                #draw the end bar showing max speed
                p2 = ent.pos + v * (ent.selectionCircleRadius + sliderLength)
                coef *= 1.5
                self.engine.debugDrawSystem.drawLine(self.setSpeedDDContext, p0 - cross * self.kSpeedSliderBarWidth * coef + v * self.kSpeedSliderBarThickness, p0 + cross * self.kSpeedSliderBarWidth * coef + v * self.kSpeedSliderBarThickness)
                self.engine.debugDrawSystem.drawLine(self.setSpeedDDContext, p2 - cross * self.kSpeedSliderBarWidth * coef + v * self.kSpeedSliderBarThickness, p2 + cross * self.kSpeedSliderBarWidth * coef + v * self.kSpeedSliderBarThickness)
                #self.engine.debugDrawSystem.drawLine(self.setSpeedDDContext, p2 - cross * self.kSpeedSliderBarWidth * coef - v * self.kSpeedSliderBarThickness * coef, p2 + cross * self.kSpeedSliderBarWidth * coef - v * self.kSpeedSliderBarThickness * coef)
                #self.engine.debugDrawSystem.drawLine(self.setSpeedDDContext, p2 - cross * self.kSpeedSliderBarWidth * coef + v * self.kSpeedSliderBarThickness * coef, p2 + cross * self.kSpeedSliderBarWidth * coef + v * self.kSpeedSliderBarThickness * coef)
                ent.selectionData.speedHandle.startWorldPos = p0
                ent.selectionData.speedHandle.worldPos = p1
                ent.selectionData.speedHandle.endWorldPos = p2

                #draw ticks for every 5 knots on the handle
                f = 0.0
                i = 0
                while f < 1.0:
                    f += knots(5.0) / ent.maxSpeed
                    if f > 1.0:
                        break
                    i += 1
                    coef = ((i % 4) == 0) and 1.0 or 0.75
                    p2 = ent.pos + v * (ent.selectionCircleRadius + sliderLength * f)
                    self.engine.debugDrawSystem.drawLine(self.setSpeedDDContext, p2 - cross * self.kSpeedSliderBarWidth * coef + v * self.kSpeedSliderBarThickness, p2 + cross * self.kSpeedSliderBarWidth * coef + v * self.kSpeedSliderBarThickness)
    '''

    def handleMouseMoved(self, ms):
        """
        Are we grabbing any speed handles?
        how do we do tihs?
        when we detect a button down we need to search for avaiable handles to grab
        if one is avaiable, then grab it, and signal the rest of the universe to ignore this left click
        """
        if self.forceMovingEntLock:
            assert(len(self.forceMovingEnts) > 0)
            mousePosWorld = self.engine.inputSystem.mousePosWorld
            dpos = mousePosWorld - self.forceMovingEntMousePos
            self.forceMovingEntMousePos = mousePosWorld
            for ent in self.forceMovingEnts:
                ent.pos += dpos
                ent.pos.dirty = True
        '''
        elif self.adjustingSpeedHandleForEnt:
            #thoughts?? can just check dot product to find how much our pos lies along that line
            ent                             = self.adjustingSpeedHandleForEnt
            vecEntToMouse                   = ent.pos - self.engine.inputSystem.mousePosWorld
            vecEntToHandleEnd               = ent.pos - ent.selectionData.speedHandle.endWorldPos
            vecEntToHandleEnd.normalise()
            d                               = vecEntToMouse.dotProduct(vecEntToHandleEnd) - ent.selectionCircleRadius
            speed = ent.maxSpeed * mathlib.clamp(d / self.kSpeedSliderLength, 0.0, 1.0)
            for ent in self.selectedEnts:
                action = actionMgr.AdjustSpeed(self.engine.gameTime, ent.handle, mathlib.clamp(speed, 0.0, ent.maxSpeed))
                self.engine.actionMgr.enqueue(action)

        else:
            closest         = None
            closestDist     = self.kSpeedHandleMouseOverTolerance
            mousePosScreen = vector2(ms.X.abs / float(ms.width) * 2.0 - 1.0, 
                                     ms.Y.abs / float(ms.height) * -2.0 + 1.0)

            for ent in self.selectedEnts:
                mat                  = self.engine.cameraSystem.camera.getProjectionMatrix() * self.engine.cameraSystem.camera.getViewMatrix()
                if ent.selectionData.speedHandle.worldPos:
                    speedHandlePosScreen = mat * ent.selectionData.speedHandle.worldPos
                    speedHandlePosScreen = vector2(speedHandlePosScreen.x, speedHandlePosScreen.y)
                    distScreen           = (speedHandlePosScreen - mousePosScreen).length()
                    if distScreen < closestDist:
                        closestDist = distScreen
                        closest     = ent

            for ent in self.selectedEnts:
                if ent == closest:
                    ent.selectionData.speedHandle.underMouse = True
                else:
                    ent.selectionData.speedHandle.underMouse = False
        '''
        return False

    def handleMousePressed(self, ms):
        lock = self.engine.inputSystem.getInputLock(MouseButton.LEFT)
        if lock:
            if self.engine.inputSystem.mouseDownModifiers[MouseButton.LEFT][Modifier.ALT]:
                if self.engine.inputSystem.entUnderMouse:
                    self.forceMovingEntLock = lock
                    self.forceMovingEntLock.acquire()
                    self.forceMovingEntMousePos = self.engine.inputSystem.mousePosWorld
                    if self.engine.inputSystem.entUnderMouse in self.selectedEnts:
                        self.forceMovingEnts = self.selectedEnts
                    else:
                        self.forceMovingEnts = [self.engine.inputSystem.entUnderMouse]
            '''
            else:
                for ent in self.selectedEnts:
                    if ent.selectionData.speedHandle.underMouse:
                        lock.acquire()
                        self.adjustSpeedHandleInputLock = lock
                        self.adjustingSpeedHandleForEnt = ent
                        break
            '''

    def handleMouseReleased(self, ms):
        if self.forceMovingEntLock:
            self.forceMovingEntLock.release()
            self.forceMovingEntLock = None
            self.forceMovingEnts = None
            self.forceMovingEntMousePos = None

        # if self.adjustSpeedHandleInputLock:
        #     self.adjustSpeedHandleInputLock.release()
        #     self.adjustSpeedHandleInputLock = None
        #     self.adjustingSpeedHandleForEnt = None
