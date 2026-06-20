import requests
import re
from datetime import datetime, timezone, timedelta
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.models.exam_file import ExamFile
from app.utils.logger import crawler_logger, log
from app.core.config import settings


class CrawlerService:
    def __init__(self, db: Session):
        self.db = db
        self.base_url = settings.BASE_URL
        self.exam_list_url = urljoin(self.base_url, "EXAM_LIST/")

    def crawl_exam_files(self, crawl_latest_only: bool = False) -> list[ExamFile]:
        """
        Crawls the DTU exam website to find exam file links.
        
        Args:
            crawl_latest_only: If True, crawl only 100 most recent files and delete existing data first
            
        Returns:
            list[ExamFile]: A list of newly crawled exam files.
        """
        crawler_logger.info("Starting exam file crawl...")
        new_files = []
        
        try:
            # Always delete existing data before crawling new ones
            deleted_count = self.db.query(ExamFile).delete()
            self.db.commit()
            crawler_logger.info(f"Deleted {deleted_count} existing exam files before crawling.")
            
            # Step 1: Access and parse the exam list pages to get detail page links
            collected_links: list[tuple[str, str]] = []
            page = 1
            max_pages = 7  # Reduced to ensure we get ~100 files
            max_links = 105  # Limit to 100 files
            
            while page <= max_pages and len(collected_links) < max_links:
                page_url = f"{self.exam_list_url}?page={page}&lang=VN"
                crawler_logger.info(f"Fetching exam list page: {page_url}")
                response = requests.get(page_url, timeout=15)
                
                if response.status_code == 404:
                    break
                response.raise_for_status()
                
                page_soup = BeautifulSoup(response.content, "html.parser")
                
                # Find all links to detail pages
                # Pattern: <a href="../EXAM_LIST_Detail/?ID=...&lang=VN" class="txt_l4">...
                anchors = page_soup.find_all("a", href=True)
                found_on_page = False
                
                for a in anchors:
                    href = a.get("href")
                    if not href:
                        continue
                    
                    # Pick any link that points to the detail page
                    if "EXAM_LIST_Detail" in href:
                        text = a.get_text(" ", strip=True)
                        # deduplicate by href
                        if href not in [h for h, _ in collected_links]:
                            collected_links.append((href, text))
                            found_on_page = True
                            if len(collected_links) >= max_links:
                                break
                
                if not found_on_page:
                    break
                page += 1

            if not collected_links:
                crawler_logger.warning("No detail links found on the exam list pages.")
                return []

            crawler_logger.info(f"Found {len(collected_links)} detail links to process.")

            # Process collected links
            for href, raw_text in collected_links:
                detail_url = urljoin(self.base_url, href)
                title = " ".join(raw_text.split())

                try:
                    # Get the file URL from detail page
                    file_url = self._get_file_url_from_detail(detail_url)
                    if not file_url:
                        crawler_logger.warning(f"No Excel file found for: {title}")
                        continue
                    
                    # Check if already exists
                    if self.db.query(ExamFile).filter(ExamFile.download_link == file_url).first():
                        crawler_logger.info(f"Skipping existing file: {file_url}")
                        continue
                    
                    crawler_logger.info(f"Found new file: {title}")

                    # Extract filename from title (keep only the filename part without the path)
                    # The title format is like: "Tổng quan Hành vi Tổ chức trong Du lịch OB 253 (B-D-F) (17:18 29/05/2026)"
                    file_name = title.strip()

                    # Save to database
                    # Use GMT+7 for the crawled time
                    gmt7 = timezone(timedelta(hours=7))
                    now_gmt7 = datetime.now(gmt7).replace(tzinfo=None)
                    new_exam_file = ExamFile(
                        file_name=file_name,
                        download_link=file_url,
                        crawl_time=now_gmt7,
                        created_at=now_gmt7,
                    )
                    self.db.add(new_exam_file)
                    self.db.commit()
                    self.db.refresh(new_exam_file)
                    new_files.append(new_exam_file)
                    crawler_logger.success(f"Successfully saved: {file_name}")

                except requests.HTTPError as e:
                    log.error(f"HTTP error accessing detail page {detail_url}: {e}")
                except Exception as e:
                    log.error(f"An error occurred while processing {detail_url}: {e}")
            
            if crawl_latest_only and new_files:
                crawler_logger.info(f"Crawl finished. Added {len(new_files)} new files.")
            elif not crawl_latest_only:
                crawler_logger.info(f"Crawl finished. Found {len(new_files)} new files.")

        except requests.RequestException as e:
            log.error(f"Could not connect to the exam list page: {e}")
        except Exception as e:
            log.error(f"An unexpected error occurred during crawling: {e}")

        return new_files

    def _get_file_url_from_detail(self, detail_url: str) -> str | None:
        """
        Parses a detail page to find the URL of the Excel file.
        Based on the HTML structure: <a href="../uploads/..." class="txt_l4">
        """
        response = requests.get(detail_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the Excel / file link - look for links containing "uploads" and ending with excel extensions
        file_link = None
        for a in soup.find_all("a", href=True):
            href = a.get("href", "")
            if "uploads" in href.lower() and re.search(r"\.(xls|xlsx|xlsm|pdf|zip)$", href, re.IGNORECASE):
                file_link = a
                break
        
        if file_link:
            return urljoin(self.base_url, file_link["href"])
        return None
