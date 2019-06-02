# -*- coding: utf-8 -*-
import sqlite3

class SqlManager:
    '''Manage sql database class'''
    def __init__(self, db_name):
        self.con = sqlite3.connect('database/'+db_name)
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS data_set(title, abstract, auther, research_group, doi, publishdate, importdate, tag, comment)")
    
    def add_datalist(self, data):
        '''Add data to database. data = [['tltle1', 'abst1', 'auther1', 'group1', 'doi1', 'p_date1', 'i_date1', 'tag1', comment1'], ['tltle2', 'abst2', 'auther2', 'group2', 'doi2', 'p_date2', 'i_date2', 'tag2', 'comment2']]'''
        self.cursor.executemany("INSERT INTO data_set VALUES(?,?,?,?,?,?,?,?,?)", data)
        self.con.commit()
    
    def get_alldata(self):
        '''Get all data from database and return'''
        self.cursor.execute("select * from data_set")
        return self.cursor
    
    def write_tag_data(self, tag, doi):
        self.cursor.execute("update data_set set tag = ? where doi = ?",(tag, doi))
        self.con.commit()
    
    def write_comment_data(self, comment, doi):
        self.cursor.execute("update data_set set comment = ? where doi = ?",(comment, doi))
        self.con.commit()
