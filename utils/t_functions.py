import pandas as pd
import re


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

def remove_stopwords(text):
    # remove flemuish prepositions
    stop_words = ["aan","aangaande","aangezien","achte","achter","achterna","af","afgelopen",
                  "al","aldaar","aldus","alhoewel","alias","alle","allebei","alleen","alles",
                  "als","alsnog","altijd","altoos","ander","andere","anders","anderszins","beetje",
                  "behalve","behoudens","beide","beiden","ben","beneden","bent","bepaald","betreffende",
                  "bij","bijna","bijv","binnen","binnenin","blijkbaar","blijken","boven","bovenal",
                  "bovendien","bovengenoemd","bovenstaand","bovenvermeld","buiten","bv","daar",
                  "daardoor","daarheen","daarin","daarna","daarnet","daarom","daarop","daaruit",
                  "daarvanlangs","dan","dat","de","deden","deed","der","derde","derhalve","dertig",
                  "deze","dhr","die","dikwijls","dit","doch","doe","doen","doet","door","doorgaand",
                  "drie","duizend","dus","echter","een","eens","eer","eerdat","eerder","eerlang","eerst",
                  "eerste","eigen","eigenlijk","elk","elke","en","enig","enige","enigszins","enkel","er",
                  "erdoor","erg","ergens","etc","etcetera","even","eveneens","evenwel","gauw","ge",
                  "gedurende","geen","gehad","gekund","geleden","gelijk","gemoeten","gemogen","genoeg",
                  "geweest","gewoon","gewoonweg","haar","haarzelf","had","hadden","hare","heb","hebben",
                  "hebt","hedden","heeft","heel","hem","hemzelf","hen","het","hetzelfde","hier",
                  "hierbeneden","hierboven","hierin","hierna","hierom","hij","hijzelf","hoe","hoewel",
                  "honderd","hun","hunne","ieder","iedere","iedereen","iemand","iets","ik","ikzelf",
                  "in","inderdaad","inmiddels","intussen","inzake","is","ja","je","jezelf","jij",
                  "jijzelf","jou","jouw","jouwe","juist","jullie","kan","klaar","kon","konden",
                  "krachtens","kun","kunnen","kunt","laatst","later","liever","lijken","lijkt","maak",
                  "maakt","maakte","maakten","maar","mag","maken","me","meer","meest","meestal","men",
                  "met","mevr","mezelf","mij","mijn","mijnent","mijner","mijzelf","minder","miss",
                  "misschien","missen","mits","mocht","mochten","moest","moesten","moet","moeten",
                  "mogen","mr","mrs","mw","na","naar","nadat","nam","namelijk","nee","neem","negen",
                  "nemen","nergens","net","niemand","niet","niets","niks","noch","nochtans","nog",
                  "nogal","nooit","nu","nv","of","ofschoon","om","omdat","omhoog","omlaag","omstreeks",
                  "omtrent","omver","ondanks","onder","ondertussen","ongeveer","ons","onszelf","onze",
                  "onzeker","ooit","ook","op","opnieuw","opzij","over","overal","overeind","overige",
                  "overigens","paar","pas","per","precies","recent","redelijk","reeds","rond","rondom",
                  "samen","sedert","sinds","sindsdien","slechts","sommige","spoedig","steeds","tamelijk",
                  "te","tegen","tegenover","tenzij","terwijl","thans","tien","tiende","tijdens","tja",
                  "toch","toe","toen","toenmaals","toenmalig","tot","totdat","tussen","twee","tweede",
                  "u","uit","uitgezonderd","uw","vaak","vaakwat","van","vanaf","vandaan","vanuit",
                  "vanwege","veel","veeleer","veertig","verder","verscheidene","verschillende",
                  "vervolgens","via","vier","vierde","vijf","vijfde","vijftig","vol","volgend",
                  "volgens","voor","vooraf","vooral","vooralsnog","voorbij","voordat","voordezen",
                  "voordien","voorheen","voorop","voorts","vooruit","vrij","vroeg","waar","waarom",
                  "waarschijnlijk","wanneer","want","waren","was","wat","we","wederom","weer","weg",
                  "wegens","weinig","wel","weldra","welk","welke","werd","werden","werder","wezen",
                  "whatever","wie","wiens","wier","wij","wijzelf","wil","wilden","willen","word",
                  "worden","wordt","zal","ze","zei","zeker","zelf","zelfde","zelfs","zes","zeven",
                  "zich","zichzelf","zij","zijn","zijne","zijzelf","zo","zoals","zodat","zodra",
                  "zonder","zou","zouden","zowat","zulk","zulke","zullen","zult"]
    
    filtered_text = " ".join([word for word in text.split() if word.lower() not in stop_words])
    return filtered_text

def clean_special_characters(text):
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    return cleaned_text