"""
Performance monitoring for 7000 cameras
"""
import logging
import time
import psutil
from flask import current_app

logger = logging.getLogger(__name__)

def check_system_health():
    """Check system health and performance metrics"""
    try:
        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        
        # Log warnings if thresholds exceeded
        if memory_percent > 80:
            logger.warning(f"High memory usage: {memory_percent}%")
        
        if cpu_percent > 80:
            logger.warning(f"High CPU usage: {cpu_percent}%")
            
        if disk_percent > 90:
            logger.warning(f"High disk usage: {disk_percent}%")
        
        return {
            'memory_percent': memory_percent,
            'cpu_percent': cpu_percent,
            'disk_percent': disk_percent,
            'status': 'healthy' if all(x < 80 for x in [memory_percent, cpu_percent, disk_percent]) else 'warning'
        }
        
    except Exception as e:
        logger.error(f"Error checking system health: {e}")
        return {'status': 'error', 'error': str(e)}

def log_slow_query(query_time, threshold=2.0):
    """Log slow queries"""
    if query_time > threshold:
        logger.warning(f"Slow query detected: {query_time:.2f}s (threshold: {threshold}s)")

def monitor_database_pool():
    """Monitor database connection pool health"""
    try:
        engine = current_app.extensions['sqlalchemy'].engine
        pool = engine.pool
        
        logger.info(f"DB Pool - Size: {pool.size()}, Checked in: {pool.checkedin()}, Overflow: {pool.overflow()}")
        
        if pool.overflow() > 0:
            logger.warning(f"Database pool overflow detected: {pool.overflow()}")
            
    except Exception as e:
        logger.error(f"Error monitoring database pool: {e}")
