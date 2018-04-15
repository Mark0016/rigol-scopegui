'''This file is part of rigol-scopegui.

   Copyright (c) 2017 Márk Vasi

   rigol-scopegui is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   rigol-scopegui is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with rigol-scopegui.  If not, see <http://www.gnu.org/licenses/>.'''

from PyQt4 import QtGui,QtCore

from triggerWidgets.design import edgewidget,pulsewidget,slopewidget,videowidget


INPUT_VALIDATOR = QtGui.QRegExpValidator(QtCore.QRegExp('[-]?[0-9]*\.?[0-9]+[TGMkmunp]?'))

INTERVAL_VALIDATOR = QtGui.QRegExpValidator(QtCore.QRegExp('[0-9]*\.?[0-9]+[TGMkmunp]?([-][0-9]*\.?[0-9]+[TGMkmunp]?)?'))

def toFloat(string):

    prefixes = { 'T':10**12,
                 'G':10**9,
                 'M':10**6,
                 'k':10**3,
                 'm':10**-3,
                 'u':10**-6,
                 'n':10**-9,
                 'p':10**-12 }

    for prefix in prefixes.keys():
       if prefix in string:
            return float(string.replace(prefix,''))*prefixes[prefix]

    return float(string)

def toInterval(string):
    l = string.split('-')
    if len(l) == 1:
        return toFloat(string)
    l[0] = toFloat(l[0])
    l[1] = toFloat(l[1])
    return [min(l),max(l)]


class EdgeWidget(QtGui.QWidget,edgewidget.Ui_Form):

    updated = QtCore.pyqtSignal(dict,str)

    properties = {'source':1,'edge':'POS','level':0}

    def __init__(self):
        super(self.__class__,self).__init__()

        self.setupUi(self)

        self.level.setValidator(INPUT_VALIDATOR)

        self._connections()

    def setSource(self,index):
        self.properties['source']=index+1
        self.updated.emit(self.properties,'edge')

    def setEdge(self,index):
        if index == 0: self.properties['edge']='POS'
        elif index == 1: self.properties['edge']='NEG'
        else: self.properties['edge']='RFAL'
        self.updated.emit(self.properties,'edge')

    def setLevel(self,text):
        self.properties['level']=toFloat(text)
        self.updated.emit(self.properties,'edge')

    def _connections(self):
        self.level.returnPressed.connect(lambda: self.setLevel(self.level.text()))
        self.edge.activated.connect(lambda: self.setEdge(self.edge.currentIndex()))
        self.source.activated.connect(lambda: self.setSource(self.source.currentIndex()))


class PulseWidget(QtGui.QWidget,pulsewidget.Ui_Form):

    updated = QtCore.pyqtSignal(dict,str)

    properties = {'source':1,'polarity':'P','when':'GR','pulsewidth':1e-6,'level':0}

    def __init__(self):
        super(self.__class__,self).__init__()

        self.setupUi(self)

        self.pulseWidth.setValidator(INTERVAL_VALIDATOR)
        self.level.setValidator(INPUT_VALIDATOR)

        self._connections()

    def setSource(self,index):
        self.properties['source']=index+1
        self.updated.emit(self.properties,'pulse')

    def setPolarity(self,index):
        if index == 0: self.properties['polarity']='P'
        else: self.properties['polarity']='N'
        self.updated.emit(self.properties,'pulse')

    def setWhen(self,index):
        if index == 0: self.properties['when']='GR'
        elif index == 1: self.properties['when']='LES'
        else: self.properties['when']='GL'
        self.updated.emit(self.properties,'pulse')

    def setWidth(self,text):
        self.properties['pulsewidth']=toInterval(text)
        self.updated.emit(self.properties,'pulse')

    def setLevel(self,text):
        self.properties['level']=toFloat(text)
        self.updated.emit(self.properties,'pulse')

    def _connections(self):
        self.level.returnPressed.connect(lambda: self.setLevel(self.level.text()))
        self.pulseWidth.returnPressed.connect(lambda: self.setWidth(self.pulseWidth.text()))
        self.source.activated.connect(lambda: self.setSource(self.source.currentIndex()))
        self.when.activated.connect(lambda: self.setWhen(self.when.currentIndex()))
        self.polarity.activated.connect(lambda: self.setPolarity(self.polarity.currentIndex()))
        
  
