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

#ifndef CENT_H
#define CENT_H

#include <Python.h>
#include <limits.h>
#include "const.h"
#include "structmember.h"
#include "mathlib.h"
#include "float2.h"
#include "units.h"
#include "cdebugline.h"
#include "CDesiredState.h"


/////////////////////////////////////////////////////////////////////////
/// LowLevelBoatAI
/// Low level Ai is implemented as fast c code 
/// So that we can have lots of boats running around
/// The outside universe can grab keys, and use them to pull object data
/////////////////////////////////////////////////////////////////////////


enum Voters
{
    VOTERS_MAINTAIN_HEADING,
    VOTERS_TOWARDS_DEST,
    VOTERS_AVOID_COLLISIONS,
    VOTERS_AVOID_CRAMPED_COLLISIONS,
    VOTERS_NUM,
};

typedef struct {
    float angle;
    float votes[VOTERS_NUM];
    float2 offset;
} AngleVote;

typedef struct {
    PyObject_HEAD
    int id;

    float maxSpeed;
    float maxSpeedAstern;
    float maxAcceleration;
    float maxRotationalSpeed;
    float2 boundingBoxSize;
    float collisionLookAheadTime;
    float maxDistanceForFullStop;
    float minDistanceForFullStop;
    float crampDistance;
    int collisionClass;

    float2 pos;
    float yaw;
    float speed;

    float2 vel; //driven by yaw / speed

    //misc
    unsigned int ticksUntilAngleVoting;
    AngleVote angleVotes[numAngleVotes];

    //helmsman directives
    float helmDesiredSpeed;
    float helmDesiredHeading;

    //navigator directives
    float navDesiredSpeed;
    float navDesiredHeading;

    //aI Directives
    float2 destination;
    bool stopAtDestination;
    bool inRamMode;

    CDebugLine debugLines[kMaxDebugLines];
    int numDebugLines;

    int updateCounter;

} CEnt;


//Global methods 
static PyObject*
RunUnitTests(PyObject* _self, PyObject* args)
{
    printf("RunUnitTests()\n");
    Py_INCREF(Py_None); 
    return Py_None;
}

static PyObject*
CEnt_getInvalidFloat(PyObject* _self, PyObject* args)
{
    PyObject *result = Py_BuildValue("(f)", kInvalidFloat);
    return result;
}

static PyMethodDef cent_methods[] = {
    {"runUnitTests", RunUnitTests, METH_VARARGS, "Run My Internal Unit Tests to verify assumptions"},
    {"getInvalidFloat",  CEnt_getInvalidFloat, METH_VARARGS, "Get our invalid float sentinel"},
    {NULL, NULL, 0, NULL},   /* Sentinel */
};

//global table of ALL registered cents 
CEnt* gCEnts[1024];
int gCEntCounter = 0;

//standard alloc
static PyObject *
CEnt_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    CEnt *self;
    self = (CEnt*)(type->tp_alloc(type, 0));
    if (self != NULL)
    {
        self->maxSpeed = 0.0f;
        self->maxSpeedAstern = 0.0f;
        self->maxAcceleration = 0.0f;
        self->maxRotationalSpeed = 0.0f;
        self->boundingBoxSize.x = 0.0f;
        self->boundingBoxSize.y = 0.0f;
        self->maxDistanceForFullStop = 50.0;
        self->minDistanceForFullStop = 1500.0;

        self->pos.x = 0.0f;
        self->pos.y = 0.0f;
        self->yaw = 0.0f;
        self->speed = 1.0f;


        float2 v;
        v.x = 1.0f;
        v.y = 0.0f;



        self->helmDesiredSpeed = kInvalidFloat;
        self->helmDesiredHeading = kInvalidFloat;

        self->navDesiredSpeed = kInvalidFloat;
        self->navDesiredHeading = kInvalidFloat;

        self->destination.x = kInvalidFloat;
        self->destination.y = kInvalidFloat;
        self->stopAtDestination = true;
        self->inRamMode = false;

        self->numDebugLines = 0;
        self->updateCounter = 0;
    }
    return (PyObject *)self;
}

//standard dealloc
static void
CEnt_dealloc(PyObject* self)
{
    self->ob_type->tp_free((PyObject*)self);
}

