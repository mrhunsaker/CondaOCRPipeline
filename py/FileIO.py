# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 12:23:46 2023

@author: COnnor.gibbs
"""

import os
def absolute_file_paths(directory):
    """get a list of files associated with a directory"""
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))

from tkinter import Tk
from tkinter.filedialog import askdirectory
def choose_directory(msg):
    """prompt the user to pick a directory with a message"""
    # Create Tkinter root window
    root = Tk()
    root.withdraw()  # Hide the root window

    # Prompt the user to select a directory
    directory = askdirectory(title = msg)
    
    return directory

import chardet
def read_txt_lines(txt_path):
    """read lines of a text file to a list"""
    with open(txt_path, 'rb') as my_file:
        raw_data = my_file.read()

    # Use chardet to detect the encoding
    result = chardet.detect(raw_data)
    encoding = result['encoding']

    # Open the file again with the detected encoding
    with open(txt_path, 'r', encoding=encoding) as my_file:
        data = my_file.read()
        data_into_list = data.split("\n")
    
    # Remove empty strings
    data_into_list = [x for x in data_into_list if x != '']
    
    # Split by tab
    data_into_list = [x.split('\t') for x in data_into_list]
    data_into_list = [[elem for elem in inner_list if elem != ''] for inner_list in data_into_list]
    
    return data_into_list