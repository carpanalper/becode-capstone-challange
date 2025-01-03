import os
import sqlite3
import pandas as pd

db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'news.db')

# connect to the db
def get_data_from_db():
    conn = sqlite3.connect(db_path)  
    query = "SELECT * FROM news"  
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# getting the news from last 24 hours
def get_daily_news():
    conn = sqlite3.connect(db_path)
    query = '''
            SELECT * 
            FROM news
            WHERE date >= datetime('now', '-1 day');
            '''
    daily_df = pd.read_sql(query,conn)
    conn.close()
    return daily_df

# getting the news from last 7 days
def get_weekly_news():
    conn = sqlite3.connect(db_path)
    query = '''
            SELECT * 
            FROM news
            WHERE date >= datetime('now', '-7 day');
            '''
    weekly_df = pd.read_sql(query,conn)
    conn.close()
    return weekly_df

# time distribution of news
def get_time_distribution():
    conn = sqlite3.connect(db_path)
    query = '''
            SELECT strftime('%H', date) AS hour, COUNT(*) AS count
            FROM news
            GROUP BY hour
            ORDER BY hour;
            '''
    time_df = pd.read_sql(query,conn)
    conn.close()
    return time_df

# titles 
def get_titles():
    conn = sqlite3.connect(db_path)
    query = '''
            SELECT title
            FROM news;
            '''
    titles_df = pd.read_sql(query,conn)
    conn.close()

    return titles_df

def delete_null_title():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM news
    WHERE title IS NULL
    ''')
    conn.commit()
    conn.close()