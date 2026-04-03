"""Initialize database"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.models import init_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("✅ Database initialized successfully!")