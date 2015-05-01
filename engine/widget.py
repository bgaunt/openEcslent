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

import pdb;

import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

from units import idealScreenPos, degrees
from mgr import EngineObject, Mgr
from vector import vector2, point2
from misc import EasyLog1
from inputSystem import MouseEvent, MouseButton, Modifier, InputEvent

import boat

class UIDefaults:
    POS = (0, 0)
    WIDTH = 100
    HEIGHT = 20

    PANEL_SIZE = (100, 20)
    PANEL_MATERIAL = "ECSLENT/navy/material/shipInfo/overlay"
    LINE_SEP_MATERIAL  = "ECSLENT/line"

    LABEL_SIZE = (100, 20)
    LABEL_X_OFFSET = 5
    LABEL_Y_OFFSET = 5
    LABEL_TEXT_COLOR = (1.0, 1.0, 0.7)

    BUTTON_SIZE = (50, 20)
    BUTTON_OFF_TEXT_COLOR = (1.0, 1.0, 0.0)
    BUTTON_ON_TEXT_COLOR  = (0.0, 0.0, 0.5)

    MENU_ITEM_SIZE = (100, 20)
    MENU_DEFAULT_TEXT_COLOR = (1.0, 1.0, 0.0)
    MENU_SELECTED_TEXT_COLOR = (0.0, 0.0, 0.5)
    MENU_MATERIAL = "ECSLENT/navy/material/rmenu"

class Widget(EngineObject):
    """Top level UI object
    """
    def __init__(self, engine, parent = None, pos=None, size=None):
        if pos is None: #if we default parameter these all objects will share a common instantiation which WILL cause nightmares
            pos = point2(0,0)
        if size is None: #if we default parameter these all objects will share a common instantiation which WILL cause nightmares
            size = point2(100,13)

        EngineObject.__init__(self, engine)
        assert engine is not None
        if type(pos) is tuple:
            pos = point2(*pos)
        if type(size) is tuple:
            size = point2(*size)

        self._pos = pos
        self._size = size
        self.engine = engine
        self.parent = parent

    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, value):
        self._pos = value
        self.posChanged()
    def posChanged(self):
        pass

    @property
    def size(self):
        return self._size
    @size.setter
    def size(self, value):
        self._size = value
        self.sizeChanged()
    def sizeChanged(self):
        pass

    @property
    def width(self):
        return self._size.x
    @width.setter
    def width(self, val):
        self.size = point2(val, self.size.y)

    @property
    def height(self):
        return self._size.y
    @height.setter
    def height(self, val):
        self.size = point2(self.size.x, val)
           

    @property
    def screenPos(self):
        if self.parent:
            return self.parent.screenPos + self.pos
        else:
            return self.pos

    def cursorInMe(self, mx, my):
        ax, ay = (self.screenPos.x, self.screenPos.y)
        return ((mx >= ax) and (mx <= ax + self.width) and (my >= ay) and (my <= ay + self.height))



class UIOverlay(Widget):
    """
    All UI elements live within this overlay.
    """
    def __init__(self, engine):
        Widget.__init__(self, engine)
        self.overlayManager = ogre.OverlayManager.getSingleton()
        self.pid         = "UIPanel" + str(engine.widgetMgr.getNextId())
        self.panel       = self.overlayManager.createOverlayElement("Panel", self.pid)
        self.panel.setMetricsMode(ogre.GMM_PIXELS)#RELATIVE_ASPECT_ADJUSTED)
        self.panel.setPosition(0, 0)
        width  = self.engine.gfxSystem.renderWindow.getWidth()
        height = self.engine.gfxSystem.renderWindow.getHeight() # VERY IMPORTANT or rayscene queries fail
        self.panel.setDimensions(width, height)        
        self.panel.setMaterialName("ECSLENT/UI")
        self.panel.show()

        self.id = "MainUI"
        self.overlayName = "UIOverlay" + str(engine.widgetMgr.getNextId())
        self.overlay     = self.overlayManager.create(self.overlayName)
        self.overlay.add2D(self.panel)
        self.overlay.show()
        self.panel.show()

    def show(self):
        self.overlay.show()
        self.panel.show()

    def hide(self):
        self.panel.hide()
        self.overlay.hide()

    def render(self):
        pass

    def tick(self, dtime):
        pass
        



        
