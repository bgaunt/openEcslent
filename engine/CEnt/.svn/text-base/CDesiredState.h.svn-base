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

#ifndef DESIRED_STATE_H
#define DESIRED_STATE_H

#include <Python.h>
#include <limits.h>
#include "structmember.h"
#include "mathlib.h"
#include "float2.h"
#include "units.h"
#include "cdebugline.h"
#include "const.h"

///So a desired state is a struct containing all possible desired states
//In python we interpret and work with these and fun objects with inheritence and all that fancyness.
//In c land they are just a single struct

enum CDesiredStateType
{
    DESIRED_STATE_TYPE_INVALID,
    DESIRED_STATE_TYPE_STOPPED_AT_POSITION,
    DESIRED_STATE_TYPE_MAINTAINING_RELATIVE_TO_ENT,
};

typedef struct {
    PyObject_HEAD
    CDesiredStateType type;

    union {
        float2 pos;             //world position or primary offset
        float2 offset;
    };

    int targetID;

} CDesiredState;

//standard alloc
static PyObject *
CDesiredState_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    CDesiredState *self;
    self = (CDesiredState*)(type->tp_alloc(type, 0));
    if (self != NULL)
    {
        self->type = DESIRED_STATE_TYPE_INVALID;
        self->pos.x = 0.0f;
        self->pos.y = 0.0f;
        self->offset.x = 0.0f;
        self->offset.y = 0.0f;
        self->targetID = kInvalidHandle;
    }
    return (PyObject *)self;
}

//standard dealloc
static void
CDesiredState_dealloc(PyObject* self)
{
    self->ob_type->tp_free((PyObject*)self);
}

static int
CDesiredState_init(CDesiredState *self, PyObject *args, PyObject *kwds)
{
    if (!PyArg_ParseTuple(args, "i", 
                &self->type
                ))
        return -1;

    return 0;
}

static const char*
CDesiredState_str(CDesiredState* self)
{
    static char str[1024];
    switch(self->type)
    {
    case DESIRED_STATE_TYPE_STOPPED_AT_POSITION:
        snprintf(str, 1024, "(%4.2f, %4.2f)", self->pos.x, self->pos.y);
        break;

    case DESIRED_STATE_TYPE_MAINTAINING_RELATIVE_TO_ENT:
        snprintf(str, 1024, "[%i]->(%4.2f, %4.2f)", self->targetID, self->offset.x, self->offset.y);
        break;
    }
    return str;
}

static PyObject*
CDesiredState_str(PyObject* self)
{
    return Py_BuildValue("s", CDesiredState_str((CDesiredState*)self));
}

static PyMethodDef CDesiredState_methods[] = {
    {NULL, NULL, 0, NULL},   /* Sentinel */
};

static PyMemberDef CDesiredState_members[] = {
    {"type",                    T_INT,      offsetof(CDesiredState, type),                           0, "type"},
    {"posX",                    T_FLOAT,    offsetof(CDesiredState, pos) + offsetof(float2, x),      0, "posX"},
    {"posY",                    T_FLOAT,    offsetof(CDesiredState, pos) + offsetof(float2, y),      0, "posY"},
    {"offsetX",                 T_FLOAT,    offsetof(CDesiredState, pos) + offsetof(float2, x),      0, "offsetX"},
    {"offsetY",                 T_FLOAT,    offsetof(CDesiredState, pos) + offsetof(float2, y),      0, "offsetY"},
    {"targetID",                T_INT,      offsetof(CDesiredState, targetID),                       0, "targetID"},

    {NULL}  /* Sentinel */
};

static PyTypeObject CDesiredState_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                        /*ob_size*/
    "cent.CDesiredState",                              /*tp_name*/
    sizeof(CDesiredState),                             /*tp_basicsize*/
    0,                                        /*tp_itemsize*/
    (destructor) CDesiredState_dealloc,                /*tp_dealloc*/
    0,                                        /*tp_print*/
    0,                                        /*tp_getattr*/
    0,                                        /*tp_setattr*/
    0,                                        /*tp_compare*/
    CDesiredState_str,                                 /*tp_repr*/
    0,                                        /*tp_as_number*/
    0,                                        /*tp_as_sequence*/
    0,                                        /*tp_as_mapping*/
    0,                                        /*tp_hash */
    0,                                        /*tp_call*/
    CDesiredState_str,                                 /*tp_str*/
    0,                                        /*tp_getattro*/
    0,                                        /*tp_setattro*/
    0,                                        /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
    "CDesiredState",                                   /*tp_doc */
    0,                                        /*tp_traverse */
    0,                                        /*tp_clear */
    0,                                        /*tp_richcompare */
    0,                                        /*tp_weaklistoffset */
    0,                                        /*tp_iter */
    0,                                        /*tp_iternext */
    CDesiredState_methods,                             /*tp_methods */
    CDesiredState_members,                             /*tp_members */
    0,                                        /*tp_getset */
    0,                                        /*tp_base */
    0,                                        /*tp_dict */
    0,                                        /*tp_descr_get */
    0,                                        /*tp_descr_set */
    0,                                        /*tp_dictoffset */
    (initproc)CDesiredState_init,                      /*tp_init */
    0,                                        /*tp_alloc */
    CDesiredState_new,                                 /*tp_new */
};

#endif //DESIRED_STATE_H
