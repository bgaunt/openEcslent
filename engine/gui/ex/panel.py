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
import ogre.io.OIS as OIS

class Panel:
    '''
    '''
    def __init__(self, context, name = "ex.Panel", pos = (0.0, 0.0), dim = (100, 100), material = None):
        context = context
        overlayManager = ogre.OverlayManager.getSingleton() #
        self.px = pos[0]
        self.py = pos[1]
        self.dx = dim[0]
        self.dy = dim[1]

        self.title = name

        self.overlayName = "ECSLENT/Overlay/" + name + "/" + str(context.getNextId())
        self.overlay     = overlayManager.create(self.overlayName)
        self.id          = self.overlayName + "Panel/" + str(context.getNextId())
        self.panel       = overlayManager.createOverlayElement("Panel", self.id)
        self.panel.setMetricsMode(ogre.GMM_PIXELS)#RELATIVE_ASPECT_ADJUSTED)
        self.panel.setPosition(self.px, self.py)
        self.panel.setDimensions(self.dx, self.dy)
        if material:
            self.panel.setMaterialName(material)
        self.panel.show()
        self.overlay.add2D(self.panel)
        self.overlay.show()

        self.x = 0
        self.y = 0
        self.ygap = 0
        self.locations = {}
        self._items = []

    def show(self):
        self.overlay.show()
        self.panel.show()

    def hide(self):
        self.panel.hide()
        self.overlay.hide()

    def setPosition(self, x, y):
        self.px = x
        self.py = y
        self.panel.setPosition(x, y)

    def addItem(self, item):
        self._items.append(item)
        dim = item.getDimensions()
        item.setPosition(self.x, self.y)
        self.panel.addChild(item.getTextArea())

        self.y += dim[1] + self.ygap

        self.dy = self.y
        self.panel.setDimensions(self.dx, self.dy)


    def deleteItem(self, item):
        item.hide()
        self._item.remove(element)

    def getElements(self):
        return self._items

    def getPanel(self):
        return self.panel

