import requests
from bs4 import BeautifulSoup as bs
import json

news_json = 'news.json'
latest_news_json = 'latest_news.json'

def append_to_json(new_data):
    try:
        # Read the existing data from the file if it exists
        with open(news_json, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # Create a set of existing links for quick lookup
    existing_links = {entry['link'] for entry in data}

    # Filter out the new data that already exists in the JSON file
    unique_data = [entry for entry in new_data if entry['link'] not in existing_links]

    # Append the unique data to the list
    data.extend(unique_data)

    # Write the updated data back to the JSON file
    with open(news_json, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

    with open(latest_news_json, 'w', encoding='utf-8') as file:
        json.dump(unique_data, file, indent=4)

#pulling latest news from vrt.be
url = "https://www.vrt.be/vrtnws/nl/net-binnen/"
response = requests.get(url)
soup = bs(response.content, "html.parser")

# Find all <li> elements
li_elements = soup.find('ul', class_='sc-ggpjZQ iJyTnM').find_all('li')
scraped_news = []

# Iterate over each <li> element
for li in li_elements:
    # Extract the <a> tag (link) and get the href attribute
    link = li.find('a')
    if link:
        href = link.get('href')
    else:
        href = None
       
    # Find the <span> with the specified class
    thema = li.find('span', class_='prose-captions text-text-mode line-clamp-1')
    if thema:
        topic = thema.text
    else:
        topic = None

    # Find the <h3> element
    header = li.find('h3')
    if header:
       title = header.text
    else:
        title = None

    # Find the <time> element
    time_tag = li.find('time') 
    if time_tag:
        datetime_value = time_tag.get('datetime')
    else:
        datetime_value = None 

    #append data to the list
    scraped_news.append({
        'title': title,
        'topic': topic,
        'date' : datetime_value,
        'link': href
    })

# Append the new data to the JSON file
append_to_json(scraped_news)

with open(news_json, 'r') as file:
    total_data = json.load(file)
    print(f"Total entries: {len(total_data)}")

with open(latest_news_json, 'r') as file:
        new_data = json.load(file)
        print(f"New entries: {len(new_data)}")