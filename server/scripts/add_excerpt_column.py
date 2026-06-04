"""
Script to add excerpt column to exam_files table.
This script adds the excerpt column to store the original content from detail pages.
"""
import sys
import os

# Add the app/server parent directory to the path so `import app` works when run from server/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.database import engine
from app.models.exam_file import ExamFile
from sqlalchemy import text

def add_excerpt_column():
    """Add excerpt column to exam_files table if it doesn't exist."""
    with engine.connect() as conn:
        # Check if column exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'exam_files' AND column_name = 'excerpt'
        """)).fetchone()
        
        if result:
            print("Column 'excerpt' already exists.")
            return
        
        # Add column
        conn.execute(text("ALTER TABLE exam_files ADD COLUMN excerpt TEXT"))
        conn.commit()
        print("Successfully added 'excerpt' column to exam_files table.")

if __name__ == "__main__":
    add_excerpt_column()
