# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication
from gui import gui

if __name__ == '__main__':
    main_app = QApplication(sys.argv)
    main_window = gui.MainWidget()    
    sys.exit(main_app.exec_())
