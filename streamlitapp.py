import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pytz
import time

# connect to the db
def get_data_from_db():
    conn = sqlite3.connect('news.db')  
    query = "SELECT * FROM news"  
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# getting the news from last 24 hours
def get_daily_news():
    conn = sqlite3.connect("news.db")
    query = '''
            SELECT * 
            FROM news
            WHERE date >= datetime('now', '-1 day');
            '''
    df = pd.read_sql(query,conn)
    conn.close()
    return df

# thema frequency
def get_topic_counts(df):
    return df['topic'].value_counts().head(10)

# Streamlit App
def main():
    # db data
    df = get_data_from_db()
    
    # frequency calculation
    topic_counts = get_topic_counts(df)

    #since
    local_tz = datetime.datetime.now().astimezone().tzinfo

    df['date'] = pd.to_datetime(df['date'])
    oldest_date = df['date'].min().astimezone(local_tz)
    oldest_date_str = oldest_date.to_pydatetime().strftime('%Y-%m-%d %H:%M')
    
    # latest update
    last_update =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # total entries
    total_entries = len(df)

    # Info
    st.subheader('VRT Breaking News Topic Distribution')
    st.write(f"Total Entries: {total_entries}")
    st.write(f"Last Update: {last_update}")

    #daily top 10
    daily_news = get_daily_news()
    daily_top_10 = daily_news['topic'].value_counts().head(10)

    col1, col2 = st.columns(2)

    with col1: 
        # Daily Bar chart
        fig, ax = plt.subplots()
        ax.bar(daily_top_10.index, daily_top_10.values)
        ax.set_xlabel('Topic')
        ax.set_ylabel('No of News')
        ax.set_title('Frequency of Topics (Last Day)')
        plt.xticks(rotation=90)
        #show chart
        st.write(f"News of the Last Day:{len(daily_news)}")
        st.pyplot(fig)
      
    with col2:
        # All time Bar chart 
        fig, ax = plt.subplots()
        ax.bar(topic_counts.index, topic_counts.values)
        ax.set_xlabel('Topic')
        ax.set_ylabel('No of News')
        ax.set_title('Frequency of Topics (All Time)')
        plt.xticks(rotation=90)
        
        # show chart
        st.write(f"Since: {oldest_date_str}")
        st.pyplot(fig)
    
    #refreshing the page every 30 min
    while True:
        time.sleep(1 * 60 * 30) 
        st.rerun()
    
# run the app 
main()