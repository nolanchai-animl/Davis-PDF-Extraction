# OCR

This project implements OCR for the first 10 pages of a general PDF. This program will be compatiable with SQL databases. Currently the `testing.ipynb` file has functionality up to scanning the first ten pages of `example.pdf` and processing the scanned results into images that box and show what was scanned.

I plan to clean up and improve functionality of code next. I also plan to incorporate funcrionality with SQL databases down the line. More info and questions I have can be seen in the `testing.ipynb` file.

*Recently* I have replaced `easyocr` for `pytesseract`. I had to include the `Tesseract-OCR` directory which includes tessearct binaries. Then pytesseract is implemented using uv add pytesseract

To verify tesseract is working run command `.\Tesseract-OCR\tesseract.exe`, not just `tesseract -v` (that didn't work for some reason).