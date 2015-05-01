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

#ifndef FLOAT2_H
#define FLOAT2_H
typedef struct {
    float x;
    float y;
} float2;

inline float lengthSquared(const float2& v)
{
    return v.x * v.x + v.y * v.y;
}

inline float length(const float2& v)
{
    return sqrt(v.x * v.x + v.y * v.y);
}

inline float2 add(const float2& a, const float2& b)
{
    float2 answer;
    answer.x = a.x + b.x;
    answer.y = a.y + b.y;
    return answer;
}

inline float2 sub(const float2& a, const float2& b)
{
    float2 answer;
    answer.x = a.x - b.x;
    answer.y = a.y - b.y;
    return answer;
}

inline float2 mul(const float2& a, float2& b)
{
    float2 answer;
    answer.x = a.x * b.x;
    answer.y = a.y * b.y;
    return answer;
}

inline float2 mul(const float2& f2, float c)
{
    float2 answer;
    answer.x = f2.x * c;
    answer.y = f2.y * c;
    return answer;
} 

inline float2 normalized(const float2& a)
{
    float l = length(a);
    float2 answer;
    answer.x = a.x / l;
    answer.y = a.y / l;
    return answer;
}

inline float dotProduct(const float2& a, const float2& b)
{
    return a.x * b.x + a.y * b.y;
}

float2 yawVector(const float2& vec, float yaw)
{
    float cosYaw = cos(yaw);
    float sinYaw = sin(yaw);
    float2 answer;
    answer.x = cosYaw * vec.x + sinYaw * vec.y;
    answer.y = -sinYaw * vec.x + cosYaw * vec.y;
    return answer;
}

inline void rotate90(float2& f)
{
    float t = f.y;
    f.y = f.x;
    f.x = -t;
}
#endif
