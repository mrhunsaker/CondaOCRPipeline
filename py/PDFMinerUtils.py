# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 12:30:51 2023

@author: COnnor.gibbs
"""

# pdfminer products
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure

# clean ups
import numpy as np
import pandas as pd
import ctypes

def parse_layout(layout):
    """Recursively parse layout tree."""
    layout_list = list()
    for lt_obj in layout:
        plt_dict = dict()
        plt_dict["class"] = lt_obj.__class__.__name__
        plt_dict["coords"] = lt_obj.bbox
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            plt_dict["text"] = lt_obj.get_text().strip()
        elif isinstance(lt_obj, LTFigure):
            parse_layout(lt_obj)  # Recursive
        layout_list.append(plt_dict)
    
    return layout_list

def extract_pdf_text(pdf_path):
    """Convert layout tree to list of pdf pages.

        Returns a list of lists. The outer list enumerates the pages of the pdf.
        The inner list enumerates the objects of a pdf page. Each element of the
        inner list is a dictionary, providing the object type, coordinates, and
        text (if available).

        Parameters
        ----------
        pdf_path : str, required
            The absolute path of a pdf document.
        """
    fp = open(pdf_path, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    layouts = list()
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
        layout = device.get_result()
        layout = parse_layout(layout)
        layout = np.array(layout)
        layouts.append(layout)
    
    return layouts

def get_page_coordinates(pdf):
    """Provides the coordinates of each page of a pdf.

        Returns a data frame of page coordinates. Each row represents a page, and
        each column represents the boundary of the page.

        Parameters
        ----------
        pdf : list, required
            A list of lists with pdf text.
        """
    new_pdf = [[tb for tb in pg if tb['coords'][0] == 0 and tb['coords'][2] == 0] for pg in pdf]
    
    # find page coordinates
    coords = []
    for pg_num, pg in enumerate(new_pdf):
        y1 = np.array([x['coords'][1] for x in pg])
        y2 = np.array([x['coords'][3] for x in pg])
        y1 = np.where(y1 == np.max(y1))[0]
        y2 = np.where(y2 == np.max(y2))[0]
        y = np.intersect1d(y1, y2)[0]
        coords.append(new_pdf[pg_num][y])
    
    # extract the coordinates
    coords = np.array([x['coords'] for x in coords])
    coords = coords.ravel().reshape(-1, 4)
    
    # organize left, right, bottom, top
    cols = ['left', 'right', 'bottom', 'top']
    coords = np.column_stack((coords[:, 0], coords[:, 2], coords[:, 1], coords[:, 3]))
    coords = pd.DataFrame(coords, columns = cols)
    
    return coords
    
def get_page_data(page):
    """Structures a page's objects into a data frame.

            Returns a data frame with coordinates and page text.

            Parameters
            ----------
            page : list, required
                A list of dictionaries, representing the objects of a pdf page.
            """
    # extract coordinates
    coords = np.array([x['coords'] for x in page])
    text = [x['text'] if 'text' in x else '' for x in page]
    
    # organize left, right, bottom, top
    cols = ['left', 'right', 'bottom', 'top']
    coords = np.column_stack((coords[:, 0], coords[:, 2], coords[:, 1], coords[:, 3]))
    coords = pd.DataFrame(coords, columns = cols)
    
    # organize
    coords['text'] = text
    
    return coords

# extract all data from pdf
def extract_pdf_data(pdf):
    """Recursively structure the objects of a pdf.

            Returns a data frame with coordinates and page text for each page of
            a pdf.

            Parameters
            ----------
            df : list, required
                A list of of list of dictionaries, representing the objects of a pdf page.
            """
    # extract page data for each page
    page_data = []
    for pg_num, pg in enumerate(pdf, start=1):
        data = get_page_data(pg)
        data.insert(0, "page", pg_num)
        page_data.append(data)
        
    # combine
    data = pd.concat(page_data)
    data.index = range(data.shape[0])
    
    return data

def disperse_row(pdf_data, row, seperator, direction, sort = False):
    """Split a row of pdf data over several rows.

            Returns a data frame with at least as many rows as input. The text 
            associated with the specified row is split at the specified seperator.
            The results are dispersed over new rows, subsequently replacing the 
            input row. Coordinates are adjusted accordingly according to the width
            of text and direction of dispersion.

            Parameters
            ----------
            pdf_data : data frame, required
                A data frame representing the extracted data of a pdf.
            row : row index, required
                A valid row index of the pdf_data.
            seperator : str, required
                A string on which the text in the row index is split and dispersed.
            direction : str, required
                A string 'vertical' or 'horizontal' representing the direction 
                with which the text is dispersed. If vertical, the bottom and top
                coordinates are adjusted proportional to the number of splits. 
                If horizontal, the left and right coordinates are adjusted proportional
                to the relative character width of the splitted text.
            sort : bool, required
                A boolean whether or not to sort the new resulting data frame.
                Defaults to False.
            """
    # get new text
    pdf_row = pdf_data.loc[row, :]
    new_page = pdf_row['page']
    new_text = pdf_row['text'].split(seperator)
    new_n = len(new_text)
    
    # if no change return
    if new_n == 1:
        return pdf_data
    
    # get new boundaries based on direction
    if direction == 'horizontal':
        weights = np.array([len(x) for x in new_text])
        weights = weights/np.sum(weights)
        new_bounds = pdf_row['left'] + np.cumsum(weights*(pdf_row['right'] - pdf_row['left']))
        new_bounds = np.insert(new_bounds, 0, pdf_row['left'])
        new_cols = ['left', 'right']
        old_cols = ['bottom', 'top']
        old_bounds = np.repeat(pdf_row[old_cols].values.reshape(-1, 2), new_n, axis = 0)
    elif direction == 'vertical':
        new_bounds = np.linspace(pdf_row['bottom'], pdf_row['top'], num = new_n + 1)
        new_cols = ['bottom', 'top']
        old_cols = ['left', 'right']
        old_bounds = np.repeat(pdf_row[old_cols].values.reshape(-1, 2), new_n, axis = 0)
    else:
        raise ValueError("direction must be either vertical or horizontal")
    
    # save the boudaries as a data frame
    new_bounds_list = []
    for i, x in enumerate(new_bounds):
        if i < new_n:
            new_bounds_list.append([x, new_bounds[i + 1]])
    new_bounds = pd.DataFrame(np.array(new_bounds_list), columns = new_cols)
    old_bounds = pd.DataFrame(np.array(old_bounds), columns = old_cols)
    new_text = pd.DataFrame(np.array(new_text).reshape(new_n, -1), columns = ['text'])
    new_page = pd.DataFrame(np.array(new_page).repeat(new_n).reshape(new_n, -1), columns = ['page'])
    
    # combine
    new_row = pd.concat([new_page, old_bounds, new_bounds, new_text], axis = 1)
    new_row = new_row[['page', 'left', 'right', 'bottom', 'top', 'text']]
    
    # replace
    new_pdf_data = pd.concat([pdf_data.drop(pdf_row.name, axis = 0), new_row])
    
    # sort if needed
    if sort:
        new_pdf_data = new_pdf_data.sort_values(by=['page', 'top', 'left'], ascending = [True, False, True])
    
    # reindex
    new_pdf_data.index = range(new_pdf_data.shape[0])
    
    return new_pdf_data
        
def disperse(pdf_data, seperator, direction):
    """Recursively splits pdf text along a specified seperator.

            Returns a data frame with at least as many rows as input. The text 
            data is recursively split at the specified seperator until the specified
            seperator is no longer present in the pdf data. Coordinates are 
            adjusted accordingly according to the width of text split and direction 
            of dispersion.

            Parameters
            ----------
            pdf_data : data frame, required
                A data frame representing the extracted data of a pdf.
            seperator : str, required
                A string on which text data is recursively split and dispersed.
            direction : str, required
                A string 'vertical' or 'horizontal' representing the direction 
                with which the text is dispersed. If vertical, the bottom and top
                coordinates are recursively adjusted proportional to the number 
                of splits. If horizontal, the left and right coordinates are 
                recursively  adjusted proportional to the relative character 
                width of the splitted text.
            """
    n = pdf_data.shape[0]
    sep_in = np.array([seperator in x for x in pdf_data['text']])
    ctr = 0
    
    # recurse
    while np.any(sep_in) and ctr <= n:
        row = np.where(sep_in)[0][0]
        row_idx = pdf_data.index[row]
        pdf_data = disperse_row(pdf_data, row = row_idx, seperator = seperator, direction = direction, sort = False)
        sep_in = np.array([seperator in x for x in pdf_data['text']])
        ctr = ctr + 1
        
    # sort and reindex
    pdf_data = pdf_data.sort_values(by=['page', 'top', 'left'], ascending = [True, False, True])
    pdf_data.index = range(pdf_data.shape[0])
        
    return pdf_data

def coalesce_rows(pdf_data, rows, direction, sort = True):
    """Coalesce pdf data dispersed over several rows.

            Returns a data frame with no more than the number of rows as input. 
            The text associated with the specified rows are combined into a new
            row. Coordinates are adjusted and text is combined according to 
            the direction of coalescence.

            Parameters
            ----------
            pdf_data : data frame, required
                A data frame representing the extracted data of a pdf.
            rows : row indices, required
                Valid row indices of the pdf_data.
            direction : str, required
                A string 'vertical' or 'horizontal' representing the direction 
                with which the text is coalesced. If vertical, text is combined
                with a new line character. If horizontal, text is combined with
                a space.
            sort : bool, required
                A boolean whether or not to sort the new resulting data frame.
                Defaults to True.
            """
    # get new text
    pdf_rows = pdf_data.loc[rows, :]
    if pdf_rows['page'].nunique() > 1:
        raise ValueError("data to coalesce must be on one page.")
    new_page = pdf_rows['page'].unique()[0]
    new_text = pdf_rows['text']
    new_n = len(new_text)
    
    # if no change return
    if new_n == 1:
        return pdf_data
    
    # set seperator
    if direction == 'vertical':
        seperator = '\n'
    elif direction == 'horizontal':
        seperator = ' '
    else:
        raise ValueError("direction must be either vertical or horizontal")
        
    # get new boundaries based on direction
    new_row = np.array([[np.min(pdf_rows['left']), np.max(pdf_rows['right']), 
                           np.min(pdf_rows['bottom']), np.max(pdf_rows['top'])]])
    new_cols = ['left', 'right', 'bottom', 'top']
    new_row = pd.DataFrame(new_row, columns = new_cols)
                
    # save the text and page
    new_row['text'] = new_text.str.cat(sep = seperator)
    new_row['page'] = new_page
    new_row = new_row[['page', 'left', 'right', 'bottom', 'top', 'text']]
    
    # replace
    new_pdf_data = pd.concat([pdf_data.drop(pdf_rows.index, axis = 0), new_row])
    
    # sort if needed
    if sort:
        new_pdf_data = new_pdf_data.sort_values(by=['page', 'top', 'left'], ascending = [True, False, True])
    
    # reindex
    new_pdf_data.index = range(new_pdf_data.shape[0])
    
    return new_pdf_data