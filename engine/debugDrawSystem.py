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

from mgr import System
from vector import vector3
import mathlib
import ogre.renderer.OGRE as ogre
import colors

class Drawable(object):
    def render(self, lines):
        assert False, 'Not Implemented'

class DebugDrawLine(Drawable):
    def __init__(self, a, b, color):
        self.a = a
        self.b = b
        self.color = color

    def render(self, lineRenderers):
        h = hash(self.color)
        renderer = lineRenderers[h]
        renderer.addPoint(self.a)
        renderer.addPoint(self.b)

class DebugDrawContext(object):
    """
    Aspects request contexts, which are just groupings within which they can do groups of draws
    this allows support for both continual redraws and occasional redraws correctly
    """
    drawables = []
    def __init__(self):
        pass

    def clear(self):
        """
        Clear all the stuff we wanted to draw
        """
        self.drawables = []

    def render(self, lines):
        """
        Draw all my stuff
        """
        for drawable in self.drawables:
            drawable.render(lines)

    def __str__(self):
        return 'DDContext%i' % id(self)

c = 0
class DebugDrawSystem(System):
    """
    Holds a bunch of functions for doing debug drawing
    super useful and important
    """
    contexts = []
    lines = None
    lineRenderers = {}

    def __init__(self, engine):
        System.__init__(self, engine)

    def initEnginePost(self):
        for color in colors.colors:
            h = hash(color)
            self.lineRenderers[h] = LineRenderer("LineRenderer%i" % h, self.engine.gfxSystem.sceneManager, color=(color.r, color.g, color.b) )
        #if self.lines is None:
            #self.lines = LineRenderer("DebugDrawLines", self.engine.gfxSystem.sceneManager, color=(1,1,1))

    def render(self):
        for renderer in self.lineRenderers.values():
            renderer.clearPoints()

        for context in self.contexts:
            #context.render(self.lines)
            context.render(self.lineRenderers)

        for renderer in self.lineRenderers.values():
            renderer.draw()

        #if self.lines.points:
            #import pdb; pdb.set_trace()
            #self.lines.draw()

    def getContext(self):
        context = DebugDrawContext()
        self.contexts.append(context)
        return context

    def drawLine(self, context, a, b, yoffset=0, color=colors.WHITE):
        context.drawables.append(DebugDrawLine(a + vector3(0,yoffset,0), b + vector3(0,yoffset,0), color))

    def drawRay(self, context, a, b, yoffset=0, len=None, color=colors.WHITE):
        if len != None:
            b.normalise()
            b *= len

        self.drawLine(context, a, a + b, yoffset=yoffset, color=color)

    def drawAngleRay(self, context, pos, angle, len=100, yoffset=0, color=colors.WHITE):
        vec = vector3(len, 0, 0)
        mathlib.yawVector(vec, angle)
        self.drawRay(context, pos, vec, yoffset=yoffset, color=color)

    def drawCircle(self, context, center, radius, segments = 8, yoffset=0, color=colors.WHITE):
        lastPoint = center + vector3(radius, 0.0, 0.0)
        for i in range(1, segments+1):
            offset = vector3(radius, 0.0, 0.0)
            mathlib.yawVector(offset, i * mathlib.twopi / segments)
            point = center + offset
            self.drawLine(context, lastPoint, point, yoffset=yoffset, color=color)
            lastPoint = point

    def drawAABB25(self, context, aabb, yoffset=0, color=colors.WHITE):
        corners = aabb.calcCorners()
        for (a,b) in zip(corners, corners[1:] + corners[:1]):
            self.drawLine(context, a, b, yoffset=yoffset, color=color)

debugDrawSystem = None

class LineRenderer(object):
    """Creates an object that contains a renderable line between two points
    def __init__(self, name, sceneManager, color = (1, 1, 1), parentNode = None, lineType = None):
    """

    def __init__(self, name, sceneManager, color=(1,1,1), parentNode=None, lineType=None):
        self.sm = sceneManager
        self.mm = ogre.MaterialManager.getSingleton()
        self.color = color
        self.line = None
        self.lineType = lineType or ogre.RenderOperation.OT_LINE_LIST
        self.points = []
        self.lineNode = None
        self.name = name
        self.parentNode = parentNode

        self.setup()

    def setup(self):
        """Called by the constructor to set things up and get ready
        """
        self.line = self.sm.createManualObject(self.name)
        parent = self.parentNode or self.sm.getRootSceneNode()
        self.lineNode = parent.createChildSceneNode(self.name)
        self.lineNode.attachObject(self.line)
        self.materialName = self.name + "Material"
        self.material = self.mm.create(self.materialName, "General")
        self.material.setReceiveShadows(False)
        self.material.getTechnique(0).setLightingEnabled(True)
        self.material.getTechnique(0).getPass(0).setDiffuse(0,0,0,1)
        self.material.getTechnique(0).getPass(0).setAmbient(0,0,0)
        self.material.getTechnique(0).getPass(0).setSelfIllumination(*self.color)

        #self.line.begin(self.materialName, ogre.RenderOperation.OT_LINE_LIST)
        self.line.begin(self.materialName, self.lineType)
        self.line.position(0, 0, 0)
        self.line.position(0, 0, 0)
        self.line.position(0, 0, 0)
        self.line.position(0, 0, 0)
        self.line.end()


    def addPoint(self, pos):
        """Add a point to the set of lines to draw. Presumably this point is part of one of the lines
        """
        self.points.append(pos)
        #if pos.x == 5:
            #raise Exception
        

    def clearPoints(self):
        """No lines to draw
        """
        self.points = []

    counter = 0
    writeToFile = False
    def draw(self):
        """Draw the lines
        """
        
        if self.writeToFile:
            self.counter += 1
            if self.counter % 10 == 0:
                f = open('lines.txt', 'w')
                f.write('\n'.join([str(x) for x in self.points]))
                f.close()

        self.npoints = len(self.points)
        self.line.beginUpdate(0)
        self.line.position(0, 0, 0)
        self.line.position(0, 0, 0)
        if self.npoints == 1:
            # draw line from origin to point
            self.line.position(0, 5, 0)
            p = self.points[0]
            self.line.position(p[0], p[1]+5, p[2])

        else:
            for p in self.points:
                self.line.position(p[0], p[1]+5, p[2])
        self.line.end()

    def flipVisibility(self):
        """Hide the lines
        """
        self.lineNode.flipVisibility()

        
