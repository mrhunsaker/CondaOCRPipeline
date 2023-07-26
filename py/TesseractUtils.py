# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 13:09:17 2023

@author: COnnor.gibbs
"""

from pathlib import Path

import sys
import pytesseract
import platform
import io
import pandas as pd
from tempfile import TemporaryDirectory
from pdf2image import convert_from_path
from PIL import Image

# this is a pointer to the module object instance itself
exe_paths = sys.modules[__name__]

# SET TESSERACT AND POPPLER EXECUTABLES
exe_paths.tesseract = r"C:\Users\COnnor.gibbs\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
exe_paths.poppler = r"C:\Users\COnnor.gibbs\AppData\Local\Programs\poppler-23.07.0\Library\bin"

def extract_pdf_text(pdf_path):
    """Convert pdf to list of lists of strings.

        Returns a list of lists of strings. The outer list enumerates the pages 
        of the pdf. The inner list enumerates lines of pdf pages. Each element of the
        inner list is a string, providing the inferred text in that relative 
        position.

        Parameters
        ----------
        pdf_path : str, required
            The absolute path of a pdf document.
        """
    # get output directory and poppler path by platform
    if platform.system() == "Windows":
        pytesseract.pytesseract.tesseract_cmd = exe_paths.tesseract
        path_to_poppler_exe = Path(exe_paths.poppler)
        
    # get pdf file as path
    pdf_path = Path(pdf_path)
    
    # store all pages of the pdf in a list
    image_file_list = []
    
    # start converting, holding temporary images
    with TemporaryDirectory() as tempdir:
        # convert pdf to images at 500 DPI
        if platform.system() == "Windows":
            pdf_pages = convert_from_path(
                pdf_path, 500, poppler_path = path_to_poppler_exe
            )
        else:
            pdf_pages = convert_from_path(pdf_path, 500)
            
        """
        Part #1 : Converting PDF to images
        """
 
        # iterate through all the pages stored above
        for page_enumeration, page in enumerate(pdf_pages, start = 1):
 
            # create a file name to store the image
            filename = f"{tempdir}\page_{page_enumeration:03}.jpg"
 
            # save the image of the page in system
            page.save(filename, "JPEG")
            image_file_list.append(filename)
 
        """
        Part #2 - Recognizing text from the images using OCR
        """
        
        txt_list = []
        # iterate from 1 to total number of pages
        for image_file in image_file_list:
            # recognize the text as string in image using pytesserct
            text = str(pytesseract.image_to_string(Image.open(image_file)))
            
            # write the entire pdf to a list
            txt_list.append(text)
                
    return txt_list

def extract_pdf_data(pdf_path):
    """Convert pdf to a dataframe.

        Returns a dataframe containing box boundaries, confidences, and other 
        information about the script, orientation, and text present in the pdf. 
        Requires Tesseract 3.05+. For more information, please check the Tesseract 
        TSV documentation.
        
        Resulting columns include:
            * `page_num`: The page number.
            * `block_num`: The inferred textbox number.
            * `par_num`: The inferred paragraph number (if detected).
            * `line_num`: The inferred line number (if detected).
            * `word_num`: The inferred word number (if detected).
            * `left`: The left coordinate of the bounding box around the block.
            * `top`: The top coordinate of the bounding box around the block.
            * `width`: The width of the bounding box around the block.
            * `height`: The height of the bounding box around the block.
            * `conf`: The confidence level of the detected block.
            * `text`: The detected text within the block.

        Parameters
        ----------
        pdf_path : str, required
            The absolute path of a pdf document.
        """
    if platform.system() == "Windows":
        pytesseract.pytesseract.tesseract_cmd = exe_paths.tesseract
        path_to_poppler_exe = Path(exe_paths.poppler)
            
    # get pdf file as path
    pdf_path = Path(pdf_path)
    
    # store all pages of the pdf in a list
    image_file_list = []
    
    # start converting, holding temporary images
    with TemporaryDirectory() as tempdir:
        # convert pdf to images at 500 DPI
        if platform.system() == "Windows":
            pdf_pages = convert_from_path(
                pdf_path, 500, poppler_path = path_to_poppler_exe
            )
        else:
            pdf_pages = convert_from_path(pdf_path, 500)
            
        """
        Part #1 : Converting PDF to images
        """
 
        # iterate through all the pages stored above
        for page_enumeration, page in enumerate(pdf_pages, start = 1):
 
            # create a file name to store the image
            filename = f"{tempdir}\page_{page_enumeration:03}.jpg"
 
            # save the image of the page in system
            page.save(filename, "JPEG")
            image_file_list.append(filename)
 
        """
        Part #2 - Recognizing text from the images using OCR
        """
        
        data_list = []
        for image_file_num, image_file in enumerate(image_file_list, start = 1):
            # recognize the text as string in image using pytesserct
            data = pytesseract.image_to_data(Image.open(image_file))
            
            # create a tsv like file and read as pandas
            data = io.StringIO(data)
            data = pd.read_csv(data, sep='\t', lineterminator='\n')
            data['page_num'] = image_file_num
            
            # write the data as a list
            data_list.append(data)
            
        data = pd.concat(data_list)
        
    return data
