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



SELECTION_RADIUS_SQUARED  = 10000

from engine import transform
from engine.vector import vector3

class SelectionHandler: #perhaps a manager? loading a level would change the plane to check against
    def __init__(self, context, mouse): # shush about all the assignments below. I am too old to type the fqn although I know why you should
        self.context   = context
        self.mouse = self.context.engine.inputSystem.mouse
        self.mouse.capture()
        ms = self.mouse.getMouseState()
        ms.height = self.context.engine.gfxSystem.renderWindow.getHeight()
        ms.width  = self.context.engine.gfxSystem.renderWindow.getWidth()

        self.selectedEnts = []

    def checkAndSetSelected(self, mouseEvent):
        import pdb; pdb.set_trace()
        for ent in self.selectedEnts:
            ent.selectionCircle.hide()
        self.selectedEnts = [] 
        pos, ents = self.cursorToWorld(mouseEvent.get_state())
        for ent in ents:
            self.selectedEnts.append(ent)
            #self.state.selectedEntities.append(ent)
            #ent.gfxNode.showBoundingBox(True)
            ent.selectionCircle.show()


    def cursorToWorld(self, ms):
        mouseRay = self.context.engine.cameraSystem.camera.getCameraToViewportRay(ms.X.abs/float(ms.width), ms.Y.abs/float(ms.height))
        result  =  mouseRay.intersects(self.context.engine.gfxSystem.waterPlane)
        if result.first:
            pos =  mouseRay.getPoint(result.second)
            return self.checkForEntsInRadius(pos, SELECTION_RADIUS_SQUARED)
        else:
            return (None, [])

    def checkForEntsInRadius(self, pos, radiusSquared):
        listOfEnts = []
        for ent in self.context.engine.entMgr.ents:
            if ent.hasSquad:
                for squadMember in ent.squad.squadMembers:
                    d = pos.squaredDistance(ent.pos)
                    if d < radiusSquared:
                        listOfEnts.append(ent)
                        print str(ent)
        return (pos, listOfEnts)


