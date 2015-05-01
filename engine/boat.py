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

from ent import Ent
from renderable import Renderable
from units import *
from unitAI import UnitAI
from squadAI import SquadAI
from vector import vector2, vector3
from wake import Wake

from control import ManualControl

class Boat(Ent):
    aspects = [Renderable, UnitAI, ManualControl, Wake]

    mesh = 'boat.mesh'
    lod1 = None
    lod2 = None

    maxSpeed = knots(31.0)
    accelSpeed = 1.0
    rotationalSpeed = 0.1
    moveTolerance = meters(100)
    avoidanceSize = vector3(meters(154), 0.0, meters(30)) * .5 #radius to diameter
    collisionLookAheadTime = minutes(5.0)

    throttlePidParams = (1.0,0,0,10)
    rudderPidParams = (0.25, 0.5, 0.0, 10)
    runHelsmanPIDSolver = False

    hasSquad = True
    selectable = True
    isNormal = True

    selectionCircleRadius = meters(15)
    uiOverlayRadius = None #default to selectionCircleRadius * 0.9
    #state
    isUnderMouse = False
    #RBPhysics25d
    #mass = tons(1000)
    #inertia = tons(1000)
    #dragX = 1.0
    #dragZ = 25.0
    #rotationalDrag = 25.0
    #maxRotationalSpeed  = radiansPerSecond(1.0)
    #maxRudderPower      = radiansPerSecondSquared(4500.0)
    #control parameters

    length = meters(100)
    height = meters(30)
    beam   = meters(30)
    draft  = meters(10)

    moveToReachedTolerance = 150.0

    maxDistanceForFullStop = 50.0
    minDistanceForFullStop = 1500.0
    crampDistance          = 7500
    collisionClass         = 1

    interactionWeight = 100

#----------------------------------------------------------------------------
#-- UTILTITY ENTITIES -------------------------------------------------------
#----------------------------------------------------------------------------
class Squad(Ent):
    aspects = [SquadAI]

#----------------------------------------------------------------------------
#-- FIRST CLASS ENTITIES - TUNED AND USABLE ---------------------------------
#----------------------------------------------------------------------------

class SmallBoat(Boat):
    lod1 = (800, 'smallBoatOverlay.mesh')
    lod2 = (4000, 'smallBoatOverlay2.mesh')
    maxDistanceForFullStop  = 5.0
    minDistanceForFullStop  = 300.0
    selectionCircleRadius   = meters(45)
    crampDistance           = 3500
    collisionClass          = 1

    length = meters(8)
    height = meters(3)
    beam   = meters(3)
    draft  = meters(1)
    wakeSize = 1

    #UI
    interactionWeight = 100
    interactionSpringDistance = 150
    interactionSpringForce  = 100

class MediumBoat(Boat):
    maxDistanceForFullStop  = 50.0
    minDistanceForFullStop  = 500.0
    selectionCircleRadius   = meters(125)
    crampDistance           = 15000
    collisionClass          = 2

    length = meters(20)
    height = meters(10)
    beam   = meters(10)
    draft  = meters(2)

    wakeSize = 2

    #UI
    interactionWeight = 1000
    interactionSpringDistance = 500
    interactionSpringForce = 100

class LargeBoat(Boat):
    maxDistanceForFullStop  = 50.0
    minDistanceForFullStop  = 1500.0
    selectionCircleRadius   = meters(250)
    crampDistance           = 95000
    collisionClass          = 3

    length = meters(100)
    height = meters(30)
    beam   = meters(30)
    draft  = meters(10)

    wakeSize = 3

    #UI
    interactionWeight = 2000
    interactionSpringDistance = 500
    interactionSpringForce = 100

class SPEEDBOAT(SmallBoat):
    uiname = 'SpeedBoat'
    mesh = 'boat.mesh'

    maxSpeed = knots(30.0)
    accelSpeed = gameUnit(1.0)
    rotationalSpeed = degreesSecond(12.0)

    avoidanceSize = vector3(meters(7.62), 0.0, meters(2.44)) # * .5 #diameter to radius
    length = meters(7.62)

class ALIENBOAT(SmallBoat):
    uiname = 'AlienBoat'
    mesh = 'alienship.mesh'

    maxSpeed = knots(45.0)
    accelSpeed = gameUnit(1.0)
    rotationalSpeed = degreesSecond(15.0)
    length = meters(8.0)
    beam = meters(4.0)
    avoidanceSize = vector3(length, 0.0, beam)
    
class SAILBOAT(SmallBoat):
    uiname = 'SailBoat'
    mesh = 'sailboat.mesh'
    
    maxSpeed = knots(20.0)
    accelSpeed = gameUnit(.5)
    rotationalSpeed = degreesSecond(12.0)
    length = meters(8.0)
    beam = meters(3.0)
    avoidanceSize = vector3(length, 0.0, beam)

class DDG51(MediumBoat):
    #uiname = 'ArleighBurke'
    #mesh = 'DDG52'
    uiname = 'DDG51'
    mesh = 'ddg51.mesh'

    maxSpeed = knots(31.6)
    accelSpeed = feetSecondSqrd(0.4)
    rotationalSpeed = degreesSecond(2.5)
    avoidanceSize = vector3(feet(466.0), 0.0, feet(59.0)) * .5 #radius to diameter
    length = feet(466.0)
    width  = feet(59.0)
    beam  = feet(59.0)


#----------------------------------------------------------------------------
#-- SECOND CLASS ENTITIES - COPY PASTED FROM CSC -----------------------------
#----------------------------------------------------------------------------


class SLEEK(MediumBoat):
    uiname = 'SLEEK'
    mesh = 'sleek.mesh'

    maxSpeed = knots(32.08)
    accelSpeed = feetSecondSqrd(0.4)
    rotationalSpeed = degreesSecond(0.8)
    avoidanceSize = vector3(feet(458), 0.0, feet(60)) * .5 #radius to diameter

    width  = feet(60)
    length = feet(458)


class CVN68(LargeBoat):
    uiname = 'Nimitz'
    mesh = 'cvn68.mesh'

    maxSpeed = knots(33.6)
    accelSpeed = feetSecondSqrd(0.2)
    rotationalSpeed = degreesSecond(0.8)

    #control parameters
    moveTolerance = meters(200)
    avoidanceSize = vector3(meters(332.85), 0.0, meters(200)) * .5 #radius to diameter
    collisionLookAheadTime = minutes(20.0)
    length = meters(332.85)


class CIGARETTE(SmallBoat):
    uiname = 'Cigarette'
    mesh = 'cigarette.mesh'

    maxSpeed = knots(50.0)
    accelSpeed = gameUnit(1.2)
    rotationalSpeed = degreesSecond(12)

    avoidanceSize = vector3(meters(7.62), 0.0, meters(2.44))  #* .5 #diameter to radius

    length = meters (7.62)
    width  = meters (2.44)


