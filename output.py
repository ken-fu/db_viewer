# -*- coding: utf-8 -*-
import glob
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from tqdm import tqdm
import datetime

from translate import translater


class Output:
    '''output data to pdf or terminal'''

    def output_list(self, paper_list):
        for i in paper_list:
            print("title: %s" % i[0])
            print("date: %s" % i[5])
            print("")
            print("abstraction: %s" % i[1])
            print("")
            print("url: %s" % i[4])
            print("##########################################")

    def output_pdf(self, paper_list, article_name):
        if paper_list == []:
            return

        # config for pdf
        pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
        styles = getSampleStyleSheet()
        my_style = styles["Normal"]
        my_style.name = "bonlife"
        my_style.fontName = "HeiseiKakuGo-W5"
        my_style.fontSize = 10
        my_style.spaceAfter = 1
        my_style.leading = 20
        my_style.leftIndent = 0
        my_style.rightIndent = 0
        my_style.wordWrap = 'CJK'
        style = my_style

        output_filepath = "./workspace/%s_%s.pdf" % (article_name, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        doc = SimpleDocTemplate(output_filepath, leftMargin=0.5*inch,
                                rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []

        # Output processing. Page break for each paper
        for i in tqdm(range(len(paper_list)), desc='Output now'):
            
            story.append(
                Paragraph("title(en) : " + paper_list[i][0], style))
            story.append(Paragraph("title(jp) : " +
                                    translater(paper_list[i][0]), style))
            story.append(Spacer(1, .25*inch))
            story.append(
                Paragraph("abstract(en) : " + paper_list[i][1], style))
            story.append(Spacer(1, .25*inch))
            story.append(Paragraph("abstract(jp) : " +
                                    translater(paper_list[i][1]), style))
            story.append(Spacer(1, .25*inch))
            story.append(Paragraph("DATE: " + str(paper_list[i][5].split('-')[0])+"/"+str(
                paper_list[i][5].split('-')[1])+"/"+str(paper_list[i][5].split('-')[2]), style))
            story.append(Paragraph("URL: " + paper_list[i][4], style))
            story.append(PageBreak())

        doc.build(story)

        print('Output process finished !!!')

class Output_for_GUI:
    '''output data prosess class for gui.py'''
    def output_to_csv(self, data_list, flag, PB, PB_progress):
        '''(data_list, flag, PB, PB_progress) ex) flag = [True, False, False, ...]　Output an item which value is True. PB is ProgressBar widget. PB_progress is value of ProgressBar'''
        output_file = open('./workspace/output_%s.csv'%(datetime.datetime.today().date()), 'w', encoding="utf_8_sig")
        col_name = ['tltle', 'abstract', 'first auther', 'research group', 'doi', 'p_date', 'i_date', 'tag', 'flag']
        result = ''
        for col in range(9):
            if flag[col]:
                result += col_name[col]
                result += ','
        result += '\n'
        for row in data_list:
            for col in range(9):
                if flag[col]:
                    result += row[col].replace(',','_')
                    result += ','
            result += '\n'
            PB_progress += 1
            PB.configure(value=PB_progress)
        output_file.write(result)
        output_file.close()
    
    def output_to_pdf(self, data_list, flag, PB, PB_progress):
        '''(data_list, flag, PB, PB_progress) ex) flag = [True, False, False, ...]　Output an item which value is True. PB is ProgressBar widget. PB_progress is value of ProgressBar'''
        col_name = ['tltle', 'abstract', 'first auther', 'research group', 'doi', 'p_date', 'i_date', 'tag', 'flag']
        # config for pdf
        pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
        styles = getSampleStyleSheet()
        my_style = styles["Normal"]
        my_style.name = "bonlife"
        my_style.fontName = "HeiseiKakuGo-W5"
        my_style.fontSize = 10
        my_style.spaceAfter = 1
        my_style.leading = 20
        my_style.leftIndent = 0
        my_style.rightIndent = 0
        my_style.wordWrap = 'CJK'
        style = my_style
        PB_progress2 = 0

        output_filepath = './workspace/output_%s.pdf'%(datetime.datetime.today().date())
        doc = SimpleDocTemplate(output_filepath, leftMargin=0.5*inch,
                                rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []

        # Output processing. Page break for each paper
        for row in data_list:
            for col in range(9):
                if flag[col]:
                    story.append(Paragraph(col_name[col] + ' : ' + row[col], style))
                    story.append(Spacer(1, .25*inch))
            story.append(PageBreak())
            PB_progress2 += 1
            PB.configure(value=PB_progress2)

        doc.build(story)