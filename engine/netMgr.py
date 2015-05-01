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

from threading import Thread
from collections import deque
import time
import socket
import sys
import struct
import os
import yaml
import math


#ecslent imports
from vector import vector3
import boat
from mgr import Mgr, EngineObject
import mathlib
from units import *
from netAspect import NetAspect
from control   import ManualControl
import command

from entMgr import Player


gMoveCameraToEntPos = None
def createUDPSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(1)
    return sock

def myIP():
    ip = socket.gethostbyname(socket.gethostname())
    #if not ('127.0.0.1' == ip or '127.0.1.1' == ip):
    if not ip.startswith('127'):
        return ip
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com', 0))
        ip, p = s.getsockname()
        s.close()
        return ip
    except:
        return None

IgnoreMessagesFromSelf = False
RECEIVE_BUFFER_LENGTH  = 100
SERVER_FREQUENCY       = 0.47
CLIENT_FREQUENCY       = 0.07

class Listener(Thread):
    def __init__(self, ip, port, packetSize, isServer):
        self.ip = ip
        print self.ip, " Creating Listener"

        self.port = port
        self.packetSize = packetSize
        self.isServer = isServer
        self.listenSocket = None
        self.die    = False
        self.receiveQueue  = deque(maxlen=RECEIVE_BUFFER_LENGTH)
        Thread.__init__(self)


    def run(self):
        self.listenSocket = createUDPSocket()
        self.listenSocket.bind(('', self.port))
        print self.ip, " Running listener thread "
        while not self.die:
            try:
                msg, address = self.listenSocket.recvfrom(self.packetSize)
                #print "From: ", str(address)
                if not (address[0] == self.ip):
                    self.receiveQueue.appendleft((msg, address))
            except (socket.timeout):
                pass
                #print self.ip, " Waiting for network server"
            except:
                raise
        print "Stopping Listener thread "
        sys.stdout.flush()

    def stop(self):
        self.die = True
        self.listenSocket.close()
        time.sleep(0.5)

    def getMessages(self):
        msg = self.getMessage()
        while msg:
            yield msg
            msg = self.getMessage()

    def getMessage(self):
        try:
            msg, address = self.receiveQueue.pop()# pop on the right
            return msg
        except (IndexError): # empty!
            #print self.ip, "No Message Traffic!, no network"
            return None
        except:
            raise

class Broadcaster(Thread):
    def __init__(self, ip, port, packetSize, isServer):
        Thread.__init__(self)
        self.ip = ip
        print self.ip, " Creating Broadcaster"
        self.port = port
        self.packetSize = packetSize
        self.isServer = isServer
        self.broadcastSocket = None
        self.die    = False
        self.sendQueue  = deque() # must send all commands

    def run(self):
        self.broadcastSocket = createUDPSocket()
        print self.ip, " Running Command Broadcaster thread "
        while not self.die:
            try:
                while self.sendQueue:
                    msg = self.sendQueue.pop()
                    n = self.broadcastSocket.sendto(msg, ('<broadcast>', self.port))

                if self.isServer:
                    time.sleep(SERVER_FREQUENCY)
                else:
                    time.sleep(CLIENT_FREQUENCY)                    
                #print n, " bytes sent"
            except (IndexError):
                time.sleep(SERVER_FREQUENCY)
                pass
            except:
                raise

        print self.ip, "Stopping broadcast thread "
        sys.stdout.flush()
        
    def stop(self):
        self.die = True
        self.broadcastSocket.close()
        time.sleep(0.5)

    def putMessage(self, msg):
        self.sendQueue.appendleft(msg)

    def putPriorityMessage(self, msg):
        self.sendQueue.append(msg)

    def putMessages(self, msg):
        self.sendQueue.extendleft(msg)


class NetMgr(Mgr):

    PacketSize = 65536
    DefaultPort = 54321

    InfoMessage        = 0
    StatusMessage      = 1
    RequestInfoMessage = 2
    RequestShipStatus  = 3
    CommandMessage     = 4
    CreateShip         = 5 # not used
    AbsoluteInfo       = 6 
    SquelchCommand     = 7


    netEnts = {}
    unknowns = {}
    entNameClassMap = {}

    tick = None

    def __init__(self, engine):
        EngineObject.__init__(self, engine)
        assert engine is not None
        print "Creating Net Manager"
        self.address = None
        self.ip = myIP()
        if not self.ip:
            self.ip = self.engine.localOptions.networkingOptions.ip
        self.port = self.DefaultPort

        self.ignoreMessagesFromSelf = True
        self.listener    = None
        self.broadcaster = None
        self.isServer    = False
        self.startTime   = time.clock()

