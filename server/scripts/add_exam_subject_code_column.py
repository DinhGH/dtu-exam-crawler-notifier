#!/usr/bin/env python3
"""One-time migration script to add exam_subject_code column to exam_files table."""

import os
import sys

# Add the app directory to the path so we can import the database
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import text
from app.core.database import engine


def add_exam_subject_code_column():
    """Add exam_subject_code column to exam_files if it doesn't exist."""
    sql = """
    ALTER TABLE exam_files 
    ADD COLUMN IF NOT EXISTS exam_subject_code VARCHAR(50);
    """
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    print("Successfully added exam_subject_code column to exam_files table.")


if __name__ == "__main__":
    add_exam_subject_code_column()