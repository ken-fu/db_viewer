# -*- coding: utf-8 -*-
import pyperclip
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QTreeView, QComboBox, QTextEdit, QLineEdit
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

        
        self.show()
    
    def create_tree(self):
        self.mainTree = QTreeView(self)
        self.mainTree.move(10,50)
        self.mainTree.setFixedSize(430,600)
    
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

        self.B_DR = QPushButton("Go",self)
        self.B_DR.move(1000,10)

        self.L_search = QLabel("Keyword Search",self)
        self.L_search.move(450,50)
        self.TB_search = QLineEdit(self)
        self.TB_search.setFixedWidth(400)
        self.TB_search.move(600,50)
        self.B_search = QPushButton("Go",self)
        self.B_search.move(1000,45)


        self.L_TFilter = QLabel("Tag Filter",self)
        self.L_TFilter.move(450,85)
        self.CB_TFilter = QComboBox(self)
        self.CB_TFilter.addItems(self.Tag_list)
        self.CB_TFilter.move(600,80)
        self.CB_TFilter.setFixedWidth(150)
        self.B_TFilter = QPushButton("Go",self)
        self.B_TFilter.move(1000,80)

        self.B_reset = QPushButton("Filter Reset",self)
        self.B_reset.move(900,115)
    
    def create_widgets(self):
        self.article_list = get_all_database()

        self.CB_article = QComboBox(self)
        self.CB_article.addItem("----")
        self.CB_article.addItems(self.article_list)
        self.CB_article.move(15,10)

        self.B_output = QPushButton("Output",self)
        self.B_output.move(220,10)

        self.B_TagEdit = QPushButton("Tag Edit",self)
        self.B_TagEdit.move(320,10)

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
        
        self.L_Tag = QLabel("Tag",self)
        self.L_Tag.move(800,350)
        self.TB_Tag = QLineEdit(self)
        self.TB_Tag.move(800,370)
        self.TB_Tag.setFixedWidth(120)
        self.B_Tag = QPushButton("Write",self)
        self.B_Tag.move(920,335)
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

        self.B_trans = QPushButton("En -> Jp",self)
        self.B_trans.move(550,400)
        self.B_Ttrans = QPushButton("En -> Jp",self)
        self.B_Ttrans.move(550,120)

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


if __name__ == '__main__':

    app = QApplication(sys.argv)
    mw = MainWidget()    
    sys.exit(app.exec_())