class Panel(Widget):
    """
    """
    class Placement:
        Below = 0
        Right = 1

    def __init__(self, engine, parent = None, name = "ex.Panel", pos = (0.0, 0.0), size = UIDefaults.PANEL_SIZE, material = None):
        Widget.__init__(self, engine, parent = parent, pos = pos, size = size)
        self.overlayManager = ogre.OverlayManager.getSingleton()

        self.pid         = name + str(engine.widgetMgr.getNextId())
        self.panel       = self.overlayManager.createOverlayElement("Panel", self.pid)
        self.panel.setMetricsMode(ogre.GMM_PIXELS)#RELATIVE_ASPECT_ADJUSTED)
        self.panel.setPosition(self.pos.x, self.pos.y)
        #self.panel.setDimensions(self.width, self.height)
        self.height = 0 # otherwise, the panel has extra height when using as a parent for labels and other widgets.
        self.panel.setDimensions(self.width, self.height)
        if material:
            self.panel.setMaterialName(material)

        self.panel.show()        

        if not self.parent:
            self.id = name
            self.overlayName = name + str(engine.widgetMgr.getNextId())
            self.overlay     = self.overlayManager.create(self.overlayName)
            self.overlay.add2D(self.panel)
            self.overlay.show()
            #print "---------> Created overlay and added panel to overlay: ",  self.overlayName

        self.panel.show()

        self.belowPos = point2(0,0)
        self.rightPos = point2(0,0)
        self.xgap = 0
        self.ygap = 0
        self._items = []

        self.lheight = 1
        self._linePanels = [] # used by menu items
        self.addSep(0)
        pass

    def linePanel(self):
        lid = self.pid + "line/" + str(self.engine.widgetMgr.getNextId())
        lp = self.overlayManager.createOverlayElement("Panel", lid)
        lp.setMetricsMode(ogre.GMM_PIXELS)#RELATIVE_ASPECT_ADJUSTED)
        lp.setPosition(0, 0)
        lp.setDimensions(self.width, self.lheight)
        lp.setMaterialName("ECSLENT/line")
        lp.show()
        return lp
 
    def addSep(self, y):
        lp = self.linePanel()
        self._linePanels.append(lp)
        lp.setPosition(0, y) # lineSep, 0, 0
        self.panel.addChild(lp)

    def adjustSeps(self):
        '''
        QUEST: What is this? - cmiles
        '''
        for lp in self._linePanels:
            lp.setDimensions(self.width, self.lheight)

    def render(self):
        for item in self._items:
            item.render()

    def show(self):
        if not self.parent:
            self.overlay.show()
        self.panel.show()
        for item in self._items:
            item.show()

    def hide(self):
        for item in self._items:
            item.hide()
        self.panel.hide()
        if not self.parent:
            self.overlay.hide()

    def posChanged(self):
        self.panel.setPosition(self.pos.x, self.pos.y)
        for item in self._items:
            item.posChanged()

    def addItem(self, item, func = None, placement = Placement.Below):
        self._items.append(item)
        if(self.width < item.width):
            self.width = item.width
            self.adjustSeps()

        #pdb.set_trace()
        if placement == Panel.Placement.Below:
            item.pos = self.belowPos
            self.rightPos = self.belowPos + point2(item.width + self.xgap, 0)
            self.belowPos = point2(0, self.belowPos.y + item.height + self.ygap)

        elif placement == Panel.Placement.Right:
            item.pos = self.rightPos
            self.rightPos = self.rightPos + point2(item.width + self.xgap, 0)

        if self.rightPos.x > self.width:
            self.width = self.rightPos.x

        if self.belowPos.y > self.height:
            self.height = self.belowPos.y
        #self.height += item.height

        #print 'Panel.addItem', self, item, placement, item.pos, self.belowPos, self.rightPos

        self.panel.addChild(item.getOverlayElementToAdd())

        self.panel.setDimensions(self.width, self.height)
        self.addSep(self.height)

    def deleteItem(self, item):
        item.hide()
        self._item.remove(element)

    def getItems(self):
        return self._items

    def getOverlayElementToAdd(self):
        return self.panel


class Label(Widget):
    '''
    '''
    def __init__(self, engine, parent = None, caption = "Ex.Label", color = (1.0, 1.0, 0.7), size = UIDefaults.LABEL_SIZE, pos = (0, 0)):
        '''
        '''
        Widget.__init__(self, engine, parent = parent, pos = pos, size = size)
        self.overlayManager =  ogre.OverlayManager.getSingleton()
        self.caption = caption
        self.color   = color

        self.xOffset = 5
        self.yOffset = 2

        self.id = "ECSLENT/Label/" + str(self) + "/" + caption  + "/" + str(engine.widgetMgr.getNextId())
        self.textArea = self.overlayManager.createOverlayElement("TextArea", self.id)
        self.textArea.setMetricsMode(ogre.GMM_PIXELS)
        self.textArea.setCaption(caption)
        self.textArea.setPosition(self.pos.x  + self.xOffset, self.pos.y + self.yOffset)
        self.textArea.setDimensions(self.width, self.height)
        self.textArea.setFontName("BlueHighway")
        self.textArea.setCharHeight(self.height)
        self.textArea.setColour(self.color)
        self.textArea.show()

        #textArea.setColourTop((1.0, 1.0, 0.7))
        #textArea.setColourBottom((1.0, 1.0, 0.7))

    def render(self):
        pass

    def tick(self, dtime):
        pass
#-------------------------------------------------------------------
    def getTextArea(self):
        return self.textArea
#-------------------------------------------------------------------
    def getOverlayElementToAdd(self):
        return self.textArea
#-------------------------------------------------------------------
    def show(self):
        self.textArea.show()
#-------------------------------------------------------------------
    def hide(self):
        self.textArea.hide()
#-------------------------------------------------------------------
    def setCaption(self, caption):
        self.caption = caption
        self.textArea.setCaption(self.caption)
