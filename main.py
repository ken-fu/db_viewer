# -*- coding: utf-8 -*-
'''----paper checker----
(created by ken)'''
import sys
import importlib
from PyQt5.QtWidgets import QApplication

from gui import gui
from file_manager.sql_manager import SqlManager
from file_manager.folder_check import get_all_addon

def main():
    '''main'''
    print('')
    print('')
    print("----db_viewer----")
    print("(created by ken)")
    print('')
    print('0 : View paper data (GUI)')
    print('1 : update database (get new paper data)')
    
    print('other : exit')

    mode = int(input('select mode : '))

    if(mode == 0):
        main_app = QApplication(sys.argv)
        main_window = gui.MainWidget()    
        sys.exit(main_app.exec_())
    
    if(mode == 1):
        # Examine available add-ons, scrape, write to a database
        i = 0
        functions = get_all_addon()
        for function in functions:
            print("%d : %s"%(i, function, ))
            i += 1
        while True:
            try:
                selectnum = int(input("select number : "))
                module = importlib.import_module(f'addon.{functions[selectnum]}')
                get_paper = module.GetPaper()
                result = get_paper.get_paper()
                sql_m = SqlManager(functions[selectnum]+'.db')
                sql_m.add_datalist(reversed(result))
                input("Push enter key...")
                break
            except ValueError:
                break
    
    else:
        return


if __name__ == '__main__':
    main()

    
