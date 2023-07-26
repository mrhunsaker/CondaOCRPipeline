# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 12:28:10 2023

@author: COnnor.gibbs
"""

from time import strptime
def is_valid_date(string):
    """Checks if a string is a valid date"""
    try:
        strptime(string, '%m/%d/%Y')
        return True
    except ValueError:
        return False

import re
def is_ssn(string):
    """Checks if string is a valid social security number"""
    pattern = r'^\d{9}$'  # Regex pattern for exactly nine digits
    return bool(re.match(pattern, string))

def remove_empty(x):
    x = [[elem for elem in inner_list if elem != ''] for inner_list in x]
    return x

def remove_string(x, string):
    """Recursively remove a string from a list of lists of strings."""
    for inner_list in x:
        for i in range(len(inner_list)):
            inner_list[i] = inner_list[i].replace(string, '')
    return x