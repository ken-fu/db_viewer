# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTreeView, QAbstractItemView
from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractTableModel

class MyTableModel(QAbstractTableModel):
    def __init__(self, list, headers=[], parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.list = list
        self.headers = headers

    def rowCount(self, parent):
        return len(self.list)

    def columnCount(self, parent):
        return len(self.list[0])

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):
        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            return self.list[row][column]

        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.list[row][column]
            return value
    
    def display_data(self, index):
        return_data = []
        for i in range(len(self.list[0])):
            return_data.append(self.list[index.row()][i])
        return return_data

    def setData(self, index, value, role = Qt.EditRole):
        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            self.list[row][column] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role):

        if role == Qt.DisplayRole:

            if orientation == Qt.Horizontal:

                if section < len(self.headers):
                    return self.headers[section]
                # else:
                #     return "not implemented"
            else:
                return "item %d" % section

class MainTreeView(QTreeView):
    def __init__(self, parent=None):
        super(MainTreeView, self).__init__(parent)
        self.setItemsExpandable(False)
        self.setIndentation(0)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def drawBranches(self, painter, rect, index):
        return