static int
CEnt_init(CEnt *self, PyObject *args, PyObject *kwds)
{
    if (!PyArg_ParseTuple(args, "ffffffffffi", 
                &self->maxSpeed,
                &self->maxSpeedAstern, 
                &self->maxAcceleration,
                &self->maxRotationalSpeed,
                &self->boundingBoxSize.x,
                &self->boundingBoxSize.y,
                &self->collisionLookAheadTime,
                &self->maxDistanceForFullStop,
                &self->minDistanceForFullStop,
                &self->crampDistance,
                &self->collisionClass
                ))
        return -1;

    return 0;
}

static const char*
CEnt_tostr(CEnt* self)
{
    static char str[1024];
    snprintf(str, 1024, "{[maxSpeed:%6.2f, maxSpeedAstern:%6.2f, maxRotationalSpeed:%6.2f, maxAcceleration:%6.2f,  boundingBoxSize:%6.2f, %6.2f](pos:%6.2f,%6.2f, yaw:%6.2f, speed:%6.2f, destination:%6.2f,%6.2f)}", self->maxSpeed, self->maxSpeedAstern, self->maxRotationalSpeed, self->maxAcceleration, self->boundingBoxSize.x, self->boundingBoxSize.y, self->pos.x, self->pos.y, self->yaw, self->speed, self->destination.x, self->destination.y);
    return str;
}

static PyObject*
CEnt_str(PyObject* self)
{
    return Py_BuildValue("s", CEnt_tostr((CEnt*)self));
}





void DrawLine(CEnt* self, float2 a, float2 b, float3 rgb)
{
    if(self->numDebugLines >= kMaxDebugLines)
        return;

    CDebugLine& line = self->debugLines[self->numDebugLines++];
    line.a = a;
    line.b = b;
    line.rgb = rgb;
}

void DrawRay(CEnt* self, float2 a, float2 b, float3 rgb)
{
    DrawLine(self, a, add(a, b), rgb);
}

void DrawAngleRay(CEnt* self, float2 a, float angle, float len, float3 rgb)
{
    float2 v;
    v.x = len;
    v.y = 0.0f;
    v = yawVector(v, angle);
    DrawRay(self, a, v, rgb);
}


void DoHelmsman(CEnt* self, float dtime)
{
    ////////////////////////////////////////////////////////////////////////
    // HELMSMAN ////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////
    //self.ent.speed = self.ent.speed + mathlib.clamp(self.ent.helmDesiredSpeed - self.ent.speed, -self.ent.accelSpeed * dtime, self.ent.accelSpeed * dtime)
    if(kInvalidFloat == self->helmDesiredSpeed || kInvalidFloat == self->helmDesiredHeading)
        return;

    float timeScaledAcceleration = self->maxAcceleration * dtime;
    self->speed = self->speed + clamp(self->helmDesiredSpeed - self->speed, -timeScaledAcceleration, timeScaledAcceleration);

    //self.ent.pos += mathlib.yawVector(vector3(self.ent.speed,0,0), self.ent.yaw) * dtime
    float cosYaw = cos(-self->yaw);
    float sinYaw = sin(-self->yaw);

    self->vel.x = self->speed * cosYaw;
    self->vel.y = self->speed * sinYaw;

    self->pos = add(self->pos, mul(self->vel, dtime));
    //float timeScaledSpeed = self->speed * dtime;
    //self->pos.x += timeScaledSpeed * cosYaw;
    //self->pos.y += timeScaledSpeed * sinYaw;

    //self.ent.yaw += mathlib.clamp(self.ent.desiredOrientation - self.ent.yaw, -self.ent.rotationalSpeed * dtime, self.ent.rotationalSpeed * dtime)
    float timeScaledRotationalSpeed = self->maxRotationalSpeed * dtime;
    //if (self->helmDesiredSpeed > 0.5f)
    if (self->speed > 0.5f)
    {
        //printf("helmDesiredHeading:%f yaw:%f ", self->helmDesiredHeading, self->yaw);
        float angleDiff = differenceBetweenAngles(self->helmDesiredHeading, self->yaw);
        //printf("angleDiff:%f ", angleDiff);
        float dYaw = clamp(differenceBetweenAngles(self->helmDesiredHeading, self->yaw), -timeScaledRotationalSpeed, timeScaledRotationalSpeed);
        //printf("dYaw:%f ", dYaw);
        self->yaw += dYaw;
        //printf("\n");
    }


#ifdef DRAW_DESIRED_SPEED_HEADING
    float3 rgb;
    rgb.x = 1.0f;
    rgb.y = 1.0f;
    rgb.z = 1.0f;

    DrawAngleRay(self, self->pos, self->helmDesiredHeading, self->helmDesiredSpeed * 15.0f, rgb);
#endif
}