#-------------------------------------------------------------------
    def getCaption(self):
        return self.caption

    def posChanged(self):
        #print 'Label.posChanged', self.pos, self.screenPos
        self.textArea.setPosition(self.pos.x + self.xOffset, self.pos.y + self.yOffset)

    def sizeChanged(self):
        #print 'Label.sizeChanged', self.size
        self.textArea.setDimensions(self.width, self.height)

    def setCharHeight(self, height):
        self.height = height
        self.setCharHeight(height)

class LabelPair(Panel):
    """
    About 90% of the time we use labels in pairs
    the first is a fixed piece of text describing what the second is
    the second being the actual data we are representing - which varies over time
    """
    def __init__(self, engine, parent, label1Text, label2Text='', columnWidths=(100,200), columnHeightPixels = UIDefaults.PANEL_SIZE[1]):
        Panel.__init__(self, engine, parent=parent, pos=(0,0), size=(columnWidths[0] + columnWidths[1], columnHeightPixels))
        self.label1 = Label(engine, parent=self, caption=label1Text, pos=(0,0), size=(columnWidths[0], columnHeightPixels))
        self.addItem(self.label1, placement=Panel.Placement.Below)
        self.label2 = Label(engine, parent=self, caption=label2Text, pos=(columnWidths[0],0), size=(columnWidths[1], columnHeightPixels))
        self.addItem(self.label2, placement=Panel.Placement.Right)

    @property
    def leftCaption(self):
        self.label1.caption
    @leftCaption.setter
    def leftCaption(self, caption):
        self.label1.setCaption(caption)

    @property
    def rightCaption(self):
        self.label2.caption
    @leftCaption.setter
    def rightCaption(self, caption):
        self.label2.setCaption(caption)


    @property
    def caption(self):
        return self.caption
    @caption.setter
    def caption(self, caption):
        self.label2.setCaption(caption)

class ButtonState:
    ON  = 0
    OFF = 1

class Button(Label):
    """a button that can be clicked on to perform actions
    """
    def __init__(self, engine, parent, name = "ex.Button", pos = (0, 0), size = (50, 20), func = None):
        Label.__init__(self, engine, parent = parent, caption = name, pos  = pos, size = size)
        self.state = ButtonState.OFF
        self.mouse = engine.inputSystem.mouse
        self.func = func
        engine.inputSystem.registerMouseHandler(MouseEvent.MOUSE_PRESSED, MouseButton.LEFT, self.handleMousePress)
        pass

    def tick(self, dtime):
        pass

    def render(self):
        pass

    def handleMousePress(self, ms):
        if self.cursorInMe(ms.X.abs, ms.Y.abs):        
            self.state = 1 - self.state
            if self.state == ButtonState.OFF:
                self.textArea.setColour((1.0, 1.0, 0.0))
            else:
                self.textArea.setColour((0.0, 0.0, 0.5))

            if self.func:
                self.func(ms, self.caption)

#-----------------------------------------------------------------------------------------------------------------
class MenuItem(Panel):
    '''A panel and a label
    '''

    def __init__(self, engine, parent = None, name = "ex.MenuItem", pos = (0, 0), size = (100, 15), func = None, material="ECSLENT/navy/material/rmenu"):
        Panel.__init__(self, engine, parent = parent, name = name+"Panel", pos = pos, size = size, material = material)
        self.label = Label(engine, parent = None, caption = name, pos = (0, 0), size = size)
        self.height = 15
        self.label.show()
        self.panel.addChild(self.label.textArea)
        self.name = name
        self.func = func
        self.isSelected = False

        self._subMenu = Panel(engine, parent = self, pos = (0, 0), size = (0, 0), material = material)
        self._subMenu.pos = point2(self.width + self.xgap, 0)
        self.panel.addChild(self._subMenu.panel)
        self._subMenu.hide()

        self.registerEventHandlers()
        self.isActive = False

    def registerEventHandlers(self):
        #print "------------------------------------------------------------------MenuItem registering Event Handlers"
        #self.engine.inputSystem.registerMouseHandler(MouseEvent.MOUSE_MOVED, MouseButton.RIGHT, self.handleRightMouseDrag)
        self.engine.inputSystem.registerMouseHandler(MouseEvent.MOUSE_RELEASED, MouseButton.RIGHT, self.fire)

    def addItem(self, mi):
        self._subMenu.addItem(mi)

    def clearSelection(self):
        self.isSelected = False;
        for it in self._subMenu._items:
            it.clearSelection()

    def tick(self, dtime):
        pass

    def hideAllOther(self, mi):
        for item in self._subMenu._items:
            if mi != item:
                item.isSelected = False
                item._subMenu.hide()

    def render(self):
        ms = self.engine.inputSystem.ms

        if not self.isActive:
            if ms.buttonDown(MouseButton.RIGHT) and (self.engine.inputSystem.keyboard.isKeyDown(OIS.KC_LCONTROL) or self.engine.inputSystem.keyboard.isKeyDown(OIS.KC_RCONTROL)):
                self.show()
                self.isActive = True
        else:
            if not ms.buttonDown(MouseButton.RIGHT):
                self.hide()
                self._subMenu.hide()
                self.isActive = False

        if self.isActive:
            # I have a parent
            if self.inMe(): #self.cursorInMe(ms.X.abs, ms.Y.abs - self.height):
                self.isSelected = True
                self.parent.hideAllOther(self)
                self.label.textArea.setColour(UIDefaults.MENU_SELECTED_TEXT_COLOR)
                self.show()
                self._subMenu.show()
            else:
                self.label.textArea.setColour(UIDefaults.MENU_DEFAULT_TEXT_COLOR)
                self._subMenu.hide()

            for item in self._subMenu._items:
                item.render()

    def inMe(self):
        ms = self.engine.inputSystem.ms
        if isinstance(self.parent, TopMenu):
            return self.cursorInMe(ms.X.abs, ms.Y.abs - self.parent.height)
        else:
            return self.cursorInMe(ms.X.abs - self.parent.width, ms.Y.abs - self.parent.height)

    def fire(self, ms):
        if self.isLeaf() and self.isSelected: 
            #print "Firing: ", self.name
            self.func(self, ms)
 
    def isLeaf(self):
        return not self._subMenu._items

    
