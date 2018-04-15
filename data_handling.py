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

import vxi11
from PyQt4 import QtCore
from numpy import linspace, array


def timeoutHandler(func):
    def f(*a,**kwa):
        try:
            func(*a,**kwa)
        except vxi11.vxi11.Vxi11Exception:
            pass
    return f
                

class DataThread(QtCore.QThread):

    updated = QtCore.pyqtSignal(list,list,int)

    def __init__(self,ip,channel=1,zeroPoint=127,fullRange=200,perf=False):
        super(self.__class__,self).__init__()
        
        self.channel = channel
        self.ip = ip
        self.z = zeroPoint
        self.r = fullRange
        self.perf = perf

        self.first = True

        self.scope = vxi11.Instrument(self.ip)
        
        

    def run(self):

        if self.first:
            self.setup()
            self.first = False

        if not self.perf:
            self.updateChScale()
            self.updateChOffset()
            self.updateTbScale()
        
        self.updateChannel()
        self.updateData()
        
    @timeoutHandler
    def setup(self):

        self.scope = vxi11.Instrument(self.ip)
        self.scope.timeout = 200

        self.scope.write(':WAV:MODE NORM')
        self.scope.write(':WAV:FORM BYTE')
        self.updateChannel()
        self.updateChScale()
        self.updateChOffset()
        self.updateTbScale()

    @timeoutHandler
    def updateData(self):

        yd = self.processedData()
        tbr = self.tbscal*12
        xd = list(linspace(0,tbr,len(yd)))

        self.updated.emit(xd,yd,self.channel)


    def processedData(self):

        d = array(list(self._getRawData()))

        u = self.chscal*8/self.r
        os = self.choffs

        return list((d-self.z)*u-os)

    def updateChannel(self):
        self.scope.write(':WAV:SOUR CHAN{}'.format(self.channel))

    def updateChScale(self):
        self.chscal = float(self.scope.ask(':CHAN{}:SCAL?'.format(self.channel)))

    def updateTbScale(self):
        self.tbscal = float(self.scope.ask(':TIM:SCAL?'))

    def updateChOffset(self):
        self.choffs = float(self.scope.ask(':CHAN{}:OFFS?'.format(self.channel)))
        

    def _getRawData(self):

        fd = self.scope.ask_raw(':WAV:DATA?'.encode('utf-8'))
        hl = int(chr(fd[1]))+2
        rd = fd[hl:-1]
        return rd

class XYThread(QtCore.QThread):

    updated = QtCore.pyqtSignal(list,list,int)

    def __init__(self,ip,xchannel=1,ychannel=2,zeroPoint=127,fullRange=200):
        super(self.__class__,self).__init__()
        
        self.xchannel = xchannel
        self.ychannel = ychannel
        self.ip = ip
        self.z = zeroPoint
        self.r = fullRange

    @timeoutHandler
    def run(self):

        self.setupX()
        xd = self.processedXData()

        self.setupY()
        yd = self.processedYData()

        self.updated.emit(xd,yd,1)
        

    def setupX(self):

        self.scope = vxi11.Instrument(self.ip)
        self.scope.timeout = 200

        self.scope.write(':WAV:SOUR CHAN%d'%self.xchannel)
        self.scope.write(':WAV:MODE NORM')
        self.scope.write(':WAV:FORM BYTE')

    def setupY(self):

        self.scope = vxi11.Instrument(self.ip)
        self.scope.timeout = 200

        self.scope.write(':WAV:SOUR CHAN%d'%self.ychannel)
        self.scope.write(':WAV:MODE NORM')
        self.scope.write(':WAV:FORM BYTE')




    def processedXData(self):

        d = array(list(self._getRawData()))

        u = float(self.scope.ask(':CHAN%d:SCAL?'%self.xchannel))*8/self.r
        os = float(self.scope.ask(':CHAN%d:OFFS?'%self.xchannel))

        return list((d-self.z)*u-os)

    def processedYData(self):

        d = array(list(self._getRawData()))

        u = float(self.scope.ask(':CHAN%d:SCAL?'%self.ychannel))*8/self.r
        os = float(self.scope.ask(':CHAN%d:OFFS?'%self.ychannel))

        return list((d-self.z)*u-os)
        

    def _getRawData(self):

        fd = self.scope.ask_raw(':WAV:DATA?'.encode('utf-8'))
        hl = int(chr(fd[1]))+2
        rd = fd[hl:-1]
        return rd
    
    
