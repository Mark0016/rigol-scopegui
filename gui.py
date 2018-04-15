#!/usr/bin/env python3

##'''This file is part of rigol-scopegui.
##
##   Copyright (c) 2017 Márk Vasi
##
##   rigol-scopegui is free software: you can redistribute it and/or modify
##   it under the terms of the GNU General Public License as published by
##   the Free Software Foundation, either version 3 of the License, or
##   (at your option) any later version.
##
##   rigol-scopegui is distributed in the hope that it will be useful,
##   but WITHOUT ANY WARRANTY; without even the implied warranty of
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##   GNU General Public License for more details.
##
##   You should have received a copy of the GNU General Public License
##   along with rigol-scopegui.  If not, see <http://www.gnu.org/licenses/>.'''

from PyQt4 import QtGui,QtCore
import pyqtgraph as pg
import sys
import vxi11
from ipaddress import IPv4Address
from math import log10
from properties import Properties
from time import sleep

from data_handling import DataThread, XYThread

import ip_popup_design
import scopegui_design_3 as design


INPUT_VALIDATOR = QtGui.QRegExpValidator(QtCore.QRegExp('[-]?[0-9]*\.?[0-9]+[TGMkmunp]?'))


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

def toSI(f=float):

    if f == 0:
        return str(f)
    prefixes = { 4 :'T',
                 3 :'G',
                 2 :'M',
                 1 :'k',
                 0 :'',
                 -1:'m',
                 -2:'u',
                 -3:'n',
                 -4:'p' }

    a = log10(abs(f))//3

    return '{}{}'.format(round(f/(10**(a*3)),3),prefixes[a])
    
    
class Trigger(object):

    channel = 1
    level = 0
    blevel = None
    
    
    def __init__(self):
        super(self.__class__,self).__init__()

class IpWindow(QtGui.QMainWindow,ip_popup_design.Ui_MainWindow):

    addressChanged = QtCore.pyqtSignal(str)
    
    def __init__(self,currentAddress = None):
        super(self.__class__,self).__init__()

        self.setupUi(self)
        if currentAddress != None:
            self.lineEdit.setText(str(currentAddress))

        self._connections()

    def changeAddress(self):
        try:
            IPv4Address(self.lineEdit.text())
        except ValueError:
            return
        
        ip = self.lineEdit.text()
        self.addressChanged.emit(ip)
        self.close()

    def _connections(self):

        self.buttonBox.rejected.connect(self.close)
        self.buttonBox.accepted.connect(self.changeAddress)
        self.lineEdit.returnPressed.connect(self.changeAddress)


class MainWindow(QtGui.QMainWindow,design.Ui_MainWindow):

