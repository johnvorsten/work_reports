# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 09:15:43 2020

@author: z003vrzk
"""
# Python Imports
import os
import subprocess
import tkinter as tk
from tkinter import filedialog

# Local imports
from FLN_report import create_bln_dict, bln_dict_to_df



if __name__ == '__main__':
    # Get system profile report from user
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    file_path = os.path.normpath(file_path)

    # Create dictionary of BLN profile
    bln_dict = create_bln_dict(file_path)

    # Convert dictionary of BLN profile to dataframe for report generation
    fln_dataframe = bln_dict_to_df(bln_dict)

    # Save dataframe to .csv file
    save_path = os.path.join(os.getcwd(), 'FLN_Schedule_output.csv')
    fln_dataframe.to_csv(save_path, index=False)

    subprocess.run('start EXCEL.exe "%s"' %save_path, shell=True)
