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

import math

class ThickCircle (object):
    ''' An object that draws a circle centered at c, with radius r, and thickness t
    '''
    def __init__(self, name, sm, color = (1, 1, 1), parentNode = None, circleType = ogre.RenderOperation.OT_TRIANGLE_LIST):
        self.name = name
        self.sceneManager = sm
        self.color = color
        self.circleType = circleType
        self.parentNode = parentNode or self.sceneManager.getRootSceneNode()
        self.mm = ogre.MaterialManager.getSingleton()
        self.accuracy = 32
        self.yup = 5

        self.circle = self.sceneManager.createManualObject(self.name)
        self.materialName = self.name + 'Material'
        self.material = self.mm.create(self.materialName, "General")
        self.material.setReceiveShadows(False)
        self.material.getTechnique(0).setLightingEnabled(True)
        self.material.getTechnique(0).getPass(0).setDiffuse(0,0,0,1)
        r, g, b = self.color
        self.material.getTechnique(0).getPass(0).setAmbient(0,0,0)
        self.material.getTechnique(0).getPass(0).setSelfIllumination(r,g,b)

        self.circleNode = self.parentNode.createChildSceneNode()
        self.circleNode.attachObject(self.circle)


    def setup(self, center = (0, 5, 0), radius = 100, thickness = 10, startTheta = 0.0, endTheta = math.pi * 2.0):
        self.center = center
        self.radius = radius
        self.thickness = thickness

        self.circle.clear()
        self.circle.begin(self.materialName, self.circleType)
        self.index = 0
        inc   = ((endTheta - startTheta) * 2.0) / self.accuracy
        theta = startTheta
        for i  in range(0, self.accuracy):
            self.circle.position(self.radius * math.cos(theta), self.yup, self.radius * math.sin(theta))
            self.circle.position(self.radius * math.cos(theta - inc), self.yup, self.radius * math.sin(theta - inc))
            self.circle.position((self.radius - self.thickness) * math.cos(theta - inc), self.yup, (self.radius - self.thickness) * math.sin(theta - inc))
            self.circle.position((self.radius - self.thickness) * math.cos(theta), self.yup, (self.radius - self.thickness) * math.sin(theta))
            self.circle.quad(self.index, self.index+1, self.index+2, self.index+3)
            self.index += 4
            theta += inc
        self.circle.end()

    def clear(self):
        self.circleNode.setVisible(False)
    
    def show(self):
        self.circleNode.setVisible(True)

    def hide(self):
        self.circleNode.setVisible(False)

    def flipVisibility(self):
        self.circleNode.flipVisibility()

    def draw(self):
        self.circleNode.show()
