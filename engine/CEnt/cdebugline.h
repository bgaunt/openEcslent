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

#ifndef DEBUGLINE_H
#define DEBUGLINE_H

#include <Python.h>
#include <limits.h>
#include "structmember.h"
#include "mathlib.h"
#include "float2.h"
#include "float3.h"
#include "units.h"

/////////////////////////////////////////////////////////////////////////
/// LowLevelBoatAI
/// Low level Ai is implemented as fast c code 
/// So that we can have lots of boats running around
/// The outside universe can grab keys, and use them to pull object data
/////////////////////////////////////////////////////////////////////////

typedef struct {
    PyObject_HEAD
    float2 a;
    float2 b;
    float3 rgb;
} CDebugLine;

//standard alloc
static PyObject *
CDebugLine_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    CDebugLine* self;
    self = (CDebugLine*)(type->tp_alloc(type, 0));
    if (self != NULL)
    {
        self->a.x = 0.0f;
        self->a.y = 0.0f;
        self->b.x = 0.0f;
        self->b.y = 0.0f;
        self->rgb.x = 0.0f;
        self->rgb.y = 0.0f;
        self->rgb.z = 0.0f;
    }
    return (PyObject *)self;
}

//standard dealloc
static void
CDebugLine_dealloc(PyObject* self)
{
    self->ob_type->tp_free((PyObject*)self);
}

static int
CDebugLine_init(CDebugLine *self, PyObject *args, PyObject *kwds)
{
    if (!PyArg_ParseTuple(args, "fffffff", 
                &self->a.x,
                &self->a.y, 
                &self->b.x,
                &self->b.y,
                &self->rgb.x,
                &self->rgb.y,
                &self->rgb.z
            )
        )
        return -1;

    return 0;
}
static const char*
CDebugLine_tostr(CDebugLine* self)
{
    printf("CDebugLine_tostr(%p)", self);
    static char str[1024];
    snprintf(str, 1024, "[%f,%f]->[%f,%f]", self->a.x, self->a.y, self->b.x, self->b.y);
    printf(": %s\n", str);
    return str;
}

static PyObject*
CDebugLine_str(PyObject* self)
{
    return Py_BuildValue("s", CDebugLine_tostr((CDebugLine*)self));
}

static PyMethodDef CDebugLine_methods[] = {
    {NULL, NULL, 0, NULL},   /* Sentinel */
};

static PyMemberDef CDebugLine_members[] = {
    {"ax", T_FLOAT, offsetof(CDebugLine, a) + offsetof(float2, x), 0, "ax"},
    {"ay", T_FLOAT, offsetof(CDebugLine, a) + offsetof(float2, y), 0, "ay"},
    {"bx", T_FLOAT, offsetof(CDebugLine, b) + offsetof(float2, x), 0, "bx"},
    {"by", T_FLOAT, offsetof(CDebugLine, b) + offsetof(float2, y), 0, "by"},

    {"r",  T_FLOAT, offsetof(CDebugLine, rgb) + offsetof(float3, x), 0, "r"},
    {"g",  T_FLOAT, offsetof(CDebugLine, rgb) + offsetof(float3, y), 0, "g"},
    {"b",  T_FLOAT, offsetof(CDebugLine, rgb) + offsetof(float3, z), 0, "b"},

    {NULL}  /* Sentinel */
};

static PyTypeObject CDebugLine_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                          /*ob_size*/
    "cent.CDebugLine",                          /*tp_name*/
    sizeof(CDebugLine),                         /*tp_basicsize*/
    0,                                          /*tp_itemsize*/
    (destructor) CDebugLine_dealloc,            /*tp_dealloc*/
    0,                                          /*tp_print*/
    0,                                          /*tp_getattr*/
    0,                                          /*tp_setattr*/
    0,                                          /*tp_compare*/
    CDebugLine_str,                             /*tp_repr*/
    0,                                          /*tp_as_number*/
    0,                                          /*tp_as_sequence*/
    0,                                          /*tp_as_mapping*/
    0,                                          /*tp_hash */
    0,                                          /*tp_call*/
    CDebugLine_str,                             /*tp_str*/
    0,                                          /*tp_getattro*/
    0,                                          /*tp_setattro*/
    0,                                          /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,   /*tp_flags*/
    "CDebugLine",                               /*tp_doc */
    0,                                          /*tp_traverse */
    0,                                          /*tp_clear */
    0,                                          /*tp_richcompare */
    0,                                          /*tp_weaklistoffset */
    0,                                          /*tp_iter */
    0,                                          /*tp_iternext */
    CDebugLine_methods,                         /*tp_methods */
    CDebugLine_members,                         /*tp_members */
    0,                                          /*tp_getset */
    0,                                          /*tp_base */
    0,                                          /*tp_dict */
    0,                                          /*tp_descr_get */
    0,                                          /*tp_descr_set */
    0,                                          /*tp_dictoffset */
    (initproc)CDebugLine_init,                  /*tp_init */
    0,                                          /*tp_alloc */
    CDebugLine_new,                             /*tp_new */
};

#endif //DEBUGLINE_H