class SlopeWidget(QtGui.QWidget,slopewidget.Ui_Form):
    
    updated = QtCore.pyqtSignal(dict,str)

    properties = {'source':1,'polarity':'P','when':'GR','time':1e-6,'level':0,'blevel':0}

    def __init__(self):
        super(self.__class__,self).__init__()

        self.setupUi(self)

        self.aLevel.setValidator(INPUT_VALIDATOR)
        self.bLevel.setValidator(INPUT_VALIDATOR)
        self.time.setValidator(INTERVAL_VALIDATOR)

        self._connections()
        

    def setWhen(self,index):
        if index == 0: self.properties['when']='GR'
        elif index == 1: self.properties['when']='LES'
        else: self.properties['when']='GL'
        self.updated.emit(self.properties,'slope')

    def setSlope(self,index):
        if index == 0: self.properties['polarity']='P'
        else: self.properties['polarity']='N'
        self.updated.emit(self.properties,'slope')

    def setSource(self,index):
        self.properties['source']=index+1
        self.updated.emit(self.properties,'slope')

    def setALevel(self,text):
        self.properties['level']=toFloat(text)
        self.updated.emit(self.properties,'slope')

    def setBLevel(self,text):
        self.properties['blevel']=toFloat(text)
        self.updated.emit(self.properties,'slope')

    def setTime(self,text):
        self.properties['time']=toInterval(text)
        self.updated.emit(self.properties,'slope')
    
    def _connections(self):
        self.aLevel.returnPressed.connect(lambda: self.setALevel(self.aLevel.text()))
        self.bLevel.returnPressed.connect(lambda: self.setBLevel(self.bLevel.text()))
        self.time.returnPressed.connect(lambda: self.setTime(self.time.text()))

        self.source.activated.connect(lambda: self.setSource(self.source.currentIndex()))
        self.when.activated.connect(lambda: self.setWhen(self.when.currentIndex()))
        self.slope.activated.connect(lambda: self.setSlope(self.slope.currentIndex()))
        


class VideoWidget(QtGui.QWidget,videowidget.Ui_Form):
    
    updated = QtCore.pyqtSignal(dict,str)

    def __init__(self):
        super(self.__class__,self).__init__()

        self.setupUi(self)

        self.level.setValidator(INPUT_VALIDATOR)
        self.line.setValidator(QtGui.QIntValidator(1,625))

        self.properties = {'source':1,'polarity':'POS','level':0,'mode':'ODDF','line':1,'standard':'NTSC'}

        self._connections()

    def setSource(self,index):
        self.properties['source']=index+1
        self.updated.emit(self.properties,'video')

    def setLevel(self,text):
        self.properties['level']=toFloat(text)
        self.updated.emit(self.properties,'video')

    def setPolarity(self,index):
        if index == 0: self.properties['polarity']='POS'
        else: self.properties['polarity'] = 'NEG'
        self.updated.emit(self.properties,'video')

    def setMode(self,index):
        d = {0:'ODDF',1:'EVEN',2:'LINE',3:'ALIN'}
        self.properties['mode'] = d[index]
        self.updated.emit(self.properties,'video')

    def setLine(self,text):
        self.properties['line'] = int(text)
        self.updated.emit(self.properties,'video')

    def setStandard(self,index):
        d = {0:'NTSC',1:'PALS',2:'480P',3:'576P'}
        self.properties['standard'] = d[index]
        self.updated.emit(self.properties,'video')        

    def _connections(self):
        self.level.returnPressed.connect(lambda: self.setLevel(self.level.text()))
        self.source.activated.connect(lambda: self.setSource(self.source.currentIndex()))
        self.polarity.activated.connect(lambda: self.setPolarity(self.polarity.currentIndex()))
        self.line.returnPressed.connect(lambda: self.setLine(self.line.text()))
        self.mode.activated.connect(lambda: self.setMode(self.mode.currentIndex()))
        self.standard.activated.connect(lambda: self.setStandard(self.standard.currentIndex()))
    
