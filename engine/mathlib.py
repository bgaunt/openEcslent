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

import math
pi = math.pi
twopi = math.pi * 2.0
halfpi = math.pi * 0.5
kFloatEqualityTolerance = 0.01

def between(minValue, maxValue, x):
    return  ((minValue - kFloatEqualityTolerance) < x) and ((maxValue + kFloatEqualityTolerance) > x)

def fequals(x, y, tolerance = kFloatEqualityTolerance):
    return abs(x - y) < tolerance

def vectorEquals(v1, v2, tolerance = kFloatEqualityTolerance):
    return fequals(v1.x, v2.x, tolerance) and fequals(v1.y, v2.y, tolerance) and fequals(v1.z, v2.z, tolerance)

def cleanupAngle(angle):
    return math.fmod(angle, pi)

def differenceBetweenAngles(angle1, angle2):
    d = angle2 - angle1
    while d > pi:
        d -= twopi
    while d < -pi:
        d += twopi
    return d

def clamp(a, minValue, maxValue):
    if a > maxValue:
        return maxValue
    if a < minValue:
        return minValue
    return a

def randomVectorSquare(maxRadius):
    import random
    import vector
    x = random.uniform(-maxRadius, maxRadius)
    z = random.uniform(-maxRadius, maxRadius)
    return vector.vector3(x, 0, z)

def randomVectorCircular(minRadius, maxRadius):
    import random
    import vector
    r = random.uniform(minRadius, maxRadius)
    t = random.uniform(0, twopi)
    return vector.vector3(r * math.cos(t), 0, r * math.sin(t))

def ipol(val1, val2, amount):
    return val1 * (1.0 - amount) + val2 * amount


def yawVector(vec, theta):
    x = vec.x
    z = vec.z
    vec.x =  math.cos(theta) * x + math.sin(theta) * z
    vec.z = -math.sin(theta) * x + math.cos(theta) * z
    return vec

def yawwedVector(vec, theta):
    from vector import vector3
    v = vector3(vec.x, vec.y, vec.z)
    return yawVector(v, theta)

def vectorToYaw(vec):
    return math.atan2(-vec.z, vec.x)

def lineCollisionBase(p1, p2, p3, p4):
    from vector import vector3
    try:
        ua = ((p4.x - p3.x) * (p1.z - p3.z) - (p4.z - p3.z) * (p1.x - p3.x)) / ((p4.z - p3.z) * (p2.x - p1.x) - (p4.x - p3.x) * (p2.z - p1.z))
        ub = ((p2.x - p1.x) * (p1.z - p3.z) - (p2.z - p1.z) * (p1.x - p3.x)) / ((p4.z - p3.z) * (p2.x - p1.x) - (p4.x - p3.x) * (p2.z - p1.z))
        return ua, ub
    except:
        return 0, 0

def lineCollision(p1, p2, p3, p4):
    from vector import vector3
    ua, ub = lineCollisionBase(p1, p2, p3, p4)
    px = p1.x + ua * (p2.x - p1.x)
    pz = p1.z + ua * (p2.z - p1.z)
    return vector3(px, 0.0, pz)

def lineSegmentCollision(p1, p2, p3, p4):
    from vector import vector3
    ua, ub = lineCollisionBase(p1, p2, p3, p4)
    if ua >= 0.0 and ua <= 1.0 and ub >= 0.0 and ub <= 1.0:
        px = p1.x + ua * (p2.x - p1.x)
        pz = p1.z + ua * (p2.z - p1.z)
        return vector3(px, 0.0, pz)
    else:
        return None

def unitTests():
    from vector import vector3
    '''
    for x in range(100):
        #create a bunch of vectors, and convert to thetas and back to make sure everything works
        vec0 = randomVectorSquare(100)
        #self.engine.debugDrawSystem.drawRay( self.immediateData.ddContext, self.ent.pos, toDest)
        theta = vectorToYaw(vec0)
        vec1 = yawVector(vector3(0, 0, vec0.length()), theta)
        assert vec1.positionEquals(vec0)
        '''

    #check some lineCollisions
    for x in range(100):
        p1 = randomVectorSquare(100)
        p2 = randomVectorSquare(100)
        p3 = randomVectorSquare(100)
        p4 = randomVectorSquare(100)

        pa = lineCollision(p1, p2, p3, p4)
        pb = lineCollision(p3, p4, p1, p2)
        assert pa.positionEquals(pb)

# Networking 
def lerpVector(v1, v2, t):
    return v1 + ((v2 - v1) * t)

#def lerpYaw(y1, y2, t):
#    return y1 + ((y2 - y1) * t)


# VShip specific
from vector import vector3
def ecslentVector(vsVec):
    z, x, y = vsVec
    return vector3(x, 0, -z)

def enumeratePairs(l):
    results = []
    for i, a in enumerate(l):
        for b in l[i+1:]:
            results.append((a,b))
    return results
    
