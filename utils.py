"""
Helper functions and utilities for the application
"""
import os
import logging
from datetime import datetime, timezone
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)


def utc_now():
    """Return current time as timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


def local_now():
    """Return current local time as a timezone-aware datetime."""
    return datetime.now().astimezone()


def local_dt(dt, fmt='%Y-%m-%d %H:%M'):
    """
    Convert a datetime (assumed UTC if naive) to local timezone and format it.
    
    Usage in templates: {{ some_dt|local_dt('%Y-%m-%d') }}
    
    Args:
        dt: datetime object to convert
        fmt: format string for output
    
    Returns:
        Formatted datetime string or empty string if dt is None
    """
    if not dt:
        return ''
    try:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone().strftime(fmt)
    except Exception as e:
        logger.error(f"Error formatting datetime {dt}: {str(e)}")
        return str(dt)


def days_since(dt, reference_dt=None):
    """Deprecated - no longer needed"""
    return 0


def duration_between(start_dt, end_dt):
    """Deprecated - no longer needed"""
    return 0


def allowed_upload_file(filename, allowed_extensions):
    """
    Check if uploaded file has allowed extension.
    
    Args:
        filename: name of the file
        allowed_extensions: set of allowed file extensions
    
    Returns:
        True if file is allowed, False otherwise
    """
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in allowed_extensions


def check_file_size(file, max_size_mb=5):
    """
    Check if uploaded file size is within allowed limit.
    
    Args:
        file: uploaded file object
        max_size_mb: maximum allowed size in MB (default: 5MB)
    
    Returns:
        tuple: (is_valid, size_bytes, size_mb)
    """
    if not file:
        return False, 0, 0
    
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    
    size_mb = file_size / (1024 * 1024)
    is_valid = size_mb <= max_size_mb
    
    return is_valid, file_size, size_mb


def ensure_directories(*directories):
    """
    Create directories if they don't exist.
    
    Args:
        *directories: paths to create
    """
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Directory ensured: {directory}")


def safe_save_file(file, folder, allowed_extensions, original_name=False):
    """
    Safely save an uploaded file.
    
    Args:
        file: FileStorage object from request.files
        folder: destination folder
        allowed_extensions: set of allowed extensions
        original_name: if True, keep original filename; if False, use random name
    
    Returns:
        Tuple of (success: bool, filename: str, message: str)
    """
    try:
        if not file or file.filename == "":
            return False, "", "No file provided"
        
        if not allowed_upload_file(file.filename, allowed_extensions):
            ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else "unknown"
            return False, "", f"File extension '{ext}' not allowed"
        
        filename = secure_filename(file.filename)
        if not original_name:
            # Generate unique filename
            import uuid
            name, ext = filename.rsplit('.', 1)
            filename = f"{uuid.uuid4().hex[:8]}_{name}.{ext}"
        
        filepath = os.path.join(folder, filename)
        file.save(filepath)
        logger.info(f"File saved successfully: {filepath}")
        return True, filename, ""
    
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        return False, "", str(e)


def get_fault_status(fault):
    """
    Get human-readable status of a fault.
    
    Args:
        fault: Fault model instance
    
    Returns:
        Status string in Arabic
    """
    if fault.resolved_at:
        return "مصلح"
    return "قيد الانتظار"


def calculate_time_diff(start_dt, end_dt=None):
    """
    Calculate time difference between two datetimes.
    
    Args:
        start_dt: start datetime
        end_dt: end datetime (defaults to now)
    
    Returns:
        Dictionary with days, hours, minutes
    """
    if end_dt is None:
        end_dt = utc_now()
    
    if start_dt.tzinfo is None:
        start_dt = start_dt.replace(tzinfo=timezone.utc)
    
    diff = end_dt - start_dt
    
    total_seconds = int(diff.total_seconds())
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    
    return {
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'total_seconds': total_seconds
    }


def format_time_diff(diff_dict):
    """
    Format time difference dictionary to Arabic string.
    
    Args:
        diff_dict: dictionary from calculate_time_diff()
    
    Returns:
        Formatted string in Arabic
    """
    parts = []
    
    if diff_dict['days'] > 0:
        parts.append(f"{diff_dict['days']} يوم" if diff_dict['days'] == 1 else f"{diff_dict['days']} أيام")
    
    if diff_dict['hours'] > 0:
        parts.append(f"{diff_dict['hours']} ساعة" if diff_dict['hours'] == 1 else f"{diff_dict['hours']} ساعات")
    
    if diff_dict['minutes'] > 0 and len(parts) < 2:
        parts.append(f"{diff_dict['minutes']} دقيقة" if diff_dict['minutes'] == 1 else f"{diff_dict['minutes']} دقائق")
    
    return " و ".join(parts) if parts else "أقل من دقيقة"