class TopMenu(MenuItem):
    '''A top level menu is the root of a hierarchical menu system
    '''
    def __init__(self, engine, name = "TopMenuItem", pos = (0, 0), size = (100, 15), func = None, material="ECSLENT/navy/material/rmenu"):
        MenuItem.__init__(self, engine, parent = None, name = name, pos = pos, size = size, func = func, material = material)
        # these should be generalized to respond to events
        self._subMenu.pos = point2(0, self.height + self.ygap + self.lheight)
        self.registerEventHandlers()
        self.hide()
        self.isActive = False

    def registerEventHandlers(self):
        #print "-----------------------------------------------------------------------TopItem registering Event Handlers"
        self.engine.inputSystem.registerMouseHandler(MouseEvent.MOUSE_PRESSED, MouseButton.RIGHT, self.handleRightMousePress)
        self.engine.inputSystem.registerMouseHandler(MouseEvent.MOUSE_RELEASED, MouseButton.RIGHT, self.hideAll)

    def handleRightMousePress(self, ms):
        self.pos = point2(ms.X.abs, ms.Y.abs)
        self.clearSelection() # clear selection
 
    def hideAll(self, ms):
        self.hide()
        self._subMenu.hide()

    def render(self):
        ms = self.engine.inputSystem.ms

        if not self.isActive:
            if ms.buttonDown(MouseButton.RIGHT) and self.engine.inputSystem.mouseDownModifiers[MouseButton.RIGHT][Modifier.CTRL]:
            #(self.engine.inputSystem.keyboard.isKeyDown(OIS.KC_LCONTROL) or self.engine.inputSystem.keyboard.isKeyDown(OIS.KC_RCONTROL)):
                self.show()
                self.isActive = True
        else:
            if not ms.buttonDown(MouseButton.RIGHT):
                self.hide()
                self._subMenu.hide()
                self.isActive = False

        if self.isActive:
            self.isSelected = False
            self.show()
            self._subMenu.show()
#
            for item in self._subMenu._items:
                item.render()

    def tick(self, dtime):
        pass

#-----------------------------------------------------------------------------------------------------------------
def printClick(item, ms):
    print "Clicked: %s (%4i, %4i)" % (item.name, ms.X.abs, ms.Y.abs)

class DebugButtonWidget(Panel):
    ''' Displays a Debug button
    '''
    def __init__(self, engine, name = "Debug", pos = (1, 150), size = (70, 20), func = printClick):
        Panel.__init__(self, engine, name = name, pos = pos, size = size, material = "ECSLENT/navy/material/button")
        self.debugButton = Button(engine, self, name = name, pos = (0, 0), size = size, func = func)
        self.addItem(self.debugButton)

    def tick(self, dtime):
        pass

    def render(self):
        self.debugButton.render()
        

class InitMenuButton(Panel):
    ''' Displays an InitMenu button
    '''
    def __init__(self, engine, name = "Debug", pos = (1, 150), size = (70, 20), func = printClick):
        Panel.__init__(self, engine, name = name, pos = pos, size = size, material = "ECSLENT/navy/material/button")
        self.button = Button(engine, self, name = name, pos = (0, 0), size = size, func = func)
        self.addItem(self.button)

    def tick(self, dtime):
        pass

    def render(self):
        self.button.render()
        

class FramerateWidget(Panel):
    '''Displays and updates framerate
    '''
    def __init__(self, engine, name = "Framerate: ", pos = (1, 1), size = (100, 13)):
        Panel.__init__(self, engine, name = name, pos = pos, size = size)
        self.label = Label(engine, caption = name, pos = (0,0), size = size)
        self.addItem(self.label)
        self.show()
        self.label.show()
        
    def tick(self, dtime):
        stats = self.engine.gfxSystem.renderWindow.getStatistics()
        self.label.setCaption("Framerate: %5i" % stats.avgFPS)

    def render(self):
        #print "panel.show: ", self.posx, ", ", self.posy
        #self.show()
        #self.label.show()
        pass

