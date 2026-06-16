import requests
from pathlib import Path

url = "https://pdaotao.duytan.edu.vn/uploads/Exam/31052026-9h30-KOR%20206%20(B-D-F-H-J-L).pdf"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    print(f"Attempting to download: {url}")
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    file_path = Path("test_download.pdf")
    with open(file_path, 'wb') as f:
        f.write(response.content)
    print(f"Successfully downloaded to {file_path.absolute()}")
except Exception as e:
    print(f"Error: {e}")