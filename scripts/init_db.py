import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import init_database

if __name__ == "__main__":
    init_database()
    print("Database initialized successfully")