##---------------init---------------##    

    def __init__(self,app = QtGui.QApplication):
        super(self.__class__,self).__init__()

        self.app = app

        self.properties = Properties()

        self.setupUi(self)

        self.trigger = Trigger()

        if self.properties['main']['ip']==None:
            self.changeIpAddress()
            self.setupComplete = False
        elif self.properties['main']['autosetup']:
            self.setCurrentSettings()
            self.setupPlotThreads()
        else:
            self.setVisuals()
            self.setupPlotThreads()

        self.setupPlots()

        

        self._setLeValidator()
        self._connections()

    def setVisuals(self):

        self.setupLe()
        self.setupProbe()
        self.setupCoupling()
        self.setupTimebaseMode()
        self.setupTrigger()
        self.setupXYChannel()


    def setupPlots(self):

        self.plotWidget.plot(pen = pg.mkPen('y'))
        self.plotWidget.plot(pen = pg.mkPen('c'))
        self.plotWidget.plot(pen = pg.mkPen('m'))
        self.plotWidget.plot(pen = pg.mkPen('b'))
        self.plotWidget.plot(pen = pg.mkPen('r',style=QtCore.Qt.DashLine))
        self.plotWidget.plot(pen = pg.mkPen('r',style=QtCore.Qt.DashLine))

        self.plotWidget.getAxis('left').setLabel(units='V')
        self.plotWidget.getAxis('left').enableAutoSIPrefix()

        self.plotWidget.getAxis('bottom').setLabel(units='s')
        self.plotWidget.getAxis('bottom').enableAutoSIPrefix()

        self.plotlines = self.plotWidget.getPlotItem().listDataItems()

    def setupPlotThreads(self):
        
        self.ytth = [DataThread(self.properties['main']['ip'],channel=ch+1) for ch in range(4)]
        for th in self.ytth:
            th.updated.connect(self.setPlotData)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updatePlots)
        self.timer.start(1000)

    def setupLe(self):

        self.ch1ScaleLe.setText(toSI(self.properties['channel1']['scale']))
        self.ch1OffsetLe.setText(toSI(self.properties['channel1']['offset']))

        self.ch2ScaleLe.setText(toSI(self.properties['channel2']['scale']))
        self.ch2OffsetLe.setText(toSI(self.properties['channel2']['offset']))

        self.ch3ScaleLe.setText(toSI(self.properties['channel3']['scale']))
        self.ch3OffsetLe.setText(toSI(self.properties['channel3']['offset']))

        self.ch4ScaleLe.setText(toSI(self.properties['channel4']['scale']))
        self.ch4OffsetLe.setText(toSI(self.properties['channel4']['offset']))

        self.tbScaleLe.setText(toSI(self.properties['timebase']['scale']))
        self.tbOffsetLe.setText(toSI(self.properties['timebase']['offset']))

    def setupTimebaseMode(self):

        d = {'YT':self.tbYT,'XY':self.tbXY,'ROLL':self.tbROLL}

        d[self.properties['timebase']['mode']].setChecked(True)

    def setupXYChannel(self):

        self.tbXChannel.setCurrentIndex(self.properties['timebase']['xchannel']-1)
        self.tbYChannel.setCurrentIndex(self.properties['timebase']['ychannel']-1)
    
    def setupProbe(self):

        valueList = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
        
        self.ch1Probe.setCurrentIndex(valueList.index(self.properties['channel1']['probe']))
        self.ch2Probe.setCurrentIndex(valueList.index(self.properties['channel2']['probe']))
        self.ch3Probe.setCurrentIndex(valueList.index(self.properties['channel3']['probe']))
        self.ch4Probe.setCurrentIndex(valueList.index(self.properties['channel4']['probe']))

    def setupCoupling(self):

        l = [{'AC':self.ch1AC,'DC':self.ch1DC,'GND':self.ch1GND},
             {'AC':self.ch2AC,'DC':self.ch2DC,'GND':self.ch2GND},
             {'AC':self.ch3AC,'DC':self.ch3DC,'GND':self.ch3GND},
             {'AC':self.ch4AC,'DC':self.ch4DC,'GND':self.ch4GND}]

        for ch in (1,2,3,4):
            l[ch-1][self.properties['channel%d'%ch]['coupling']].setChecked(True)

    def setupTrigger(self):

        btnmode = {'edge': self.trgEdge,
                   'pulse': self.trgPulse,
                   'slope': self.trgSlope,
                   'video' : self.trgVideo}
        btnmode[self.properties['trigger']['mode']].setChecked(True)
        self.changeTriggerMode(self.properties['trigger']['mode'],offline=True)

        btnsweep = {'normal':self.trgNormal,
                    'auto':self.trgAuto,
                    'single':self.trgSingle}
        btnsweep[self.properties['trigger']['sweep']].setChecked(True)

        
##-------------main-methods-------------##

    def changeIpAddress(self):

        def chaddress(ip):
            self.properties['main']['ip'] = ip
            if not self.setupComplete:
                self.setupPlotThreads()
            if self.properties['main']['autosetup']:
                self.setCurrentSettings()

        self.ipWindow = IpWindow(self.properties['main']['ip'])
        self.ipWindow.addressChanged.connect(chaddress)
        self.ipWindow.show()

    def openConfig(self):
        self.fdlcfg = QtGui.QFileDialog()
        self.fdlcfg.setFilter('Configuration file (*.scopecfg);;All files (*) ')
        self.fdlcfg.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        if self.fdlcfg.exec_():
            self.properties.load(self.fdlcfg.selectedFiles()[0])
            self.setVisuals()
            
    def saveConfig(self):
        self.fdscfg = QtGui.QFileDialog()
        self.fdscfg.setFilter('Configuration file (*.scopecfg);;All files (*)')
        self.fdscfg.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        if self.fdscfg.exec_():
            self.properties.save(self.fdscfg.selectedFiles()[0])