#-------structs to parse incoming outgoing messages

        self.header       = struct.Struct("=Biii")
        self.info         = struct.Struct("=i 256s256s ff fff ii")
        #self.absoluteInfo = struct.Struct("i fff fff f 256s")
        self.status       = struct.Struct("=i fff fff ff ff H")
        self.int          = struct.Struct("=i")
        self.squelch      = struct.Struct("=i")
        self.command      = struct.Struct("=iff")
        self.createShip   = struct.Struct("=256s 256s fff f")
        self.absoluteInfo = struct.Struct("=i fff fff f 256s")


    def simTimeMilli(self):
        return (time.clock() - self.startTime) * 1000.0 # convert to milli

#-------optimization trick changes between two tick methods---------
#-------Sets self.tick to be one of two methods
#-------self.vShipTick turns on VShip networking
#-------self.passTick runs without networking - does nothing
    def initialize(self):
        '''
        Optimization trick changes between two tick methods
        Sets self.tick to be one of three methods
            -self.clientTick turns on VShip networking
            -self.serverTick runs as server/VShip
            -self.passTick runs without networking - does nothing
        '''
        if self.engine.localOptions.networkingOptions.enableNetworking:
            self.commandQueue = deque()
            self.squelchQueue = deque()
            isServer = self.engine.localOptions.networkingOptions.server
            self.listener = Listener(self.ip, self.port, self.PacketSize, isServer)
            self.broadcaster = Broadcaster(self.ip, self.port, self.PacketSize, isServer)
            if self.engine.localOptions.networkingOptions.server:
                self.tick = self.serverTick
            else:
                self.tick = self.clientTick
        else:
            self.tick        = self.passTick

    def passTick(self, dtime):
        pass

    def serverTick(self, dtime):
        self.handleClientMessages(dtime)
        self.serve(dtime)
        #self.sendForceMoveInfo() # both client and server can move ents

    def clientTick(self, dtime):
        self.handleServerMessages(dtime)
        self.sendRequests()
        #self.sendForceMoveInfo() # both client and server can move ents

#------- End optimization trick-----------------------------

# ----------------------------------------------------------

    def loadLevel(self):
        if self.engine.localOptions.networkingOptions.enableNetworking:
            self.loadVShipMap()
            self.listener.start()
            self.broadcaster.start()


    def releaseLevel(self):
        if self.engine.localOptions.networkingOptions.enableNetworking:
            self.listener.stop()
            self.broadcaster.stop()


