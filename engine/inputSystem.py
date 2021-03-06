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

import copy
import math
import time

import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

from misc import EasyLog, EasyLog1

import sys
import mgr 
import command
import desiredState
import mathlib
from vector import vector3
import actionMgr

import squadAI

import rect

kCameraMinHeight = 25
kSelectionRadius  = .05

kPressTime = 0.2
kCameraKeyMovementTrailoffTime = 0.2
kCameraZoomInOutTrailTime = 0.05
kCameraMaxTrailTime = 0.5
kCameraSpeed = 450
kCameraRotateSpeed = 0.25
#---------------------------------------------------------------    
class InputEvent:
    KEY_DOWN = 0
    KEY_UP = 1
    KEY_PRESSED = 2
    NUM = 3

class MouseEvent:
    MOUSE_PRESSED  = 0
    MOUSE_DRAGGED  = 1
    MOUSE_RELEASED = 2
    MOUSE_MOVED    = 3
    NUM            = 4
    INVALID         = 5

class JoyEvent:
    BUTTON_PRESSED  = 0
    BUTTON_RELEASED = 1
    AXIS_MOVED      = 2
    POV_MOVED       = 3
    VECTOR3_MOVED   = 4
    NUM             = 5
    INVALID         = 6

class MouseButton:
    LEFT    = OIS.MB_Left
    RIGHT   = OIS.MB_Right
    MIDDLE  = OIS.MB_Middle
    BUTTON3 = OIS.MB_Button3
    BUTTON4 = OIS.MB_Button4
    BUTTON5 = OIS.MB_Button5
    BUTTON6 = OIS.MB_Button6
    BUTTON7 = OIS.MB_Button7
    NUM     = 8
    LIST    = [LEFT, RIGHT, MIDDLE, BUTTON3, BUTTON4, BUTTON5, BUTTON6, BUTTON7]

class JoyButtons: # XBox Controller, the buttons need to be checked
    BACK       = 0
    A          = 1
    B          = 2
    X          = 3
    Y          = 4
    LEFT       = 5
    RIGHT      = 6
    START      = 7
    XBOX       = 8
    LEFT_AXIS  = 9
    RIGHT_AXIS = 10
    POV        = 11

    NUM     = 12
    LIST    = [BACK, A, B, X, Y, LEFT, RIGHT, START, XBOX, LEFT_AXIS, RIGHT_AXIS, POV]

class JoyAxes: # XBox Controller
    LEFT_LEFTRIGHT    = 0
    LEFT_UPDOWN       = 1
    LEFT_LEFT         = 2
    RIGHT_LEFTRIGHT   = 3
    RIGHT_UPDOWN      = 4
    RIGHT_RIGHT       = 5
    NUM               = 6

    LIST    = [LEFT_LEFTRIGHT, LEFT_UPDOWN, LEFT_LEFT, RIGHT_LEFTRIGHT, RIGHT_UPDOWN, RIGHT_RIGHT]

class KeyState:
    DOWN = 0
    UP = 1

class Modifier:
    NONE = 0
    CTRL = 1
    SHIFT = 2
    ALT = 3
    NUM = 4

class InputLock(object):
    def __init__(self):
        self.locked = False
    def acquire(self):
        self.locked = True
    def release(self):
        self.locked = False

