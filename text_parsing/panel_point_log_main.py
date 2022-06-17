"""Input a file and parse a Point Definition report
Author: John Vorsten
Date: 2022-06-17"""

# Python Imports
import os
import subprocess
import tkinter as tk
from tkinter import filedialog
import difflib
import csv
import sys

# Local imports
from text_parsing.panel_point_log_parser import parse_text_to_pointdefinition_list, write_dataclass_to_csv

# Declarations
DEFAULT_CSV_FILEOUT = 'panel_point_log_report.csv'
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

    # Get text file report from user
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

    # List of PointDefinition dataclass objects
    points = parse_text_to_pointdefinition_list(file_path)

    # Print each dataclass to a .csv file where each instance is a row
    write_dataclass_to_csv(save_path, points)

    return None

if __name__ == '__main__':
    raise SystemExit(main())
