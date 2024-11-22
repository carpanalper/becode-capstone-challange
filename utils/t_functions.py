import pandas as pd

# thema frequency
def get_topic_counts(df):
    return df['topic'].value_counts().head(10)

def publish_time_statistics(df):
    # defining time ranges and initializing a counter
    bins = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
    labels = [f"{start}-{end}" for start, end in zip(bins[:-1], bins[1:])]

    # converting date to datetime and extracting the hour
    df['date'] = pd.to_datetime(df['date'])
    df['publish_hour'] = df['date'].dt.hour

    # creating a new column with the time range
    df['time_range'] = pd.cut(df['publish_hour'], bins=bins, labels=labels)
    time_range_counts = df['time_range'].value_counts().sort_index()

    # creating a dataframe for the result
    result_df = pd.DataFrame(time_range_counts).reset_index()
    result_df.columns = ["Time Range", "No of News"]

    return result_df

def day_agenda(df):
    # converting date to datetime and extracting the day
    df['date'] = pd.to_datetime(df['date']).dt.date
    # counting the number of news per day
    topic_counts = df.groupby(['date', 'topic']).size().reset_index(name='count')
    # finding the most frequent topic per day
    most_frequent_topics = topic_counts.loc[topic_counts.groupby('date')['count'].idxmax()]

    return most_frequent_topics


def weekly_agenda(df):
    # Convert 'date' to datetime and extract the week start (Monday as the start of the week)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if df['date'].isna().any():
        raise ValueError("Some entries in 'date' could not be converted to datetime.")
    
    df['week_start'] = df['date'] - pd.to_timedelta(df['date'].dt.weekday, unit='d')
    df['week_start'] = df['week_start'].dt.date  # Extract the date part only

    # Count the number of news per week and topic
    topic_counts = df.groupby(['week_start', 'topic']).size().reset_index(name='count')

    # Find the most frequent topic per week
    most_frequent_topics = topic_counts.loc[topic_counts.groupby('week_start')['count'].idxmax()]

    # Calculate the total news count per week
    total_weekly_counts = topic_counts.groupby('week_start')['count'].sum().reset_index(name='total_entries')

    # Merge the most frequent topics with the total weekly counts
    most_frequent_topics = most_frequent_topics.merge(total_weekly_counts, on='week_start')

    # Calculate the percentage of the most frequent topic
    most_frequent_topics['percentage'] = round((most_frequent_topics['count'] / most_frequent_topics['total_entries']) * 100, 2)

    # Sort by week_start for consistency in plots
    most_frequent_topics = most_frequent_topics.sort_values(by='week_start', ascending=False)
    
    return most_frequent_topics