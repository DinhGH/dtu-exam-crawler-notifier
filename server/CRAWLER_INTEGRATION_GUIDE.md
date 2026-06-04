# Integration Guide for Crawler Team

## Overview
This guide shows the Crawler Team (Member 1) how to integrate with the User System & Email Notification backend.

## Data Flow

```
Crawler (Member 1) → Extract Exam Data → Call reconciliation → 
                                                              ↓
                                                    NotificationService
                                                              ↓
                                                    Match with Subscriptions
                                                              ↓
                                                    Send Notifications (Email)
```

## Integration Steps

### 1. Import the Notification Service

```python
from app.services.notification_service import NotificationService
from app.core.database import SessionLocal
```

### 2. After Crawling & Processing Exam Data

After your crawler team extracts exam data from Excel files and processes it, call the reconciliation method:

```python
def process_new_exam_file(file_path: str, file_name: str):
    """
    Process new exam file and notify subscribed users
    
    Args:
        file_path: Path to the Excel file
        file_name: Name of the file (e.g., "exam_list_20240615.xlsx")
    """
    # 1. Read and process the Excel file (Your implementation)
    exam_data = read_exam_file(file_path)  # Your method
    
    # 2. Clean and normalize data
    cleaned_data = clean_exam_data(exam_data)  # Your method
    
    # 3. Call reconciliation - THIS IS WHERE WE INTEGRATE
    db = SessionLocal()
    try:
        result = NotificationService.reconcile_and_notify(
            db=db,
            exam_list_data=cleaned_data,
            exam_file_name=file_name
        )
        
        # Process result
        if result["success"]:
            print(f"✓ Notifications created: {result['created_notifications']}")
            print(f"  Skipped (duplicates): {result['skipped_notifications']}")
            print(f"  Errors: {result['error_count']}")
        else:
            print(f"✗ Reconciliation failed: {result['message']}")
            
        return result
    finally:
        db.close()
```

### 3. Expected Data Format

The `exam_list_data` should be a list of dictionaries with at least these keys:

```python
exam_list_data = [
    {
        # REQUIRED fields (use these exact key names or add aliases in reconcile_and_notify)
        "course_code": "CS101",  # or "mã_môn"
        
        # REQUIRED for subscription matching
        # (already stored in subscription table)
        
        # OPTIONAL fields (exam information)
        "exam_date": "2024-06-15",  # or "ngày_thi"
        "exam_time": "08:00",  # or "giờ_thi"
        "exam_room": "Room 101",  # or "phòng_thi"
        
        # Other fields like:
        # "student_id": "SV001",
        # "student_name": "Nguyễn Văn A",
    },
    # ... more exam records
]
```

### 4. Error Handling

```python
try:
    result = NotificationService.reconcile_and_notify(db, exam_data, file_name)
    
    if not result["success"]:
        # Log error and alert
        logger.error(f"Reconciliation error: {result['message']}")
        # Send alert to admin
        send_admin_alert(f"Failed to process exam file: {file_name}")
        
    # Check for partial failures
    if result.get("error_count", 0) > 0:
        logger.warning(f"Some records failed: {result['error_count']}")
        
except Exception as e:
    logger.error(f"Critical error during reconciliation: {str(e)}")
    raise
```

## Database Connection

The reconciliation method requires a database session. You can:

### Option 1: Use SQLAlchemy Session (Recommended)
```python
from app.core.database import SessionLocal

db = SessionLocal()
try:
    result = NotificationService.reconcile_and_notify(db, data, filename)
finally:
    db.close()
```

### Option 2: Use FastAPI Dependency in Endpoint
```python
from fastapi import Depends
from app.core.database import get_db

@app.post("/process-exam-file")
async def process_exam_file(
    file: UploadFile,
    db: Session = Depends(get_db)
):
    exam_data = process_your_file(file)
    result = NotificationService.reconcile_and_notify(db, exam_data, file.filename)
    return result
```

## What Happens in reconciliation_and_notify()

```
For each exam record in the data:
  1. Extract course_code from record
  2. Find all subscriptions matching this course_code
  3. For each matching subscription:
     a. Check if notification already sent for this email+course+file
     b. If not sent before:
        - Create notification record in database
        - Send email immediately to student
        - Update subscription's last_notified_at timestamp
     c. If already sent:
        - Increment skipped_count (avoid duplicate notifications)
  4. Return statistics
```