class CursorWidget(Panel):
    '''Displays and updates framerate
    '''
    def __init__(self, engine, name = "Cursor", pos = (5, 5), size = (8, 8), material = "ECSLENT/cursor/yellow"):
        Panel.__init__(self, engine, name = name, pos = pos, size = size, material = material)
        engine.inputSystem.registerMouseHandler(MouseEvent.MOUSE_MOVED, MouseButton.RIGHT, self.handleMouseMove)
        self.show()

    def handleMouseMove(self, ms):
        self.setPosition(ms.X.abs, ms.Y.abs)

    def tick(self, dtime):
        pass

    def render(self):
        pass

class GameInfoWidget(Panel):
    def __init__(self, engine, name = "ShipInfo", pos = (580, 20), size = (100, 100), material = "ECSLENT/navy/material/shipInfo/overlay"):
        Panel.__init__(self, engine,  pos = pos, size = size, material = material)
        #self.clock    = Label(engine, caption = "Clock: ", pos = (0,0), size = (100, 13))
        self.clock = LabelPair(engine, self, 'Clock:', columnWidths=(100,200))
        self.addItem(self.clock)

        self.timeScale = LabelPair(engine, self, 'Time Scale:', columnWidths=(100,200))
        self.addItem(self.timeScale)

    def tick(self, dtime):
        self.clock.caption = '%6.2f' % self.engine.gameTime
        self.timeScale.caption = '%6.2f' % self.engine.timeScale


class ShipCommands(Panel):
    def __init__(self, engine, name = "ShipCommands", material = "ECSLENT/navy/material/shipInfo/overlay"):
        negativePosX = 250
        negativePosY = 140
        width  = engine.gfxSystem.renderWindow.getWidth()
        height = engine.gfxSystem.renderWindow.getHeight() 
        heightStretchFactor = height/768.0
        widthStretchFactor  = width/1024.0
        posX = int(negativePosX * widthStretchFactor)
        posY = int(negativePosY * heightStretchFactor)
        colWidth = int(80 * widthStretchFactor)
        print width, widthStretchFactor, height, heightStretchFactor
     
        Panel.__init__(self, engine,  pos = (width  - posX, height - posY), size = (100, 20), material = material)

        columnWidths = (colWidth, colWidth*2)
        colHeight = int(22 * heightStretchFactor)

        self.maxCommandsDisplayed = 5
        self.widgetName         = Label(engine, self, 'Current Command Sequence', size = (240, colHeight))
        self.addItem(self.widgetName)
        self.commandsInfo = []
        for i in range (self.maxCommandsDisplayed):
            pair = LabelPair(engine, self, '', columnWidths=columnWidths, columnHeightPixels = colHeight)
            self.commandsInfo.append(pair)
            self.addItem(pair)
        self.show()

    def updateLabels(self, ent):
        import command
        import desiredState

        for i in range (self.maxCommandsDisplayed):
            pair = self.commandsInfo[i]
            pair.leftCaption = ''
            pair.rightCaption = ''

        i = 0
        for command in ent.UnitAI.commands:
            if i < self.maxCommandsDisplayed:
                order, details = command.uiStr().split(':', 1)
                pair = self.commandsInfo[i]
                pair.leftCaption = order
                loc = details.strip()
                l   = loc.find('(')
                pair.rightCaption = loc[l:]
                i += 1

                
    def tick(self, dtime):
        ent = self.engine.selectionSystem.primaryEnt
        if ent:
            self.updateLabels(ent)

    def render(self):
        pass



class ShipInfoWidget(Panel):

    def __init__(self, engine, name = "ShipInfo", pos = (1, 16), size = (100, 20), material = "ECSLENT/navy/material/shipInfo/overlay"):

        width  = engine.gfxSystem.renderWindow.getWidth()
        height = engine.gfxSystem.renderWindow.getHeight() 
        sevenSixEightPosY = 140
        heightStretchFactor = height/768.0
        widthStretchFactor  = width/1024.0
        posY = int(sevenSixEightPosY * heightStretchFactor)
        colWidth = int(118 * widthStretchFactor)
        #print width, widthStretchFactor, height, heightStretchFactor
        
        Panel.__init__(self, engine,  pos = (int(18 * widthStretchFactor), height - posY), size = size, material = material)
        columnWidths = (colWidth, colWidth)

        colHeight = int(22 * heightStretchFactor)

        self.shipName           = LabelPair(engine, self, '[Player:,Side:]', columnWidths=columnWidths, columnHeightPixels = colHeight)
        self.shipSpeed          = LabelPair(engine, self, 'Speed[kts]:', columnWidths=columnWidths, columnHeightPixels = colHeight)
        self.shipHeading        = LabelPair(engine, self, 'Heading:', columnWidths=columnWidths, columnHeightPixels = colHeight)
        self.shipPos            = LabelPair(engine, self, 'Pos:', columnWidths=columnWidths, columnHeightPixels = colHeight)
        self.timeToTarget       = LabelPair(engine, self, 'TimeToTarget:', columnWidths=columnWidths, columnHeightPixels = colHeight)
        self.distanceToTarget   = LabelPair(engine, self, 'DistToTarget:', columnWidths=columnWidths, columnHeightPixels = colHeight)

        self.addItem(self.shipName)
        self.addItem(self.shipSpeed)
        self.addItem(self.shipHeading)
        self.addItem(self.shipPos)
        self.addItem(self.timeToTarget)
        self.addItem(self.distanceToTarget)
        self.show()

    def updateLabels(self, ent):
        from units import toKnots
        from units import toDegrees
        import command
        import desiredState
        self.shipName.caption = str(ent)
        if ent.player:
            self.shipName.leftCaption   = '[Player:%1i, Side:%1i]' % (ent.player.playerId, ent.player.side)
        self.shipPos.caption = '(%-3i, %3i)' % (ent.pos.x, ent.pos.z)
        self.shipSpeed.caption = '%-5.2f' % toKnots(ent.speed)
        self.shipHeading.caption = '%-5.2f' % toDegrees(ent.yaw) #import from units.posy

        if ent.UnitAI.command:
            if type(ent.UnitAI.command) == command.MoveTo:
                if ent.UnitAI.destination:
                    dtot = (ent.UnitAI.destination - ent.pos).length()
                    self.distanceToTarget.caption = '%-7.0f'% dtot
                    if ent.speed > 0:
                        self.timeToTarget.caption = '%-5.0f'% (dtot/ent.speed)

    def tick(self, dtime):
        ent = self.engine.selectionSystem.primaryEnt
        if ent:
            self.updateLabels(ent)

    def render(self):
        pass
        
