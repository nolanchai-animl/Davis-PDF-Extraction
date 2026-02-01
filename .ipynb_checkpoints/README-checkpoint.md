# OCR

This project implements OCR for the first 10 pages of a general PDF. This program will be compatiable with SQL databases.

### General Questions

- what libraries should I use for the OCR?
  - Looked at tesseract. I would use pytesseract wrapper, though this means I would have to locally download tesseract for my OS, so I would have a system dependency
  - Could bundle tesseract binaries in files but that sounds hard
  - Could also use `easyocr` but that varies in model accuracy
  - After reviewing more, `easyocr` seems like a solid choice
- How do you get the OCR model to read the PDF?
  - Have not looked into this yet, will have to do this
  - Found some documentation on `easyocr`, will look at it tomorrow
- How do you make this program interact and pull from specific SQL databases?
  - Not sure yet, this will be something to look into down the line (after OCR model implementation)
