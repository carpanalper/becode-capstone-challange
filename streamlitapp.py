import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# connect to the db
def get_data_from_db():
    conn = sqlite3.connect('news.db')  
    query = "SELECT * FROM news"  
    df = pd.read_sql(query, conn)
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
    df['date'] = pd.to_datetime(df['date'])
    oldest_date = df['date'].min()
    oldest_date_str = oldest_date.to_pydatetime().strftime('%Y-%m-%d %H:%M')
    
    # latest update
    last_updated = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # total entries
    total_entries = len(df)
    
    # Info
    st.title('Frequency of Themes')
    st.write(f"Since: {oldest_date_str}")
    st.write(f"Last Updated: {last_updated}")
    st.write(f"Total Entries: {total_entries}")
    
    
    # Bar chart 
    fig, ax = plt.subplots()
    ax.bar(topic_counts.index, topic_counts.values)
    ax.set_xlabel('Topic')
    ax.set_ylabel('Frequency')
    ax.set_title('Frequency of Topics')

    plt.xticks(rotation=90)
    
    # graph streamlit
    st.pyplot(fig)
    
# run the app
if __name__ == "__main__":
    main()
