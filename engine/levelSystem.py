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

import traceback
from mgr import System
import yaml
"""Owns data on all the various levels we can load and run
"""
class LevelData(object):
    name = 'unnamed'
    dimensions = [10000, 10000]
    gridSize = 10

class LevelSystem(System):
    filename = 'data/levels.yaml'

    def initialize(self):
        self.currentLevel = None
        self.levels = {}
        self.levels['openwater'] = LevelData()
        self.levels['openwater'].name = 'openwater'
        self.levelToLoad = None

    def initEngine(self):
        try:
            f = open(self.filename, 'r')
            self.levels = yaml.load(f)
            f.close()
        except:
            traceback.print_exc()

        f = open(self.filename, 'w')
        yaml.dump(self.levels, f)
        f.close()

    def loadLevel(self):
        assert self.levelToLoad != None
        self.currentLevel = self.levels[self.levelToLoad]
        self.levelToLoad = None

    def releaseLevel(self):
        self.currentLevel = None

    def releaseEngine(self):
        self.levels = None
