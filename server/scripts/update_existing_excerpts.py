"""
Update excerpt for existing exam files.
This script fetches the excerpt from each detail page and updates the database.
"""
import sys
import os

# Add the app/server parent directory to the path so `import app` works when run from server/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.exam_file import ExamFile
from app.core.config import settings
import requests
from bs4 import BeautifulSoup

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_excerpt_from_detail(detail_url: str) -> str | None:
    """
    Parses a detail page to extract the excerpt for display.
    Returns the text from the border_main td (main content area).
    """
    try:
        response = requests.get(detail_url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the main content area (border_main td)
        border_main = soup.find("td", class_="border_main")
        if border_main:
            # Extract text, keeping line breaks for formatting
            text = border_main.get_text("\n", strip=True)
            return text[:1000] if text else None  # Limit to first 1000 chars
        return None
    except Exception as e:
        print(f"Error fetching {detail_url}: {e}")
        return None

def update_existing_excerpts():
    """Update excerpt for all existing exam files."""
    db = SessionLocal()
    try:
        # Get all exam files
        exam_files = db.query(ExamFile).all()
        print(f"Found {len(exam_files)} exam files to update.")
        
        updated_count = 0
        for file in exam_files:
            if not file.detail_url:
                continue
            
            excerpt = get_excerpt_from_detail(file.detail_url)
            if excerpt:
                file.excerpt = excerpt
                updated_count += 1
                print(f"[{updated_count}] Updated excerpt for: {file.title[:50]}...")
            
            # Commit every 5 files to avoid long transactions
            if updated_count > 0 and updated_count % 5 == 0:
                db.commit()
                print(f"  Committed {updated_count} updates so far...")
        
        db.commit()
        print(f"\nSuccessfully updated {updated_count} exam files with excerpts.")
    
    except Exception as e:
        db.rollback()
        print(f"Error updating excerpts: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_existing_excerpts()