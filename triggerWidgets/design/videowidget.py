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

# Form implementation generated from reading ui file 'videowidget.ui'
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
        self.standard = QtGui.QComboBox(Form)
        self.standard.setObjectName(_fromUtf8("standard"))
        self.standard.addItem(_fromUtf8(""))
        self.standard.addItem(_fromUtf8(""))
        self.standard.addItem(_fromUtf8(""))
        self.standard.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.standard)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.mode = QtGui.QComboBox(Form)
        self.mode.setObjectName(_fromUtf8("mode"))
        self.mode.addItem(_fromUtf8(""))
        self.mode.addItem(_fromUtf8(""))
        self.mode.addItem(_fromUtf8(""))
        self.mode.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.mode)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.line = QtGui.QLineEdit(Form)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout.addWidget(self.label_6)
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
        self.label_3.setText(_translate("Form", "Standard", None))
        self.standard.setItemText(0, _translate("Form", "NTSC", None))
        self.standard.setItemText(1, _translate("Form", "PAL/Secam", None))
        self.standard.setItemText(2, _translate("Form", "480p", None))
        self.standard.setItemText(3, _translate("Form", "576p", None))
        self.label_4.setText(_translate("Form", "Mode", None))
        self.mode.setItemText(0, _translate("Form", "Odd Field", None))
        self.mode.setItemText(1, _translate("Form", "Even Field", None))
        self.mode.setItemText(2, _translate("Form", "Line", None))
        self.mode.setItemText(3, _translate("Form", "All Lines", None))
        self.label_5.setText(_translate("Form", "Line", None))
        self.label_6.setText(_translate("Form", "Level", None))

