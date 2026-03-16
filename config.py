"""
Application configuration management
"""
import os
from datetime import timedelta


def _get_database_uri():
    """Get database URI with fallback to SQLite"""
    url = os.environ.get('DATABASE_URL') or 'sqlite:///camera_system.db'
    if url.startswith('postgresql') or url.startswith('postgres://'):
        try:
            import psycopg2  # noqa: F401
            return url
        except ImportError:
            print("Warning: psycopg2 not installed. Falling back to SQLite.")
            return 'sqlite:///camera_system.db'
    return url


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = _get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    LOGO_FOLDER = os.path.join('static', 'logo')
    COMPANY_LOGO = os.path.join('static', 'logo', 'company_logo.png')
    
    # Application settings
    COMPANY_NAME = os.environ.get('COMPANY_NAME', 'CCTV Portal EG')
    LOGO_SIZE = int(os.environ.get('LOGO_SIZE', '50'))
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Fault configuration
    FAULT_EXPIRY_DAYS = 7


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # Requires HTTPS
    
    # Ensure SECRET_KEY is set in production
    @classmethod
    def init_app(cls, app):
        if cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError("Please set SECRET_KEY environment variable in production!")


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
