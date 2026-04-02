"""
ocr.py
------
Handles PDF to image conversion and OCR using pytesseract
"""

from pathlib import Path
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

def pdf_to_image(pdf_path: str, dpi: int=300) -> list[Image.Image]:
    """Convert each page of a PDF to a PIL Image"""
    return convert_from_path(str(Path(pdf_path).resolve()), dpi=dpi)

def ocr_image(image: Image.Image, lang: str="eng") -> str:
    """Run pytesseract on a PIL image and return extracted text"""
    config = r"--oem 3 --psm 3" # LSTM engine, automatic page segmentation
    return pytesseract.image_to_string(image, lang=lang, config=config)

def scan_pdf(pdf_path: str, dpi: int=300, lang: str="eng"):
    """
    Generator that gives (page_number, text) for each page in the PDF
    Keeps memory usage low by procesing one page at a time
    """
    images = pdf_to_image(pdf_path, dpi=dpi) # unfortunately all pages load at once here
    total = len(images)
    for page_num, image in enumerate(images, start=1):
        text = ocr_image(image, lang=lang)
        yield page_num, total, text