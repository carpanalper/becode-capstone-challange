import sqlite3
import json

def database_connection():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS news 
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        url TEXT UNIQUE NOT NULL,
        topic TEXT,
        title TEXT,
        date DATETIME
    )                                 
                    ''')
    
    return conn, cursor

def database_count():
    conn, cursor = database_connection()
    cursor.execute("SELECT COUNT(*) FROM news")
    count = cursor.fetchone()[0]
    conn.close()
    print(f"Total entries in the database: {count}")
    return count

def json_to_db(file_name="latest_news.json"):
    #read json file
    with open(file_name, 'r') as f:
        news_list = json.load(f)
    
    #connect to database
    conn, cursor = database_connection()

    #insert news into database
    cursor.executemany('''
    INSERT INTO news (url, topic, title, date)
    VALUES (?, ?, ?, ?)
                       ''',[(elem['link'], elem['topic'], elem['title'], elem['date']) for elem in news_list])
    
    conn.commit()
    conn.close()
    print(f"Inserted {len(news_list)} entries into the database")

json_to_db()
database_count()