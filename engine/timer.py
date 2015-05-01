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

from mgr import EngineObject
import random

class Timer(object):
    """Class used to manage events that re-occur on some schedule
    """
    def __init__(self, resetTime, randomize=True, fireFirstCheck = False):
        self.resetTime = resetTime
        if fireFirstCheck:
            self.timeUntilReset = -1.0
        elif randomize:
            self.timeUntilReset = random.uniform(0.0, self.resetTime)
        else:
            self.timeUntilReset = self.resetTime

    def activate(self):
        """This timer will fire next time it is checked
        """
        self.timeUntilReset = -1.0

    def reset(self):
        self.timeUntilReset = self.resetTime

    def check(self, dtime, reset=True):
        self.timeUntilReset -= dtime
        if self.timeUntilReset < 0.0:
            if reset:
                self.reset()
            return True
        else:
            return False
        
