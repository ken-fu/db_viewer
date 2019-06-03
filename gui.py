# -*- coding: utf-8 -*-
import pyperclip
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QTreeView, QComboBox, QTextEdit, QLineEdit, QAbstractItemView, QCheckBox, QDialog, QProgressBar, QMessageBox
from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractTableModel
import sqlite3
import importlib
from sql_manager import SqlManager
import threading
import re
import configparser

import translate
from output import Output_for_GUI
from folder_check import get_all_database
from ini_sorter import ini_sorter

class MyTableModel(QAbstractTableModel):
    def __init__(self, list, headers = [], parent = None):
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

class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(1080, 720)
        self.move(100, 100)
        self.setWindowTitle('Database Viewer')

        self.import_tag()
        self.create_tree()
        self.create_filter_widgets()
        self.create_widgets()

        self.headers = ["Add Date", "T", "C","Title"]
        
        self.show()
    
    def create_tree(self):
        self.mainTree = MainTreeView(self)
        self.mainTree.move(10,50)
        self.mainTree.setFixedSize(430,600)
        self.mainTree.clicked.connect(self.update_text)
        self.mainTree.setEditTriggers(QAbstractItemView.NoEditTriggers)
    
    def create_filter_widgets(self):
        self.L_DR = QLabel("Publish Date Range",self)
        self.L_DR.move(450,15)

        self.CB_Y = QComboBox(self)
        self.CB_Y.addItems(["2015","2016","2017","2018","2019","2020","2021","2022","2023"])
        self.CB_Y.move(600,10)
        self.CB_Y.setFixedWidth(80)

        self.CB_M = QComboBox(self)
        for temp_mon in range(1,13):
            self.CB_M.addItem(str(temp_mon))
        self.CB_M.move(670,10)
        self.CB_M.setFixedWidth(60)

        self.CB_D = QComboBox(self)
        for temp_day in range(1,32):
            self.CB_D.addItem(str(temp_day))
        self.CB_D.move(720,10)
        self.CB_D.setFixedWidth(60)

        self.label_combo = QLabel("~",self)
        self.label_combo.move(780,15)

        self.CB_2Y = QComboBox(self)
        self.CB_2Y.addItems(["2015","2016","2017","2018","2019","2020","2021","2022","2023"])
        self.CB_2Y.move(800,10)
        self.CB_2Y.setFixedWidth(80)

        self.CB_2M = QComboBox(self)
        for temp_mon in range(1,13):
            self.CB_2M.addItem(str(temp_mon))
        self.CB_2M.move(870,10)
        self.CB_2M.setFixedWidth(60)

        self.CB_2D = QComboBox(self)
        for temp_day in range(1,32):
            self.CB_2D.addItem(str(temp_day))
        self.CB_2D.move(920,10)
        self.CB_2D.setFixedWidth(60)

        self.ChB_DR = QCheckBox("",self)
        self.ChB_DR.move(1005,15)
        self.ChB_DR.stateChanged.connect(self.filter_check)

        self.L_search = QLabel("Keyword Search",self)
        self.L_search.move(450,50)
        self.TB_search = QLineEdit(self)
        self.TB_search.setFixedWidth(400)
        self.TB_search.move(600,50)
        self.ChB_search = QCheckBox("",self)
        self.ChB_search.move(1005,50)
        self.ChB_search.stateChanged.connect(self.filter_check)


        self.L_TFilter = QLabel("Tag Filter",self)
        self.L_TFilter.move(450,85)
        self.CB_TFilter = QComboBox(self)
        self.CB_TFilter.addItems(self.Tag_list)
        self.CB_TFilter.move(600,80)
        self.CB_TFilter.setFixedWidth(150)
        self.ChB_TFilter = QCheckBox("",self)
        self.ChB_TFilter.move(1005,85)
        self.ChB_TFilter.stateChanged.connect(self.filter_check)

    
    def create_widgets(self):
        self.article_list = get_all_database()

        self.CB_article = QComboBox(self)
        self.CB_article.addItem("----")
        self.CB_article.addItems(self.article_list)
        self.CB_article.move(15,10)
        self.CB_article.activated[str].connect(self.import_database)

        self.B_output = QPushButton("Output",self)
        self.B_output.move(220,10)
        self.B_output.clicked.connect(self.create_output_sub_win)

        self.B_TagEdit = QPushButton("Tag Edit",self)
        self.B_TagEdit.move(320,10)
        self.B_TagEdit.clicked.connect(self.create_tag_edit_sub_win)
        

        self.L_title = QLabel("Title",self)
        self.L_title.move(450,130)
        self.TB_title = QTextEdit(self)
        self.TB_title.move(450,150)
        self.TB_title.setFixedSize(600,42)

        self.L_FA = QLabel("First Auther",self)
        self.L_FA.move(450,200)
        self.TB_FA = QLineEdit(self)
        self.TB_FA.move(450,220)
        self.TB_FA.setFixedWidth(420)

        self.L_PD = QLabel("Publish Date",self)
        self.L_PD.move(900,200)
        self.TB_PD = QLineEdit(self)
        self.TB_PD.move(900,220)
        self.TB_PD.setFixedWidth(150)

        self.L_RG = QLabel("Research Group",self)
        self.L_RG.move(450,250)
        self.TB_RG = QTextEdit(self)
        self.TB_RG.move(450,270)
        self.TB_RG.setFixedSize(600,60)

        self.L_doi = QLabel("DOI",self)
        self.L_doi.move(450,350)
        self.TB_doi = QLineEdit(self)
        self.TB_doi.move(450,370)
        self.TB_doi.setFixedWidth(330)
        self.B_doi = QPushButton("Copy",self)
        self.B_doi.move(550,335)
        self.B_doi.clicked.connect(self.doi_copy)
        
        self.L_Tag = QLabel("Tag",self)
        self.L_Tag.move(800,350)
        self.TB_Tag = QLineEdit(self)
        self.TB_Tag.move(800,370)
        self.TB_Tag.setFixedWidth(120)
        self.B_Tag = QPushButton("Write",self)
        self.B_Tag.move(920,335)
        self.B_Tag.clicked.connect(self.tag_write)
        self.CB_Tag = QComboBox(self)
        self.CB_Tag.addItems(self.Tag_list)
        self.CB_Tag.move(920,365)
        self.CB_Tag.setFixedWidth(150)

        self.L_abst = QLabel("Abstract",self)
        self.L_abst.move(450,410)
        self.TB_abst = QTextEdit(self)
        self.TB_abst.move(450,430)
        self.TB_abst.setFixedSize(600,220)

        self.B_comment = QPushButton("Comment",self)
        self.B_comment.move(450,660)
        self.comment_data = ''
        self.B_comment.clicked.connect(self.create_comment_sub_win)

        self.B_trans = QPushButton("En -> Jp",self)
        self.B_trans.move(550,400)
        self.B_trans.clicked.connect(self.abst_translate)
        self.B_Ttrans = QPushButton("En -> Jp",self)
        self.B_Ttrans.move(550,120)
        self.B_Ttrans.clicked.connect(self.title_translate)
    
    # Update the tree according to the selected journal
    # paper_view_list is for display and is rewritten by filtering
    def set_tree(self):
        self.model = MyTableModel(self.paper_view_list, self.headers)
        self.mainTree.setModel(self.model)
        self.mainTree.setColumnWidth(0,90)
        self.mainTree.setColumnWidth(1,30)
        self.mainTree.setColumnWidth(2,5)
        self.mainTree.setColumnWidth(3,270)
        self.mainTree.hideColumn(4)
        self.mainTree.hideColumn(5)
        self.mainTree.hideColumn(6)
        self.mainTree.hideColumn(7)
        self.mainTree.hideColumn(8)
        self.mainTree.hideColumn(9)

    def import_tag(self):
        while True:
            try:
                file = open('tag_config.ini', 'r')
                file.close()
                break
            except FileNotFoundError:
                file = open('tag_config.ini', 'a+')
                file.write('[Tag]\n')
                file.write('00 = Tag\n')
                file.close()
                break
            
        self.conf_parser = configparser.ConfigParser()
        self.conf_parser.read('tag_config.ini')
        self.item_list = list(self.conf_parser['Tag'])
        self.Tag_list = []
        for item in self.item_list:
            self.Tag_list.append(item+":"+self.conf_parser['Tag'][item])

    def import_database(self,article_name):
        if article_name == '----' :
            return
        
        self.c = sqlite3.connect('database/'+ article_name +'.db')
        self.c.execute("PRAGMA foreign_keys = 1")
        

        sql = "select * from data_set"
        self.paper_list = []
        for row in list(self.c.execute(sql))[::-1]:
            #self.paper_list.append(r)
            self.temp_comment_data = ''
            if re.sub('\s','',row[8]) != '':
                self.temp_comment_data = '*'

            row_out = (row[6],row[7],self.temp_comment_data,row[0],row[1],row[2],row[3],row[4],row[5],row[8])
            self.paper_list.append(row_out)
            
        self.paper_view_list = self.paper_list[:]
        self.set_tree()

    def update_text(self):
        index = self.mainTree.selectedIndexes()[0]
        temp_data = self.model.display_data(index)
        self.TB_title.setText(temp_data[3])
        self.TB_abst.setText(temp_data[4])
        self.TB_FA.setText(temp_data[5])
        self.TB_RG.setText(temp_data[6])
        self.TB_doi.setText(temp_data[7])
        self.TB_PD.setText(temp_data[8])
        if(temp_data[1].zfill(2) != '00'):
            self.TB_Tag.setText(self.conf_parser['Tag'][temp_data[1].zfill(2)])
        self.comment_data = temp_data[9]
    
    def reset_text(self):
        self.TB_title.clear()
        self.TB_abst.clear()
        self.TB_FA.clear()
        self.TB_RG.clear()
        self.TB_doi.clear()
        self.TB_PD.clear()
        self.TB_Tag.clear()
        self.comment_data = ''

    def title_translate(self,event):
        title_text = self.TB_title.toPlainText()
        title_jp = translate.translater(title_text)
        self.TB_title.setText(title_jp)

    def abst_translate(self,event):
        abst_text = self.TB_abst.toPlainText()
        abst_jp = translate.translater(abst_text)
        self.TB_abst.setText(abst_jp)
    
    def doi_copy(self,event):
        pyperclip.copy(self.TB_doi.text())
    
    # Write tag information of selected articles in database
    def tag_write(self,event):
        self.SQL_M = SqlManager(self.CB_article.currentText()+'.db')
        self.SQL_M.write_tag_data(self.CB_Tag.currentText().split(':')[0], re.sub('\s','', self.TB_doi.text()))
        self.import_database(self.CB_article.currentText())
        self.filter_check()
    
    def filter_by_keyword(self):
        # Find out whether there is a list to filter
        try:
            self.paper_view_list
        except AttributeError:
            return
        
        filter_words = self.TB_search.text()
        filter_words = re.sub('\s','', filter_words)
        if (filter_words == ''):
            return
        self.paper_temp_list = self.paper_view_list[:]
        self.paper_view_list = []
        for row in self.paper_temp_list:
            # Determine whether the title or abst contains keywords
            if (filter_words.lower() in row[3].lower() or filter_words.lower() in row[4].lower()):
                self.paper_view_list.append(row)
    
    def filter_by_date_range(self):
        try:
            self.paper_view_list
        except AttributeError:
            return
        self.startdate = int(self.CB_Y.currentText() + self.CB_M.currentText().zfill(2) + self.CB_D.currentText().zfill(2))
        self.enddate = int(self.CB_2Y.currentText() + self.CB_2M.currentText().zfill(2) + self.CB_2D.currentText().zfill(2))
        self.paper_temp_list = self.paper_view_list[:]
        self.paper_view_list = []
        for row in self.paper_temp_list:
            # Determine whether it is within the specified period
            p_date_list = row[8].split('-')
            p_date = p_date_list[0] + p_date_list[1].zfill(2) + p_date_list[2].zfill(2)
            if (int(p_date) >= self.startdate and int(p_date) <= self.enddate):
                self.paper_view_list.append(row)

    def filter_by_tag(self):
        try:
            self.paper_view_list
        except AttributeError:
            return
        self.paper_temp_list = self.paper_view_list[:]
        self.paper_view_list = []
        for row in self.paper_temp_list:
            # Check that the selected tag matches the item in the list
            if (row[1].replace('-','').zfill(2) == self.CB_TFilter.currentText().split(':')[0]):
                self.paper_view_list.append(row)
    
    def filter_check(self):
        self.paper_view_list = self.paper_list[:]
        if self.ChB_search.checkState() == Qt.Checked:
            self.filter_by_keyword()
        if self.ChB_DR.checkState() == Qt.Checked:
            self.filter_by_date_range()
        if self.ChB_TFilter.checkState() == Qt.Checked:
            self.filter_by_tag()
        self.set_tree()
    
    def create_tag_edit_sub_win(self):
        self.TagEdit_SW = TagEditSubWin(self)
        self.TagEdit_SW.show()
        self.import_tag()
        self.CB_Tag.clear()
        self.CB_Tag.addItems(self.Tag_list)
        self.CB_TFilter.clear()
        self.CB_TFilter.addItems(self.Tag_list)
    
    def create_output_sub_win(self):
        self.Out_SW = OutputSubWin(self.paper_view_list,self)
        self.Out_SW.show()
    
    def create_comment_sub_win(self):
        temp_article = self.CB_article.currentText()
        temp_doi = self.TB_doi.text()
        self.Comment_SW = CommentSubWin(temp_article,self.comment_data,temp_doi,self)
        self.Comment_SW.show()
        self.import_database(temp_article)
        self.set_tree()
        self.reset_text()

