//---------------------------------------------------------------------------
// Copyright 2010, 2011 Sushil J. Louis and Christopher E. Miles, 
// Evolutionary Computing Systems Laboratory, Department of Computer Science 
// and Engineering, University of Nevada, Reno. 
//
// This file is part of OpenECSLENT 
//
//    OpenECSLENT is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    OpenECSLENT is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with OpenECSLENT.  If not, see <http://www.gnu.org/licenses/>.
//---------------------------------------------------------------------------
//-------------------------End Copyright Notice------------------------------

#ifndef MATHLIB_H
#define MATHLIB_H
const float pi = 3.1415f;
const float twopi = pi * 2.0f;
const float halfpi = pi / 2.0f;
#include "float2.h"

float clamp(float val, float min, float max)
{
    if(val <= min)
        return min;
    else if (val >= max)
        return max;
    return val;
}

inline float makeAnglePosNeg(float angle)
{
    //printf("makeAnglePosNeg:%f ", angle);
    while (angle > pi)
        angle -= twopi;
    while (angle < -pi)
        angle += twopi;
    //printf("->%f ", angle);
    return angle;
}

inline float differenceBetweenAngles(float angle1, float angle2)
{
    return makeAnglePosNeg(angle1 - angle2);
}

float min(float a, float b)
{
    if( b < a ) return b;
    return a;
}

float max(float a, float b)
{
    if( b > a ) return b;
    return a;
}

float2 lineCollisionBase(float2 p1, float2 p2, float2 p3, float2 p4)
{
    float2 u;
    u.x = ((p4.x - p3.x) * (p1.y - p3.y) - (p4.y - p3.y) * (p1.x - p3.x)) / ((p4.y - p3.y) * (p2.x - p1.x) - (p4.x - p3.x) * (p2.y - p1.y));
    u.y = ((p2.x - p1.x) * (p1.y - p3.y) - (p2.y - p1.y) * (p1.x - p3.x)) / ((p4.y - p3.y) * (p2.x - p1.x) - (p4.x - p3.x) * (p2.y - p1.y));
    return u;
}

float2 lineCollision(float2 p1, float2 p2, float2 p3, float2 p4)
{
    float2 u = lineCollisionBase(p1, p2, p3, p4);
    float2 answer;
    answer.x = p1.x + u.x * (p2.x - p1.x);
    answer.y = p1.y + u.x * (p2.y - p1.y);
    return answer;
}

bool lineSegmentCollision(float2 p1, float2 p2, float2 p3, float2 p4, float2& outPoint)
{
    float2 u = lineCollisionBase(p1, p2, p3, p4);
    if (u.x >= 0.0f && u.x <= 1.0f && u.y >= 0.0f && u.y <= 1.0f)
    {
        outPoint.x = p1.x + u.x * (p2.x - p1.x);
        outPoint.y = p1.y + u.x * (p2.y - p1.y);
        return true;
    }
    return false;
}

// Initial AlmostEqualULPs version - fast and simple, but
// some limitations.
// modified from from http://www.cygnus-software.com/papers/comparingfloats/comparingfloats.htm
bool FEqualityDiscrete(float A, float B, int maxUlps)
{
    assert(sizeof(float) == sizeof(int));
    return abs(*(int*)&A - *(int*)&B) < maxUlps;
}

//KNuths float equality functions
bool approximatelyEqual(float a, float b, float epsilon)
{
    return fabs(a - b) <= ( (fabs(a) < fabs(b) ? fabs(b) : fabs(a)) * epsilon);
}

bool essentiallyEqual(float a, float b, float epsilon)
{
    return fabs(a - b) <= ( (fabs(a) > fabs(b) ? fabs(b) : fabs(a)) * epsilon);
}

bool definitelyGreaterThan(float a, float b, float epsilon)
{
    return (a - b) > ( (fabs(a) < fabs(b) ? fabs(b) : fabs(a)) * epsilon);
}

bool definitelyLessThan(float a, float b, float epsilon)
{
    return (b - a) > ( (fabs(a) < fabs(b) ? fabs(b) : fabs(a)) * epsilon);
}

#endif
