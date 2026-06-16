from pypdf import PdfReader
import re
import sys
from pathlib import Path

# Path to the downloaded file
file_path = Path("storage/excel/Đọc 2 - KOR 206 (B-D-F-H-J-L) (08_19 29-05-2026)")
if not file_path.exists():
    print(f"File not found: {file_path}")
    sys.exit(1)

reader = PdfReader(str(file_path))
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    print(f"--- Page {i+1} ---")
    lines = text.split('\n')
    for line in lines:
        print(f"Line: '{line}'")
        # Try splitting with more flexible regex
        parts = re.split(r'\s+', line.strip())
        print(f"  Parts: {parts}")