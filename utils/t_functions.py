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