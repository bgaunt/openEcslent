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

import mathlib
from vector import vector2, vector3
class AARect:
#a rectangle that has axis aligned along world space
    def __init__(self, UL, LR):
        self.UL = UL
        self.LR = LR

    @property
    def corners(self):
        result = []
        result.append(vector3(self.UL.x, self.UL.y, self.UL.z))
        result.append(vector3(self.LR.x, self.UL.y, self.UL.z))
        result.append(vector3(self.LR.x, self.UL.y, self.LR.z))
        result.append(vector3(self.UL.x, self.UL.y, self.LR.z))
        return result

    @property
    def edges(self):
        c = self.corners
        return zip(c, c[1:] + c[0:1])


class Rect:
    def __init__(self, UL, size, yaw):
        self.UL = UL
        self.size = size
        self.yaw = yaw

    @property
    def corners(self):
        result = []
        result.append(self.UL)
        result.append(self.UL + mathlib.yawVector(vector3(self.size.x,    0,           0), self.yaw))
        result.append(self.UL + mathlib.yawVector(vector3(self.size.x,    0, self.size.z), self.yaw))
        result.append(self.UL + mathlib.yawVector(vector3(0.0,            0, self.size.z), self.yaw))
        return result

    @property
    def edges(self):
        c = self.corners
        return zip(c, c[1:] + c[0:1])
