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
from vector import vector2, quat, mat3
"""
for each real world unit we want to use we have a handy function which converts it to game units 
    - ALWAYS do this - 
    as it keeps life soo easy and lcean to read
    especially if we have to move around internal units this is super handy
"""
def feet(f):
    return f * 0.3048 

def knots(knots):
    return knots * 0.514444444

def toKnots(gameSpeed):
    return gameSpeed / 0.514444444

def degrees(d):
    return d * mathlib.pi / 180.0

def toDegrees(r):
    return r * 180/mathlib.pi


def feetSecondSqrd(f):
    return feet(f)

def degreesSecond(f):
    return degrees(f)

def pitchYawRoll(p, y, r):
    m = mat3()
    m.FromEulerAnglesXYZ(degrees(p), degrees(y), degrees(r))
    q = quat()
    q.FromRotationMatrix(m)
    return q

idealScreenSize = vector2(1024,800)
screenSize = vector2(800,600)
def idealScreenPos(x, y):
    return vector2(x,y) * screenSize / idealScreenSize


"""These are already in game units so just pass through
"""
def gameUnit(f):
    return f

meters = gameUnit
seconds = gameUnit
metersSecondSqrd = gameUnit
radiansPerSecond = gameUnit
radiansPerSecondSquared = gameUnit
tons = gameUnit

def minutes(m):
    return seconds(m * 60.0)


