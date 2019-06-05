# -*- coding: utf-8 -*-
import sys
import sqlite3
import re
import configparser
import pyperclip

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QComboBox, QTextEdit
from PyQt5.QtWidgets import QLineEdit, QAbstractItemView, QCheckBox
from PyQt5.Qt import Qt




from file_manager.sql_manager import SqlManager
from file_manager.translate import translater
from file_manager.folder_check import get_all_database

from gui.base_widgets import MyTableModel, MainTreeView
from gui.sub_widgets import TagEditSubWin, CommentSubWin, OutputSubWin


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(1080, 720)
        self.move(100, 100)
        self.setWindowTitle('Database Viewer')

        self.import_tag()
        self.create_tree()
        self.create_filter_widgets()
        self.create_widgets()

        self.headers = ["Add Date", "T", "C", "Title"]
        self.show()
    
    def create_tree(self):
        '''create main tree widget'''
        self.main_tree = MainTreeView(self)
        self.main_tree.move(10, 50)
        self.main_tree.setFixedSize(430, 600)
        self.main_tree.clicked.connect(self.update_text)
        self.main_tree.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def create_filter_widgets(self):
        '''create filtering related widgets'''
        self.label_dr = QLabel("Publish Date Range", self)
        self.label_dr.move(450, 15)

        self.combobox_y = QComboBox(self)
        self.combobox_y.addItems(["2015", "2016", "2017", "2018",
                                  "2019", "2020", "2021", "2022", "2023"])
        self.combobox_y.move(600, 10)
        self.combobox_y.setFixedWidth(80)

        self.combobox_m = QComboBox(self)
        for temp_mon in range(1, 13):
            self.combobox_m.addItem(str(temp_mon))
        self.combobox_m.move(670, 10)
        self.combobox_m.setFixedWidth(60)

        self.combobox_d = QComboBox(self)
        for temp_day in range(1, 32):
            self.combobox_d.addItem(str(temp_day))
        self.combobox_d.move(720, 10)
        self.combobox_d.setFixedWidth(60)

        self.label_combo = QLabel("~", self)
        self.label_combo.move(780, 15)

        self.combobox_2y = QComboBox(self)
        self.combobox_2y.addItems(["2015", "2016", "2017", "2018",
                                   "2019", "2020", "2021", "2022", "2023"])
        self.combobox_2y.move(800, 10)
        self.combobox_2y.setFixedWidth(80)

        self.combobox_2m = QComboBox(self)
        for temp_mon in range(1, 13):
            self.combobox_2m.addItem(str(temp_mon))
        self.combobox_2m.move(870, 10)
        self.combobox_2m.setFixedWidth(60)

        self.combobox_2d = QComboBox(self)
        for temp_day in range(1, 32):
            self.combobox_2d.addItem(str(temp_day))
        self.combobox_2d.move(920, 10)
        self.combobox_2d.setFixedWidth(60)

        self.checkbox_dr = QCheckBox("", self)
        self.checkbox_dr.move(1005, 15)
        self.checkbox_dr.stateChanged.connect(self.filter_check)

        self.label_search = QLabel("Keyword Search", self)
        self.label_search.move(450, 50)
        self.textbox_search = QLineEdit(self)
        self.textbox_search.setFixedWidth(400)
        self.textbox_search.move(600, 50)
        self.checkbox_search = QCheckBox("", self)
        self.checkbox_search.move(1005, 50)
        self.checkbox_search.stateChanged.connect(self.filter_check)

        self.label_tagfilter = QLabel("Tag Filter", self)
        self.label_tagfilter.move(450, 85)
        self.combobox_tagfilter = QComboBox(self)
        self.combobox_tagfilter.addItems(self.tag_list)
        self.combobox_tagfilter.move(600, 80)
        self.combobox_tagfilter.setFixedWidth(150)
        self.checkbox_tagfilter = QCheckBox("", self)
        self.checkbox_tagfilter.move(1005, 85)
        self.checkbox_tagfilter.stateChanged.connect(self.filter_check)

    def create_widgets(self):
        '''create widgets on main window'''
        self.article_list = get_all_database()

        self.combobox_article = QComboBox(self)
        self.combobox_article.addItem("----")
        self.combobox_article.addItems(self.article_list)
        self.combobox_article.move(15, 10)
        self.combobox_article.activated[str].connect(self.import_database)

        self.pbutton_output = QPushButton("Output", self)
        self.pbutton_output.move(220, 10)
        self.pbutton_output.clicked.connect(self.create_output_sub_win)

        self.pbutton_tagedit = QPushButton("Tag Edit", self)
        self.pbutton_tagedit.move(320, 10)
        self.pbutton_tagedit.clicked.connect(self.create_tag_edit_sub_win)

        self.label_title = QLabel("Title", self)
        self.label_title.move(450, 130)
        self.textbox_title = QTextEdit(self)
        self.textbox_title.move(450, 150)
        self.textbox_title.setFixedSize(600, 42)

        self.label_fa = QLabel("First Auther", self)
        self.label_fa.move(450, 200)
        self.textbox_fa = QLineEdit(self)
        self.textbox_fa.move(450, 220)
        self.textbox_fa.setFixedWidth(420)

        self.label_pd = QLabel("Publish Date", self)
        self.label_pd.move(900, 200)
        self.textbox_pd = QLineEdit(self)
        self.textbox_pd.move(900, 220)
        self.textbox_pd.setFixedWidth(150)

        self.label_rg = QLabel("Research Group", self)
        self.label_rg.move(450, 250)
        self.textbox_rg = QTextEdit(self)
        self.textbox_rg.move(450, 270)
        self.textbox_rg.setFixedSize(600, 60)

        self.label_doi = QLabel("DOI", self)
        self.label_doi.move(450, 350)
        self.textbox_doi = QLineEdit(self)
        self.textbox_doi.move(450, 370)
        self.textbox_doi.setFixedWidth(330)
        self.pbutton_doi = QPushButton("Copy", self)
        self.pbutton_doi.move(550, 335)
        self.pbutton_doi.clicked.connect(self.doi_copy)

        self.label_tag = QLabel("Tag", self)
        self.label_tag.move(800, 350)
        self.textbox_tag = QLineEdit(self)
        self.textbox_tag.move(800, 370)
        self.textbox_tag.setFixedWidth(120)
        self.pbutton_tag = QPushButton("Write", self)
        self.pbutton_tag.move(920, 335)
        self.pbutton_tag.clicked.connect(self.tag_write)
        self.combobox_tag = QComboBox(self)
        self.combobox_tag.addItems(self.tag_list)
        self.combobox_tag.move(920, 365)
        self.combobox_tag.setFixedWidth(150)

        self.label_abst = QLabel("Abstract", self)
        self.label_abst.move(450, 410)
        self.textbox_abst = QTextEdit(self)
        self.textbox_abst.move(450, 430)
        self.textbox_abst.setFixedSize(600, 220)

        self.pbutton_comment = QPushButton("Comment", self)
        self.pbutton_comment.move(450, 660)
        self.comment_data = ''
        self.pbutton_comment.clicked.connect(self.create_comment_sub_win)

        self.pbutton_trans = QPushButton("En -> Jp", self)
        self.pbutton_trans.move(550, 400)
        self.pbutton_trans.clicked.connect(self.abst_translate)
        self.pbutton_title_trans = QPushButton("En -> Jp", self)
        self.pbutton_title_trans.move(550, 120)
        self.pbutton_title_trans.clicked.connect(self.title_translate)

    # Update the tree according to the selected journal
    # paper_view_list is for display and is rewritten by filtering
    def set_tree(self):
        '''initialization main tree'''
        self.model = MyTableModel(self.paper_view_list, self.headers)
        self.main_tree.setModel(self.model)
        self.main_tree.setColumnWidth(0, 90)
        self.main_tree.setColumnWidth(1, 30)
        self.main_tree.setColumnWidth(2, 5)
        self.main_tree.setColumnWidth(3, 270)
        self.main_tree.hideColumn(4)
        self.main_tree.hideColumn(5)
        self.main_tree.hideColumn(6)
        self.main_tree.hideColumn(7)
        self.main_tree.hideColumn(8)
        self.main_tree.hideColumn(9)

    def import_tag(self):
        '''import tag data from tag_config.ini'''
        while True:
            try:
                file = open('config/tag_config.ini', 'r')
                file.close()
                break
            except FileNotFoundError:
                file = open('config/tag_config.ini', 'a+')
                file.write('[Tag]\n')
                file.write('00 = Tag\n')
                file.close()
                break

        self.conf_parser = configparser.ConfigParser()
        self.conf_parser.read('config/tag_config.ini')
        self.item_list = list(self.conf_parser['Tag'])
        self.tag_list = []
        for item in self.item_list:
            self.tag_list.append(item+":"+self.conf_parser['Tag'][item])

    def import_database(self, article_name):
        '''import paper database'''
        if article_name == '----':
            return

        self.db_data = sqlite3.connect('database/' + article_name + '.db')
        self.db_data.execute("PRAGMA foreign_keys = 1")

        sql = "select * from data_set"
        self.paper_list = []
        for row in list(self.db_data.execute(sql))[::-1]:
            self.temp_comment_data = ''
            if re.sub('\s', '', row[8]) != '':
                self.temp_comment_data = '*'

            row_out = (row[6], row[7], self.temp_comment_data, row[0],
                       row[1], row[2], row[3], row[4], row[5], row[8])
            self.paper_list.append(row_out)

        self.paper_view_list = self.paper_list[:]
        self.set_tree()

    def update_text(self):
        '''update textbox of main window'''
        index = self.main_tree.selectedIndexes()[0]
        temp_data = self.model.display_data(index)
        self.textbox_title.setText(temp_data[3])
        self.textbox_abst.setText(temp_data[4])
        self.textbox_fa.setText(temp_data[5])
        self.textbox_rg.setText(temp_data[6])
        self.textbox_doi.setText(temp_data[7])
        self.textbox_pd.setText(temp_data[8])
        if(temp_data[1].zfill(2) != '00'):
            self.textbox_tag.setText(self.conf_parser['Tag'][temp_data[1].zfill(2)])
        self.comment_data = temp_data[9]

    def reset_text(self):
        '''reset textbox of main window'''
        self.textbox_title.clear()
        self.textbox_abst.clear()
        self.textbox_fa.clear()
        self.textbox_rg.clear()
        self.textbox_doi.clear()
        self.textbox_pd.clear()
        self.textbox_tag.clear()
        self.comment_data = ''

    def title_translate(self):
        '''translate (en -> jp) title'''
        title_text = self.textbox_title.toPlainText()
        title_jp = translater(title_text)
        self.textbox_title.setText(title_jp)

    def abst_translate(self):
        '''translate (en -> jp) abst'''
        abst_text = self.textbox_abst.toPlainText()
        abst_jp = translater(abst_text)
        self.textbox_abst.setText(abst_jp)

    def doi_copy(self):
        '''copy doi text box'''
        pyperclip.copy(self.textbox_doi.text())

    # Write tag information of selected articles in database
    def tag_write(self):
        '''write tag data to database'''
        self.sql_m = SqlManager(self.combobox_article.currentText()+'.db')
        self.sql_m.write_tag_data(self.combobox_tag.currentText().split(':')[
            0], re.sub('\s', '', self.textbox_doi.text()))
        self.import_database(self.combobox_article.currentText())
        self.filter_check()

    def filter_by_keyword(self):
        '''filtering by keyword of textbox'''
        # Find out whether there is a list to filter
        try:
            self.paper_view_list
        except AttributeError:
            return

        filter_words = self.textbox_search.text()
        filter_words = re.sub('\s', '', filter_words)
        if(filter_words == ''):
            return
        self.paper_temp_list = self.paper_view_list[:]
        self.paper_view_list = []
        for row in self.paper_temp_list:
            # Determine whether the title or abst contains keywords
            if (filter_words.lower() in row[3].lower() or filter_words.lower() in row[4].lower()):
                self.paper_view_list.append(row)

    def filter_by_date_range(self):
        '''filtering by date range of combobox'''
        try:
            self.paper_view_list
        except AttributeError:
            return
        self.startdate = int(self.combobox_y.currentText(
        ) + self.combobox_m.currentText().zfill(2) + self.combobox_d.currentText().zfill(2))
        self.enddate = int(self.combobox_2y.currentText(
        ) + self.combobox_2m.currentText().zfill(2) + self.combobox_2d.currentText().zfill(2))
        self.paper_temp_list = self.paper_view_list[:]
        self.paper_view_list = []
        for row in self.paper_temp_list:
            # Determine whether it is within the specified period
            p_date_list = row[8].split('-')
            p_date = p_date_list[0] + \
                p_date_list[1].zfill(2) + p_date_list[2].zfill(2)
            if (int(p_date) >= self.startdate and int(p_date) <= self.enddate):
                self.paper_view_list.append(row)

    def filter_by_tag(self):
        '''filtering by tag of combobox'''
        try:
            self.paper_view_list
        except AttributeError:
            return
        self.paper_temp_list = self.paper_view_list[:]
        self.paper_view_list = []
        for row in self.paper_temp_list:
            # Check that the selected tag matches the item in the list
            if(row[1].replace('-', '').zfill(2) == self.combobox_tagfilter.currentText().split(':')[0]):
                self.paper_view_list.append(row)

    def filter_check(self):
        '''filtering by keyword, date range, tag'''
        self.paper_view_list = self.paper_list[:]
        if self.checkbox_search.checkState() == Qt.Checked:
            self.filter_by_keyword()
        if self.checkbox_dr.checkState() == Qt.Checked:
            self.filter_by_date_range()
        if self.checkbox_tagfilter.checkState() == Qt.Checked:
            self.filter_by_tag()
        self.set_tree()

    def create_tag_edit_sub_win(self):
        '''create tag edit sub window'''
        self.tagedit_sw = TagEditSubWin(self)
        self.tagedit_sw.show()
        self.import_tag()
        self.combobox_tag.clear()
        self.combobox_tag.addItems(self.tag_list)
        self.combobox_tagfilter.clear()
        self.combobox_tagfilter.addItems(self.tag_list)

    def create_output_sub_win(self):
        '''create output sub window'''
        self.out_sw = OutputSubWin(self.paper_view_list, self)
        self.out_sw.show()

    def create_comment_sub_win(self):
        '''create comment sub window'''
        temp_article = self.combobox_article.currentText()
        temp_doi = self.textbox_doi.text()
        self.comment_sw = CommentSubWin(
            temp_article, self.comment_data, temp_doi, self)
        self.comment_sw.show()
        self.import_database(temp_article)
        self.set_tree()
        self.reset_text()
