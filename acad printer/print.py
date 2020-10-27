# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 14:26:51 2020

@author: z003vrzk
"""
# Python imports
import os
import subprocess

# Third party imports

# Local imports


#%% 
# Print autocad drawings using the autocad command line
# See https://knowledge.autodesk.com/support/autocad-lt/learn-explore/caas/CloudHelp/cloudhelp/2019/ENU/AutoCAD-LT/files/GUID-95BB6824-0700-4019-9672-E6B502659E9E-htm.html
# For basic of running scripts at autocad startup


#%% 
"""Opening autocad and executing an autocad 'batch' type script or a .scr file

/b is the switch for opening an autocad file and designating a script to run
when you open the program (b stands for batch process)

/pl background plotting and publishing (what does it do exactly? - 
publishes a drawign set description file in the background
<path><drawing set descriptions file>.DSD)

/t template file name (creates a new drawing based on template... dont use)

see https://knowledge.autodesk.com/support/autocad/learn-explore/caas/CloudHelp/cloudhelp/2016/ENU/AutoCAD-Core/files/GUID-625E395D-143A-494F-A1EA-1BF119B927DC-htm.html
for instructions on the -PLOT autocad command line interface command"""

acad_executable_path = r"C:\Program Files\Autodesk\AutoCAD 2019\acad.exe"
drawing_file_path = r"D:\Jobs\239338_BAU_BSS_ACC_Bond_Rio_Grande_Retro\MDT\000 Main Riser.dwg"
scr_file_path = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\acad printer\single_print.scr"


subprocess.call([acad_executable_path, 
                 drawing_file_path, 
                 r'/b', 
                 scr_file_path,])



#%% Determine layout orientation of each drawing type

class AutocadPrinter():
    """Automatically print all the drawings in a job.
    Use the drawing sheet type defined in SQL databases to assign printer
        configurations
    """
    
    def __init__(self):
        pass
    
    def write_drawing_sheet_set_file(self):
        pass
    
    def publish_autocad_script(self):
        pass
    
    def query_drawing_types(self):
        pass
    
    
    













