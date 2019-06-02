# -*- coding: utf-8 -*-
'''Examine the folder and return in a list'''
import os
import glob

def get_all_database():
    filepaths = [file for file in glob.glob("./database/[a-zA-Z0-9]*.db")]
    databases = []
    for filepath in filepaths:
        module_name = os.path.splitext(os.path.basename(filepath))[0]
        databases.append(module_name)
    return databases

def get_all_addon():
    filepaths = [file for file in glob.glob("./addon/[a-zA-Z0-9]*.py")]
    functions = []
    for filepath in filepaths:
        module_name = os.path.splitext(os.path.basename(filepath))[0]
        functions.append(module_name)
    return functions