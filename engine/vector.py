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

#import math
import ogre.renderer.OGRE as ogre
#import mathlib
vector2 = ogre.Vector2
vector3 = ogre.Vector3
vector4 = ogre.Vector4
quat = ogre.Quaternion
mat3 = ogre.Matrix3
mat4 = ogre.Matrix4

class point2(object):
    def __init__(self, x, y):
        assert type(x) is int and type(y) is int
        self.x = x
        self.y = y
    def __add__(self, rhs):
        assert type(rhs) is point2
        return point2(self.x + rhs.x, self.y + rhs.y)
    def __str__(self):
        return '%i,%i' % (self.x, self.y)
    __repr__ = __str__



class pqPair(object):
    def __init__(self, p = None, q = None):
        if p == None:
            p = vector3(0,0,0)
        assert type(p) is vector3
        self.p = p

        if q == None:
            q = quat(1,0,0,0)
        assert type(q) is quat
        self.q = q

    def applyToOgreNode(self, ogreNode):
        ogreNode.setPosition(self.p)
        ogreNode.setOrientation(self.q)

    def fromOgreNode(self, ogreNode):
        self.p = ogreNode.getPosition()
        self.q = ogreNode.getOrientation()

def vector3_reduce(self):
    return vector3, (self.x, self.y, self.z)
vector3.__reduce__ = vector3_reduce

def quat_reduce(self):
    return quat, (self.w, self.x, self.y, self.z)
quat.__reduce__ = quat_reduce

#test our custom pickling support for ogre math types
if __name__ == '__main__':
    import pickle
    import sys
    from types import *
    v = vector3()
    print v.__reduce__()
    pickle.dump(v, sys.stdout)
    q = quat(0,0,0,1)
    print q.__reduce__()
    pickle.dump(q, sys.stdout)

'''
class vector3(object):
    """
    three dimensional vector
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def yaw(self, theta):
        x = self.x
        y = self.y
        self.x =  math.cos(theta) * x + math.sin(theta) * y
        self.y = -math.sin(theta) * x + math.cos(theta) * y

    def __add__(self, rhs):
        return vector3(     self.x + rhs.x, 
                            self.y + rhs.y,
                            self.z + rhs.z)

    def __sub__(self, rhs):
        return vector3(     self.x - rhs.x, 
                            self.y - rhs.y,
                            self.z - rhs.z)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __str__(self):
        return '(%.2f,%.2f,%.2f)' % (self.x, self.y, self.z)
    def __repr__(self):
        return self.__str__()
    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        if index == 2:
            return self.z
        assert False, "Out of bounds"

    @staticmethod
    def zero():
        return vector3(0,0,0)
'''
