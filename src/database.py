import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Establish connection to PostgreSQL database"""
    return psycopg2.connect(os.getenv('DATABASE_URL'))

def init_database():
    """Initialize database tables"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create table for stock data
    cur.execute('''
        CREATE TABLE IF NOT EXISTS stock_data (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            date DATE NOT NULL,
            open NUMERIC(10, 4),
            high NUMERIC(10, 4),
            low NUMERIC(10, 4),
            close NUMERIC(10, 4),
            volume BIGINT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(symbol, date)
        )
    ''')
    
    # Create table for LLM insights
    cur.execute('''
        CREATE TABLE IF NOT EXISTS daily_recommendations (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL UNIQUE,
            symbol VARCHAR(10) NOT NULL,
            summary TEXT,
            recommendations TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

def insert_stock_data(symbol, date, open_price, high, low, close_price, volume):
    """Insert stock data into database"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        INSERT INTO stock_data (symbol, date, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (symbol, date) DO UPDATE SET
            open = EXCLUDED.open,
            high = EXCLUDED.high,
            low = EXCLUDED.low,
            close = EXCLUDED.close,
            volume = EXCLUDED.volume
    ''', (symbol, date, open_price, high, low, close_price, volume))
    
    conn.commit()
    cur.close()
    conn.close()

def get_yesterdays_data(symbol):
    """Retrieve yesterday's stock data"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        SELECT date, open, high, low, close, volume
        FROM stock_data
        WHERE symbol = %s
        AND date = CURRENT_DATE - INTERVAL '1 day'
    ''', (symbol,))
    
    result = cur.fetchone()
    cur.close()
    conn.close()
    
    if result:
        return {
            'date': result[0],
            'open': result[1],
            'high': result[2],
            'low': result[3],
            'close': result[4],
            'volume': result[5]
        }
    return None

def insert_recommendation(date, symbol, summary, recommendations):
    """Insert LLM recommendations into database"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        INSERT INTO daily_recommendations (date, symbol, summary, recommendations)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (date) DO UPDATE SET
            symbol = EXCLUDED.symbol,
            summary = EXCLUDED.summary,
            recommendations = EXCLUDED.recommendations
    ''', (date, symbol, summary, recommendations))
    
    conn.commit()
    cur.close()
    conn.close()