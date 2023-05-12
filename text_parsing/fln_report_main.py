# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 09:15:43 2020

@author: john Vorsten
"""
# Python Imports
import os
import subprocess
import tkinter as tk
from tkinter import filedialog
import sys

# Local imports
from text_parsing.fln_report_parser import create_bln_dict, write_bln_dictionary_to_file

# Declarations
DEFAULT_CSV_FILEOUT = 'fln_report'
if sys.platform.__contains__('linux'):
    DEFAULT_SAVE_DIR = os.getenv("HOME", None)
elif sys.platform == 'win32':
    DEFAULT_SAVE_DIR = os.getenv("USERPROFILE", None)
elif sys.platform == 'darwin':
    DEFAULT_SAVE_DIR = os.getenv("HOME", None)
else:
    DEFAULT_SAVE_DIR = None

#%%

def main():

    # Get system profile report from user
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    file_path = os.path.normpath(file_path)
    # Ask user for save file path
    save_path = filedialog.asksaveasfilename(
        title="Save output file as",
        initialdir=DEFAULT_SAVE_DIR,
        initialfile=DEFAULT_CSV_FILEOUT,
        filetypes=(('Comma separated value', '*.csv'),),
        defaultextension='.csv')
    if not save_path:
        raise SystemExit(ValueError(str(save_path), ' is not a valid save path'))
    save_path = os.path.normpath(save_path)

    # Create dictionary of BLN profile
    bln_dict = create_bln_dict(file_path)

    # Save dataframe to .csv file
    save_path = os.path.join(os.getcwd(), 'FLN_Schedule_output.csv')
    write_bln_dictionary_to_file(bln_dict, save_path)


    subprocess.run('start EXCEL.exe "%s"' % save_path, shell=True)

    return None


if __name__ == '__main__':
    main()
