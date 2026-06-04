#!/usr/bin/env python3
"""Migration script to add download_link column to exam_files table."""

import os
import sys

# Add the app directory to the path so we can import the database
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import text
from app.core.database import engine


def add_download_link_column():
    """Add download_link column to exam_files if it doesn't exist."""
    # First check if the column exists
    check_sql = """
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'exam_files' 
    AND column_name = 'download_link';
    """
    
    add_sql = """
    ALTER TABLE exam_files 
    ADD COLUMN IF NOT EXISTS download_link TEXT;
    """
    
    with engine.connect() as conn:
        # Check if column exists
        result = conn.execute(text(check_sql)).fetchone()
        if result:
            print("Column 'download_link' already exists in exam_files table.")
        else:
            conn.execute(text(add_sql))
            conn.commit()
            print("Successfully added 'download_link' column to exam_files table.")


if __name__ == "__main__":
    add_download_link_column()