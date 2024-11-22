import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time
from t_functions import publish_time_statistics, get_topic_counts, weekly_agenda 
from queries import get_data_from_db, get_daily_news, get_weekly_news

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
    st.write(f"Last Update: {last_update}")
    st.write(f"Total entries: {total_entries}")

    st.divider()

    #topics 
    df_cleaned = df.dropna(subset=['topic'])
    sorted_topics = sorted(df_cleaned['topic'].unique()) 
    selected_topics = st.multiselect("Choose Topics:", options=sorted_topics, default='Leuven')
    st.write(f"Total Topics: {len(sorted_topics)}")
    st.write(f"Latest News for Selected Topics:")

    if selected_topics:
        filtered_df = df_cleaned[df_cleaned['topic'].isin(selected_topics)]
        latest_news = filtered_df.sort_values(by='date', ascending=False).head(3)
        for idx, row in latest_news.iterrows():
            st.write(f"- **{row['title'].strip()}** (Topic: {row['topic']}, Date: {row['date'].strftime('%Y-%m-%d')})")
    else:
        st.write("Please select a topic to display the latest news.")

    st.divider()
    
    #daily top 10
    daily_news = get_daily_news()
    daily_top_10 = daily_news['topic'].value_counts().head(10)

    #weekly top 10
    weekly_news = get_weekly_news()
    weekly_top_10 = weekly_news['topic'].value_counts().head(10)

    option = st.selectbox(
    "Choose the range of entries",
    ("Last 24 Hours", "Last Week", "All Time"), index=1
)
    if option == 'Last 24 Hours':
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

    elif option == 'Last Week':
        # Weekly Bar chart
        fig, ax = plt.subplots()
        ax.bar(weekly_top_10.index, weekly_top_10.values)
        ax.set_xlabel('Topic')
        ax.set_ylabel('No of News')
        ax.set_title('Frequency of Topics (Last 7 days)')
        plt.xticks(rotation=90)
        # show chart
        st.write(f"Last 7 days: {len(weekly_news)} Entries")
        st.pyplot(fig)

    elif option == 'All Time':
        # All time Bar chart 
        fig, ax = plt.subplots()
        ax.bar(topic_counts.index, topic_counts.values)
        ax.set_xlabel('Topic')
        ax.set_ylabel('No of News')
        ax.set_title('Frequency of Topics (All Time)')
        plt.xticks(rotation=90)
        # show chart
        st.write(f"Since: {oldest_date_str}")
        st.write(f"Total Entries: {total_entries}")
        st.pyplot(fig)

    # Time statistics
    time_stats = publish_time_statistics(df)
    
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

    # weekly agenda table
    st.subheader("Most Frequent Topic per Week")
    agenda = weekly_agenda(df)
    st.dataframe(agenda, use_container_width=True, hide_index=True)
    
    #refreshing the page every 30 min
    while True:
        time.sleep(1 * 60 * 30) 
        st.rerun()
    
# run the app 
main()