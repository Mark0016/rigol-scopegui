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
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pulsewidget.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(156, 470)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.source = QtGui.QComboBox(Form)
        self.source.setObjectName(_fromUtf8("source"))
        self.source.addItem(_fromUtf8(""))
        self.source.addItem(_fromUtf8(""))
        self.source.addItem(_fromUtf8(""))
        self.source.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.source)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.polarity = QtGui.QComboBox(Form)
        self.polarity.setObjectName(_fromUtf8("polarity"))
        self.polarity.addItem(_fromUtf8(""))
        self.polarity.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.polarity)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.when = QtGui.QComboBox(Form)
        self.when.setObjectName(_fromUtf8("when"))
        self.when.addItem(_fromUtf8(""))
        self.when.addItem(_fromUtf8(""))
        self.when.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.when)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.pulseWidth = QtGui.QLineEdit(Form)
        self.pulseWidth.setObjectName(_fromUtf8("pulseWidth"))
        self.verticalLayout.addWidget(self.pulseWidth)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.level = QtGui.QLineEdit(Form)
        self.level.setObjectName(_fromUtf8("level"))
        self.verticalLayout.addWidget(self.level)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Source", None))
        self.source.setItemText(0, _translate("Form", "CH1", None))
        self.source.setItemText(1, _translate("Form", "CH2", None))
        self.source.setItemText(2, _translate("Form", "CH3", None))
        self.source.setItemText(3, _translate("Form", "CH4", None))
        self.label_2.setText(_translate("Form", "Polarity", None))
        self.polarity.setItemText(0, _translate("Form", "Positive", None))
        self.polarity.setItemText(1, _translate("Form", "Negative", None))
        self.label_3.setText(_translate("Form", "When", None))
        self.when.setItemText(0, _translate("Form", "Greater", None))
        self.when.setItemText(1, _translate("Form", "Less", None))
        self.when.setItemText(2, _translate("Form", "Interval", None))
        self.label_4.setText(_translate("Form", "PulseWidth", None))
        self.label_5.setText(_translate("Form", "Level", None))

