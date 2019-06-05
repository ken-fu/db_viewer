# -*- coding: utf-8 -*-
import re
import configparser

from PyQt5.QtWidgets import QPushButton, QComboBox, QTextEdit, QLineEdit
from PyQt5.QtWidgets import QAbstractItemView, QCheckBox, QDialog, QProgressBar, QMessageBox
from PyQt5.Qt import Qt


from file_manager.sql_manager import SqlManager
from file_manager.output import OutputForGUI
from file_manager.ini_sorter import ini_sorter

from gui.base_widgets import MyTableModel, MainTreeView


class TagEditSubWin(QDialog):
    '''tag edit sub window'''
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.resize(400, 300)
        self.import_tag()
        self.create_widgets()

    def create_widgets(self):
        '''create widgets on main window'''
        self.make_sub_tree()
        self.set_sub_tree()
        self.pbutton_add_newtag = QPushButton('Add new tag', self)
        self.pbutton_add_newtag.move(230, 60)
        self.pbutton_add_newtag.clicked.connect(self.add_tag)

        self.textbox_rename_tag_num = QLineEdit(self)
        self.textbox_rename_tag_num.move(230, 100)
        self.textbox_rename_tag_num.setFixedWidth(30)
        self.textbox_rename_tag = QLineEdit(self)
        self.textbox_rename_tag.move(270, 100)
        self.textbox_rename_tag.setFixedWidth(120)
        self.pbutton_rename_tag = QPushButton('Rename select tag', self)
        self.pbutton_rename_tag.move(230, 130)
        self.pbutton_rename_tag.clicked.connect(self.rename_tag)
        self.pbutton_del_tag = QPushButton('Delete tad', self)
        self.pbutton_del_tag.move(230, 160)
        self.pbutton_del_tag.clicked.connect(self.del_tag)

    def import_tag(self):
        '''import tag data from tag_config.ini'''
        self.conf_parser = configparser.ConfigParser()
        self.conf_parser.read('config/tag_config.ini')
        self.item_list = list(self.conf_parser['Tag'])
        self.tag_list = []
        for item in self.item_list:
            self.tag_list.append([item, self.conf_parser['Tag'][item]])

    def add_tag(self):
        '''add new tag'''
        for num in range(1, 100):
            if(str(num).zfill(2) not in self.item_list):
                self.conf_parser.set('Tag', str(num).zfill(2), '')
                self.conf_parser.write(open('config/tag_config.ini', 'w'))
                ini_sorter()
                break
        self.import_tag()
        self.set_sub_tree()

    def rename_tag(self):
        '''rename old tag'''
        self.tag_num = re.sub('\s', '', self.textbox_rename_tag_num.text())
        self.tag_name = re.sub('\s', '', self.textbox_rename_tag.text())
        self.conf_parser.set('Tag', self.tag_num, self.tag_name)
        self.conf_parser.write(open('config/tag_config.ini', 'w'))

        self.import_tag()
        self.set_sub_tree()

    def del_tag(self):
        '''delete old tag'''
        self.tag_num = re.sub('\s', '', self.textbox_rename_tag_num.text())
        self.conf_parser.remove_option('Tag', self.tag_num)
        self.conf_parser.write(open('config/tag_config.ini', 'w'))

        self.import_tag()
        self.set_sub_tree()

    def make_sub_tree(self):
        '''create sub tree widget'''
        self.subtree = MainTreeView(self)
        self.subtree.move(10, 10)
        self.subtree.setFixedSize(200, 250)
        self.subtree.clicked.connect(self.sub_win_text_change)
        self.subtree.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def set_sub_tree(self):
        '''initialization sub tree'''
        self.model = MyTableModel(self.tag_list, ["Num", "Name"])
        self.subtree.setModel(self.model)

    def sub_win_text_change(self):
        '''update textbox of sub window'''
        index = self.subtree.selectedIndexes()[0]
        temp_data = self.model.display_data(index)
        self.textbox_rename_tag_num.setText(temp_data[0])
        self.textbox_rename_tag.setText(temp_data[1])

    def show(self):
        '''show()'''
        self.exec_()