"""
Highest level system for all the various UI land stuff
Notes: Mouse events are inconsistent with which button they report
The buttonDown call seems to be accurate so we rebuild our own information on which buttons have changed
"""
class InputSystem(mgr.System, ogre.FrameListener, ogre.WindowEventListener, OIS.KeyListener, OIS.MouseListener, OIS.JoyStickListener):
    def __init__(self, engine):
        mgr.System.__init__(self, engine)
        ogre.FrameListener.__init__(self)
        ogre.WindowEventListener.__init__(self)
        OIS.KeyListener.__init__(self)
        OIS.MouseListener.__init__(self)
        OIS.JoyStickListener.__init__(self)

        self.handlers = [dict() for x in range(InputEvent.NUM)]
        self.mouseHandlers = [dict() for x in range(MouseEvent.NUM)]
        self.joyHandlers = [dict() for x in range(JoyEvent.NUM)]
        self.keyStates = {}
        self.mouseButtonsDown = {}
        self.mouseDownPos = {}
        self.mouseDownOver = {}
        self.mouseDownModifiers = {}
        self.inputLocks = {}
        for mb in MouseButton.LIST:
            self.mouseButtonsDown[mb] = False
            self.mouseDownPos[mb] = None
            self.mouseDownOver[mb] = None
            self.mouseDownModifiers[mb] = [False for x in range(Modifier.NUM)]
            self.inputLocks[mb] = InputLock()

        self.ms = None

        #box selection
        self.selectionDDContext = self.engine.debugDrawSystem.getContext()
        self.boxSelection = None
        self.maintainDDContext = self.engine.debugDrawSystem.getContext()
        self.translationToApply = vector3(0,0,0)
        self.translationToApplyTimeLeft = 0

    def initialize(self):
        self.groundPlane = ogre.Plane((0, 1, 0), 0)
        self.entUnderMouse = None
        self.closestEntToMouse = None
        #self.selectedEnts = []

        self.keyboard = None
        self.mouse    = None
        self.joystick = None

    @EasyLog1
    def initEngine(self):
        import os
        #add me to ogre's frame listener list
        self.engine.gfxSystem.root.addFrameListener(self)


        import platform
        int64 = False
        for bit in platform.architecture():
            if '64' in bit:
                int64 = True
        windowHandle = 0
        renderWindow = self.engine.gfxSystem.root.getAutoCreatedWindow()
        if int64:
            windowHandle = renderWindow.getCustomAttributeUnsignedLong("WINDOW")
        else:
            windowHandle = renderWindow.getCustomAttributeInt("WINDOW")

        paramList = [("WINDOW", str(windowHandle))]

        t = [("x11_mouse_grab", "true"), ("x11_mouse_hide", "false")]
        paramList.extend(t)

        '''
        windowHandle = 0
        renderWindow = self.engine.gfxSystem.root.getAutoCreatedWindow() # or self.renderWindow
        windowHandle = renderWindow.getCustomAttributeInt("WINDOW")

        if os.name == "nt":
            t = [("w32_mouse","DISCL_FOREGROUND"), ("w32_mouse", "DISCL_NONEXCLUSIVE")]
        else:
            t = [("x11_mouse_grab", "false"), ("x11_mouse_hide", "false")]
            #t = [("x11_mouse_grab", "false"), ("x11_mouse_hide", "true")]

        paramList    = [("WINDOW", str(windowHandle))]

        paramList.extend(t)
        '''

        self.inputManager = OIS.createPythonInputSystem(paramList)
        self.keyboard = None
        self.mouse    = None
        self.joystick = None
        try:
            self.keyboard = self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, True)
        except Exception, e:
            print "----------------------------------->No Keyboard"
            raise e
        try:
            self.mouse    = self.inputManager.createInputObjectMouse(OIS.OISMouse, True)
            self.mouse.capture()
            self.ms = self.mouse.getMouseState()
        except Exception, e:
            print "----------------------------------->No Mouse"            
            raise e
        
        try:
            self.joystick = self.inputManager.createInputObjectJoyStick(OIS.OISJoyStick, True)
        except Exception, e:
            self.joystick = None
            print "----------------------------------->No Joy, Don't Worry Be Happy"
            print "----------------------------------->Who uses joysticks anyways? - so 1995"
        self.keyboard.setEventCallback(self)
        self.mouse.setEventCallback(self)
        
        if self.joystick:
            self.joystick.setEventCallback(self)

        self.mouse.capture()
        ms = self.mouse.getMouseState()
        ms.height = self.engine.gfxSystem.renderWindow.getHeight() # VERY IMPORTANT or rayscene queries fail
        ms.width  = self.engine.gfxSystem.renderWindow.getWidth()

        ogre.WindowEventUtilities.addWindowEventListener(renderWindow, self)

        #self.selectionHandler = selectionHandler.SelectionHandler(self.guiContext, self.mouse)

    def loadlevel(self):
        self.entUnderMouse = None
        self.closestEntToMouse = None
        #self.selectedEnts = []

    def releaseLevel(self):
        self.entUnderMouse = None
        self.closestEntToMouse = None
        #self.selectedEnts = []

    def releaseEngine(self):
        self.inputManager.destroyInputObjectKeyboard(self.keyboard)
        self.inputManager.destroyInputObjectMouse(self.mouse)
        if(self.joystick):
            self.inputManager.destroyInputObjectJoyStick(self.joystick)
        OIS.InputManager.destroyInputSystem(self.inputManager)
        self.inputManager = None

    def registerMouseHandler(self, event, mouseButton, func):# func takes OIS.MouseEvent as arg
        self.mouseHandlers[event].setdefault(mouseButton, list())
        self.mouseHandlers[event][mouseButton].append(func)

    def callMouseHandlers(self, event, mouseButton, ms):
        self.mouseHandlers[event].setdefault(mouseButton, list())
        for handler in self.mouseHandlers[event][mouseButton]:
            handler(ms)

    def registerJoyHandler(self, event, joyButton, func):# func takes OIS.JoyEvent JoyState as arg
        self.joyHandlers[event].setdefault(joyButton, list())
        self.joyHandlers[event][joyButton].append(func)

    def callJoyHandlers(self, event, joyButton, js):
        self.joyHandlers[event].setdefault(joyButton, list())
        for handler in self.joyHandlers[event][joyButton]:
            handler(js)

    def registerHandler(self, event, key, func, modifier = Modifier.NONE):
        self.handlers[event].setdefault(key, list())
        self.handlers[event][key].append((func, modifier))

    def callHandlers(self, event, key):
        """
        for each modifier type we have groups of keys - of which we need one
        for instance the control modifier means we need either the left or right control modifier down
        then we have to check that all other modifiers are not active
        """

        self.handlers[event].setdefault(key, list())
        modifierKeys = {
                Modifier.NONE  : (set(),),
                Modifier.SHIFT : (set((OIS.KC_LSHIFT,   OIS.KC_RSHIFT)),),
                Modifier.ALT   : (set((OIS.KC_LMENU,     OIS.KC_RMENU)),),
                Modifier.CTRL  : (set((OIS.KC_LCONTROL, OIS.KC_RCONTROL)),),
        }

        allModifiers = set((OIS.KC_LSHIFT, OIS.KC_RSHIFT, OIS.KC_LMENU, OIS.KC_RMENU, OIS.KC_LCONTROL, OIS.KC_RCONTROL))

        for handler, modifier in self.handlers[event][key]:
            keysIWant = modifierKeys[modifier]
            keysIDontWant = copy.copy(allModifiers)
            for group in keysIWant:
                keysIDontWant.difference_update(group) #take out all the groups we dont want

            passModifiers = True
            for dontKey in keysIDontWant:
                if self.keyboard.isKeyDown(dontKey):
                    passModifiers = False

            for group in keysIWant:
                haveAKeyInThisGroup = len(group) == 0
                for key in group:
                    if self.keyboard.isKeyDown(key):
                        haveAKeyInThisGroup = True
                        break
                if not haveAKeyInThisGroup:
                    passModifiers = False

            if passModifiers:
                handler()

    def updateMouseOver(self):
        self.ms.width = self.engine.gfxSystem.viewport.actualWidth 
        self.ms.height = self.engine.gfxSystem.viewport.actualHeight
        self.mousePos = (self.ms.X.abs/float(self.ms.width), self.ms.Y.abs/float(self.ms.height))
        mouseRay = self.engine.cameraSystem.camera.getCameraToViewportRay(*self.mousePos)
        result  =  mouseRay.intersects(self.groundPlane)

        if result.first:
            pos =  mouseRay.getPoint(result.second)
            self.mousePosWorld = pos

            lock = self.getInputLock(MouseButton.LEFT)
            if lock:
                closest = None
                closestDistance = (kSelectionRadius * self.engine.cameraSystem.height) ** 2

                closestSelectedEnt = None
                closestSelectedEntDistance = sys.float_info[0] #float.max

                for ent in self.engine.entMgr.ents:
                    if not ent.selectable:
                        continue
                    distSqrd = pos.squaredDistance(ent.pos)
                    if distSqrd < closestDistance:
                        closest = ent
                        closestDistance = distSqrd

                    if ent.isSelected and distSqrd < closestSelectedEntDistance:
                        closestSelectedEntDistance = distSqrd
                        closestSelectedEnt = ent

                #update closestEntToMouse
                if closestSelectedEnt and closestSelectedEnt != self.closestEntToMouse:
                    if self.closestEntToMouse:
                        self.closestEntToMouse.isClosestEntToMouse = False
                    closestSelectedEnt.isClosestEntToMouse = True
                    self.closestEntToMouse = closestSelectedEnt

                #update entUnderMouse
                if closest and closest != self.entUnderMouse:
                    if self.entUnderMouse:
                        self.entUnderMouse.isUnderMouse = False
                    closest.isUnderMouse = True
                    self.entUnderMouse = closest
                elif closest == None:
                    if self.entUnderMouse:
                        self.entUnderMouse.isUnderMouse = False
                        self.entUnderMouse = None
        else:
            self.mousePosWorld = None

    def keyPressed( self, evt ):
        self.keyStates[evt.key] = (KeyState.DOWN, time.time())
        self.callHandlers(InputEvent.KEY_DOWN, evt.key)
        return True

    def keyReleased(self, evt):
        #check for key_pressed
        lastState, timeDown = self.keyStates[evt.key]
        assert lastState == KeyState.DOWN
        timePressed = time.time() - timeDown
        if timePressed < kPressTime:
            self.callHandlers(InputEvent.KEY_PRESSED, evt.key)

        #always fire key_up
        self.keyStates[evt.key] = (KeyState.UP, time.time())
        self.callHandlers(InputEvent.KEY_DOWN, evt.key)
        return True

    def buttonPressed(self, evt, button):
        self.callJoyHandlers(JoyEvent.BUTTON_PRESSED, button, evt.get_state())
        #print "------------------------------------>", " Button Pressed: ", button
        
        return True

    def buttonReleased(self, evt, button):
        self.callJoyHandlers(JoyEvent.BUTTON_RELEASED, button, evt.get_state())
        #print "------------------------------------>",  " Button Released: ", button
        return True

    def axisMoved(self, evt, axis):
        state = evt.get_state()
        if state.mAxes[axis].abs > 5000 or state.mAxes[axis].abs < - 5000 :
            self.callJoyHandlers(JoyEvent.AXIS_MOVED, axis, state)            
            #print "------------------------------------>",  " Axis  : ", axis, state.mAxes[axis].abs
        return True


    def povMoved(self, evt, povid):
        state = evt.get_state()
        self.callJoyHandlers(JoyEvent.POV_MOVED, povid, state)            
        #print "------------------------------------>",  povid, state.mPOV[povid].direction
        return True


    mouseHasMoved = False
    def mouseMoved(self, evt):
        self.mouseHasMoved = True
        state   = evt.get_state()
        orie    = self.engine.cameraSystem.cameraNode.getOrientation()
        yaw     = orie.getYaw().valueRadians()
        self.callMouseHandlers(MouseEvent.MOUSE_MOVED, None, evt.get_state())
        self.doCameraZoomInOut(state.Z.rel / 120.0)
        lock = self.getInputLock(MouseButton.LEFT)
        if lock:
            if self.mouseButtonsDown[MouseButton.LEFT]:
                if not self.mousePosWorld:
                    return False
                if self.boxSelection:
                    UL = self.boxSelection.UL
                else:
                    UL = self.mousePosWorld
                size = mathlib.yawVector(self.mousePosWorld - UL, -yaw)
                self.boxSelection = rect.Rect(UL=UL, size=size, yaw=yaw)
            else:
                self.boxSelection = None
        return False

    def mousePressed(self, evt, id):
        changes = self.getButtonChanges(evt.get_state())
        for button, change in changes.items():
            if change == MouseEvent.MOUSE_PRESSED:
                #print 'pressed rmb'
                self.mouseDownPos[button] = self.mousePosWorld
                self.mouseDownOver[button] = self.entUnderMouse
                lock = self.getInputLock(button)
                if lock:
                    if self.engine.inputSystem.keyboard.isKeyDown(OIS.KC_LSHIFT) or self.engine.inputSystem.keyboard.isKeyDown(OIS.KC_RSHIFT):
                        self.mouseDownModifiers[button][Modifier.SHIFT] = True
                    if self.engine.inputSystem.keyboard.isKeyDown(OIS.KC_LMENU) or self.engine.inputSystem.keyboard.isKeyDown(OIS.KC_RMENU):
                        self.mouseDownModifiers[button][Modifier.ALT] = True
                    if self.engine.inputSystem.keyboard.isKeyDown(OIS.KC_LCONTROL) or self.engine.inputSystem.keyboard.isKeyDown(OIS.KC_RCONTROL):
                        self.mouseDownModifiers[button][Modifier.CTRL] = True
                else:
                    print 'inputServer failed to get inputlock for mousebutton'

                self.callMouseHandlers(MouseEvent.MOUSE_PRESSED, button, evt.get_state())
        return True

    def mouseReleased(self, evt, id):
        """For some reason the evt that comes in does not have the button that was released..
        wtf..
        do a quick search to figure this out
        """
        changes = self.getButtonChanges(evt.get_state())
        for button, change in changes.items():
            if change == MouseEvent.MOUSE_RELEASED:
                lock = self.getInputLock(button)
                if lock:
                    if button == MouseButton.LEFT:
                        newSelectedEnts = []
                        if self.boxSelection is None:
                            if self.entUnderMouse:
                                newSelectedEnts.append(self.entUnderMouse)
                        else:
                            for ent in self.engine.entMgr.ents:
                                if not ent.selectable:
                                    continue
                                inBox = True
                                for edge in self.boxSelection.edges:
                                    direction = (edge[1] - edge[0]).dotProduct(ent.pos - edge[0])
                                    inBox = inBox and direction > 0
                                if inBox:
                                    newSelectedEnts.append(ent)

                        self.engine.selectionSystem.selectEnts(newSelectedEnts)
                        self.boxSelection = None

                    elif button == MouseButton.RIGHT and not self.mouseDownModifiers[MouseButton.RIGHT][Modifier.CTRL]:
                        #target = self.mouseDownOver[button]
                        #if not target:
                            #destination = desiredState.StoppedAtPosition(self.mouseDownPos[MouseButton.RIGHT])
                        #else:
                            #offset = mathlib.yawVector(self.mousePosWorld - target.pos, -target.yaw)
                            #destination = desiredState.MaintainingRelativeToEnt(target, offset)

                        replaceExistingCommands = False
                        if not self.mouseDownModifiers[MouseButton.RIGHT][Modifier.SHIFT]:
                            replaceExistingCommands = True
                            
                        if self.engine.selectionSystem.selectedEnts:
                            destinationPos=self.mousePosWorld
                            target = self.mouseDownOver[button]
                            for ent in self.engine.selectionSystem.selectedEnts:
                                if not self.engine.localOptions.networkingOptions.enableNetworking or ent.player.playerId == -1 or ent.player.playerId == self.engine.entMgr.player.playerId:
                                    if not target:
                                        destination = desiredState.StoppedAtPosition(destinationPos)
                                    else:
                                        offset = mathlib.yawVector(destinationPos - target.pos, -target.yaw)
                                        destination = desiredState.MaintainingRelativeToEnt(target, offset)
                                    action = actionMgr.MoveToAction(self.engine.gameTime, ent.handle, destination, replaceExistingCommands)

                                    self.engine.actionMgr.enqueue(action)
                                    print 'Ordering MoveTo %s -> %s' % (ent, destination)
                                
                self.callMouseHandlers(MouseEvent.MOUSE_RELEASED, id, evt.get_state())
                self.mouseDownPos[button]       = None
                self.mouseDownOver[button]      = None
                self.mouseDownModifiers[button] = [False for x in range(Modifier.NUM)]
        return False

    def tick(self, dtime):
        self.keyboard.capture()    
        self.mouse.capture()
        if self.joystick:
            self.joystick.capture()

        self.ms = self.mouse.getMouseState()

        self.updateMouseOver()
        self.doCameraMovement(dtime)

        self.checkQuit()


        for button in MouseButton.LIST:
            down = self.ms.buttonDown(button)
            self.mouseButtonsDown[button] = down
        
        self.updateLiveActionDisplays()

    def updateLiveActionDisplays(self):
        self.maintainDDContext.clear()
        if self.mouseButtonsDown[MouseButton.RIGHT]:
            if self.mouseDownOver[MouseButton.RIGHT]:
                for ent in self.engine.selectionSystem.selectedEnts:
                    self.engine.debugDrawSystem.drawLine(self.maintainDDContext, ent.pos, self.mousePosWorld)
                #ordering a maintain
                self.engine.debugDrawSystem.drawLine(self.maintainDDContext, self.mouseDownOver[MouseButton.RIGHT].pos, self.mousePosWorld)
            else:
                for ent in self.engine.selectionSystem.selectedEnts:
                    self.engine.debugDrawSystem.drawLine(self.maintainDDContext, ent.pos, self.mouseDownPos[MouseButton.RIGHT])
                #ordering a move + heading
                #draggedVector = self.mousePosWorld - self.mouseDownPos[MouseButton.RIGHT]
                #if draggedVector.length() > 50.0:
                    #self.engine.debugDrawSystem.drawAngleRay(self.maintainDDContext, self.mouseDownPos[MouseButton.RIGHT], mathlib.vectorToYaw(draggedVector), len=500)

    def getButtonChanges(self, mouseState):
        result = {}
        for button in MouseButton.LIST:
            down = self.ms.buttonDown(button)
            if down != self.mouseButtonsDown[button]:
                if down:
                    result[button] = MouseEvent.MOUSE_PRESSED
                else:
                    result[button] = MouseEvent.MOUSE_RELEASED
            else:
                result[button] = MouseEvent.INVALID
        return result



    mousePosWorld = None
    def render(self):
        self.selectionDDContext.clear()
        if self.boxSelection:
            for edge in self.boxSelection.edges:
                self.engine.debugDrawSystem.drawLine(self.selectionDDContext, edge[0], edge[1])

        #self.ddContext.clear()
        #if self.mousePosWorld != None:
            #self.engine.debugDrawSystem.drawCircle(self.ddContext, self.mousePosWorld, 50)
        #if self.entUnderMouse != None:
            #self.engine.debugDrawSystem.drawCircle(self.ddContext, self.entUnderMouse.pos, 150, 16)
        #for ent in self.selectedEnts:
            #self.engine.debugDrawSystem.drawCircle(self.ddContext, ent.pos, 175, 16)

    def checkQuit(self):
        if self.keyboard.isKeyDown(OIS.KC_ESCAPE):
            self.engine.transition(self.engine.State.MAINMENU)
            self.engine.transition(self.engine.State.RELEASED)

    def doCameraMovement(self, dtime):
        direction = ogre.Vector3(0,0,0)

        cameraPitchNode = self.engine.cameraSystem.camera.parentSceneNode
        cameraNode = cameraPitchNode.parentSceneNode

        if self.keyboard.isKeyDown(OIS.KC_W): direction.z -= 1
        if self.keyboard.isKeyDown(OIS.KC_S): direction.z += 1
        if self.keyboard.isKeyDown(OIS.KC_A): direction.x -= 1
        if self.keyboard.isKeyDown(OIS.KC_D): direction.x += 1
        if self.keyboard.isKeyDown(OIS.KC_R): direction.y += 1
        if self.keyboard.isKeyDown(OIS.KC_F): direction.y -= 1

        if self.mouseHasMoved:
            if self.mousePos[0] > 0.99: direction.x += 1
            if self.mousePos[0] < 0.01: direction.x -= 1
            if self.mousePos[1] > 0.99: direction.z += 1
            if self.mousePos[1] < 0.01: direction.z -= 1

        if self.keyboard.isKeyDown(OIS.KC_LSHIFT) or self.keyboard.isKeyDown(OIS.KC_RSHIFT): direction *= 5.0

        direction = (cameraNode.orientation * direction) * kCameraSpeed * dtime
        self.translationToApply += direction
        self.translationToApplyTimeLeft = max(self.translationToApplyTimeLeft, kCameraKeyMovementTrailoffTime)

        eulerRotations = ogre.Vector3(0,0,0)
        if self.keyboard.isKeyDown(OIS.KC_Q): eulerRotations.y += 1
        if self.keyboard.isKeyDown(OIS.KC_E): eulerRotations.y -= 1
        if self.keyboard.isKeyDown(OIS.KC_Z): eulerRotations.x += 1
        if self.keyboard.isKeyDown(OIS.KC_X): eulerRotations.x -= 1
        if self.keyboard.isKeyDown(OIS.KC_Y): eulerRotations.z -= 1
        if self.keyboard.isKeyDown(OIS.KC_H): eulerRotations.z += 1
        if self.keyboard.isKeyDown(OIS.KC_LSHIFT) or self.keyboard.isKeyDown(OIS.KC_RSHIFT): eulerRotations *= 5.0

        if self.joystick and self.engine.cameraSystem.usingFPSCamera:
            self.doJoyCamera(eulerRotations)

        eulerRotations *= dtime * kCameraRotateSpeed

        cameraNode.yaw(eulerRotations.y)
        cameraPitchNode.pitch(eulerRotations.x)
        cameraPitchNode.roll(eulerRotations.z)

        if self.translationToApplyTimeLeft > 0.0:
            applyRatio = min(1.0, dtime / self.translationToApplyTimeLeft)
            translateAmount = self.translationToApply * applyRatio
            self.translationToApply -= translateAmount
            translateAmount.y = max(translateAmount.y, kCameraMinHeight - cameraNode.getPosition().y)
            cameraNode.translate(translateAmount)
            self.translationToApplyTimeLeft = max(0.0, self.translationToApplyTimeLeft - dtime)

    def doCameraZoomInOut(self, inOut):
        zoomSpeed = 10
        if inOut and self.mousePosWorld:
            cameraPitchNode = self.engine.cameraSystem.camera.parentSceneNode
            cameraNode = cameraPitchNode.parentSceneNode
            cameraPos = cameraNode.getPosition()
            centerTranslate = (self.mousePosWorld - cameraPos) * zoomSpeed
            centerTranslate /= math.log(centerTranslate.length()) * math.log(cameraPos.y)

            #cast an intersection at the cneter of the screen, and add an exponent move away from that point as well, exaggerates the zoomin / out which feels better
            #mouseRay = self.engine.cameraSystem.camera.getCameraToViewportRay(0.5, 0.5)
            #result  =  mouseRay.intersects(self.groundPlane)

            #centerPoint = None
            #if result.first:
            #    centerPoint = mouseRay.getPoint(result.second)
            #    adjustment = 0.01 * self.mousePosWorld - centerPoint
            #    adjustment = adjustment / math.log(adjustment.length())
            #    mousePosCentered = vector3(self.mousePos[0] - 0.5, 0.0, self.mousePos[1] - 0.5)
                #adjustmentCoefs.x = max(0.0, (abs(mousePosCentered[0]) - 0.3) / 0.2 )
                #adjustmentCoefs.z = max(0.0, (abs(mousePosCentered[0]) - 0.3) / 0.2 )

            #    centerTranslate += adjustment * .1 #mousePosCentered.length()


            self.translationToApply += centerTranslate * inOut
            self.translationToApplyTimeLeft += kCameraZoomInOutTrailTime
            self.translationToApplyTimeLeft = min(kCameraMaxTrailTime, self.translationToApplyTimeLeft)

    def doJoyCamera(self, eulerRotations):
        joystate = self.joystick.getJoyStickState()
        if joystate.mAxes[JoyAxes.RIGHT_LEFTRIGHT].abs > 10000: eulerRotations.y -= 1
        if joystate.mAxes[JoyAxes.RIGHT_LEFTRIGHT].abs < -10000: eulerRotations.y += 1

        if joystate.mAxes[JoyAxes.RIGHT_UPDOWN].abs > 10000: eulerRotations.x += 1
        if joystate.mAxes[JoyAxes.RIGHT_UPDOWN].abs < -10000: eulerRotations.x -= 1

    def getInputLock(self, button):
        if not self.inputLocks[button].locked:
            return self.inputLocks[button]
        else:
            return None

