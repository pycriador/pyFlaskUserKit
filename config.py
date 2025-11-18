import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration class"""
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    
    # Database configuration
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite')
    
    if DATABASE_TYPE == 'mysql':
        MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
        MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
        MYSQL_USER = os.getenv('MYSQL_USER')
        MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
        MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
        
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
            f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
        )
    else:
        # SQLite as default
        SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH', 'instance/app.db')
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_DB_PATH}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Admin configuration
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')