class ShipMouseOverInfoWidget(ShipInfoWidget):
    def __init__(self, engine, name = "MouseOverInfo", pos = (1, 16), size = (10, 10), material = "ECSLENT/navy/material/shipInfo/overlay"):
        ShipInfoWidget.__init__(self, engine,  name = name, pos = pos, size = size, material = material)

    def tick(self, dtime):
        ent = self.engine.inputSystem.entUnderMouse
        if ent:
            ms = self.engine.inputSystem.mouse.getMouseState()
            self.pos = point2(ms.X.abs + 20 , ms.Y.abs + 20)
            self.show()
            self.updateLabels(ent)
        else:
            self.hide()

class F1HelpWidget(Panel):
    def __init__(self, engine, name = "Help", pos = (730, 40), size = (540, 352), material = "ECSLENT/navy/material/f1Overlay"):
        Panel.__init__(self, engine,  pos = pos, size = size, material = material)        
        self.on = False

        columnWidths = (180, 360)
        self.help                        = LabelPair(engine, self, 'Help', columnWidths=columnWidths, columnHeightPixels = 18)
        self.help.caption                = 'Intelligent Aggressor Key Bindings'
        self.addItem(self.help)

        self.blank1                      = LabelPair(engine, self, '', columnWidths=columnWidths, columnHeightPixels = 16)
        self.addItem(self.blank1)

        self.select                      = LabelPair(engine, self, 'Select ents', columnWidths=columnWidths, columnHeightPixels = 16)
        self.select.caption              = 'Left mouse button click / drag'
        self.addItem(self.select)
        self.move                        = LabelPair(engine, self, 'Move to location', columnWidths=columnWidths, columnHeightPixels = 16)
        self.move.caption                = 'Right mouse click'
        self.addItem(self.move)
        self.maintain                    = LabelPair(engine, self, 'Maintain', columnWidths=columnWidths, columnHeightPixels = 16)
        self.maintain.caption            = 'Drag right mouse button from target to relative location'
        self.addItem(self.maintain)
        self.ram                         = LabelPair(engine, self, 'Ram ent', columnWidths=columnWidths, columnHeightPixels = 16)
        self.ram.caption                 = 'Double click right mouse button on target'
        self.addItem(self.ram)
        self.altShiftLeft                = LabelPair(engine, self, 'Reposition ships / boats', columnWidths=columnWidths, columnHeightPixels = 16)
        self.addItem(self.altShiftLeft)
        self.altShiftLeft.caption        = 'alt+left mouse drag'

        self.blank2                      = LabelPair(engine, self, '', columnWidths=columnWidths)
        self.addItem(self.blank2)

        self.chain                       = LabelPair(engine, self, 'Queue Commands', columnWidths=columnWidths, columnHeightPixels = 16)
        self.chain.caption               = 'Shift + command'
        self.addItem(self.chain)

        self.blank3                      = LabelPair(engine, self, '', columnWidths=columnWidths)
        self.addItem(self.blank3)

        self.stopAI                      = LabelPair(engine, self, 'Toggle Manual Control', columnWidths=columnWidths, columnHeightPixels = 16)
        self.stopAI.caption              = 'Spacebar'
        self.addItem(self.stopAI)
        self.manualControl               = LabelPair(engine, self, 'Manual Control', columnWidths=columnWidths, columnHeightPixels = 16)
        self.manualControl.caption       = 'Arrow Keys: Up, Down, Left, Right'
        self.addItem(self.manualControl)
        self.netSlave                    = LabelPair(engine, self, 'Toggle IA / VShip control', columnWidths=columnWidths, columnHeightPixels = 16)
        self.netSlave.caption            = 'Backspace'
        self.addItem(self.netSlave)

        self.blank4                      = LabelPair(engine, self, '', columnWidths=columnWidths)
        self.addItem(self.blank4)

        self.cameraMove                  = LabelPair(engine, self, 'Move Camera', columnWidths=columnWidths, columnHeightPixels = 16)
        self.cameraMove.caption          = 'W, A, S, D, Q, E, Z, X'
        self.addItem(self.cameraMove)
        #self.cameraRotate                = LabelPair(engine, self, 'Rotate Camera', columnWidths=columnWidths, columnHeightPixels = 16)
        #self.cameraRotate.caption        = 'Q, E, Z, X\t Left, Right, Up, Down'
        #self.addItem(self.cameraRotate)
        self.tab                         = LabelPair(engine, self, 'Pan Camera to next ent', columnWidths=columnWidths, columnHeightPixels = 16)
        self.tab.caption                 = 'Tab'
        self.addItem(self.tab)

        self.k                           = LabelPair(engine, self, 'Ship View', columnWidths=columnWidths, columnHeightPixels = 16)
        self.k.caption                   = 'K'
        self.addItem(self.k)
        self.l                           = LabelPair(engine, self, 'Tactical View', columnWidths=columnWidths, columnHeightPixels = 16)
        self.l.caption                   = 'L'
        self.addItem(self.l)

        self.blank5                      = LabelPair(engine, self, '', columnWidths=columnWidths)
        self.addItem(self.blank5)

        self.equal                       = LabelPair(engine, self, 'Increase Time Scale', columnWidths=columnWidths, columnHeightPixels = 16)
        self.equal.caption               = '='
        self.addItem(self.equal)
        self.minus                       = LabelPair(engine, self, 'Decrease Time Scale', columnWidths=columnWidths, columnHeightPixels = 16)
        self.minus.caption               = '-'
        self.addItem(self.minus)

    def tick(self, dtime):
        if self.on:
            self.show()
        else:
            self.hide()


    def toggle(self):
        if self.on:
            self.on = False
        else:
            self.on = True



    
