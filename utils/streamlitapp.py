import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time
import os
from functions import publish_time_statistics, day_agenda, get_topic_counts 
from queries import get_data_from_db, get_daily_news


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
        ax.set_title('Frequency of Topics (Last 24 hours)')
        plt.xticks(rotation=90)
        #show chart
        st.write(f"Last 24 hours: {len(daily_news)} Entries")
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
    
    # Time statistics
    time_stats = publish_time_statistics(df)
    
    #Bar chart
    #fig, ax = plt.subplots()
    #ax.bar(time_stats["Time Range"], time_stats["No of News"])
    #ax.set_xlabel("Time Range")
    #ax.set_ylabel("No of News")
    #ax.set_title("News Count by Time Range")
    #plt.xticks(rotation=45)

    #st.pyplot(fig)

    # Line chart
    fig, ax = plt.subplots()
    ax.plot(time_stats["Time Range"], time_stats["No of News"], marker='.', color='r', linestyle='-', linewidth=2)

    # Add text labels
    for i, txt in enumerate(time_stats["No of News"]):
        #ax.annotate(txt, (time_stats["Time Range"][i], time_stats["No of News"][i]), textcoords="offset points", xytext=(0,5), ha='center')
        ax.text(time_stats["Time Range"][i], txt, str(txt), ha='right', va='bottom', fontsize=10)

    # Add gridlines
    ax.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)

    ax.set_xlabel("Time Range")
    ax.set_ylabel("No of News")
    ax.set_title("News Count by Time Range")
    plt.xticks(rotation=45)

    st.pyplot(fig)

    # daily agenda
    daily_agenda = day_agenda(df)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(daily_agenda['date'], daily_agenda['count'], marker='o', color='b', linestyle='-', linewidth=2)

    # Grafik ayarları: her noktada konu adı ve sayıyı gösterme
    for i, row in daily_agenda.iterrows():
        ax.text(row['date'], row['count'], f"{row['topic']} ({row['count']})", ha='center', va='bottom')

    ax.set_xlabel("Date")
    ax.set_ylabel("Most Frequent Topic Count")
    ax.set_title("Most Frequent Topic per Day")
    ax.grid(True)

    # Streamlit ile grafiği gösterme
    st.pyplot(fig)

    #refreshing the page every 30 min
    while True:
        time.sleep(1 * 60 * 30) 
        st.rerun()
    
# run the app 
main()