# ------------------- Server ----------------------
    def handleClientMessages(self, dtime):
        for msg in self.listener.getMessages():
            unpackedMsg = self.unpack(msg)
            #print "Handle Message: "
            #print str(unpackedMsg)
            if unpackedMsg.msgType == self.CommandMessage:
                #print 'propagating command'
                self.propagateCommand(unpackedMsg)
            elif unpackedMsg.msgType == self.RequestInfoMessage:
                self.sendShipsInfo(unpackedMsg)
            elif unpackedMsg.msgType == self.CreateShip:
                self.createShips(unpackedMsg)
            elif unpackedMsg.msgType == self.AbsoluteInfo:
                self.rawShipPosOrientation(unpackedMsg)
            elif unpackedMsg.msgType == self.SquelchCommand:
                pass
            else:
                print "Server: Unknown Message type, ignoring...", str(unpackedMsg)

    def serve(self, dtime):
        #self.header       = struct.Struct("=Biii")
        packedMessage = self.header.pack(self.StatusMessage, int(self.simTimeMilli()), self.engine.entMgr.nEnts, self.status.size)
        for id, ent in self.engine.entMgr.entMap.iteritems():
            #self.status       = struct.Struct("=i fff fff ff ff H")
            ds, dh = 0, 0
            if ent.UnitAI.state == ent.UnitAI.State.MANUAL_CONTROL:
                ds, dh = ent.ManualControl.desiredSpeed, ent.ManualControl.desiredHeading
            elif ent.UnitAI.state == ent.UnitAI.State.AI:
                ds, dh = ent.UnitAI.helmDesiredSpeed, ent.UnitAI.helmDesiredHeading
            elif ent.UnitAI.state == ent.UnitAI.State.STOP:
                ds, dh = 0, ent.UnitAI.helmDesiredHeading
            else:
                ds, dh = ent.desiredSpeed, ent.desiredHeading

            msg = self.status.pack(id, ent.pos.x, ent.pos.y, ent.pos.z, ent.velocity.x, ent.velocity.y, ent.velocity.z, ent.yaw, 0.0, ds, dh, 0)
            packedMessage += msg
        self.send(packedMessage)

    def propagateCommand(self, unpkdMsg):
        for data in unpkdMsg.data:
            #print "Propagating: ", str(data)
            if data.id in self.engine.entMgr.entMap.keys():
                ent = self.engine.entMgr.entMap[data.id]
                #print "Propagating Entity: ", str(ent), " Id: ", data.id
                ent.desiredHeading = data.dh
                ent.desiredSpeed   = data.ds
                ent.squad.SquadAI.commands = [command.NetSlave(self.engine)]
            else:
                print "Unknown id: %s, this is a BUG" % (data.id)


    def sendShipsInfo(self, unpkdMsg):
        msg = self.header.pack(self.InfoMessage, int(self.simTimeMilli()), len(self.engine.entMgr.entMap.keys()), self.info.size)
        for eid, ent in self.engine.entMgr.entMap.iteritems():
            msg += self.info.pack(eid, str(ent), ent.__class__.__name__, ent.maxSpeed, ent.maxSpeed/10.0, ent.length, ent.beam, ent.draft, ent.player.playerId, ent.player.side)
        self.prioritySend(msg)

    def createShips(self, unpkdMsg):
        pass

    def rawShipPosOrientation(self, unpkdMsg):
        '''Updates forced move pos and orientations
        '''
        for data in unpkdMsg.data:
            if data.id in self.engine.entMgr.entMap.keys():
                ent = self.engine.entMgr.entMap[data.id]
                ent.pos = vector3(data.pos[0], data.pos[1], data.pos[2])
                ent.yaw = data.yaw
                #ent.uiname = str(data.label)
        pass


#----Communicate with Server----------------------------

    def sendForceMoveInfo(self):
        if self.engine.selectionSystem.forceMovingEnts:
            self.forcingMove = True
            msg = self.header.pack(self.AbsoluteInfo, int(self.simTimeMilli()), len(self.engine.selectionSystem.forceMovingEnts), self.absoluteInfo.size)
            for ent in self.engine.selectionSystem.forceMovingEnts:
                if self.engine.localOptions.networkingOptions.vShipNet:
                    entid = self.VShipIdMap[str(ent)]
                else:
                    entid = ent.id
                msg += self.absoluteInfo.pack(entid, ent.pos.x, ent.pos.y, ent.pos.z, ent.velocity.x, ent.velocity.y, ent.velocity.z, ent.yaw, '')
            self.send(msg)
        else:
            self.forcingMove = False


#----Communicate with Server----------------------------

    def sendRequests(self):
        self.sendUnknownEntQueries()
        self.combineCommandsIntoNetMessage()
        self.combineSquelchesIntoNetMessage()
        self.sendForceMoveInfo() #I'm sending this in clientTick for symmetry with server


    def moveAbsolute(self):
        pass


    def sendUnknownEntQueries(self):
        for id in self.unknowns.keys():
            self.prioritySend(self.packNewEntQuery([id]))
        
    def packNewEntQuery(self, msg):
        packedMsg = self.header.pack(self.RequestInfoMessage , int(self.simTimeMilli()), len(msg), self.int.size)
        for i in msg:
            packedMsg += self.int.pack(i)
        return packedMsg

    def prioritySend(self, packedMsg): # from netAspect and from createEnts here
        self.broadcaster.putPriorityMessage(packedMsg)

    def addCommand(self, packedCommand): # from netAspect
        #print "Adding Command: ",  VCommand(self.command.unpack_from(packedCommand, 0))
        self.commandQueue.appendleft(packedCommand)

    def addSquelch(self, packedCommand): # from netAspect
        self.squelchQueue.appendleft(packedCommand)

#---------------not needed?--------------------------------------------------------------------------------
    def addForcedMove(self, packedCommand):
        self.forcedMoveQueue.appendleft(packedCommand)

    def combineForcedMovesIntoNetMessage(self):
        if self.forcedMoveQueue:
            packedMsg = self.header.pack(self.AbsoluteInfo, int(self.simTimeMilli()), 1, self.absoluteInfo.size)
            while self.forcedMoveQueue:
                packedMsg += self.forcedMoveQueue.pop()
            self.send(packedMsg)
