# -*- coding: utf-8 -*-
"""sample"""
import datetime
from tqdm import tqdm


class GetPaper():
    def __init__(self):
        self.ARTICLE = 'hoge'
        self.TARGET_URL = 'target url'

    def logger(self, title_list):
        '''Output doi of checked papers to log'''
        file = open('./log/log_%s.txt' % (self.ARTICLE, ), 'a')
        for title in title_list:
            file.write(title + '\n')
        file.close()

    def get_paper(self):
        paper_list = []
        doi_list = []

        while True:
            try:
                file = open('./log/log_%s.txt' % (self.ARTICLE, ), 'r')
                break
            except FileNotFoundError:
                file = open('./log/log_%s.txt' % (self.ARTICLE, ), 'a+')
                break

        past_list = file.read()
        file.close()

        file = open('./log/log_%s.txt' % (self.ARTICLE, ), 'a')
        file.write(str(datetime.datetime.today()) + '\n')
        file.close()

        # Check for new articles. End if there is a previous check
        for j in tqdm(range(10), desc='Check now'):
            doi = 'hoge%d'% j
            if (doi in past_list):
                break
            doi_list.append(doi)

        print('Check finished')

        # Scraping detailed information
        for i in tqdm(range(len(doi_list)), desc='Scraping now'):
            doi = doi_list[i]
            title = 'title%d'% i
            abst = 'abst%d'% i
            auther = 'auther%d'% i
            auther_group = 'auther_group%d'% i
            url = 'url%d'% i
            date_str = 'YY-MM-DD'
            paper_list.append(
                [title, abst, auther, auther_group, url, date_str, str(datetime.date.today()), '', ''])
        self.logger(doi_list)
        print("Scraping finished")
        return paper_list