##--------scope-base-functions----------##

    def stopScope(self):
        scope = vxi11.Instrument(self.properties['main']['ip'])

        scope.write(':STOP')

    def runScope(self):
        scope = vxi11.Instrument(self.properties['main']['ip'])

        scope.write(':RUN')

    def autosetScope(self):
        scope = vxi11.Instrument(self.properties['main']['ip'])

        scope.write(':AUT')

        
##----------read-all-settings-----------##    

    def setCurrentSettings(self):

        scope = vxi11.Instrument(self.properties['main']['ip'])

        for channel in (1,2,3,4):
            d = self.properties['channel{}'.format(channel)]
            d['coupling'] = scope.ask(':CHAN{}:COUP?'.format(channel))
            d['offset'] = float(scope.ask(':CHAN{}:OFFS?'.format(channel)))
            d['scale'] = float(scope.ask(':CHAN{}:SCAL?'.format(channel)))
            d['probe'] = float(scope.ask(':CHAN{}:PROB?'.format(channel)))

        tb = self.properties['timebase']
        tb['scale'] = float(scope.ask(':TIM:SCAL?'))
        tb['offset'] = float(scope.ask(':TIM:OFFS?'))

        modes = {'EDGE':'edge',
                 'PULS':'pulse',
                 'SLOP':'slope',
                 'VID':'video'}

        sweep = {'NORM':'normal',
                 'AUTO':'auto',
                 'SING':'single'}

        trg = self.properties['trigger']
        trg['mode'] = modes[scope.ask(':TRIG:MODE?')]
        trg['sweep'] = sweep[scope.ask(':TRIG:SWE?')]

        self.setVisuals()

            
            
    

##-----------------plotting-------------##
        
    def updatePlots(self):   

        if self.properties['timebase']['mode'] in ('YT','ROLL'):

            enabled = (self.ch1Enable.checkState(),self.ch2Enable.checkState(),
                       self.ch3Enable.checkState(),self.ch4Enable.checkState())

            for i,th in enumerate(self.ytth):
                if enabled[i]:
                    th.run()

        elif self.properties['timebase']['mode'] == 'XY':

            th = XYThread(self.properties['main']['ip'],
                          self.properties['timebase']['xchannel'],
                          self.properties['timebase']['ychannel'])

            th.updated.connect(self.setPlotData)
            th.run()

                    

    def setPlotData(self,x,y,ch):

        self.plotlines[ch-1].setData(x,y)
        if self.properties['timebase']['mode'] in ('YT','ROLL'):
            self.plotWidget.getPlotItem().setLimits(xMin=min(x),xMax=max(x))
        else:
            self.plotWidget.getPlotItem().setLimits(xMin=None,xMax=None)

    def resetPlots(self):

        for plot in self.plotlines:
            plot.setData([0])

    def clearTrigger(self):
        self.plotlines[4].setData([0])
        self.plotlines[5].setData([0])

    def showTrigger(self):

        if self.trgShow.checkState() == 0:
            self.clearTrigger()

        else:
            rng = self.plotlines[self.trigger.channel-1].dataBounds(0)

            self.plotlines[4].setData(rng,[self.trigger.level,self.trigger.level])

            if self.trigger.blevel != None:
                self.plotlines[5].setData(rng,[self.trigger.blevel,self.trigger.blevel])
    
