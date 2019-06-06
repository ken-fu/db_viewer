DB_viewer
==================
  
## Overview
This program is a viewer of SQL database.
Handles data obtained by scraping etc. converted to database with sqlite3.
Please refer to folder_check / sql_manager.py and addon / sample.py for the format.
You can handle various journals by adding processing (such as scraping) in addon.
Please refer to addon / sample.py for the format of the process to be added.
However, please be careful that scraping does not violate the terms and conditions of each journal.
  

## Requirement
python 3.6.2  
reportlab==3.4.0  
tqdm==4.24.0  
pyperclip==1.7.0
PyQt==5.12.2

## Usage
Clone it to a suitable place and run it from main.py.
mode 0 is a viewer by GUI.
mode 1 is the database update process.
You will see the features added within addon.
Although I use PyQt5, I have not confirmed the operation in environments other than mac, so the layout may not be correct.

## Author
ken