#---------------not needed?--------------------------------------------------------------------------------
    #----these two \/\/\/\/ look very similar--------
    def combineSquelchesIntoNetMessage(self):
        if self.squelchQueue:
            packedMsg = self.header.pack(self.SquelchCommand, int(self.simTimeMilli()), 1, self.squelch.size)
            while self.squelchQueue:
                packedMsg += self.squelchQueue.pop()
            self.send(packedMsg)
    #----these two \/\/\/\/ look very similar--------
    def combineCommandsIntoNetMessage(self): # every tick
        if self.commandQueue:
            packedMsg = self.header.pack(self.CommandMessage , int(self.simTimeMilli()), len(self.commandQueue), self.command.size)
            while self.commandQueue:
                packedMsg += self.commandQueue.pop()
            #print "Sending: "
            #print str(self.unpack(packedMsg))
            self.send(packedMsg)

    def send(self, packedMsg):
        self.broadcaster.putMessage(packedMsg)
#------------------------------------------------------------

    def loadVShipMap(self): # after all ents have been registered

        self.entNameClassMap = {}
        for entType in self.engine.entMgr.types:
            self.entNameClassMap[entType.__name__] = entType
        print str(self.entNameClassMap.keys())

#---------Communicate with listener------------------

    def handleServerMessages(self, dtime):
        for msg in self.listener.getMessages():
            unpackedMsg = self.unpack(msg)
            if unpackedMsg.msgType == self.StatusMessage:
                self.updateStatus(unpackedMsg)
            elif unpackedMsg.msgType == self.InfoMessage:
                self.createEnts(unpackedMsg)
            elif unpackedMsg.msgType == self.SquelchCommand:
                #print "Squelching: ", str(unpackedMsg)
                self.squelchEnts(unpackedMsg)
            elif unpackedMsg.msgType == self.AbsoluteInfo:
                pass
            else:
                pass
                print "Unknown Message type, ignoring...", str(unpackedMsg)

#------------------------------------------------------
    def squelchEnts(self, status):
        for d in status.data:
            try: 
                ent = self.netEnts[d.id]
                #print "Squelching: ", str(ent)
                netAsp = ent.findAspect(NetAspect)
                netAsp.squelch()
            except KeyError:
                print "Unknown ent with id: ", d.id

    def updateStatus(self, status):
        for d in status.data:
            if d.id in self.netEnts.keys():
                ent = self.netEnts[d.id]
                ent.updateQueue.appendleft(d)
            else:
                self.unknowns[d.id] = d

    def createEnts(self, infoMsg):
        for info in infoMsg.data:
            if info.id in self.unknowns.keys():
                if info.type in self.entNameClassMap:
                    entityType = self.entNameClassMap[info.type]
                else:
                    print info.type, " not found"
                    entityType = boat.DDG51

                handle = self.engine.entMgr.createHandle()
                
                ent = self.engine.entMgr.createEntity(handle, entityType, additionalAspects=[NetAspect], playerInfo = Player(info.side, info.playerId))
                global gMoveCameraToEntPos
                gMoveCameraToEntPos = ent

                ent.uiname = info.label
                print info.label, info.type
                # create VShip or other net aspect here
                aspect = ent.findAspect(NetAspect)
                status = self.unknowns[info.id]

                aspect.initNetworking(info.id, status)# sets initial speed, yaw, ds, dh, ...
                ent.dump() # print on console

                del self.unknowns[info.id]
                self.netEnts[info.id] = ent
                
        
    def unpack(self, msg):
        mHeader = self.header.unpack_from(msg)
        unpackedMsg = VMessageHeader(mHeader)
        #print str(unpackedMsg)
        #print unpackedMsg.time, time.time()
        if unpackedMsg.msgType == self.InfoMessage:
            self.extractData(msg, unpackedMsg,  VInfo, self.info)
        elif unpackedMsg.msgType == self.StatusMessage:
            self.extractData(msg, unpackedMsg, VStatus, self.status)
        elif unpackedMsg.msgType == self.SquelchCommand:
            self.extractData(msg, unpackedMsg, VSquelchCommand, self.squelch)
        elif unpackedMsg.msgType == self.RequestInfoMessage:
            #pass # If this was a server send newly created ent info
            self.extractData(msg, unpackedMsg, VInt, self.int)
        elif unpackedMsg.msgType == self.CommandMessage:
            self.extractData(msg, unpackedMsg, VCommand, self.command)
            pass # only the server responds to the rest of the cases
        elif unpackedMsg.msgType == self.RequestShipStatus:
            self.extractData(msg, unpackedMsg, VInt, self.int)
            pass
        elif unpackedMsg.msgType == self.CreateShip:
            self.extractData(msg, unpackedMsg, VCreateShip, self.createShip)
            pass 
        elif unpackedMsg.msgType == self.AbsoluteInfo:
            self.extractData(msg, unpackedMsg, VSetAbsoluteInfo, self.absoluteInfo)
            pass 
        else:
            print "UNPACK: Unknown message type", str(mHeader)
        return unpackedMsg
            
            
    def extractData(self, msg, unpackedMsg, type, struct):
        offset = self.header.size
        for i in range (0, unpackedMsg.entCount):
            x = type(struct.unpack_from(msg, offset))
            offset += struct.size
            unpackedMsg.data.append(x)
            x.time = unpackedMsg.time