##-------------trigger-functions--------------##

    def changeTriggerMode(self,mode,offline=False):

        widgets = {'edge':self.trgEdgeWidget,
                   'pulse':self.trgPulseWidget,
                   'slope':self.trgSlopeWidget,
                   'video':self.trgVideoWidget}
        
        self.trgStackedWidget.setCurrentWidget(widgets[mode])

        if mode != 'slope':
            self.trigger.blevel = None

        
        if not offline:
            scope = vxi11.Instrument(self.properties['main']['ip'])
            scope.write(':TRIG:MODE %s'%mode)

    def setTriggerSweep(self,sweep):

        self.properties['trigger']['sweep'] = sweep

        scope = vxi11.Instrument(self.properties['main']['ip'])
        scope.write(':TRIG:SWE {}'.format(sweep))

    def setTriggerHoldoff(self,text):

        h = toFloat(text)
        self.properties['trigger']['holdoff'] = h

        scope = vxi11.Instrument(self.properties['main']['ip'])
        scope.write(':TRIG:HOLD {}'.format(h))

    def setTriggerNoiseRejection(self,enable=True):

        self.properties['trigger']['nrej'] = enable

        scope = vxi11.Instrument(self.properties['main']['ip'])
        scope.write(':TRIG:NREJ {:d}'.format(enable))
        

    def setTrigger(self,props,mode):

        self.properties[mode] = props

        commands = {'edge':':TRIG:EDG',
                    'pulse':':TRIG:PULS',
                    'slope':':TRIG:SLOPE',
                    'video':'TRIG:VID'}

        scope = vxi11.Instrument(self.properties['main']['ip'])
            
        #levels
        if mode != 'slope':
            scope.write(commands[mode]+':LEV %f'%props['level'])
            self.trigger.blevel = None
        else:
            scope.write(commands[mode]+':ALEV %f'%props['level'])
            scope.write(commands[mode]+':BLEV %f'%props['blevel'])
            self.trigger.blevel = props['blevel']
        self.trigger.level = props['level']

        #ploarity/when
        if mode == 'edge':
            scope.write(commands[mode]+':SLOP %s'%props['edge'])
        elif mode in ('pulse','slope'):
            scope.write(commands[mode]+':WHEN %s'%(props['polarity']+props['when']))
        elif mode == 'video':
            scope.write(commands[mode]+':POL %s'%props['polarity'])

        #time/width
        if mode == 'pulse':
            if type(props['pulsewidth']) == float:
                scope.write(commands[mode]+':WIDT %f'%props['pulsewidth'])
            else:
                scope.write(commands[mode]+':LWID %f'%props['pulsewidth'][0])
                scope.write(commands[mode]+':UWID %f'%props['pulsewidth'][1])
        elif mode == 'slope':
            if type(props['time']) == float:
                scope.write(commands[mode]+':TIME %f'%props['time'])
            else:
                scope.write(commands[mode]+':TLOW %f'%(props['time'][0]))
                scope.write(commands[mode]+':TUPP %f'%(props['time'][1]))

        #video
        if mode == 'video':
            scope.write(commands[mode]+':MODE {}'.format(props['mode']))
            scope.write(commands[mode]+':LINE {}'.format(props['line']))
            scope.write(commands[mode]+':STAN {}'.format(props['standard']))
              
            

        #source
        if mode != 'pattern':
            scope.write(commands[mode]+':SOUR %s'%('CHAN%d'%props['source']))
            self.trigger.channel = props['source']


            
        
