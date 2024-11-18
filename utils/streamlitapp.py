import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time
from t_functions import publish_time_statistics, day_agenda, get_topic_counts, weekly_agenda 
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

    #daily top 10
    daily_news = get_daily_news()
    daily_top_10 = daily_news['topic'].value_counts().head(10)

    #weekly top 10
    weekly_news = get_weekly_news()
    weekly_top_10 = weekly_news['topic'].value_counts().head(10)

    option = st.selectbox(
    "Choose the range of entries",
    ("Last 24 Hours", "Last Week", "All Time"),
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

    # agenda
    agenda = weekly_agenda(df)

    # Plotting the results
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(agenda['week_start'], agenda['count'], marker='o', color='b', linestyle='-', linewidth=2)

    # Annotate each point with topic name and count
    for i, row in agenda.iterrows():
        ax.text(row['week_start'], row['count'], f"{row['topic']}", 
                ha='center', va='bottom', fontsize=8)

    ax.set_xticks(agenda['week_start']) # Set the x-ticks to be the week start dates

    # Set axis labels and title
    ax.set_xlabel("Week Start Date")
    ax.set_ylabel("Most Frequent Topic Count")
    ax.set_title("Most Frequent Topic per Week")
    ax.grid(True)

    # Rotate X-axis labels for better readability
    plt.xticks(rotation=45)

    # Display the plot in Streamlit
    st.pyplot(fig)

    #refreshing the page every 30 min
    while True:
        time.sleep(1 * 60 * 30) 
        st.rerun()
    
# run the app 
main()