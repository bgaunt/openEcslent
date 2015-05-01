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

#ifndef CNETDATA_H
#define CNETDATA_H

#include <Python.h>
#include <limits.h>
#include "structmember.h"
#include "mathlib.h"
#include "float2.h"
#include "float3.h"
#include "units.h"

typedef struct {
    PyObject_HEAD
    float timeStamp;
    float2 pos;
    float yaw;
    float speed;
    float desiredSpeed;
    float desiredHeading;
} CNetData;

//standard alloc
static PyObject *
CNetData_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    CNetData* self;
    self = (CNetData*)(type->tp_alloc(type, 0));
    if (self != NULL)
    {
        self->timeStamp = 0;
        self->pos.x = 0.0f;
        self->pos.y = 0.0f;
        self->yaw = 0.0f;
        self->speed = 0.0f;
        self->desiredSpeed = 0.0f;
        self->desiredHeading = 0.0f;
    }
    return (PyObject *)self;
}

//standard dealloc
static void
CNetData_dealloc(PyObject* self)
{
    self->ob_type->tp_free((PyObject*)self);
}

static int
CNetData_init(CNetData *self, PyObject *args, PyObject *kwds)
{
    if (!PyArg_ParseTuple(args, "fffffff", 
                &self->timeStamp,
                &self->pos.x,
                &self->pos.y,
                &self->yaw,
                &self->speed,
                &self->desiredSpeed,
                &self->desiredHeading
            )
        )
        return -1;

    return 0;
}

static const char*
CNetData_tostr(CNetData* self)
{
    printf("CNetData_tostr(%p)", self);
    static char str[1024];
    snprintf(str, 1024, "ts:%6.2f p:%6.2f,%6.2f y:%6.2f s:%6.2f ds:%6.2f dh:%6.2f", self->timeStamp, self->pos.x, self->pos.y, self->yaw, self->speed, self->desiredSpeed, self->desiredHeading);
    printf(": %s\n", str);
    return str;
}

static PyObject*
CNetData_str(PyObject* self)
{
    return Py_BuildValue("s", CNetData_tostr((CNetData*)self));
}

static PyMethodDef CNetData_methods[] = {
    {NULL, NULL, 0, NULL},   /* Sentinel */
};

static PyMemberDef CNetData_members[] = {
    {"timeStamp",   T_FLOAT, offsetof(CNetData, timeStamp), 0, "timeStamp"},
    {"posX",        T_FLOAT, offsetof(CNetData, pos) + offsetof(float2, x), 0, "posX"},
    {"posY",        T_FLOAT, offsetof(CNetData, pos) + offsetof(float2, y), 0, "posY"},
    {"yaw",         T_FLOAT, offsetof(CNetData, yaw), 0, "yaw"},

    {"speed",           T_FLOAT, offsetof(CNetData, speed), 0, "speed"},
    {"desiredSpeed",    T_FLOAT, offsetof(CNetData, desiredSpeed), 0, "desiredSpeed"},
    {"desiredHeading",  T_FLOAT, offsetof(CNetData, desiredHeading), 0, "desiredHeading"},

    {NULL}  /* Sentinel */
};

static PyTypeObject CNetData_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                          /*ob_size*/
    "cent.CNetData",                          /*tp_name*/
    sizeof(CNetData),                         /*tp_basicsize*/
    0,                                          /*tp_itemsize*/
    (destructor) CNetData_dealloc,            /*tp_dealloc*/
    0,                                          /*tp_print*/
    0,                                          /*tp_getattr*/
    0,                                          /*tp_setattr*/
    0,                                          /*tp_compare*/
    CNetData_str,                             /*tp_repr*/
    0,                                          /*tp_as_number*/
    0,                                          /*tp_as_sequence*/
    0,                                          /*tp_as_mapping*/
    0,                                          /*tp_hash */
    0,                                          /*tp_call*/
    CNetData_str,                             /*tp_str*/
    0,                                          /*tp_getattro*/
    0,                                          /*tp_setattro*/
    0,                                          /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,   /*tp_flags*/
    "CNetData",                               /*tp_doc */
    0,                                          /*tp_traverse */
    0,                                          /*tp_clear */
    0,                                          /*tp_richcompare */
    0,                                          /*tp_weaklistoffset */
    0,                                          /*tp_iter */
    0,                                          /*tp_iternext */
    CNetData_methods,                         /*tp_methods */
    CNetData_members,                         /*tp_members */
    0,                                          /*tp_getset */
    0,                                          /*tp_base */
    0,                                          /*tp_dict */
    0,                                          /*tp_descr_get */
    0,                                          /*tp_descr_set */
    0,                                          /*tp_dictoffset */
    (initproc)CNetData_init,                  /*tp_init */
    0,                                          /*tp_alloc */
    CNetData_new,                             /*tp_new */
};

#endif //CNETDATA_H