#--------------------------------------------------------------------------------

class WidgetMgr(Mgr):
    widgets = []
    idCounter = 0

    worldToWorldMenu = None
    worldToEntMenu   = None
    entToWorldMenu   = None
    entToEntMenu     = None
    entMap  = {}  # maps ent's uiname (DDG51) to entity type (boat.DDG51)

    def __init__(self, engine):
        Mgr.__init__(self, engine)
        self.x = 0


    def initMenu(self):
        return
        self.buttonPressed = False
        screenRHS = self.engine.gfxSystem.renderWindow.getWidth()
        size = (300, 20)
        self.scenarioMap = {}

        nme = "Destroyer and Speedboat"
        self.button1 = InitMenuButton(self.engine, name = nme, pos = (300, 100), size = size, func = self.setTest1)
        self.scenarioMap[nme] = 1
        
        nme = "Five Destroyers and Destoyer"
        self.button2 = InitMenuButton(self.engine, name = nme, pos = (300, 200), size = size, func = self.setTest1)
        self.scenarioMap[nme] = 2

        nme = "Carrier and 100 speedboat swarm"
        self.button2 = InitMenuButton(self.engine, name = nme, pos = (300, 300), size = size, func = self.setTest1)
        self.scenarioMap[nme] = 6


    def setTest1(self, ms, caption):
        self.engine.testMgr.test = self.scenarioMap[caption]
        self.buttonPressed = True
        print "Clicked: ", caption



    def initEngine(self):
        """Init global UI
        """
        for etype in self.engine.entMgr.types:
            self.entMap[etype.uiname] = etype
        self.initTestMenu1()

    def crosslink(self):
        pass


    def tick(self, dtime):
        for widget in self.widgets:
            widget.tick(dtime)
        self.rightClickMenuTick(dtime)

    def rightClickMenuTick(self, dtime):
        if self.worldToWorldMenu:
            self.worldToWorldMenu.tick(dtime)
        if self.worldToEntMenu:
            self.worldToEntMenu.tick(dtime)
        if self.entToWorldMenu:
            self.entToWorldMenu.tick(dtime)
        if self.entToEntMenu:
            self.entToEntMenu.tick(dtime)

    def render(self):
        for widget in self.widgets:
            widget.render()
        self.rightClickMenuRender()

    def rightClickMenuRender(self):
        if self.worldToWorldMenu and not self.worldToEntMenu and not self.entToWorldMenu and not self.entToEntMenu:
            self.worldToWorldMenu.render()
            return

        if self.engine.selectionSystem.selectedEnts:
            if self.engine.inputSystem.entUnderMouse:
                self.entToEntMenu.render()
            else:
                self.entToWorldMenu.render()
        elif self.engine.inputSystem.entUnderMouse:
            self.worldToEntMenu.render()
        else:
            self.worldToWorldMenu.render()

    def initTestMenu1(self):
        """lets start with a few labels
        """
        l1 = FramerateWidget(self.engine)
        self.widgets.append(l1)

        ui = UIOverlay(self.engine)
        self.widgets.append(ui)

        screenRHS = self.engine.gfxSystem.renderWindow.getWidth()
        screenBottom = self.engine.gfxSystem.renderWindow.getHeight()

        defaultHeight = UIDefaults.PANEL_SIZE[1]

        gameInfoWidget = GameInfoWidget(self.engine, pos = (screenRHS - 200, 0), size = (100, defaultHeight*2))
        self.widgets.append(gameInfoWidget)


        shipInfoWidget = ShipInfoWidget(self.engine, size = (100, defaultHeight*8))
        self.widgets.append(shipInfoWidget)

        commandInfoWidget = ShipCommands(self.engine)
        self.widgets.append(commandInfoWidget)

        headerWidth = 100
        width = headerWidth * 3
        mouseOverInfoWidget = ShipMouseOverInfoWidget(self.engine, pos = (screenRHS - width, screenBottom - defaultHeight*10), size = (headerWidth, defaultHeight*10))
        self.widgets.append(mouseOverInfoWidget)

        self.f1Widget = F1HelpWidget(self.engine)
        self.widgets.append(self.f1Widget)
        self.engine.inputSystem.registerHandler(InputEvent.KEY_PRESSED, OIS.KC_F1, self.f1Widget.toggle)        

        self.worldToWorldMenu = self.makeWorldToWorldMenu()
        #self.entToWorldMenu   = self.makeEntToWorldMenu()
        #self.worldToEntMenu   = self.makeWorldToEntMenu()
        #self.entToEntMenu     = self.makeEntToEntMenu()
        '''
        db = DebugButtonWidget(self.engine, func = printClick)
        self.widgets.append(db)
 
        #------------------------------------------------------------------
        # cursor widget

        cursor = CursorWidget(self.engine)
        self.widgets.append(cursor)
        '''
        #------------------------------------------------------------------

    #---------------------Right click Menu functions------------------------------
    def makeWorldToEntMenu(self):
        menu = TopMenu(self.engine, name = "WorldToEnt", func = printClick)
        #mx = MenuItem(self.engine, parent = menu, name = "Stop", func = self.stopEnt)                
        #menu.addItem(mx)
        return menu

    def stopEnt(self, item, ms):
        ent = self.engine.inputSystem.entUnderMouse
        ent.command = None
        ent.destination = None
        ent.desiredHeading = ent.yaw
        ent.desiredSpeed   = 0
        if ent.squad:
            ent.squad.SquadAI.commands = []
            for squadMember in ent.squad.squadMembers:
                squadMember.command = None
                squadMember.destination = None


    def makeEntToEntMenu(self):
        menu = TopMenu(self.engine, name = "DefaultEntToEnt", func = printClick)        
        #for s in ['cover', 'warning fire', 'direct fire', 'cease fire']:
            #mx = MenuItem(self.engine, parent = menu, name = s, func = self.createEnt)                
            #menu.addItem(mx)
        return menu

    def makeWorldToWorldMenu(self):
        menu = TopMenu(self.engine, name = "Create Entity", func = printClick)
        for ent in self.engine.entMgr.types:
            mx = MenuItem(self.engine, parent = menu, name = ent.uiname, func = self.createEnt)                
            menu.addItem(mx)
        return menu

    def makeEntToWorldMenu(self):
        menu = TopMenu(self.engine, name = "EntToWorld", func = printClick)
        mx = MenuItem(self.engine, parent = menu, name = "Ready", func = printClick)                
        mx2 = MenuItem(self.engine, parent = mx, name = "Print", func = printClick)                
        mx3 = MenuItem(self.engine, parent = mx, name = "Move", func = self.makeCommandMoveTo)                
        mx.addItem(mx2)
        mx.addItem(mx3)
        menu.addItem(mx)
        return menu

    def makeCommandMoveTo(self, item, ms):
        import command
        import desiredState
        destination = desiredState.StoppedAtPosition(self.findWorldCoords(ms))
        command = command.MoveTo(self.engine, destination)
        for ent in self.engine.inputSystem.selectedEnts:
            ent.squad.strategicData.commands = [command]     

    def getNextId(self):
        self.idCounter += 1
        return self.idCounter

    def createEnt(self, item, ms):
        '''
        create an Entity of the appropriate type
        '''
        #print "Creating: ", item.name
        etype = self.entMap[item.name]
        pos = self.findWorldCoords(ms)
        import actionMgr
        handle = self.engine.entMgr.createHandle()
        time = self.engine.gameTime
        createAction = actionMgr.CreateEntity(time=time, handle=handle, type=etype)
        self.engine.actionMgr.enqueue(createAction)
        moveAction = actionMgr.MoveEntity(time=time, handle=handle, pos=pos)
        self.engine.actionMgr.enqueue(moveAction)

    xzPlane = ogre.Plane((0, 1, 0), 0)
    def findWorldCoords(self, ms):
        ''' Map to x,z plane from viewport
        '''
        ms.width = self.engine.gfxSystem.viewport.actualWidth 
        ms.height = self.engine.gfxSystem.viewport.actualHeight
        mouseRay = self.engine.cameraSystem.camera.getCameraToViewportRay(ms.X.abs/float(ms.width), ms.Y.abs/float(ms.height))
        result  =  mouseRay.intersects(self.xzPlane)
        pos = None
        if result.first:
            pos =  mouseRay.getPoint(result.second)
            #self.mousePosWorld = pos
        return pos

