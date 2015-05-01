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
from aspect import Aspect
from vector import vector3, vector4
from random import random
import ogre.renderer.OGRE as ogre
import timer
from gui.ex.thickCircle import ThickCircle
class Renderable(Aspect):
    """
        Something with a location that can be rendered to the screen via ogre
    """
    def init(self):
        self.ent.ogreName = str(self.ent)
        self.ent.pos = vector3(0.0, 0.0, 0.0)
        self.ent.yaw = 0.0

        self._rootNode = self.engine.gfxSystem.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.ogreName, self.ent.pos)

        gent = self.engine.gfxSystem.sceneManager.createEntity(self.ent.ogreName + '_0', self.ent.mesh)
        self._node = self._rootNode.createChildSceneNode(self.ent.ogreName + '_0', self.ent.pos)
        self._node.attachObject(gent)      

        if self.ent.lod1:
            gent1 = self.engine.gfxSystem.sceneManager.createEntity(self.ent.ogreName + '_1', self.ent.lod1[1])
            self._node1 = self._rootNode.createChildSceneNode(self.ent.ogreName + '_1', self.ent.pos)
            self._node1.attachObject(gent1)
            self._node1.translate(vector3(0, 1.00, 0))
            self._node1.setScale(vector3(48.0, 1, 48.0))
        if self.ent.lod2:
            gent2 = self.engine.gfxSystem.sceneManager.createEntity(self.ent.ogreName + '_2', self.ent.lod2[1])
            self._node2 = self._rootNode.createChildSceneNode(self.ent.ogreName + '_2', self.ent.pos)
            self._node2.attachObject(gent2)
            self._node2.translate(vector3(0, 10, 0))
            self._node2.setScale(vector3(96.0, 1, 96.0))
			
        if self.ent.selectable:
            self.selectionCircle = ThickCircle(self.ent.ogreName + '.selectionCircle', self.engine.gfxSystem.sceneManager, parentNode=self._rootNode, color=(1.0, 1.0, 0.0))
            self.mouseOverCircle = ThickCircle(self.ent.ogreName + '.mouseOverCircle', self.engine.gfxSystem.sceneManager, parentNode=self._rootNode, color=(1.0, 1.0, 1.0))
            self.updateOverlaySizes()
            self.selectionCircle.hide()
            self.mouseOverCircle.hide()

            self.prevSelectionState = None
            self.prevMouseOverState = None

        import timer
        self.updateOverlayTimer = timer.Timer(0.1, fireFirstCheck=True)

    def updateOverlaySizes(self):
        radius = self.ent.selectionCircleRadius or self.ent.avoidanceSize.x * 1.1
        cameraHeightRatio = max(1.0, self.engine.cameraSystem.height / 2000.0)
        radius *= cameraHeightRatio
        thickness = 5 * cameraHeightRatio
        self.selectionCircle.setup(radius=radius,       thickness = thickness)
        self.mouseOverCircle.setup(radius=radius + 10,  thickness = thickness)

    def tick(self, dtime):
        #dist = -(self.engine.cameraSystem.wvp * self.ent.pos).z
        dist = self.engine.cameraSystem.height
        self._rootNode.setPosition(self.ent.pos)
        self._rootNode.resetOrientation()
        self._rootNode.yaw(self.ent.yaw)
        if self.ent.lod1:
            if dist < self.ent.lod1[0]:
                self._node.setVisible(True)
                self._node1.setVisible(False)
                self._node2.setVisible(False)
            elif dist < self.ent.lod2[0]:
                self._node.setVisible(False)
                self._node1.setVisible(True)
                self._node2.setVisible(False)
            else:
                self._node.setVisible(False)
                self._node1.setVisible(False)
                self._node2.setVisible(True)

        if self.ent.selectable:
            if self.ent.isSelected != self.prevSelectionState:
                if self.ent.isSelected:
                    self.selectionCircle.show()
                else:
                    self.selectionCircle.hide()
                self.prevSelectionState = self.ent.isSelected

            if self.ent.isUnderMouse != self.prevMouseOverState:
                if self.ent.isUnderMouse:
                    self.mouseOverCircle.show()
                else:
                    self.mouseOverCircle.hide()
                self.prevMouseOverState = self.ent.isUnderMouse

            if self.ent.isSelected or self.ent.isUnderMouse:
                if self.updateOverlayTimer.check(dtime):
                    self.updateOverlaySizes()

    @property 
    def rootnode(self):
        return self._rootNode
