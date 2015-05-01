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

import ogre.renderer.OGRE as ogre

from mgr import System
from vector import vector3, quat, pqPair
from units import pitchYawRoll
import yaml
from misc import EasyLog1
from renderable import Renderable
import inputSystem
import ogre.io.OIS as OIS

class CameraData:
    def __init__(self):
        self.loc1 = (pqPair(vector3(0,500,800), pitchYawRoll(0,35,0) ), pqPair(vector3(0,0,0), pitchYawRoll(-60,0,0)))
        self.loc2 = (pqPair(vector3(0,500,800), pitchYawRoll(0,35,0) ), pqPair(vector3(0,0,0), pitchYawRoll(-60,0,0)))
        self.loc3 = (pqPair(vector3(0,500,800), pitchYawRoll(0,35,0) ), pqPair(vector3(0,0,0), pitchYawRoll(-60,0,0)))
        self.loc4 = (pqPair(vector3(0,500,800), pitchYawRoll(0,35,0) ), pqPair(vector3(0,0,0), pitchYawRoll(-60,0,0)))

class CameraSystem(System):
    filename = 'data/camera.yaml'
    def initEngine(self):
        try:
            f = open(self.filename, 'r')
            self.data = yaml.load(f)
            f.close()
        except IOError:
            self.data = CameraData()
            self.saveData()

        self.camera = self.engine.gfxSystem.sceneManager.createCamera("PlayerCamera")
        #self.camera.position = (0, 10, 500)
        #self.camera.lookAt((0,0,0))
        self.camera.nearClipDistance = 5
        self.camera.setFarClipDistance(99999*6)
        self.engine.cameraSystem.camera = self.camera

        #----------------attach camera to node so we can move camera---------------------------
        self.cameraNode = self.engine.gfxSystem.sceneManager.getRootSceneNode().createChildSceneNode("CamYawNode", (0, 100, 500))
        self.cameraPitchNode = self.cameraNode.createChildSceneNode("CamPitchNode");
        self.cameraPitchNode.attachObject(self.camera)

        self.fpsCameraNode = self.engine.gfxSystem.sceneManager.getRootSceneNode().createChildSceneNode("FPSCamYawNode")
        self.fpsCameraPitchNode = self.fpsCameraNode.createChildSceneNode("FPSCamPitchNode");

        self.loadPos1()
        self.isDataDirty = False

        self.usingFPSCamera = False
        self.height = 100

        self.wvp = self.camera.getProjectionMatrix() * self.camera.getViewMatrix()
        self.ddContext = self.engine.debugDrawSystem.getContext()
        self.mousePosWorld = vector3(0,0,0)
        self.cameraCenterPos = None

        self.engine.inputSystem.registerHandler(inputSystem.InputEvent.KEY_PRESSED, OIS.KC_TAB, self.lookatNextEnt)

    lookatIndex = None
    def lookatNextEnt(self):
        print 'lookatNextEnt', self.lookatIndex
        if self.engine.entMgr.ents:
            ent = None
            for i in range(100):
                if self.lookatIndex == None:
                    self.lookatIndex = 0
                else:
                    self.lookatIndex = (self.lookatIndex + 1) % len(self.engine.entMgr.ents)
                ent = self.engine.entMgr.ents[self.lookatIndex]
                if ent.isNormal:
                    self.lookAt(ent, 0.2)
                    break

    def crosslink(self):
        import inputSystem
        import ogre.io.OIS as OIS
        self.engine.inputSystem.registerHandler(inputSystem.InputEvent.KEY_PRESSED, OIS.KC_F5, self.loadPos1)
        self.engine.inputSystem.registerHandler(inputSystem.InputEvent.KEY_PRESSED, OIS.KC_F5, self.savePos1, modifier=inputSystem.Modifier.CTRL)

        self.engine.inputSystem.registerHandler(inputSystem.InputEvent.KEY_PRESSED, OIS.KC_L, self.detachCamera)
        self.engine.inputSystem.registerHandler(inputSystem.InputEvent.KEY_PRESSED, OIS.KC_K, self.attachCamera)


    def detachCamera(self):
        self.camera.parentSceneNode.detachObject(self.camera)
        self.cameraPitchNode.attachObject(self.camera)
        self.usingFPSCamera = False

    def attachCamera(self):
        if self.engine.selectionSystem.selectedEnts:
            self.camera.parentSceneNode.detachObject(self.camera)
            self.fpsCameraNode.parentSceneNode.removeChild(self.fpsCameraNode)
            self.fpsCameraPitchNode.attachObject(self.camera)

            renderAspect = self.engine.selectionSystem.primaryEnt.findAspect(Renderable)
            renderAspect._node.addChild(self.fpsCameraNode)
            self.fpsCameraNode.setPosition(vector3(-self.engine.selectionSystem.primaryEnt.length, self.engine.selectionSystem.primaryEnt.height, 0))

            self.fpsCameraNode.resetOrientation()
            self.fpsCameraPitchNode.resetOrientation()

            self.fpsCameraPitchNode.lookAt(vector3(0,0,0), ogre.Node.TS_PARENT)
            self.fpsCameraNode.yaw(ogre.Degree(-90))
            self.usingFPSCamera = True

    def lookAt(self, ent, time=3.0):
        print 'moving camera over ent', ent
        translate = ent.pos - self.engine.cameraSystem.cameraCenterPos
        translate.y = 0.0
        self.engine.inputSystem.translationToApply = translate
        self.engine.inputSystem.translationToApplyTimeLeft = time

    @EasyLog1
    def loadPos1(self):
        print 'loadPos1'
        self.data.loc1[0].applyToOgreNode(self.cameraNode)
        self.data.loc1[1].applyToOgreNode(self.cameraPitchNode)

    @EasyLog1
    def savePos1(self):
        print 'savePos1'
        self.data.loc1[0].fromOgreNode(self.cameraNode)
        self.data.loc1[1].fromOgreNode(self.cameraPitchNode)
        self.isDataDirty = True

    def tick(self, dtime):
        self.wvp = self.engine.cameraSystem.camera.getProjectionMatrix() * self.engine.cameraSystem.camera.getViewMatrix()
        self.wvp = self.engine.cameraSystem.camera.getViewMatrix()
        if self.isDataDirty:
            self.saveData()
            self.isDataDirty = False
        self.height = self.cameraNode.getPosition().y

        #self.ms.width = self.engine.gfxSystem.viewport.actualWidth 
        #self.ms.height = self.engine.gfxSystem.viewport.actualHeight
        #self.mousePos = (self.ms.X.abs/float(self.ms.width), self.ms.Y.abs/float(self.ms.height))
        mouseRay = self.engine.cameraSystem.camera.getCameraToViewportRay(0.5, 0.5)
        result  =  mouseRay.intersects(self.engine.inputSystem.groundPlane)

        if result.first:
            pos = mouseRay.getPoint(result.second)
            self.cameraCenterPos = pos
            #self.ddContext.clear()
            #self.engine.debugDrawSystem.drawCircle(self.ddContext, self.cameraCenterPos, 50)

    def saveData(self):
        f = open(self.filename, 'w')
        yaml.dump(self.data, f)
        f.close()