static PyObject*
CEnt_tick(PyObject* _self, PyObject* args)
{
    CEnt* self = (CEnt*) _self;

    float dtime = 0.0f;
    if (!PyArg_ParseTuple(args, "f", &dtime))
        return NULL;
    
    //need to have desired speed and heading for this to work
    DoHelmsman(self, dtime);

    Py_INCREF(Py_None); 
    return Py_None;
}

static PyObject*
CEnt_helmTick(PyObject* _self, PyObject *args)
{
    CEnt* self = (CEnt*) _self;
    float dtime = 0.0f;
    if (!PyArg_ParseTuple(args, "f", &dtime))
        return NULL;

    DoHelmsman(self, dtime);
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject*
CEnt_register(PyObject* _self, PyObject* args)
{
    CEnt* self = (CEnt*) _self;
    //printf("CEnt_register(%i, %p)\n", gCEntCounter, self);
    self->id = gCEntCounter;
    gCEnts[gCEntCounter++] = self;
    for(int i = 0; i < kMaxDebugLines; ++i)
    {
        PyObject* po = reinterpret_cast<PyObject*>(&self->debugLines[i]);
        Py_INCREF(po);
    }

    Py_INCREF(Py_None); 
    return Py_None;
}


static PyObject*
CEnt_getDebugLines(PyObject* _self, PyObject* args)
{
    CEnt* self = (CEnt*) _self;
    PyObject *list;

    /*list = PyList_New(1);
    x = PyInt_FromLong(1L);
    Py_INCREF(x);
    PyList_SetItem(list, 0, x); 
    return list;
    */
    //Py_DECREF(x);

    list = PyList_New(self->numDebugLines);
    //Py_INCREF(list);
    for(int i = 0; i < self->numDebugLines; ++i)
    {
        CDebugLine& l = self->debugLines[i];
        //PyObject* po = reinterpret_cast<PyObject*>(&self->debugLines[i]);
        //Py_INCREF(po);
        //PyList_SetItem(list, i, po);

        //Py_INCREF((PyObject*) &self->debugLines[i]);
        //PyList_SetItem(list, i, (PyObject*) &self->debugLines[i]);
        PyList_SetItem(list, i, Py_BuildValue("(f,f,f,f)", l.a.x, l.a.y, l.b.x, l.b.y));
        //x = PyInt_FromLong(i);
        //Py_INCREF(x);
        //PyList_SetItem(list, i, x); 
        //Py_DECREF(x);
    }

    return list;
}


static PyMethodDef CEnt_methods[] = {
    {"tick",        CEnt_tick, METH_VARARGS, "Update a CEnt's state by one frame"},
    {"helmTick",    CEnt_helmTick, METH_VARARGS, "Update a CEnt's helm by one frame - no AI"},
    {"register",    CEnt_register, METH_VARARGS, "Add the CEnt to our global pool of CEnts"},
    {"getDebugLines",    CEnt_getDebugLines, METH_VARARGS, "Get the list of debug lines I want to draw to the screen"},
    {NULL, NULL, 0, NULL},   /* Sentinel */
};

static PyMemberDef CEnt_members[] = {
    {"id",                 T_INT,   offsetof(CEnt, id),                                    0,"id"},
    {"maxSpeed",           T_FLOAT, offsetof(CEnt, maxSpeed),                              0,"maxSpeed"},
    {"maxSpeedAstern",     T_FLOAT, offsetof(CEnt, maxSpeedAstern),                        0,"maxSpeedAstern"},
    {"maxAcceleration",    T_FLOAT, offsetof(CEnt, maxAcceleration),                       0,"maxAcceleration"},
    {"maxRotationalSpeed", T_FLOAT, offsetof(CEnt, maxRotationalSpeed),                    0,"maxRotationalSpeed"},
    {"boundingBoxSizeX",   T_FLOAT, offsetof(CEnt, boundingBoxSize) + offsetof(float2, x), 0,"boundingBoxSizeX"},
    {"boundingBoxSizeY",   T_FLOAT, offsetof(CEnt, boundingBoxSize) + offsetof(float2, y), 0,"boundingBoxSizeY"},

    {"posX",               T_FLOAT, offsetof(CEnt, pos) + offsetof(float2, x),             0,"posx"},
    {"posY",               T_FLOAT, offsetof(CEnt, pos) + offsetof(float2, y),             0,"posy"},
    {"yaw",                T_FLOAT, offsetof(CEnt, yaw),                                   0,"yaw"},
    {"speed",              T_FLOAT, offsetof(CEnt, speed),                                 0,"speed"},
    {"velX",               T_FLOAT, offsetof(CEnt, vel) + offsetof(float2, x),             0,"velX"},
    {"velY",               T_FLOAT, offsetof(CEnt, vel) + offsetof(float2, y),             0,"velY"},

    {"helmDesiredHeading", T_FLOAT, offsetof(CEnt, helmDesiredHeading),                    0,"helmDesiredHeading"},
    {"helmDesiredSpeed",   T_FLOAT, offsetof(CEnt, helmDesiredSpeed),                      0,"helmDesiredSpeed"},
    {"navDesiredHeading",  T_FLOAT, offsetof(CEnt, navDesiredHeading),                     0,"navDesiredHeading"},
    {"navDesiredSpeed",    T_FLOAT, offsetof(CEnt, navDesiredSpeed),                       0,"navDesiredSpeed"},

    {"destinationX",       T_FLOAT, offsetof(CEnt, destination) + offsetof(float2, x),     0,"destinationX"},
    {"destinationY",       T_FLOAT, offsetof(CEnt, destination) + offsetof(float2, y),     0,"destinationY"},
    {"stopAtDestination",  T_BOOL,  offsetof(CEnt, stopAtDestination),                     0,"stopAtDestination"},
    {"inRamMode",          T_BOOL,  offsetof(CEnt, inRamMode),                             0,"inRamMode"},

    {"updateCounter",      T_INT,   offsetof(CEnt, updateCounter),                         0,"updateCounter"},

    {NULL}  /* Sentinel */
};

static PyTypeObject CEnt_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                        /*ob_size*/
    "cent.CEnt",                              /*tp_name*/
    sizeof(CEnt),                             /*tp_basicsize*/
    0,                                        /*tp_itemsize*/
    (destructor) CEnt_dealloc,                /*tp_dealloc*/
    0,                                        /*tp_print*/
    0,                                        /*tp_getattr*/
    0,                                        /*tp_setattr*/
    0,                                        /*tp_compare*/
    CEnt_str,                                 /*tp_repr*/
    0,                                        /*tp_as_number*/
    0,                                        /*tp_as_sequence*/
    0,                                        /*tp_as_mapping*/
    0,                                        /*tp_hash */
    0,                                        /*tp_call*/
    CEnt_str,                                 /*tp_str*/
    0,                                        /*tp_getattro*/
    0,                                        /*tp_setattro*/
    0,                                        /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
    "CEnt",                                   /*tp_doc */
    0,                                        /*tp_traverse */
    0,                                        /*tp_clear */
    0,                                        /*tp_richcompare */
    0,                                        /*tp_weaklistoffset */
    0,                                        /*tp_iter */
    0,                                        /*tp_iternext */
    CEnt_methods,                             /*tp_methods */
    CEnt_members,                             /*tp_members */
    0,                                        /*tp_getset */
    0,                                        /*tp_base */
    0,                                        /*tp_dict */
    0,                                        /*tp_descr_get */
    0,                                        /*tp_descr_set */
    0,                                        /*tp_dictoffset */
    (initproc)CEnt_init,                      /*tp_init */
    0,                                        /*tp_alloc */
    CEnt_new,                                 /*tp_new */
};

#endif //CENT_H
