import requests
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.models.exam_file import ExamFile
from app.utils.logger import crawler_logger, log
from app.core.config import settings

class CrawlerService:
    def __init__(self, db: Session):
        self.db = db
        self.base_url = urljoin(settings.BASE_URL, "EXAM_LIST/")
        self.exam_list_url = urljoin(self.base_url, "Default.aspx?lang=VN")
        self.storage_path = Path("storage/excel")
        self.storage_path.mkdir(exist_ok=True)

    def crawl_exam_files(self) -> list[ExamFile]:
        """
        Crawls the DTU exam website to find and download new exam files.

        Returns:
            list[ExamFile]: A list of newly downloaded exam files.
        """
        crawler_logger.info("Starting exam file crawl...")
        new_files = []
        try:
            # Step 1 & 2: Access and parse the main exam list page
            response = requests.get(self.exam_list_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Step 3: Find all detail page links
            detail_links = soup.find_all("a", href=re.compile(r"\.\./EXAM_LIST_Detail/\?ID=\d+&lang=VN"))
            if not detail_links:
                crawler_logger.warning("No detail links found on the main page.")
                return []

            for link in detail_links:
                detail_url = urljoin(self.base_url, link["href"])
                title = link.get_text(strip=True)

                # Step 4: Access each detail page
                try:
                    file_url = self._get_file_url_from_detail(detail_url)
                    if not file_url:
                        crawler_logger.warning(f"No Excel file found for: {title}")
                        continue

                    # Step 7: Check if the file URL already exists in the database
                    if self.db.query(ExamFile).filter(ExamFile.file_url == file_url).first():
                        crawler_logger.info(f"Skipping existing file: {file_url}")
                        continue
                    
                    crawler_logger.info(f"Found new file: {file_url}")

                    # Step 8: Download the new file
                    file_name = self._download_file(file_url)
                    if not file_name:
                        continue

                    # Save new file info to the database
                    new_exam_file = ExamFile(
                        title=title,
                        detail_url=detail_url,
                        file_url=file_url,
                        file_name=file_name,
                        crawl_time=datetime.now(),
                    )
                    self.db.add(new_exam_file)
                    self.db.commit()
                    self.db.refresh(new_exam_file)
                    new_files.append(new_exam_file)
                    crawler_logger.success(f"Successfully saved and downloaded: {file_name}")

                except requests.HTTPError as e:
                    log.error(f"HTTP error accessing detail page {detail_url}: {e}")
                except Exception as e:
                    log.error(f"An error occurred while processing {detail_url}: {e}")
        
        except requests.RequestException as e:
            log.error(f"Could not connect to the exam list page: {e}")
        except Exception as e:
            log.error(f"An unexpected error occurred during crawling: {e}")

        crawler_logger.info(f"Crawl finished. Found {len(new_files)} new files.")
        return new_files

    def _get_file_url_from_detail(self, detail_url: str) -> str | None:
        """
        Parses a detail page to find the URL of the Excel file.
        """
        response = requests.get(detail_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Step 5: Find the Excel file link
        file_link = soup.find("a", href=re.compile(r"\.\./uploads/Exam/.*\.xlsx?"))
        if file_link:
            # Step 6: Construct the full file URL
            return urljoin(self.base_url, file_link["href"])
        return None

    def _download_file(self, file_url: str) -> str | None:
        """
        Downloads a file from a URL to the storage directory.
        """
        try:
            response = requests.get(file_url, stream=True)
            response.raise_for_status()
            
            file_name = Path(file_url).name
            file_path = self.storage_path / file_name

            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            crawler_logger.info(f"File downloaded to: {file_path}")
            return file_name
        except requests.RequestException as e:
            log.error(f"Failed to download file {file_url}: {e}")
            return None