class CommentSubWin(QDialog):
    '''commment sub window'''
    def __init__(self, article, comment, doi, parent=None):
        QDialog.__init__(self, parent)
        self.resize(380, 300)
        self.article = article
        self.comment = comment
        self.doi = doi
        self.create_widgets()

    def create_widgets(self):
        '''create widgets on sub window'''
        self.textbox_comment = QTextEdit(self)
        self.textbox_comment.resize(340, 240)
        self.textbox_comment.move(20, 5)
        self.textbox_comment.setText(self.comment)
        self.pbutton_comment = QPushButton('Save and close window', self)
        self.pbutton_comment.move(20, 250)
        self.pbutton_comment.clicked.connect(self.comment_save)

    def comment_save(self):
        '''save inout comment data'''
        self.sql_m = SqlManager(self.article+'.db')
        self.sql_m.write_comment_data(
            self.textbox_comment.toPlainText(), self.doi)
        self.close()

    def show(self):
        '''show()'''
        self.exec_()


class OutputSubWin(QDialog):
    '''output sub window'''
    def __init__(self, paper_view_list, parent=None):
        QDialog.__init__(self, parent)
        self.resize(400, 300)
        self.paper_view_list = paper_view_list
        self.create_widgets()

    def create_widgets(self):
        '''create widgets on sub window'''
        self.checkbox_title = QCheckBox("Title", self)
        self.checkbox_title.move(50, 25)
        self.checkbox_fa = QCheckBox("First Auther", self)
        self.checkbox_fa.move(50, 50)
        self.checkbox_rg = QCheckBox("Research Group", self)
        self.checkbox_rg.move(50, 75)
        self.checkbox_doi = QCheckBox("DOI", self)
        self.checkbox_doi.move(50, 100)
        self.checkbox_pd = QCheckBox("Publish Date", self)
        self.checkbox_pd.move(50, 125)
        self.checkbox_abst = QCheckBox("Abstract", self)
        self.checkbox_abst.move(50, 150)
        self.checkbox_comment = QCheckBox("Comment", self)
        self.checkbox_comment.move(50, 175)

        self.combobox_output_mode = QComboBox(self)
        self.combobox_output_mode.addItems(["csv", "pdf"])
        self.combobox_output_mode.move(50, 200)

        self.pbutton_search = QPushButton('Go', self)
        self.pbutton_search.move(250, 200)
        self.pbutton_search.clicked.connect(self.output_paper_data)

        self.progressbar_progress = [0, len(self.paper_view_list)]
        self.progressbar_out = QProgressBar(self)
        self.progressbar_out.move(250, 230)

    def output_paper_data(self):
        '''output data'''
        val_title = (self.checkbox_title.checkState() == Qt.Checked)
        val_fa = (self.checkbox_fa.checkState() == Qt.Checked)
        val_rg = (self.checkbox_rg.checkState() == Qt.Checked)
        val_doi = (self.checkbox_doi.checkState() == Qt.Checked)
        val_pd = (self.checkbox_pd.checkState() == Qt.Checked)
        val_abst = (self.checkbox_abst.checkState() == Qt.Checked)
        val_comment = (self.checkbox_comment.checkState() == Qt.Checked)

        output_for_gui = OutputForGUI()
        if(self.combobox_output_mode.currentText() == 'csv'):
            output_for_gui.output_to_csv(self.paper_view_list, [
                False, False, False, val_title, val_abst, val_fa, val_rg, val_doi, val_pd, val_comment], self.progressbar_out, self.progressbar_progress)
            self.message_box = QMessageBox.information(
                self, "", "Finish !!!", QMessageBox.Close)
            if self.message_box:
                self.close()
        else:
            output_for_gui.output_to_pdf(self.paper_view_list, [
                False, False, False, val_title, val_abst, val_fa, val_rg, val_doi, val_pd, val_comment], self.progressbar_out, self.progressbar_progress)
            self.message_box = QMessageBox.information(
                self, "", "Finish !!!", QMessageBox.Close)
            if self.message_box:
                self.close()

    def show(self):
        '''show()'''
        self.exec_()