class TagEditSubWin(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.resize(400,300)
        self.import_tag()
        self.create_widgets()
    
    def create_widgets(self):
        self.make_sub_tree()
        self.set_sub_tree()
        self.B_add_newtag = QPushButton('Add new tag',self)
        self.B_add_newtag.move(230,60)
        self.B_add_newtag.clicked.connect(self.add_tag)

        self.TB_rename_tag_num = QLineEdit(self)
        self.TB_rename_tag_num.move(230,100)
        self.TB_rename_tag_num.setFixedWidth(30)
        self.TB_rename_tag = QLineEdit(self)
        self.TB_rename_tag.move(270,100)
        self.TB_rename_tag.setFixedWidth(120)
        self.B_rename_tag = QPushButton('Rename select tag',self)
        self.B_rename_tag.move(230,130)
        self.B_rename_tag.clicked.connect(self.rename_tag)
        self.B_del_tag = QPushButton('Delete tad',self)
        self.B_del_tag.move(230,160)
        self.B_del_tag.clicked.connect(self.del_tag)

    def import_tag(self):
        self.conf_parser = configparser.ConfigParser()
        self.conf_parser.read('tag_config.ini')
        self.item_list = list(self.conf_parser['Tag'])
        self.Tag_list = []
        for item in self.item_list:
            self.Tag_list.append([item,self.conf_parser['Tag'][item]])
    
    def add_tag(self,event):
        for num in range(1,100):
            if(str(num).zfill(2) not in self.item_list):
                self.conf_parser.set('Tag',str(num).zfill(2),'')
                self.conf_parser.write(open('tag_config.ini','w'))
                ini_sorter()
                break
        self.import_tag()
        self.set_sub_tree()
    
    def rename_tag(self,event):
        self.tag_num = re.sub('\s','', self.TB_rename_tag_num.text())
        self.tag_name = re.sub('\s','', self.TB_rename_tag.text())
        self.conf_parser.set('Tag',self.tag_num,self.tag_name)
        self.conf_parser.write(open('tag_config.ini','w'))

        self.import_tag()
        self.set_sub_tree()
    
    def del_tag(self, event):
        self.tag_num = re.sub('\s','', self.TB_rename_tag_num.text())
        self.conf_parser.remove_option('Tag',self.tag_num)
        self.conf_parser.write(open('tag_config.ini','w'))

        self.import_tag()
        self.set_sub_tree()

    def make_sub_tree(self):
        self.subTree = MainTreeView(self)
        self.subTree.move(10,10)
        self.subTree.setFixedSize(200,250)
        self.subTree.clicked.connect(self.sub_win_text_change)
        self.subTree.setEditTriggers(QAbstractItemView.NoEditTriggers)
    
    def set_sub_tree(self):
        self.model = MyTableModel(self.Tag_list,["Num","Name"])
        self.subTree.setModel(self.model)
            
    
    def sub_win_text_change(self):
        index = self.subTree.selectedIndexes()[0]
        temp_data = self.model.display_data(index)
        self.TB_rename_tag_num.setText(temp_data[0])
        self.TB_rename_tag.setText(temp_data[1])
        

    def show(self):
        self.exec_()

class CommentSubWin(QDialog):
    def __init__(self, article, comment, doi, parent=None):
        QDialog.__init__(self, parent)
        self.resize(380,300)
        self.article = article
        self.comment = comment
        self.doi = doi
        self.create_widgets()
        
    def create_widgets(self):
        self.TB_comment = QTextEdit(self)
        self.TB_comment.resize(340,240)
        self.TB_comment.move(20,5)
        self.TB_comment.setText(self.comment)
        self.B_comment = QPushButton('Save and close window', self)
        self.B_comment.move(20,250)
        self.B_comment.clicked.connect(self.comment_save)
    
    def comment_save(self):
        self.SQL_M = SqlManager(self.article+'.db')
        self.SQL_M.write_comment_data(self.TB_comment.toPlainText(), self.doi)
        self.close()
    
    def show(self):
        self.exec_()

class OutputSubWin(QDialog):
    def __init__(self,paper_view_list, parent=None):
        QDialog.__init__(self, parent)
        self.resize(400,300)
        self.paper_view_list = paper_view_list
        self.create_widgets()
        
    
    def create_widgets(self):
        

        self.ChB_title = QCheckBox("Title", self)
        self.ChB_title.move(50,25)
        self.ChB_FA = QCheckBox("First Auther", self)
        self.ChB_FA.move(50,50)
        self.ChB_RG = QCheckBox("Research Group", self)
        self.ChB_RG.move(50,75)
        self.ChB_doi = QCheckBox("DOI", self)
        self.ChB_doi.move(50,100)
        self.ChB_PD = QCheckBox("Publish Date", self)
        self.ChB_PD.move(50,125)
        self.ChB_abst = QCheckBox("Abstract", self)
        self.ChB_abst.move(50,150)
        self.ChB_comment = QCheckBox("Comment", self)
        self.ChB_comment.move(50,175)

        self.CB_output_mode = QComboBox(self)
        self.CB_output_mode.addItems(["csv","pdf"])
        self.CB_output_mode.move(50,200)

        self.B_search = QPushButton('Go',self)
        self.B_search.move(250,200)
        self.B_search.clicked.connect(self.output_paper_data)

        self.PB_progress = [0,len(self.paper_view_list)]
        self.PB_out = QProgressBar(self)
        self.PB_out.move(250,230)


    def output_paper_data(self,event):
        ValTitle = (self.ChB_title.checkState() == Qt.Checked)
        ValFA = (self.ChB_FA.checkState() == Qt.Checked)
        ValRG = (self.ChB_RG.checkState() == Qt.Checked)
        Valdoi = (self.ChB_doi.checkState() == Qt.Checked)
        ValPD = (self.ChB_PD.checkState() == Qt.Checked)
        Valabst = (self.ChB_abst.checkState() == Qt.Checked)
        Valcomment = (self.ChB_comment.checkState() == Qt.Checked)

        OfG = Output_for_GUI()
        if(self.CB_output_mode.currentText() == 'csv'):
            OfG.output_to_csv(self.paper_view_list, [False, False, False, ValTitle, Valabst
            , ValFA, ValRG, Valdoi, ValPD, Valcomment], self.PB_out, self.PB_progress)
            self.MB = QMessageBox.information(self,"","Finish !!!",QMessageBox.Close)
            if self.MB:
                self.close()
        else:
            OfG.output_to_pdf(self.paper_view_list, [False, False, False, ValTitle, Valabst
            , ValFA, ValRG, Valdoi, ValPD, Valcomment], self.PB_out, self.PB_progress)
            self.MB = QMessageBox.information(self,"","Finish !!!",QMessageBox.Close)
            if self.MB:
                self.close()
    
    def show(self):
        self.exec_()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    mw = MainWidget()    
    sys.exit(app.exec_())
