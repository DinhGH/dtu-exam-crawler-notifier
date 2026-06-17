from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv("DATABASE_URL")
print(f"URL: {url}")
try:
    engine = create_engine(url)
    with engine.connect() as conn:
        print("Successfully connected to the database!")
except Exception as e:
    print(f"Failed to connect to the database: {e}")