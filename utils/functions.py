from collections import Counter
from datetime import datetime
import pandas as pd

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