##-------------timebase-functions-------------##

    def setTimebaseMode(self,mode):

        self.resetPlots()

        self.properties['timebase']['mode'] = mode

        scope = vxi11.Instrument(self.properties['main']['ip'])

        if mode in ('YT','XY'):
            scope.write(':TIM:MODE MAIN')
        elif mode == 'ROLL':
            scope.write(':TIM:MODE ROLL')

    def setXYChannel(self,xindex,yindex):

        self.properties['timebase']['xchannel'] = xindex+1
        self.properties['timebase']['ychannel'] = yindex+1


    def setTimebaseScaleLe(self,text):

        self.properties['timebase']['scale'] = toFloat(text)
        
        scope = vxi11.Instrument(self.properties['main']['ip'])
        
        scope.write(':TIM:SCAL %f'%toFloat(text))

    def setTimebaseOffsetLe(self,text):

        self.properties['timebase']['offset'] = toFloat(text)

        scope = vxi11.Instrument(self.properties['main']['ip'])
        
        scope.write(':TIM:OFFS %f'%toFloat(text))

    def setTimebaseScale(self,index):

        step = [1, 2, 5]

        if self.properties['timebase']['mode'] == 'YT':
            start = toFloat('1n')
            scale = start * (10**((index+2)//len(step))) * step[(index+2) % len(step)]
        elif self.properties['timebase']['mode'] == 'ROLL':
            start = toFloat('100m')
            scale = start * (10**((index+1)//len(step))) * step[(index+1) % len(step)]

        self.properties['timebase']['scale'] = scale

        self.tbScaleLe.setText(toSI(scale))

        scope = vxi11.Instrument(self.properties['main']['ip'])

        scope.write(':TIM:SCAL %s'%str(scale))

    def setTimebaseOffset(self,index):

        unit = self.properties['timebase']['scale']*12/100

        offset = -(index * unit - 50 * unit)

        self.properties['timebase']['offset'] = offset

        self.tbOffsetLe.setText(toSI(offset))

        scope = vxi11.Instrument(self.properties['main']['ip'])

        scope.write(':TIM:OFFS %s'%str(offset))
        
        

##-------------channel-functions--------------##


    def enableChannel(self,channel,checkstate):

        scope = vxi11.Instrument(self.properties['main']['ip'])

        if checkstate == 2:
            scope.write(':CHAN%d:DISP 1'%channel)
        elif checkstate == 0:
            scope.write(':CHAN%d:DISP 0'%channel)
            self.plotlines[channel-1].setData([0])

    def setCoupling(self,channel,coupling):

        scope = vxi11.Instrument(self.properties['main']['ip'])

        scope.write(':CHAN%d:COUP %s'%(channel,coupling))

    def setBWL(self,channel,checkstate):

        scope = vxi11.Instrument(self.properties['main']['ip'])

        if checkstate == 2:
            scope.write(':CHAN%d:BWL 20M'%channel)
        elif checkstate == 0:
            scope.write(':CHAN%d:BWL OFF'%channel)

    def setFineAdj(self,channel,checkstate):

        scope = vxi11.Instrument(self.properties['main']['ip'])

        if checkstate == 2:
            scope.write(':CHAN%d:VERN 1'%channel)
        elif checkstate == 0:
            scope.write(':CHAN%d:VERN 0'%channel)

    def setProbe(self,channel,index):

        valueList = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]

        scope = vxi11.Instrument(self.properties['main']['ip'])

        scope.write(':CHAN%d:PROB %s'%(channel,valueList[index]))

##-----------channel-offset&scale------------##

    def _quaryProbe(self,channel):

        scope = vxi11.Instrument(self.properties['main']['ip'])
        return float(scope.ask(':CHAN%d:PROB?'%channel))

    def _quaryRange(self,channel):

        scope = vxi11.Instrument(self.properties['main']['ip'])
        return float(scope.ask(':CHAN%d:SCAL?'%channel))*8
        

    def setChannelScale(self,channel,index):

        lle = [self.ch1ScaleLe, self.ch2ScaleLe, self.ch3ScaleLe, self.ch4ScaleLe]

        step = [1, 2, 5]
        start = 0.001*(10**int(log10(self._quaryProbe(channel))))
        scale = start * (10**(index//len(step))) * step[index % len(step)]

        lle[channel-1].setText(toSI(scale))
        
        scope = vxi11.Instrument(self.properties['main']['ip'])
        
        scope.write(':CHAN%d:SCAL %f'%(channel,scale))

    def setChannelOffset(self,channel,index):

        lle = [self.ch1OffsetLe, self.ch2OffsetLe, self.ch3OffsetLe, self.ch4OffsetLe]

        rg = self._quaryRange(channel)
        offset = ((index+1)*rg/100) - rg/2
        
        lle[channel-1].setText(toSI(offset))

        scope = vxi11.Instrument(self.properties['main']['ip'])
        
        scope.write(':CHAN%d:OFFS %f'%(channel,round(offset,3)))

    def setChannelScaleLe(self,channel,text):

        scope = vxi11.Instrument(self.properties['main']['ip'])
        
        scope.write(':CHAN%d:SCAL %f'%(channel,toFloat(text)))

    def setChannelOffsetLe(self,channel,text):

        scope = vxi11.Instrument(self.properties['main']['ip'])
        
        scope.write(':CHAN%d:OFFS %f'%(channel,toFloat(text)))


##------------connections-------------##

    def closeEvent(self, event):
        self.app.closeAllWindows()
        event.accept()

    def _connections(self):

        self.ch1Enable.stateChanged.connect(lambda: self.enableChannel(1,self.ch1Enable.checkState()))
        self.ch2Enable.stateChanged.connect(lambda: self.enableChannel(2,self.ch2Enable.checkState()))
        self.ch3Enable.stateChanged.connect(lambda: self.enableChannel(3,self.ch3Enable.checkState()))
        self.ch4Enable.stateChanged.connect(lambda: self.enableChannel(4,self.ch4Enable.checkState()))

        self.ch1BWL.stateChanged.connect(lambda: self.setBWL(1,self.ch1BWL.checkState()))
        self.ch2BWL.stateChanged.connect(lambda: self.setBWL(2,self.ch2BWL.checkState()))
        self.ch3BWL.stateChanged.connect(lambda: self.setBWL(3,self.ch3BWL.checkState()))
        self.ch4BWL.stateChanged.connect(lambda: self.setBWL(4,self.ch4BWL.checkState()))

        self.ch1FineAdj.stateChanged.connect(lambda: self.setFineAdj(1,self.ch1FineAdj.checkState()))
        self.ch2FineAdj.stateChanged.connect(lambda: self.setFineAdj(2,self.ch2FineAdj.checkState()))
        self.ch3FineAdj.stateChanged.connect(lambda: self.setFineAdj(3,self.ch3FineAdj.checkState()))
        self.ch4FineAdj.stateChanged.connect(lambda: self.setFineAdj(4,self.ch4FineAdj.checkState()))

        self.ch1Probe.activated.connect(lambda: self.setProbe(1,self.ch1Probe.currentIndex()))
        self.ch2Probe.activated.connect(lambda: self.setProbe(2,self.ch2Probe.currentIndex()))
        self.ch3Probe.activated.connect(lambda: self.setProbe(3,self.ch3Probe.currentIndex()))
        self.ch4Probe.activated.connect(lambda: self.setProbe(4,self.ch4Probe.currentIndex()))
        

        self._rbuttonConnections()
        self._scaleConections()
        self._offsetConnections()
        self._timebaseConnections()
        self._triggerConnections()
        self._menuConnections()
        
    def _rbuttonConnections(self):

        self.ch1AC.clicked.connect(lambda:self.setCoupling(1,'AC'))
        self.ch1DC.clicked.connect(lambda:self.setCoupling(1,'DC'))
        self.ch1GND.clicked.connect(lambda:self.setCoupling(1,'GND'))

        self.ch2AC.clicked.connect(lambda:self.setCoupling(2,'AC'))
        self.ch2DC.clicked.connect(lambda:self.setCoupling(2,'DC'))
        self.ch2GND.clicked.connect(lambda:self.setCoupling(2,'GND'))

        self.ch3AC.clicked.connect(lambda:self.setCoupling(3,'AC'))
        self.ch3DC.clicked.connect(lambda:self.setCoupling(3,'DC'))
        self.ch3GND.clicked.connect(lambda:self.setCoupling(3,'GND'))

        self.ch4AC.clicked.connect(lambda:self.setCoupling(4,'AC'))
        self.ch4DC.clicked.connect(lambda:self.setCoupling(4,'DC'))
        self.ch4GND.clicked.connect(lambda:self.setCoupling(4,'GND'))

    def _scaleConections(self):

        self.ch1Scale.valueChanged.connect(lambda: self.setChannelScale(1,self.ch1Scale.sliderPosition()))
        self.ch2Scale.valueChanged.connect(lambda: self.setChannelScale(2,self.ch2Scale.sliderPosition()))
        self.ch3Scale.valueChanged.connect(lambda: self.setChannelScale(3,self.ch3Scale.sliderPosition()))
        self.ch4Scale.valueChanged.connect(lambda: self.setChannelScale(4,self.ch4Scale.sliderPosition()))

        self.ch1ScaleLe.returnPressed.connect(lambda: self.setChannelScaleLe(1,self.ch1ScaleLe.text()))
        self.ch2ScaleLe.returnPressed.connect(lambda: self.setChannelScaleLe(2,self.ch2ScaleLe.text()))
        self.ch3ScaleLe.returnPressed.connect(lambda: self.setChannelScaleLe(3,self.ch3ScaleLe.text()))
        self.ch4ScaleLe.returnPressed.connect(lambda: self.setChannelScaleLe(4,self.ch4ScaleLe.text()))
        

    def _offsetConnections(self):
        
        self.ch1Offset.valueChanged.connect(lambda: self.setChannelOffset(1,self.ch1Offset.sliderPosition()))
        self.ch2Offset.valueChanged.connect(lambda: self.setChannelOffset(2,self.ch2Offset.sliderPosition()))
        self.ch3Offset.valueChanged.connect(lambda: self.setChannelOffset(3,self.ch3Offset.sliderPosition()))
        self.ch4Offset.valueChanged.connect(lambda: self.setChannelOffset(4,self.ch4Offset.sliderPosition()))

        self.ch1OffsetLe.returnPressed.connect(lambda: self.setChannelOffsetLe(1,self.ch1OffsetLe.text()))
        self.ch2OffsetLe.returnPressed.connect(lambda: self.setChannelOffsetLe(2,self.ch2OffsetLe.text()))
        self.ch3OffsetLe.returnPressed.connect(lambda: self.setChannelOffsetLe(3,self.ch3OffsetLe.text()))
        self.ch4OffsetLe.returnPressed.connect(lambda: self.setChannelOffsetLe(4,self.ch4OffsetLe.text()))

    def _timebaseConnections(self):

        self.tbYT.clicked.connect(lambda: self.setTimebaseMode('YT'))
        self.tbXY.clicked.connect(lambda: self.setTimebaseMode('XY'))
        self.tbROLL.clicked.connect(lambda: self.setTimebaseMode('ROLL'))

        self.tbXChannel.activated.connect(lambda: self.setXYChannel(self.tbXChannel.currentIndex(),
                                                                              self.tbYChannel.currentIndex()))
        self.tbYChannel.activated.connect(lambda: self.setXYChannel(self.tbXChannel.currentIndex(),
                                                                              self.tbYChannel.currentIndex()))

        self.tbScaleLe.returnPressed.connect(lambda: self.setTimebaseScaleLe(self.tbScaleLe.text()))
        self.tbOffsetLe.returnPressed.connect(lambda: self.setTimebaseOffsetLe(self.tbOffsetLe.text()))
    
        self.tbScale.valueChanged.connect(lambda: self.setTimebaseScale(self.tbScale.sliderPosition()))
        self.tbOffset.valueChanged.connect(lambda: self.setTimebaseOffset(self.tbOffset.sliderPosition()))        

    def _triggerConnections(self):

        self.trgEdge.clicked.connect(lambda: self.changeTriggerMode('edge'))
        self.trgPulse.clicked.connect(lambda: self.changeTriggerMode('pulse'))
        self.trgSlope.clicked.connect(lambda: self.changeTriggerMode('slope'))
        self.trgVideo.clicked.connect(lambda: self.changeTriggerMode('video'))


        widgets = (self.trgEdgeWidget,self.trgPulseWidget,self.trgSlopeWidget,self.trgVideoWidget)
        for w in widgets:
            w.updated.connect(self.setTrigger)

        plots = self.plotlines[:4]

        for p in plots:
            p.sigPlotChanged.connect(self.showTrigger)

        self.trgNormal.clicked.connect(lambda: self.setTriggerSweep('normal'))
        self.trgAuto.clicked.connect(lambda: self.setTriggerSweep('auto'))
        self.trgSingle.clicked.connect(lambda: self.setTriggerSweep('single'))

        self.trgHoldoff.returnPressed.connect(lambda: self.setTriggerHoldoff(self.trgHoldoff.text()))
        self.trgNoise.clicked.connect(lambda: self.setTriggerNoiseRejection(True if self.trgNoise.checkState()==2 else False))

    def _menuConnections(self):

        self.action_Load_configuration.triggered.connect(self.openConfig)
        self.action_Quit.triggered.connect(self.app.closeAllWindows)
        self.action_Save_configuration.triggered.connect(self.saveConfig)
        self.actionLoad_current_settings_from_scope.triggered.connect(self.setCurrentSettings)
        self.actionIP_Adress.triggered.connect(self.changeIpAddress)

        self.action_Stop.triggered.connect(self.stopScope)
        self.action_Run.triggered.connect(self.runScope)
        self.action_Autoset.triggered.connect(self.autosetScope)
        


##------------validator-setup----------##
        
    def _setLeValidator(self):

        self.ch1ScaleLe.setValidator(INPUT_VALIDATOR)
        self.ch1OffsetLe.setValidator(INPUT_VALIDATOR)

        self.ch2ScaleLe.setValidator(INPUT_VALIDATOR)
        self.ch2OffsetLe.setValidator(INPUT_VALIDATOR)

        self.ch3ScaleLe.setValidator(INPUT_VALIDATOR)
        self.ch3OffsetLe.setValidator(INPUT_VALIDATOR)

        self.ch4ScaleLe.setValidator(INPUT_VALIDATOR)
        self.ch4OffsetLe.setValidator(INPUT_VALIDATOR)

        self.tbScaleLe.setValidator(INPUT_VALIDATOR)
        self.tbOffsetLe.setValidator(INPUT_VALIDATOR)


def main():
    app = QtGui.QApplication(sys.argv)
    GUI = MainWindow(app=app)
    GUI.show()
    app.exec_()


if __name__ == '__main__':
    main()
