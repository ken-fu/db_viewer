# -*- coding: utf-8 -*-
import configparser

def ini_sorter():
    '''Re-sort in tag_config.ini'''
    conf_parser = configparser.ConfigParser()
    conf_parser.read('tag_config.ini')
    sorted_dict = dict(sorted(conf_parser.items('Tag')))
    item_list = conf_parser['Tag']

    for item in item_list:
        conf_parser.remove_option('Tag',item)
    conf_parser.read(sorted_dict)
    for item in sorted_dict:
        conf_parser.set('Tag',item.zfill(2),sorted_dict[item])

    conf_parser.write(open('tag_config.ini','w'))
