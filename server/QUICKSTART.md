# Quick Start Guide

## Prerequisites

- Python 3.9+
- PostgreSQL database
- Gmail account (or other SMTP server) for email notifications

## Setup Instructions

### 1. Install Dependencies

```bash
cd server
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `server` directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dtu_exam_notifier
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
CRAWL_INTERVAL=60
APP_NAME=DTU Exam Crawler Notifier
DEBUG=False
```

**Important**: For Gmail, use an [App Password](https://myaccount.google.com/apppasswords) instead of your regular password.

### 3. Initialize Database

```bash
python -c "from app.core.database import init_db; init_db()"
```

This will create all required tables in your PostgreSQL database.

### 4. Run the Server

```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

### 5. Access API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Quick Test

```bash
# 1. Register a subscription
curl -X POST "http://localhost:8000/api/subscriptions/register" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test Student",
    "email": "test@example.com",
    "course_code": "CS101",
    "course_name": "Introduction to Programming"
  }'

# 2. Get all subscriptions
curl "http://localhost:8000/api/subscriptions/"

# 3. Check subscription count
curl "http://localhost:8000/api/subscriptions/stats/count"

# 4. View notification statistics
curl "http://localhost:8000/api/notifications/stats/summary"

# 5. Health check
curl "http://localhost:8000/health"
```

## Project Structure

```
server/
├── app/
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   ├── api/                 # API endpoints
│   ├── core/                # Configuration & database
│   └── main.py              # FastAPI app
├── requirements.txt         # Dependencies
├── .env                     # Environment variables
├── BACKEND_GUIDE.md         # Detailed documentation
├── CRAWLER_INTEGRATION_GUIDE.md  # Integration with crawler
└── QUICKSTART.md           # This file
```

## Database Models

### Subscriptions Table
- Stores user subscriptions for exam notifications
- Unique constraint: (email, course_code)

### NotificationHistory Table
- Tracks all sent notifications
- Records status (pending, sent, failed)
- Supports retry logic

## API Endpoints Overview

### Subscription Management
- `POST /api/subscriptions/register` - Register for notifications
- `GET /api/subscriptions/email/{email}` - Get user subscriptions
- `POST /api/subscriptions/cancel` - Cancel subscription
- `GET /api/subscriptions/check/{email}/{course_code}` - Check status

### Notification Management
- `GET /api/notifications/` - List notifications with filters
- `GET /api/notifications/email/{email}` - Get user notification history
- `GET /api/notifications/stats/summary` - Get statistics
- `POST /api/notifications/retry` - Retry failed notifications

See `BACKEND_GUIDE.md` for complete API documentation.

## Integration with Crawler

The Crawler Team (Member 1) should call this method after processing exam files:

```python
from app.services.notification_service import NotificationService
from app.core.database import SessionLocal

db = SessionLocal()
try:
    result = NotificationService.reconcile_and_notify(
        db=db,
        exam_list_data=exam_data,
        exam_file_name="exam_list_20240615.xlsx"
    )
finally:
    db.close()
```

See `CRAWLER_INTEGRATION_GUIDE.md` for detailed integration steps.

## Troubleshooting

### Database Connection Error
```
Error: could not connect to server: Connection refused
```
**Solution**: Ensure PostgreSQL is running and DATABASE_URL is correct.

### Email Sending Fails
```
Error: (535, b'5.7.8 Username and password not accepted')
```
**Solution**: Check SMTP credentials in .env file. For Gmail, use an App Password.

### Port 8000 Already in Use
```
Address already in use
```
**Solution**: Kill the process or use a different port:
```bash
uvicorn app.main:app --port 8001 --reload
```

### Module Not Found Error
```
ModuleNotFoundError: No module named 'app'
```
**Solution**: Run uvicorn from the server directory:
```bash
cd server
uvicorn app.main:app --reload
```

## Production Deployment

For production, consider:

1. **Use Gunicorn instead of Uvicorn**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
   ```

2. **Configure CORS properly**
   ```python
   # In main.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourdomain.com"],  # Specific domain
       allow_credentials=True,
       allow_methods=["GET", "POST", "PUT"],
       allow_headers=["*"],
   )
   ```

3. **Use environment-specific settings**
   ```python
   if settings.debug:
       # Development settings
   else:
       # Production settings
   ```

4. **Set up logging**
   - Configure log files
   - Use structured logging
   - Set up log rotation

5. **Database**
   - Use connection pooling
   - Regular backups
   - Monitor query performance

6. **Security**
   - Use HTTPS only
   - Validate all inputs
   - Rate limiting
   - API key authentication (if needed)

## Support Documentation

- **BACKEND_GUIDE.md** - Complete API and implementation details
- **CRAWLER_INTEGRATION_GUIDE.md** - How to integrate with crawler
- **QUICKSTART.md** - This file

For questions about specific endpoints, see the Swagger documentation at http://localhost:8000/docs
