"""
main.py
---------
Uses files db.py and ocr.py to scan a PDF and store the results in a SQLite3 database
"""

import argparse
import sys
import time
from pathlib import Path

from db import init_db, insert_document, insert_page
from ocr import scan_pdf

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="OCR a PDF with pytesseract and store results in SQLite3"
    )
    parser.add_argument("pdf", help="Path to the PDF file to scan")
    parser.add_argument("--db", default="ocr_results.db", help="SQLite3 database file (default: ocr_results.db)")
    parser.add_argument("--dpi", type=int, default=300, help="Resolution for PDF -> image conversion (default: 300)")
    parser.add_argument("--lang", default="eng", help="pytesseract language code(s), e.g. 'eng', 'fra', 'eng+fra' (default: eng)")
    
    return parser.parse_args()

def main() -> None:
    args = parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"[ERROR] File not found: {args.pdf}", file = sys.stderr)
        sys.exit(1)

    # Set up database
    conn = init_db(args.db)

    print(f"[INFO] Scanning: {pdf_path.name}")
    print(f"[INFO] Settings: {args.dpi} DPI, language='{args.lang}'")
    print(f"[INFO] Database: {args.db}\n")

    doc_id = None

    for page_num, total_pages, text in scan_pdf(args.pdf, dpi=args.dpi, lang=args.lang):
        # Create document record on first page
        if doc_id is None:
            doc_id = insert_document(conn, pdf_path.name, total_pages)
            print(f"[INFO] Document record created (id={doc_id})\n")

        t0 = time.time()
        insert_page(conn, doc_id, page_num, text)
        elapsed = time.time() - t0
        word_count = len(text.split()) if text else 0

        print(f"    Page {page_num:>4}/{total_pages}    {word_count:>6} words   ({elapsed:.1f}s)")

    conn.close()
    print(f"\n[DONE] Scan Complete. Document id={doc_id} stored in '{args.db}'")
    print(f"\nExample queries:")
    print(f"    sqlite3 {args.db} \"SELECT page_number, word_count FROM pages WHERE document_id={doc_id};\"")

if __name__ == "__main__":
    main()