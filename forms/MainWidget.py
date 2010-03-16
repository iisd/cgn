#-*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import string

class MainWidget(QtGui.QWidget):


    def NewTab(self):
        self.currentTab = PhiloTab()
        self.TabWidget.addTab(self.currentTab, "Tab1")

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.TabWidget = QtGui.QTabWidget()
        self.NewTab()

        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(self.TabWidget)

    def OpenList(self):
        return

class PhiloTab(QtGui.QWidget):

    currentItem = QtGui.QListWidgetItem()
    currentItem.desc = ''

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.lvThesis = QtGui.QListWidget()
        self.lvThesis.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
        self.lvThesis.setSortingEnabled(1)
        self.connect(self.lvThesis, QtCore.SIGNAL('itemSelectionChanged()'), 
                                                        self.SelectionChanged)

        spacer1 = QtGui.QSpacerItem(5, 0, QtGui.QSizePolicy.Minimum,
                                                QtGui.QSizePolicy.Maximum)

        self.teThesisView = QtGui.QTextEdit()

        spacer2 = QtGui.QSpacerItem(5, 0, QtGui.QSizePolicy.Minimum,
                                                QtGui.QSizePolicy.Maximum)

        Box = QtGui.QHBoxLayout(self)
        Box.addWidget(self.lvThesis)
        Box.addItem(spacer1)
        Box.addWidget(self.teThesisView)
        Box.addItem(spacer2)

    def SearchName(self, name):
        for i in xrange(self.lvThesis.count()):
            if name == self.lvThesis.item(i).text():
                return 1
        return 0
                
    def SaveListAs(self):
        return

    def OpenList(self):
        return

    def DelCurrentThesis(self):
        i = self.lvThesis.currentRow()
        if i < 0:
            return
        self.lvThesis.takeItem(i)
        

    def SelectionChanged(self):
        if self.lvThesis.currentRow() < 0:
            self.teThesisView.setText('')
            self.currentItem = QtGui.QListWidgetItem()
            return
        self.currentItem.desc = self.teThesisView.toPlainText()
        self.currentItem = self.lvThesis.currentItem()
        self.teThesisView.setText(self.currentItem.desc)

    def AddNewThesis(self):
        i = 0
        name = 'New Thesis'
        tmp = ''
        while self.SearchName(name + tmp) == 1:
            i += 1
            if i < 10:
                tmp = str(0) + str(i)
            else:
                tmp = str(i)
        if 0 < i < 10:
            name += str(0) + str(i)
        elif i >= 10:
            name += str(i)
        tmp = QtGui.QListWidgetItem(name)
        tmp.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable
                                                    | QtCore.Qt.ItemIsEnabled)
        tmp.desc = ''
        self.lvThesis.addItem(tmp)
        self.lvThesis.setCurrentItem(tmp)
