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
* Open Anaconda prompt and activate the base environment.
* Navigate to the OCR repository.
* Use the conda env create command followed by the --file flag and the path to your .yaml file to create the new environment: `conda env create --file ocr_conda.yaml`.
* Once the environment is created, you can activate it using the following command: `conda activate OCR`.
* Open the Spyder IDE with the following command: `spyder`.
* Run `engine.py`.

## Image Preprocessing Tools
The accuracy of OCR can be affected by the quality of the image. Preprocessing the image (such as resizing, denoising, or enhancing contrast) can help improve OCR results. The following discusses the strengths and weaknesses of image preprocessing tools included in the environment:
1. OpenCV:
* Strengths: OpenCV is a powerful and comprehensive computer vision library with extensive functionality. It offers a wide range of image processing algorithms and is highly efficient, optimized for speed, and suitable for real-time tasks. Its cross-platform support makes it versatile for various development environments, and it excels in handling complex image manipulations like filtering, edge detection, and geometric operations. Additionally, OpenCV can be easily integrated with other libraries, adding to its flexibility and utility.
* Weaknesses: While OpenCV's vast functionality is a great advantage, it can also be a drawback for beginners due to its complex interface and steep learning curve. The documentation, although supported by a large community, may not cover all areas in-depth, which could pose challenges for users trying to explore more specialized tasks.
2. PIL/Pillow
* Strengths: Pillow (Python Imaging Library) provides a user-friendly and straightforward API, making it an ideal choice for basic image manipulation and preprocessing tasks. It is easy to get started with, and its simple interface is consistent and intuitive. Pillow also supports various image formats, enabling easy loading, saving, and conversion of images. Its clear and well-documented functionalities contribute to a beginner-friendly experience, making it easy for users to find the information they need.
* Weaknesses: Pillow is implemented in pure Python, which can result in slower performance compared to OpenCV, especially for computationally intensive tasks. It lacks some of the more advanced computer vision and image processing functionalities that are available in OpenCV, making it less suitable for complex image manipulations. Additionally, Pillow may have limited support for some less common image formats compared to OpenCV.

## Optical Character Recognition Tools
When choosing an OCR tool, it is important to consider the following factors:
* The type of data you need to extract (text, tables, or both).
* The complexity of the PDF layout and whether the documents are scanned or not.
* The performance and accuracy required for your specific use case.
* The level of control and customization you need in the OCR process.
* The programming complexity and the available community support for each tool.

Ultimately, the best OCR tool depends on the specific requirements and characteristics of your PDF documents. It is often beneficial to try multiple tools and evaluate their performance on a representative sample of your data to find the most suitable one. The following discusses the strengths and weaknesses of OCR tools included in the environment:

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
