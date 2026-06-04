from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.core.database import init_db
from app.core.config import settings
from app.api import subscriptions, notifications

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="API for automatic exam list crawler and email notification system",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    try:
        init_db()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing database: {str(e)}")
        raise

# Include API routers
app.include_router(subscriptions.router)
app.include_router(notifications.router)

# Health check endpoint
@app.get("/")
def read_root():
    return {
        "message": "DTU Exam Notifier API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.app_name
    }