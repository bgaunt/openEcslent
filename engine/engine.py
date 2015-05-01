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

'''
Engine is the central mega manager 
Engine owns the startup options
Engine controls the main initialization / gameplay / menu states
Engine owns all the singleton pointers
as well as super high level versions of the execution loops

Because the gfx system can be enabled / we support having / not having it loaded here at the highest level

Design Notes:
    This file is going to get complex - so keep imports as local and as specific as humanly possible

Engine also has a super minimal memory manager sysetm - really just a set of counters so we can track whats been initialized
'''


from engineExceptions import NotImplementedException

from memoryMgr import MemoryMgr

from mgr import EngineObject
from timer import Timer


class Engine(EngineObject):
    kTargetFrameRate    = 30.0
    kTimeStepSize       = 1.0 / kTargetFrameRate
    gameTime            = 0.0
    gameTimeAccumulated = 0.0
    timeScale           = 1.0
    realTime            = 0.0
    doBigPrint          = False
    doBigPrintTimer     = Timer(5.0) 
    executionHandle     = None

    class State(object):
        RELEASED    = 'RELEASED'
        MINIMAL     = 'MINIMAL'
        MAINMENU    = 'MAINMENU'
        GAMEPLAY    = 'GAMEPLAY'

    #class Locks(object):
        #import lock
        #unitAILock = lock.Lock()
        #def reset(self):
            #self.unitAILock.reset()
    #locks = Locks()

    def __init__(self, localOptions):
        import time
        import random
        r = random.Random()
        r.seed(time.time())
        self.executionHandle = abs(int(r.getrandbits(32)))
        self.localOptions = localOptions

        if localOptions.engineeringOptions.loadPsyco:
            try:
                import psyco
                psyco.full()
            except ImportError:
                print 'Warning - Failed to load psyco'

        self.state = self.State.RELEASED
        self.memoryMgr = MemoryMgr(self)

        EngineObject.__init__(self, self) #weird but true - I am the memory manager

    def transition(self, state):
        ss = (self.state, state)
        if ss == (self.State.RELEASED, self.State.MINIMAL):
            self.instantiateSingletons()
            self.crosslinkSingletons()
        elif ss == (self.State.MINIMAL, self.State.MAINMENU):
            self.initEngine()
            self.initMenu()
        elif ss == (self.State.MAINMENU, self.State.GAMEPLAY):
            self.loadLevel()
        elif ss == (self.State.GAMEPLAY, self.State.MAINMENU):
            self.releaseLevel()
        elif ss == (self.State.MAINMENU, self.State.RELEASED):
            self.releaseEngine()
            import sys
            sys.exit(0)
        else:
            raise Exception('Invalid engine state transition: %s' % ss)

        self.state = state

    def instantiateSingletons(self):
        """Instantiate singletons
        """
        assert self.state == self.State.RELEASED

        from actionMgr import ActionMgr
        from aspectMgr import AspectMgr
        from entMgr import EntMgr
        from gfxSystem import GfxSystem
        from cameraSystem import CameraSystem
        from debugDrawSystem import DebugDrawSystem
        from levelSystem import LevelSystem
        from inputSystem import InputSystem
        from selectionSystem import SelectionSystem
        from widget import WidgetMgr
        from testMgr import TestMgr
        from netMgr import NetMgr

        self.actionMgr = ActionMgr(self)
        self.aspectMgr = AspectMgr(self)
        self.entMgr = EntMgr(self)
        self.gfxSystem = GfxSystem(self)
        self.cameraSystem = CameraSystem(self)
        self.debugDrawSystem = DebugDrawSystem(self)
        self.levelSystem = LevelSystem(self)
        self.inputSystem = InputSystem(self)
        self.selectionSystem = SelectionSystem(self)
        self.widgetMgr = WidgetMgr(self)
        self.testMgr = TestMgr(self)
        self.netMgr  = NetMgr(self)

        self.actionMgr.initialize()
        self.aspectMgr.initialize()
        self.entMgr.initialize()
        self.gfxSystem.initialize()
        self.cameraSystem.initialize()
        self.debugDrawSystem.initialize()
        self.levelSystem.initialize()
        self.inputSystem.initialize()
        self.selectionSystem.initialize()
        self.widgetMgr.initialize()
        self.testMgr.initialize()
        self.netMgr.initialize()


    def crosslink(self):
        import inputSystem
        import ogre.io.OIS as OIS
        if not self.engine.localOptions.networkingOptions.enableNetworking:
            self.inputSystem.registerHandler(inputSystem.InputEvent.KEY_PRESSED, OIS.KC_EQUALS, self.increaseTimeScale)
            self.inputSystem.registerHandler(inputSystem.InputEvent.KEY_PRESSED, OIS.KC_MINUS, self.decreaseTimeScale)

    def crosslinkSingletons(self):
        self.crosslink()
        self.memoryMgr.crosslink()
        self.actionMgr.crosslink()
        self.aspectMgr.crosslink()
        self.entMgr.crosslink()
        self.gfxSystem.crosslink()
        self.cameraSystem.crosslink()
        self.debugDrawSystem.crosslink()
        self.levelSystem.crosslink()
        self.inputSystem.crosslink()
        self.selectionSystem.crosslink()
        self.widgetMgr.crosslink()
        self.testMgr.crosslink()
        self.netMgr.crosslink()

    def initEngine(self):
        self.actionMgr.initEngine()
        self.aspectMgr.initEngine()
        self.entMgr.initEngine()
        self.gfxSystem.initEngine()
        self.cameraSystem.initEngine()
        self.debugDrawSystem.initEngine()
        self.levelSystem.initEngine()
        self.inputSystem.initEngine()
        self.selectionSystem.initEngine()
        self.widgetMgr.initEngine()
        self.testMgr.initEngine()
        self.netMgr.initEngine()

        self.actionMgr.initEnginePost()
        self.aspectMgr.initEnginePost()
        self.entMgr.initEnginePost()
        self.gfxSystem.initEnginePost()
        self.cameraSystem.initEnginePost()
        self.debugDrawSystem.initEnginePost()
        self.levelSystem.initEnginePost()
        self.inputSystem.initEnginePost()
        self.selectionSystem.initEnginePost()
        self.widgetMgr.initEnginePost()
        self.testMgr.initEnginePost()
        self.netMgr.initEnginePost()

    def initMenu(self):
        self.actionMgr.initMenu()
        self.aspectMgr.initMenu()
        self.entMgr.initMenu()
        self.gfxSystem.initMenu()
        self.cameraSystem.initMenu()
        self.debugDrawSystem.initEngine()
        self.levelSystem.initMenu()
        self.inputSystem.initMenu()
        self.selectionSystem.initMenu()
        self.widgetMgr.initMenu()
        self.testMgr.initMenu()
        self.netMgr.initMenu()

    def loadLevel(self):
        self.levelSystem.loadLevel()
        self.actionMgr.loadLevel()
        self.aspectMgr.loadLevel()
        self.entMgr.loadLevel()
        self.gfxSystem.loadLevel()
        self.cameraSystem.loadLevel()
        self.debugDrawSystem.loadLevel()
        self.inputSystem.loadLevel()
        self.selectionSystem.loadLevel()
        self.widgetMgr.loadLevel()
        self.testMgr.loadLevel()
        self.netMgr.loadLevel()

    def releaseLevel(self):
        self.inputSystem.releaseLevel()
        self.selectionSystem.releaseLevel()
        self.widgetMgr.releaseLevel()
        self.debugDrawSystem.releaseLevel()
        self.gfxSystem.releaseLevel()
        self.cameraSystem.releaseLevel()
        self.entMgr.releaseLevel()
        self.actionMgr.releaseLevel()
        self.aspectMgr.releaseLevel()
        self.levelSystem.releaseLevel()
        self.testMgr.releaseLevel()
        self.netMgr.releaseLevel()

    def releaseEngine(self):
        self.inputSystem.releaseEngine()
        self.selectionSystem.releaseEngine()
        self.widgetMgr.releaseEngine()
        self.levelSystem.releaseEngine()
        self.debugDrawSystem.releaseEngine()
        self.gfxSystem.releaseEngine()
        self.cameraSystem.releaseEngine()
        self.entMgr.releaseEngine()
        self.actionMgr.releaseEngine()
        self.aspectMgr.releaseEngine()
        self.testMgr.releaseEngine()
        self.netMgr.releaseEngine()

    def mainLoop(self):
        """ Step the game universe in beat to a constant time rythm
        do what we can to get a smooth framerate
        """
        import time
        import ogre.renderer.OGRE as ogre
        
        lastTime = time.time()
        dtime = 0.0
        cont = True
        weu = ogre.WindowEventUtilities() # Needed for linux/mac
        weu.messagePump()

        while cont:
            while self.gameTimeAccumulated - self.gameTime > self.kTimeStepSize:
                self.mainStep(self.kTimeStepSize)
                self.gameTime += self.kTimeStepSize
                
            self.render()

            now = time.time()
            dtime = now - lastTime
            lastTime = now
            self.gameTimeAccumulated += dtime * self.timeScale
            weu.messagePump()
            time.sleep(0.001)


    def mainStep(self, dtime):
        """ Update the universe by some time step
        """

        self._updateRealTime()
        if self.realTime > 2.0:
            #self.locks.reset()
            self.doBigPrint = self.doBigPrintTimer.check(dtime)

        self.inputSystem.tick(dtime)
        self.selectionSystem.tick(dtime)
        self.widgetMgr.tick(dtime)
        self.memoryMgr.tick(dtime)
        self.actionMgr.tick(dtime)
        self.aspectMgr.tick(dtime)
        self.entMgr.tick(dtime)
        self.gfxSystem.tick(dtime)
        self.cameraSystem.tick(dtime)
        self.debugDrawSystem.tick(dtime)
        self.testMgr.tick(dtime)
        self.netMgr.tick(dtime)

    def _updateRealTime(self):
        import time
        newRealTime = time.clock()
        self.dRealTime = newRealTime - self.realTime
        self.realTime = newRealTime

    def render(self):
        self.inputSystem.render()
        self.selectionSystem.render()
        self.widgetMgr.render()
        self.actionMgr.render()
        self.aspectMgr.render()
        self.entMgr.render()
        self.gfxSystem.render()
        self.cameraSystem.render()
        self.debugDrawSystem.render()
        self.netMgr.render()

    def increaseTimeScale(self):
        if self.timeScale < 0.9:
            self.timeScale = min(self.timeScale * 2.0, 1.0)
        else:
            self.timeScale = min(10.0, self.timeScale + 1.0)

    def decreaseTimeScale(self):
        if self.timeScale > 1.1:
            self.timeScale = max(1.0, self.timeScale - 1.0)
        else:
            self.timeScale = max(0.1, self.timeScale * .5)


