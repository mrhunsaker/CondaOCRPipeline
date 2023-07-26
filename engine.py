# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 12:38:51 2023

@author: COnnor.gibbs
"""

from py import FileIO, TesseractUtils, PDFMinerUtils
import camelot
import tabula

#------------------------------------------------------------------------------
# Using tabula
#------------------------------------------------------------------------------
tables = tabula.read_pdf("examples/sample_table.pdf", pages="all")
# number of tables
len([x for x in tables if x.shape[0] != 0])
# viewing and saving
tables[0]
tables[0].to_csv("examples/sample_table_tabula.csv")

#------------------------------------------------------------------------------
# Using camelot
#------------------------------------------------------------------------------
tables = camelot.read_pdf("examples/sample_table.pdf", flavor = "lattice")
# number of tables
tables.n
# viewing and saving
tables[0].df
tables[0].to_csv("examples/sample_table_camelot.csv")

#------------------------------------------------------------------------------
# Using PDFMiner
#------------------------------------------------------------------------------
pdf = PDFMinerUtils.extract_pdf_text("examples/sample_bill.pdf")
PDFMinerUtils.get_page_coordinates(pdf)
pdf_data = PDFMinerUtils.extract_pdf_data(pdf)
pdf_data = PDFMinerUtils.disperse(pdf_data, seperator = '\n', direction = 'vertical')
pdf_data = PDFMinerUtils.disperse(pdf_data, seperator = ' ', direction = 'horizontal')
pdf_data = pdf_data.query("text != ''")
pdf_data.index = range(pdf_data.shape[0])

#------------------------------------------------------------------------------
# Using tesseract
#------------------------------------------------------------------------------
pdf = TesseractUtils.extract_pdf_text("examples/sample_bill.pdf")
pdf_data = TesseractUtils.extract_pdf_data("examples/sample_bill.pdf")

#------------------------------------------------------------------------------
# From text file delivered by relativity, Kofax, Adobe Pro, or other OCR tools
#------------------------------------------------------------------------------
txt = FileIO.read_txt_lines('examples/sample_payroll.txt')