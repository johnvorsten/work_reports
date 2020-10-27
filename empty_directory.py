# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 09:02:54 2019

Given a directroy, iterate through all subdirectories and add a
filler file.

The filler file name with be ord(937).txt (hidden and read only)

Reasoning : 
Git repositories do not track directories with no files
In select cases, I want to keep directories when I push a repo
to a remote, and the simplest way to do this is a track a file 
inside that directory

@author: z003vrzk
"""

import os
import shutil, stat
from pathlib import Path
import win32api, win32con
#help(os)
#help(os.path)
#help(os.walk)
#help(os.isfile)
#help(os.listdir)
#help(os.chmod)
#help(os.lstat)
#help(os.stat)
#
#help(stat)
#
#help(Path)
#
## os.listdir()


#%% Working sandbox

def is_empty(directory):
    """
    input
    -------
    directory
    output
    -------
    False if directory has files
    True if directory is empty"""
    
    sub = os.listdir(directory)
    if len(sub) == 0:
        return True
    elif len(sub) >= 1:
        return False
    else:
        raise TypeError('Something went wrong')
        
def change_file_attributes(_file):
    """Change a file to FILE_ATTRIBUTE_READONLY and FIEL_ATTRIBUTE_HIDDEN
    input
    -------
    _file : string or path object
    output
    -------
    None, change a files attributes only
    
    os.chmod(_file, stat.S_IWRITE) # Add write access
    os.stat(_file) # stat system call on path
    _mode = os.stat(_file).st_mode # File mode (for protection)"""
    
    FILE_ATTRIBUTE_HIDDEN = stat.FILE_ATTRIBUTE_HIDDEN # Make Hidden File
    FILE_ATTRIBUTE_READONLY = stat.FILE_ATTRIBUTE_READONLY # Make Read Only
    
    Attribute = FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_READONLY
    
    win32api.SetFileAttributes(_file, Attribute)
    
    pass

def main(base_dir, fprint=False):
    # Get input of base directory from user
    
    file_name = chr(937) + '.txt'
    
#    dir_iter = os.walk(base_dir)
    
    empty_dirs = []
    for sub_dir in os.walk(base_dir):
        # sub_dir is 3-tuple (root, sub_directories, files in root)
        
        # Skip .git directories
        if sub_dir[0].__contains__('.git'):
            continue
        
        if all((len(sub_dir[1]) == 0, len(sub_dir[2]) == 0)):
            # Keep track of root empty directories
            empty_dirs.append(sub_dir[0])
    
    for empty_dir in empty_dirs:
        file_path = os.path.join(empty_dir, file_name)
        if fprint:
            print(file_path)
        
        # Create file
        # Write data to file (message)
        message = r'Do Not Remove - JV'
        with open(file_path, 'w') as f:
            f.write(message)
        
        # Change file attributes
        change_file_attributes(file_path)
        
    pass


mydirs = [
r"C:\Users\z003vrzk\Desktop\44OP-211506_TFC_SFA_Repl_DM2016"
r"C:\Users\z003vrzk\Desktop\44OP-227505_TFC_A600_Bio_Threat"
r"C:\Users\z003vrzk\Desktop\44OP-245597_JH_Winters_AHU_Reno"
r"C:\Users\z003vrzk\Desktop\44OP-246728_TXSU_Chemistry_Bldg_Reno"
r"C:\Users\z003vrzk\Desktop\44OP-255709_TFC_WPC_Controller_Replacement"
r"C:\Users\z003vrzk\Desktop\44OP-262004_ATT_Homestead_NLoop"
r"C:\Users\z003vrzk\Desktop\44OP-266869_401_Congress_12th_14th_Floor_VAV"
r"C:\Users\z003vrzk\Desktop\44OP-267319-AUS_TFC_REJ_DM_OA_units"
r"C:\Users\z003vrzk\Desktop\44OP-268394-401_Congress_Reed_Smith_18th_Floor_Ste_1800"
r"C:\Users\z003vrzk\Desktop\44OP-269570-DCMC_Pharmacy_Reno"
r"C:\Users\z003vrzk\Desktop\44OP-270201-BAU_BSS_NW_Surgical_Center_Reno"
]



if __name__ == '__main__':
    input_msg = """Please enter in a base directory
    Format like : path\\to\\direcory
    Input : """
    base_dir = str(input(input_msg))
    main(base_dir)
    
    
    # For iterating over a list of directories
#    for base_dir in mydirs:
#        main(base_dir)

