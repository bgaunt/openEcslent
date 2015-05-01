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

class Label:
    '''
    '''
    def __init__(self, context, caption = "Ex.Label", color = (1.0, 1.0, 0.7), dim = (100, 13), pos = (0, 0)):
        '''
        '''
        context = context
        overlayManager = ogre.OverlayManager.getSingleton()
        self.caption = caption
        self.color   = color

        self.dx, self.dy = dim[0], dim[1]
        self.px, self.py = pos[0], pos[1]

        self.xOffset = 5
        self.yOffset = 2

        self.id = "ECSLENT/Label/" + str(self) + "/" + caption  + "/" + str(context.getNextId())

        self.textArea = overlayManager.createOverlayElement("TextArea", self.id)
        self.textArea.setMetricsMode(ogre.GMM_PIXELS)
        self.textArea.setCaption(caption)
        self.textArea.setPosition(self.px  + self.xOffset, self.py + self.yOffset)
        self.textArea.setDimensions(self.dx, self.dy)
        self.textArea.setFontName("BlueHighway")
        self.textArea.setCharHeight(self.dy)
        self.textArea.setColour(self.color)

        #textArea.setColourTop((1.0, 1.0, 0.7))
        #textArea.setColourBottom((1.0, 1.0, 0.7))

         
#-------------------------------------------------------------------
    def getTextArea(self):
        return self.textArea
#-------------------------------------------------------------------
    def show(self):
        self.textArea.show()
#-------------------------------------------------------------------
    def hide(self):
        self.textArea.hide()
#-------------------------------------------------------------------
    def setCaption(self, caption):
        self.caption = caption
        self.textArea.setCaption(self.caption)
#-------------------------------------------------------------------
    def getCaption(self):
        return self.caption
#-------------------------------------------------------------------
    def setPosition(self, px, py):
        self.px = px
        self.py = py
        self.textArea.setPosition(px + self.xOffset, py + self.yOffset)
#-------------------------------------------------------------------
    def getPosition(self):
        return (self.px, self.py)
#-------------------------------------------------------------------
    def setDimensions(self, x, y):
        self.dx = x
        self.dy = y
        self.textArea.setDimensions(x, y)
#-------------------------------------------------------------------
    def getDimensions(self):
        return (self.dx, self.dy)
#-------------------------------------------------------------------
    def setCharHeight(self, height):
        self.dy = height
        self.setCharHeight(height)
#-------------------------------------------------------------------
    def tick(self, time, dtime):
        pass # do nothing, use setCaption to change label text
