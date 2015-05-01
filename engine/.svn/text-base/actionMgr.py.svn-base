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

import exceptions
from mgr import Mgr
from vector import vector3
import timer
import os
import yaml
import traceback
import command

class ActionHistory(object):
    def __init__(self):
        self.IimeOnClose = 0.0
        self.actions = []

class Action(object):
    def __init__(self, time):
        self.time = time
    def do(self, engine):
        raise exceptions.CallingAbstractFunction

class CreateEntity(Action):
    def __init__(self, time, handle, type):
        Action.__init__(self, time)
        self.handle = handle
        self.type = type

    def do(self, engine):
        #print 'CreateEntity.do', self.handle, self.type
        engine.entMgr.createEntity(self.handle, self.type)

class MoveEntity(Action):
    def __init__(self, time, handle, pos):
        Action.__init__(self, time)
        self.handle = handle
        self.pos = pos

    def do(self, engine):
        #print 'MoveEntity.do', self.handle, self.pos
        ent = engine.entMgr.findEntFromHandle(self.handle)
        ent.pos = self.pos

class MoveToAction(Action):
    def __init__(self, time, handle, desiredState, replaceExistingCommands):
        Action.__init__(self, time)
        self.handle = handle
        self.desiredState = desiredState
        self.replaceExistingCommands = replaceExistingCommands

    def do(self, engine):
        ent = engine.entMgr.findEntFromHandle(self.handle)
        self.desiredState.connectToEngine(engine)
        cmd = command.MoveTo(engine, self.desiredState)
        if self.replaceExistingCommands:
            ent.squad.SquadAI.commands = []
        ent.squad.SquadAI.commands.append(cmd)

class AdjustSpeed(Action):
    def __init__(self, time, handle, speed):
        Action.__init__(self, time)
        self.handle = handle
        self.speed = speed

    def do(self, engine):
        ent = engine.entMgr.findEntFromHandle(self.handle)
        ent.UnitAI.navDesiredSpeed      = self.speed
        ent.UnitAI.command.desiredSpeed = self.speed
        ent.uiDesiredSpeed              = self.speed

class ActionMgr(Mgr):
    history = ActionHistory()
    pendingActions = []

    def initialize(self):
        pass

    def loadLevel(self):
        #print 'ActionMgr.loadLevel'
        for filename in self.engine.localOptions.gameOptions.toLoad:
            filename = os.path.join('ActionHistory/', filename)
            f = open(filename, 'r')
            s = f.read()
            f.close()
            history = yaml.load(s)
            for action in history.actions:
                self.enqueue(action)

    historyFilename = 'ActionHistory/actionHistory.yaml'
    historyFilenameBackup = 'ActionHistory/actionHistory_backup.yaml'
    toFileTimer = timer.Timer(1.0)
    dirty = False
    def tick(self, dtime):
        while self.pendingActions:
            action = self.pendingActions[0]
            #print action, action.time, self.engine.gameTime
            if self.engine.gameTime >= action.time:
                self.pendingActions.pop(0)
                self.do(action)
            else:
                break #list is sorted - if first fails, all fail

        if self.dirty and self.toFileTimer.check(dtime):
            self.dirty = False
            try:
                os.unlink(self.historyFilenameBackup)
            except:
                print 'Failed to erase old history file'
                traceback.print_exc()

            try:
                os.rename(self.historyFilename, self.historyFilenameBackup)
            except:
                print 'Failed to backup history file'
                traceback.print_exc()

            s = yaml.dump(self.history)
            f = open(self.historyFilename, 'w')
            f.write(s)
            f.close()

    def do(self, action):
        action.do(self.engine)
        #print 'ActionMgr.do', action

    def enqueue(self, action):
        self.dirty = True
        self.pendingActions.append(action)
        self.pendingActions.sort(key=lambda action:action.time)
        #self.history.actions.append(action)
        #self.history.actions.sort(key=lambda action:action.time)

    #class TestEntityClass:
        #def __init__(self):
            #pass

    #testMode = True
    #print 'ActionMgr.Test'
    #doSaveTest = True
    #if doSaveTest:
        #h = ActionHistory()
        #a1 = CreateEntity(time=1.0, type=TestEntityClass, pos=vector3(1,0,2))
        #h.actions.append(a1)
        #print h
        #s = yaml.dump(h)
        #print s
        #f = open('test.yaml', 'w')
        #f.write(s)
        #f.close()

    #doLoadTest = True
    #if doLoadTest:
        #f = open('test.yaml', 'r')
        #s = f.read()
        #f.close()
        #print s
        #h = yaml.load(s)
        #print h
