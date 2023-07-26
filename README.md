# OCR: Optical Character Recognition
Set up Anaconda environment with image preprocessing and optical character recognition tools.

## Software Requirements
* Install [Anaconda](https://www.anaconda.com/download) for Windows.
* Install [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki) for Windows and note the location of the executable, e.g., `~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe`.
* Install [Poppler](https://github.com/oschwartz10612/poppler-windows/releases/) for Windows and note the location of the binary folder, e.g., `~\AppData\Local\Programs\poppler-23.07.0\Library\bin`.
* Install [Ghostscript](https://ghostscript.com/releases/gsdnld.html) for Windows and note the location of the binary and library folders, e.g., `~\Program Files\gs\gs10.01.2\bin` and `~\Program Files\gs\gs10.01.2\lib`, respectively.

## Setting up the Environment
* Clone the repository.
* Add the Ghostscript binary and library folders to PATH.
* Add Tesseract-OCR executable to `py/TesseractUtils.py`
* Add Poppler binary folder to `py/TesseractUtils.py`

## Image Preprocessing Tools
The accuracy of OCR can be affected by the quality of the image. Preprocessing the image (such as resizing, denoising, or enhancing contrast) can help improve OCR results. The following Python libraries are included in the environment to perform image preprocessing:
1. OpenCV
2. PIL

## Optical Character Recognition Tools
When choosing an OCR tool, it is important to consider the following factors:
* The type of data you need to extract (text, tables, or both).
* The complexity of the PDF layout and whether the documents are scanned or not.
* The performance and accuracy required for your specific use case.
* The level of control and customization you need in the OCR process.
* The programming complexity and the available community support for each tool.

Ultimately, the best OCR tool depends on the specific requirements and characteristics of your PDF documents. It is often beneficial to try multiple tools and evaluate their performance on a representative sample of your data to find the most suitable one. The following discusses the strengths and weaknesses of tools included in the environment.

1. Tabula:
* Strengths: Tabula is specifically designed for extracting tables from PDFs, making it ideal for tabular data extraction. It provides a simple interface to select tables graphically using a GUI or specify the table coordinates programmatically. Works well for structured data with clear table boundaries.
* Weaknesses: Limited to table extraction and may not be suitable for extracting non-tabular text. Performance may be affected if the PDFs are scanned documents or have complex layouts.

2. Camelot:
* Strengths: Camelot is another library dedicated to table extraction from PDFs. It can handle both simple and complex tables, including tables with merged cells or varying row/column structures. Supports multiple table detection methods. Provides both a simple API and an advanced API for fine-tuning table extraction.
* Weaknesses: Like Tabula, it is focused on table extraction, so it may not be the best choice for general text extraction.

3. Pytesseract:
* Strengths: Pytesseract is a widely used OCR library that supports various image formats. It can handle general text extraction from images and scanned documents. Works well for extracting text from images with simple layouts.
* Weaknesses: May not perform optimally on complex or noisy images with low-quality text. Lack of support for structured data extraction like tables.

4. pdfminer:
* Strengths: Pdfminer is a powerful PDF parsing library that can extract text and layout information from PDF documents. Provides detailed layout information, which can be useful for preserving the original document structure. Supports text extraction in multiple encodings.
* Weaknesses: Requires more effort and coding compared to specialized OCR tools for table extraction. Performance may vary depending on the complexity of the PDF layout.
