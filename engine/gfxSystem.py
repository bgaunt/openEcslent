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

import os
import time

import ogre.renderer.OGRE as ogre

from mgr import System
from misc import EasyLog, EasyLog1
from mgr import EngineObject
from debugDrawSystem import LineRenderer

from vector import vector3

# Hydrax


class HydraxSkyBoxes:
# Skyboxes

    _def_SkyBoxNum = 3

    mSkyBoxes = [ "Sky/ClubTropicana",
                  "Sky/EarlyMorning",
                  "Sky/Clouds"]

    mSunPosition = [ ogre.Vector3(0,10000,0),
                     ogre.Vector3(0,10000,90000),
                     ogre.Vector3(0,10000,0)
                     ]
                 
    mSunColor = [ogre.Vector3(1, 0.9, 0.6),
                 ogre.Vector3(1,0.6,0.4),
                 ogre.Vector3(0.45,0.45,0.45)]


    mCurrentSkyBox = 0


class GfxSystem(System):
    @EasyLog1
    def initEngine(self):
        if os.name == 'nt':
            self.pluginsPath = os.path.join(self.engine.localOptions.engineeringOptions.configPath, "plugins_nt.cfg")
        else:
            self.pluginsPath = os.path.join(self.engine.localOptions.engineeringOptions.configPath, "plugins.cfg")

        self.resourcesPath = os.path.join(self.engine.localOptions.engineeringOptions.configPath, "resources.cfg")
        #self.gents = {} # dictionary map of ent.name to node

        self.createRoot()
        self.defineResources()
        self.setupRenderSystem()
        self.createRenderWindow()
        self.initializeResourceGroups()
        self.createSceneManager()

    @EasyLog1
    def createRoot(self):
        self.root = ogre.Root(self.pluginsPath)#, self.resourcesPath)
    
    @EasyLog1
    def defineResources(self):
        cf = ogre.ConfigFile()
        cf.load(self.resourcesPath)
        seci = cf.getSectionIterator()
        while seci.hasMoreElements():
            secName = seci.peekNextKey()
            settings = seci.getNext()
            for item in settings:
                typeName = item.key
                archName = item.value
                ogre.ResourceGroupManager.getSingleton().addResourceLocation(archName, typeName, secName)

    @EasyLog1
    def setupRenderSystem(self):
        if not self.root.restoreConfig() and not self.root.showConfigDialog():
            raise Exception("User canceled the config dialog! -> Application.setupRenderSystem()")
 
    @EasyLog1
    def createRenderWindow(self):
        self.renderWindow = self.root.initialise(True, "Evolutionary Computing Systems Lab (ECSL) ENTity Game Engine (ECSLENT), University of Nevada, Reno")
 
    @EasyLog1
    def initializeResourceGroups(self):
        ogre.TextureManager.getSingleton().setDefaultNumMipmaps(5)
        ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()
 
    def initEnginePost(self):
        self.createViewport()
        self.initializeMap()

    @EasyLog1
    def createSceneManager(self):
        self.sceneManager = self.root.createSceneManager(ogre.ST_EXTERIOR_CLOSE, 'TerrainSM')  

    @EasyLog1
    def createViewport(self):
        self.viewport = self.root.getAutoCreatedWindow().addViewport(self.engine.cameraSystem.camera)
        self.viewport.backGroundColor = (0,0,0)
        self.engine.cameraSystem.camera.aspectRatio = float (self.viewport.actualWidth) / float (self.viewport.actualHeight)

    def initializeMap(self):
        if(self.engine.localOptions.gfxOptions.hydrax == False):
          self.initRegularMap()
        else:
            try:
                self.initHydrax()
            except ImportError:
                raise
                print "Cannot import Hydrax"
                self.initRegularMap()


    waterNode = None
    def initRegularMap(self):
        plane = ogre.Plane((0, 1, 0), 0)
        meshManager = ogre.MeshManager.getSingleton()
        
        if self.engine.localOptions.gfxOptions.renderWater:
            meshManager.createPlane('Ground', 'General', plane, 1000000, 1000000, 20, 20, True, 1, 5, 5, (0, 0, 1))
            ent = self.sceneManager.createEntity('GroundEntity', 'Ground')
            self.waterNode = self.sceneManager.getRootSceneNode().createChildSceneNode()
            self.waterNode.attachObject(ent)
            ent.setMaterialName('NavyCg')
            ent.castShadows = False

        if self.engine.localOptions.gfxOptions.renderSkybox:
            self.sceneManager.setSkyDome(True, "Examples/CloudySky", 5, 8)
            self.sceneManager.ambientLight = ogre.ColourValue(0.3, 0.3, 0.3)

            #lights - primary light representing the sun
            light1 = self.sceneManager.createLight ('DirectionalLight')
            light1.type = ogre.Light.LT_DIRECTIONAL
            light1.diffuseColour = (0.5, 0.5, 0.5)
            light1.specularColour = (.75, .75, .75)
            light1.direction = (0.2, -1, 1)

    def initHydrax(self):
        print "Initializing Hydrax"
        import ogre.addons.hydrax as Hydrax
        camera = self.engine.cameraSystem.camera
        plane = ogre.Plane((0, 1, 0), 0)
        meshManager = ogre.MeshManager.getSingleton()
        
        # Create the SkyBox
        self.sceneManager.setSkyBox(True, HydraxSkyBoxes.mSkyBoxes[HydraxSkyBoxes.mCurrentSkyBox], 99999*3, True)

        # Light
        mLight = self.sceneManager.createLight("Light0")
        mLight.setPosition( HydraxSkyBoxes.mSunPosition[ HydraxSkyBoxes.mCurrentSkyBox])
        mLight.setDiffuseColour(1, 1, 1)
        mLight.setSpecularColour( HydraxSkyBoxes.mSunColor[ HydraxSkyBoxes.mCurrentSkyBox].x,
                                   HydraxSkyBoxes.mSunColor[ HydraxSkyBoxes.mCurrentSkyBox].y,
                                   HydraxSkyBoxes.mSunColor[ HydraxSkyBoxes.mCurrentSkyBox].z)

        self.sceneManager.ambientLight = ogre.ColourValue(0.3, 0.3, 0.3)

        # Create Hydrax object
        self.hydrax = Hydrax.Hydrax(self.sceneManager, camera, self.renderWindow.getViewport(0))

        # Update Hydrax sun position and colour
        self.hydrax.setSunPosition( HydraxSkyBoxes.mSunPosition[ HydraxSkyBoxes.mCurrentSkyBox])
        self.hydrax.setSunColor( HydraxSkyBoxes.mSunColor[ HydraxSkyBoxes.mCurrentSkyBox])

        # Create our projected grid module  
        self.options = Hydrax.Perlin.Options(8, 0.085, 0.49, 1.4, 1.27)
        self.modoptions = Hydrax.ProjectedGrid.Options(64,0.0,0.0,True )                      
                        
        self.Module = Hydrax.TestCreateModule ( self.hydrax )               

        # Set our module
        self.hydrax.setModule(self.Module)

        # Load all parameters from config file
        # Remarks: The config file must be in Hydrax resource group.
        # All parameters can be set/updated directly by code(Like previous versions),
        # but due to the high number of customizable parameters, Hydrax 0.4 allows save/load config files.
        self.hydrax.loadCfg("HydraxDemo.hdx");

        #rttManager = self.hydrax.getRttManager()
        #help(rttManager)
        #rttManager.addRttListener(self.rttListener)

        # Create water
        self.hydrax.create()
        self.frameListener = HydraxListener(self.renderWindow, camera, self.sceneManager, self)
        self.root.addFrameListener(self.frameListener)   

    @EasyLog1
    def loadLevel(self):
        # make grid
        if self.engine.localOptions.gfxOptions.drawGrid:
            self.makeGrid()
        pass

    #@EasyLog1
    #def setupPositionalSound(self):
        #self.cameraNode.attachObject(self.soundManager.getListener())

    @EasyLog1
    def makeGrid(self):
        def makeGridData(level):
            maxX = level.dimensions[0]
            maxZ = level.dimensions[1]
            stepSize = level.gridSize
            """Makes a grid on the XZ plane (water plane). It returns two arrays. 
            Array1 contains the set of lines (x1, 0, y1), (x2, 0, z2) pairs for lines parallel to Z
            Array1 contains the set of lines (x1, 0, z1), (x2, 0, z2) pairs for lines parallel to X
            """
            a1 = []
            for i in range (-maxX/2, maxX/2, stepSize):
                p1 = (i, 0, -maxZ/2)
                p2 = (i, 0, maxZ/2)
                a1.append(p1)
                a1.append(p2)

            a2 = []
            for i in range(-maxZ/2, maxZ/2, stepSize):
                p1 = (-maxX/2, 0, i)
                p2 = (maxX/2, 0, i)
                a2.append(p1)
                a2.append(p2)

            return (a1, a2)

        self.gridData = makeGridData(self.engine.levelSystem.currentLevel)
        self.lineRenderer = LineRenderer("xGrid", self.sceneManager, color=(.1, .5, .5))
        for p in self.gridData[0]:
            self.lineRenderer.addPoint(p)

        for p in self.gridData[1]:
            self.lineRenderer.addPoint(p)
        self.lineRenderer.draw()
        

    @EasyLog1
    def flipGridVisibility(self):
        self.lineRenderer.flipVisibility()
        
    #@EasyLog1
    #def createSoundManager(self):
        #try:
            #import ogre.sound.OgreAL as OgreAL
            #self.soundManager = OgreAL.SoundManager()
        #except ImportError:
            #print "Cannot initialize sound system. Reboot or see if your sound card is well supported by OGREAL"
            #self.state.options.hasSound = False

    def startRenderLoop(self):
        self.root.startRendering()
        
    def render(self):
        self.engine.debugDrawSystem.render()
        self.root.renderOneFrame()

    def createGraphicalEntityAndNode(self, entity):
        gent = self.sceneManager.createEntity(entity.name, entity.entityType + ".mesh")
        node = self.sceneManager.getRootSceneNode().createChildSceneNode(entity.name, entity.position)
        node.attachObject(gent)
        self.gents[entity.name] = node
        return node

    def copyStateToGraphics(ent, node):
        """Copy position and orientation to graphics
        """
        opos = ent.position
        ov   = ogre.Vector3(opos[0], 0.0, opos[2])
        node.setPosition(ov)
        node.yaw(ogre.Radian(ent.deltaYaw))

    #def rttListener(self, *args):
        #print 'rttListener', args

    def tick(self, dtime):
        posStride = 1000.0
        if self.waterNode:
            cameraPos = self.engine.cameraSystem.cameraNode.position
            waterPos = vector3(cameraPos.x - cameraPos.x % posStride, 0.0, cameraPos.z - cameraPos.z % posStride)
            self.waterNode.setPosition(waterPos)

## Hydrax
## Event handler to add ability to alter subdivision
class HydraxListener(ogre.FrameListener):
    def __init__(self, renderWindow, camera, sceneManager, gfxSystem):
        ogre.FrameListener.__init__(self)
        self.sceneManager = sceneManager
        self.renderWindow = renderWindow
        self.camera=camera
        self.gfxSystem = gfxSystem
        self.mKeyBuffer=-1

    def frameStarted(self, e):
        global mCurrentSkyBox
        if ogre.FrameListener.frameStarted(self, e) == False:
            return False     
                                                 
        self.gfxSystem.hydrax.update(e.timeSinceLastFrame)
          
        return True