## Response Format

The `reconcile_and_notify()` method returns:

```python
{
    "success": True,  # or False if error
    "created_notifications": 45,  # Emails queued/sent
    "skipped_notifications": 5,  # Already notified before
    "error_count": 0,  # Records that failed to process
    "message": "Tạo 45 thông báo, bỏ qua 5"  # Summary message
}
```

## Example Complete Implementation

```python
# In your crawler module (Member 1)
from datetime import datetime
from app.services.notification_service import NotificationService
from app.core.database import SessionLocal
import logging

logger = logging.getLogger(__name__)

def handle_new_exam_file(file_path: str):
    """
    Complete workflow: extract, process, and notify
    """
    try:
        # Step 1: Read Excel file (Your implementation)
        raw_data = pd.read_excel(file_path)
        
        # Step 2: Transform data to standard format
        exam_data = []
        for _, row in raw_data.iterrows():
            exam_record = {
                "course_code": row["Mã môn"],
                "exam_date": str(row["Ngày thi"]),
                "exam_time": row["Giờ thi"],
                "exam_room": row["Phòng thi"],
                "student_id": row["Mã SV"],
                "student_name": row["Họ tên"],
            }
            exam_data.append(exam_record)
        
        # Step 3: Save file to database (Your implementation)
        file_record = save_exam_file(file_path)
        
        # Step 4: INTEGRATE WITH NOTIFICATION SERVICE
        db = SessionLocal()
        try:
            result = NotificationService.reconcile_and_notify(
                db=db,
                exam_list_data=exam_data,
                exam_file_name=file_record.filename
            )
            
            if result["success"]:
                logger.info(f"✓ File processed: {file_record.filename}")
                logger.info(f"  Notifications sent: {result['created_notifications']}")
                
                # Update file processing status in your database
                file_record.status = "processed"
                file_record.processed_at = datetime.utcnow()
                save_file_record(file_record)
            else:
                logger.error(f"✗ Failed to process notifications: {result['message']}")
                file_record.status = "notification_error"
                save_file_record(file_record)
                
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error processing exam file: {str(e)}")
        raise
```

## Duplicate Prevention

The system automatically prevents sending duplicate notifications by:

1. Checking if a notification with same (email, course_code, file_name, status=sent) exists
2. If exists: incrementing `skipped_notifications` counter
3. If not exists: creating and sending new notification

This means:
- ✓ Safe to re-process the same file multiple times
- ✓ Only new exam lists trigger new notifications
- ✓ Students won't receive duplicate emails for same exam

## Testing Integration

```python
# Test the integration locally
def test_reconciliation():
    db = SessionLocal()
    try:
        test_data = [
            {
                "course_code": "CS101",
                "exam_date": "2024-06-15",
                "exam_time": "08:00",
                "exam_room": "Room 101",
            }
        ]
        
        result = NotificationService.reconcile_and_notify(
            db,
            test_data,
            "test_exam_list.xlsx"
        )
        
        print(f"Result: {result}")
        assert result["success"] == True
        
    finally:
        db.close()
```

## Requirements for Successful Integration

1. ✓ Database initialized with Subscription and NotificationHistory tables
2. ✓ SMTP credentials configured in `.env`
3. ✓ At least one subscription exists in the database
4. ✓ Course codes in exam data match course codes in subscriptions
5. ✓ Email server accessible (Gmail SMTP or configured server)

## Troubleshooting

### Problem: "Database table does not exist"
**Solution**: Initialize database
```python
from app.core.database import init_db
init_db()
```

### Problem: "Failed to send email"
**Solution**: Check SMTP configuration in `.env`
```
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Problem: "No notifications created"
**Solution**: Check if subscriptions exist for the course codes
```bash
curl "http://localhost:8000/api/subscriptions/stats/count"
```

## Support

For issues or questions:
1. Check `BACKEND_GUIDE.md` for detailed API documentation
2. Review error logs in console output
3. Check database records:
   ```bash
   # Get all subscriptions
   curl "http://localhost:8000/api/subscriptions/"
   
   # Get notification statistics
   curl "http://localhost:8000/api/notifications/stats/summary"
   ```

---

**Remember**: This implementation is complete and ready for your integration. You only need to call `NotificationService.reconcile_and_notify()` after processing exam files.
