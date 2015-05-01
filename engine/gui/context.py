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

class Context:
    '''
    '''
    def __init__(self, engine):
        #import ogre.renderer.OGRE as ogre
        #self.overlayManager = ogre.OverlayManager.getSingleton()        
        self.engine = engine
        self.name = "Context"
        self.count = 0

    def getNextId(self):
        self.count += 1
        return self.count

    
