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
from aspect import Aspect
from vector import vector3


MIN_SPEED = 2

class Wake(Aspect):
    def init(self):
        self.emitterList = [0,0,0]

        #set wake attributes based on boat size(1=small,2=med,3=large)
        if self.ent.wakeSize == 1:
            self.wake = self.initWake(dimensions=(5,5), scalerRate=0.15, colorFaderAlpha=-0.06)
            self.midEmitter = Emitter(self.ent, ttl = 15, emissionRate = 50)
            self.midEmitter.setColorRange(startColorAlpha = (1, 1, 1, 0.5), endColorAlpha = (1, 1, 1, 0.8))
            '''            self.leftEmitter = Emitter(self.ent, ttl = 15, direction = vector3(-3, 0, -2))
            self.leftEmitter.setColorRange(startColorAlpha = (1, 1, 1, 0.3), endColorAlpha = (1, 1, 1, 0.8))
            self.rightEmitter = Emitter(self.ent, ttl = 15, direction = vector3(-3, 0, 2))
            self.rightEmitter.setColorRange(startColorAlpha = (1, 1, 1, 0.3), endColorAlpha = (1, 1, 1, 0.8))
            '''

        elif self.ent.wakeSize == 2:
            self.wake = self.initWake(dimensions = (18, 18), scalerRate = 0.5, colorFaderAlpha = -0.002)
            self.midEmitter = Emitter(self.ent, ttl = 40, emissionRate = 12, position = vector3(-self.ent.length/2.5, 0.5, 0))
            self.midEmitter.setColorRange(startColorAlpha = (1, 1, 1, 0.3), endColorAlpha = (1, 1, 1, 1.0))
            '''
            self.leftEmitter = Emitter(self.ent, ttl = 40, emissionRate = 12, direction = vector3(-5, 0, -2), 
                                       position = vector3(self.ent.length/3.0, 0.5, -self.ent.beam/3.0))
            self.leftEmitter.setColorRange(startColorAlpha = (1, 1, 1, 0.3), endColorAlpha = (1, 1, 1, 1.0))
            self.rightEmitter = Emitter(self.ent, ttl = 40, emissionRate = 12, direction = vector3(-5, 0, 2), 
                                        position = vector3(self.ent.length/3.0, 0.5, self.ent.beam/3.0))
            self.rightEmitter.setColorRange(startColorAlpha = (1, 1, 1, 0.3), endColorAlpha = (1, 1, 1, 1.0))
            '''
        elif self.ent.wakeSize == 3:
            self.wake = self.initWake(dimensions = (25, 25), scalerRate = 0.7, colorFaderAlpha = -0.0014)
            self.midEmitter = Emitter(self.ent, angle = ogre.Degree(4), ttl = 70, particleVelocity = (1, 5), emissionRate = 5, 
                                      position = vector3(-self.ent.length/2.5, 0.5, 0))
            self.midEmitter.setColorRange(startColorAlpha = (1, 1, 1, 0.3), endColorAlpha = (1, 1, 1, 1.0))
            '''
            self.leftEmitter = Emitter(self.ent, angle = ogre.Degree(4), ttl = 65, particleVelocity = (1, 5), emissionRate = 5, 
                                       direction = vector3(-5, 0, -2), position = vector3(self.ent.length/3.0, 0.5, -self.ent.beam/4.0))
            self.leftEmitter.setColorRange(startColorAlpha = (1, 1, 1, 0.3), endColorAlpha = (1, 1, 1, 1.0))

            self.rightEmitter = Emitter(self.ent, angle = ogre.Degree(4), ttl = 65, particleVelocity = (1, 5), emissionRate = 5, 
                                        direction = vector3(-5, 0, 2), position = vector3(self.ent.length/3.0, 0.5, self.ent.beam/4.0))
            self.rightEmitter.setColorRange(startColorAlpha = (1, 1, 1, 0.3), endColorAlpha = (1, 1, 1, 1.0))
            '''
        else:
            print "No wakes for this type of entity", str(self.ent)

    def initWake(self, dimensions, scalerRate, colorFaderAlpha):
            self.ent.pSystem = self.engine.gfxSystem.sceneManager.createParticleSystem(self.ent.ogreName + '_P')
            self.ent.Renderable.rootnode.attachObject(self.ent.pSystem)
            
            #set up billboard so that particles face the right way
            self.renderer = self.ent.pSystem.getRenderer()
            self.renderer.setBillboardType(ogre.BBT_PERPENDICULAR_COMMON)
            self.renderer.setCommonDirection(ogre.Vector3(0,1,0))
            self.renderer.setCommonUpVector(ogre.Vector3(1,0,0))

            self.ent.pSystem.setMaterialName("Water/Wake")
            x, y = dimensions
            self.ent.pSystem.setDefaultDimensions(x, y)
            self.ent.pSystem.setParticleQuota(8000)

            #affectors
            self.scaler = self.ent.pSystem.addAffector("Scaler")
            self.colourFader = self.ent.pSystem.addAffector("ColourFader")   
            # #set up affector parameters          
            self.scaler.setParameter("rate", str(scalerRate))
            self.colourFader.setParameter("alpha", str(colorFaderAlpha))

    def getEmitters(self):
        #return (self.leftEmitter, self.midEmitter, self.rightEmitter)
        return (self.midEmitter,)

    def tick(self, dtime):

        if self.ent.speed < MIN_SPEED :
            self.ent.pSystem.setEmitting(False)
        else:
            self.ent.pSystem.setEmitting(True)

        for em in self.getEmitters():
            em.emitter.setParticleVelocity(1, 3) #self.ent.speed/2)
        
#------------------------------------------------------------------------------------------------------

class Emitter:
    '''An emitter with a configuration
    '''
    def __init__(self, ent, angle = ogre.Degree(8), ttl = 9, particleVelocity = (1, 3), emissionRate = 90, direction = vector3(-1, 0, 0), position = vector3(0, -1, 0)):
        self.ent = ent
        self.emitter = self.ent.pSystem.addEmitter("Point")
        self.emitter.setAngle(angle)
        self.emitter.setTimeToLive(ttl)
        low, high = particleVelocity
        self.emitter.setParticleVelocity(low, high)
        self.emitter.setDirection(direction)
        self.emitter.setEmissionRate(emissionRate)


    def setColorRange(self, startColorAlpha = (1, 1, 1, 0.5), endColorAlpha = (1, 1, 1, 0.8)):
        self.emitter.setColourRangeStart(startColorAlpha)
        self.emitter.setColourRangeEnd(endColorAlpha)

