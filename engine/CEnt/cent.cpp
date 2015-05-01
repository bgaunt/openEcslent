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

#include <Python.h>
#include "cent.h"
#include "cdebugline.h"
#include "CNetData.h"
#include "CDesiredState.h"


PyMODINIT_FUNC initcent(void) 
{
    PyObject* m;
	
	//initialize our global methods
    m = Py_InitModule3("cent", cent_methods, "C based physics / ai universe.");

    //Initialize our classes
    //if (PyType_Ready(&Attributes_Type) < 0) return;
    //if (PyType_Ready(&State_Type) < 0)      return;

	//Py_INCREF(&Attributes_Type);
    //PyModule_AddObject(m, "Attributes", (PyObject *)&Attributes_Type);
	//Py_INCREF(&State_Type);
    //PyModule_AddObject(m, "State", (PyObject *)&State_Type);
    if (PyType_Ready(&CEnt_Type) < 0)       return;
	Py_INCREF(&CEnt_Type);
    PyModule_AddObject(m, "CEnt",       (PyObject *)&CEnt_Type);

    if (PyType_Ready(&CDebugLine_Type) < 0)       return;
	Py_INCREF(&CDebugLine_Type);
    PyModule_AddObject(m, "CDebugLine", (PyObject *)&CDebugLine_Type);

    if (PyType_Ready(&CNetData_Type) < 0)       return;
	Py_INCREF(&CNetData_Type);
    PyModule_AddObject(m, "CNetData", (PyObject *)&CNetData_Type);

    if (PyType_Ready(&CDesiredState_Type) < 0)       return;
	Py_INCREF(&CDesiredState_Type);
    PyModule_AddObject(m, "CDesiredState", (PyObject *)&CDesiredState_Type);
}