#-----------------------------------------------------------------------------
class VMessageHeader:
    def __init__(self, m):
        self.msgType  = m[0]
        self.time     = m[1]
        self.entCount = m[2]
        self.entSize  = m[3]
        self.data     = []

    def __str__(self):
        s = "-------------------Message: " + str(self.msgType) + "  nEntities: " + str(self.entCount) + "\n"
        for d in self.data:
            s += str(d) + "\n"
        return s + "-----------------"

    
class VStatus:
    def __init__(self, d):
        self.id = d[0]
        self.pos = (d[1],d[2],d[3])
        self.vel = (d[4],d[5],d[6])
        self.yaw = d[7]
        self.rSpeed = d[8]
        self.ds = d[9]
        self.dh = d[10]
        self.time  = 0
        
    def __str__(self):
        return "Id: " + str(self.id) + "  Pos: " + str(self.pos) + "  Vel: " + str(self.vel) + "  Yaw: " + str(self.yaw) +  " ds: " + str(self.ds) +  " dh: " + str(self.dh)

class VInt:
    def __init__(self, d):
        self.val = d[0]

    def __str__(self):
        return str(self.val)

class VInfo:
    def __init__(self, d):
        self.id = d[0]
        self.label = d[1].strip("\0")
        self.type = d[2].strip("\0")
        self.maxSpeed = d[3]
        self.maxSpeedReverse = d[4]
        self.length = d[5]
        self.beam = d[6]
        self.draft = d[7]
        self.playerId = d[8]
        self.side     = d[9]
        self.time  = 0
        
    def __str__(self):
        return "Id: " + str(self.id) + "  " + self.label + "  (" + self.type + ")  MaxSpeed: " + str(self.maxSpeed) + " Player: " + self.playerId + " side: " + self.side


class VSetAbsoluteInfo:
    def __init__(self, d):

        self.id = d[0]
        self.pos = (d[1], d[2], d[3])
        #if gPosOffset == None:
            #gPosOffset = self.pos
        #self.pos = (self.pos[0] - gPosOffset[0], self.pos[1] - gPosOffset[1], self.pos[2] - gPosOffset[2])
        self.vel = (d[4], d[5], d[6])
        self.yaw = d[7]
        self.label = d[8].strip('\0') #optional set label
        self.time = 0
        
    def __str__(self):
        return "Id: " + str(self.id) + "  " + self.label + " pos:  (" + str(self.pos) + ")  vel: " + str(self.vel) + " yaw: " + str(self.yaw)


class VSquelchCommand:
    def __init__(self, data):
        self.id = data[0]
        
    def __str__(self):
        return str(self.id)

class VCommand:
    def __init__(self, data):
        self.id = data[0]
        self.dh = data[1]
        self.ds = data[2]
        
    def __str__(self):
        return str(self.id) + "     " + str(self.dh)  + "     " + str(self.ds)

class VCreateShip:
    def __init__(self, data):
        self.label = data[0]
        self.type = data[1];
        self.pos = (data[2], data[3], data[4])
        self.yaw = data[5]
                          
    def __str__(self):
        return str(self.label) + "     " + str(self.type) + "     " + str(self.pos) + "     " + str(self.yaw)

                                 
