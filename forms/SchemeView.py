#-*- coding: utf-8 -*-

import sys, string
from PyQt4 import QtCore, QtGui

class SchemeView(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        self.setBackgroundBrush(QtGui.QBrush())

        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)
        self.scene.setSceneRect(QtCore.QRectF(-200, -200, 400, 400))

        self.setRenderHint(QtGui.QPainter.Antialiasing)

        self.arrows = Arrows(self.itemsOnScheme)
        self.scene.addItem(self.arrows)
        self.setCursor(QtCore.Qt.OpenHandCursor)

    curPos = QtCore.QPointF(0, 0)
    itemsOnScheme = {}
    setLink = 0

    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            event.ignore()
            return
        self.sp = event.pos()
        items = self.items(event.pos())
        if len(items) < 2:
            self.setCursor(QtCore.Qt.ArrowCursor)
            return

        self.cur = items[1]

        if self.setLink == 1:
            self.setLink = 0
            link = self.SearchByView(self.cur)
            self.setCursor(QtCore.Qt.ArrowCursor)
            if (len(self.curItem.links) < 3) & (link != self.curItem):
                self.curItem.links.append(link.text())
        else:
           self.setCursor(QtCore.Qt.ClosedHandCursor)
           self.move = 1
        self.update()
        self.arrows.update()

    def mouseReleaseEvent(self, event):
        if self.move == 1:
            self.setCursor(QtCore.Qt.OpenHandCursor)
            self.move = 0

    def mouseMoveEvent(self, event):
        if self.move == 1:
            dp = event.pos() - self.sp
            self.sp = event.pos()

            self.cur.moveBy(dp.x(), dp.y())
            self.arrows.update()

    def mouseDoubleClickEvent(self, event):
        items = self.items(event.pos())
        if len(items) < 2:
            self.setCursor(QtCore.Qt.ArrowCursor)
            return
        cur = items[1]
        if self.setLink == 0:
            self.setLink = 1
            self.curItem = self.SearchByView(cur)
            self.setCursor(QtCore.Qt.CrossCursor)
        self.update()
        self.arrows.update()

    def SearchByView(self, view):
        for key in self.itemsOnScheme:
            for item in self.itemsOnScheme[key]:
                if item == view:
                    return key
        return 0

    def delThesis(self, thesis):
        if self.itemsOnScheme.has_key(thesis):
            for item in self.itemsOnScheme[thesis]:
                self.scene.removeItem(item)
            self.scene.update()
            self.itemsOnScheme.pop(thesis)
        self.setLink = 0
        self.setCursor(QtCore.Qt.OpenHandCursor)

    def clear(self):
        self.scene.clear()
        self.itemsOnScheme = {}
        self.arrows = Arrows(self.itemsOnScheme)
        self.scene.addItem(self.arrows)
        self.setLink = 0
        self.setCursor(QtCore.Qt.OpenHandCursor)

    def setColorOfThesis(self, thesis, color = QtCore.Qt.white):
        if self.itemsOnScheme.has_key(thesis):
            for item in self.itemsOnScheme[thesis]:
                item.setColor(color)

    def addThesis(self, thesis, color = QtCore.Qt.white, x = None, y = None):
        if not self.itemsOnScheme.has_key(thesis):
            self.itemsOnScheme[thesis] = []
        if (x == None) | (y == None):
            pos = self.curPos
            self.curPos += QtCore.QPointF(10, 10)
        else:
            pos = QtCore.QPointF(x, y)
        item = ThesisView(thesis, color)
        item.setPos(pos)
        self.itemsOnScheme[thesis].append(item)
        self.scene.addItem(item)
        self.arrows.updateDic(self.itemsOnScheme)
        self.setLink = 0
        self.setCursor(QtCore.Qt.OpenHandCursor)
        

class Arrows(QtGui.QGraphicsItem):
    def __init__(self, dic):
        QtGui.QGraphicsItem.__init__(self)
        self.dic = dic
        self.setZValue(100)

    def updateDic(self, dic):
        self.update()
        self.dic = dic

    def SearchThesis(self, name):
        for key in self.dic.keys():
            if key.text() == name:
                return key
        return 0

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        for key in self.dic.keys():
            for link in key.links:
                thesis = self.SearchThesis(link)
                if thesis != 0:
                    for start in self.dic[key]:
                        StartPoint = QtCore.QPointF(start.x(), start.y())
                        for end in self.dic[thesis]:
                            EndPoint = QtCore.QPointF(end.x(), end.y())
                            painter.drawLine(StartPoint, EndPoint)
                            
                

    def boundingRect(self):
        return QtCore.QRectF(-200, -200, 400, 400)

class ThesisView(QtGui.QGraphicsItem):

    form = QtCore.QRectF(-55, -20, 110, 40)

    def __init__(self, item = QtGui.QListWidgetItem(),
                                    color = QtCore.Qt.white):
        QtGui.QGraphicsItem.__init__(self)
        self.color = color
        self.item = item
        self.setZValue(0)

    def setColor(self, color):
        self.color = color
        self.update()

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawRect(self.form)
        font = painter.font()
        font.setPixelSize(12)
        painter.setFont(font)
        painter.drawText(self.form,
                            QtCore.Qt.AlignCenter, self.item.text())

    def boundingRect(self):
        x, y, w, h = self.form.getRect()
        return QtCore.QRectF(x - 0.5, y - 0.5, w + 1, h + 1)
