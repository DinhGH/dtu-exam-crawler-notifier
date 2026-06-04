import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

BASE = "https://pdaotao.duytan.edu.vn/"
EXAM_LIST = urljoin(BASE, "EXAM_LIST/")

def inspect_main():
    print("Fetching main exam list:", EXAM_LIST)
    r = requests.get(EXAM_LIST, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "html.parser")
    # try multiple link patterns that might appear
    patterns = [
        re.compile(r"\.\./EXAM_LIST_Detail/\?ID=\d+(&lang=\w+)?"),
        re.compile(r"EXAM_LIST_Detail/\?ID=\d+(&lang=\w+)?"),
        re.compile(r"\./EXAM_LIST_Detail/\?ID=\d+(&lang=\w+)?"),
    ]
    links = []
    for p in patterns:
        found = soup.find_all("a", href=p)
        if found:
            links.extend(found)
    # fallback: find anchors with 'EXAM_LIST_Detail' in href
    if not links:
        links = [a for a in soup.find_all("a", href=True) if "EXAM_LIST_Detail" in a["href"]]
    print("Total detail links found:", len(links))
    for a in links[:10]:
        text = a.get_text(strip=True)
        href = a.get("href")
        print("-", text, "->", href)

def inspect_detail(sample_id=64476):
    detail = urljoin(BASE, f"EXAM_LIST_Detail/?ID={sample_id}&lang=VN")
    print("\nFetching detail page:", detail)
    r = requests.get(detail, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "html.parser")
    # Print the surrounding table/td where links live
    tds = soup.find_all("td", class_="border_main")
    print("Number of td.border_main found:", len(tds))
    if tds:
        print("First border_main inner text snippet:")
        print(tds[0].get_text(" ", strip=True)[:400])
        # find all anchors inside
        anchors = tds[0].find_all("a", href=True)
        print("Anchors inside first border_main:", len(anchors))
        for a in anchors[:20]:
            print(" -", a.get_text(" ", strip=True), "->", a["href"])
    # find any file links (uploads/Exam or /uploads)
    file_links = soup.find_all("a", href=re.compile(r"uploads/.+\.(xls|xlsx|xlsm|zip)$", re.IGNORECASE))
    print("File links found via regex:", len(file_links))
    for f in file_links:
        print(" FILE ->", f.get("href"))

if __name__ == "__main__":
    inspect_main()
    inspect_detail()