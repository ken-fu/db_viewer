# -*- coding: utf-8 -*-
from googletrans import Translator
translatorG = Translator()

def translater(sentence):
    '''Translation process using google translation'''
    string = sentence.replace('\n', '')
    trans_result = translatorG.translate(string, dest='ja').text
    if trans_result is not None:
        return trans_result
    else:
        return "Error"
