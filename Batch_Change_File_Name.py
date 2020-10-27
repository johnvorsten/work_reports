# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 07:49:22 2020

This module allows the user to have a default value filled in 
when they are asked for an input.  For example, if you are asking a 
user for a file path, you could use something like this : 
    
file_str = input("Please enter a file name : ")
# Do stuff with file_str

With this module, the user can be prompted, with a default file string
default_file_str = r"C:\Users\Public"
file_str = input_def("Please enter a file name : ", default_file_str)

>>> Please enter a file name : C:\Users\Public

@author: z003vrzk
"""


import win32console

_stdin = win32console.GetStdHandle(win32console.STD_INPUT_HANDLE)

def input_def(prompt, default=''):
    keys = []
    for c in default.encode():
        evt = win32console.PyINPUT_RECORDType(win32console.KEY_EVENT)
        evt.Char = c
        evt.RepeatCount = 1
        evt.KeyDown = True
        keys.append(evt)

    _stdin.WriteConsoleInput(keys)
    return raw_input(prompt)

if __name__ == '__main__':
    name = input_def('Folder name: ')
    print(name)