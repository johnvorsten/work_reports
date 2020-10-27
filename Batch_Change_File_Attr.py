# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 15:19:19 2019

Given a directroy, iterate through all subdirectories and change file 
attributes

This script changes read property attributes

Reasoning : 
Change read property to read only. Read-only files act as templates

@author: z003vrzk
"""

import os
import shutil, stat
from pathlib import Path
import win32api, win32con

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
    
    # Example set file attribute flags
    # FILE_ATTRIBUTE_HIDDEN = stat.FILE_ATTRIBUTE_HIDDEN # Make Hidden File
    FILE_ATTRIBUTE_READONLY = stat.FILE_ATTRIBUTE_READONLY # Make Read Only
    
    # Example set multiple properties
    # Attribute = FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_READONLY
    Attribute = FILE_ATTRIBUTE_READONLY
    
    # Set attribute
    win32api.SetFileAttributes(_file, Attribute)
    
    pass


def main(base_dir, fprint=False):
    # Get input of base directory from user
    
    # Keep track of all files in subdirectories
    file_paths = []
    for sub_dir in os.walk(base_dir):
        # sub_dir is 3-tuple (root, sub_directories, files in root)
        for _file in sub_dir[2]:
            _file = os.path.join(sub_dir[0], _file)
            file_paths.extend([_file])
    
    # Change file attributes
    for _file in file_paths:
        if os.path.isfile(_file): # Redundant check?
            change_file_attributes(_file)
        if fprint:
            print(_file)
        
    pass



if __name__ == '__main__':
    input_msg = """Please enter in a base directory
    Format like : path\\to\\direcory
    Input : """
    base_dir = str(input(input_msg))
    main(base_dir)