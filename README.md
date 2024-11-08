# Becode Capstone Project: Investigating Breaking News

## Description
The primary goal of this project is to simulate a basic ETL workflow by building an automated data pipeline designed to collect, process, and analyze breaking news data in real-time for research and insight generation.  

## Installation & Launching
1. Clone the repository:
   ```
   git clone git@github.com:carpanalper/becode-capstone-challange.git
   ```
2. Navigate into the project directory:
   ```
   cd becode-capstone-challenge
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the scheduler script 
   ```
   python scheduler.py
   ```
5. Terminate the program
   ```
   Ctrl + C
   ```

## Usage
The program will automatically pull the breaking news titles, add the new titles (if any) to a database and launch the streamlit interface where the latest visualisation of the most recent data is shown. The database and streamlit app is updated every 30 minutes unless the user terminates the process of `scheduler.py`.

## Features
- `reporter.py` scraps url,topic,title and date info of all the available breaking news from `https://www.vrt.be/vrtnws/nl/net-binnen/` by using `beautifulsoup`
- then archives scraped data into the `news.json` file by checking the uniqueness based on their url. also creates `latest_news.json` file which is updated with only the new entries on each run with the above-mentioned webpage. finally informs user about the total number of archived entries and the number of new entries.
- `db_update.py` builds a database to store scraped data by using the url as a primary key. then updates the database with the `latest_news.json`  
- `streamlitapp.py` reads data from the database and creates a bar chart showing the most frequent 10 topics of all the entries stored in the database so far. Informs the user about the total number of entries, the date of the earliest entry in the database and latest update time of the chart using `pandas` and `matplotlib`
- It is notable that all these dates and times are all shown in the local time zone of the user. Secondly the page is automatically refresh every 30 min to show most updated analysis.
- Finally, the crucial player for automation is `scheduler.py` which orchestrates and schedules all above-mentioned scripts by using `apscheduler`. It enables pulling data and updating database every 30 minutes. It informs the user about the process on each turn. It also launches streamlit app once and stops when the process is terminated. 

## Future Improvements  
- Better design for the project folders
- Necassary configurations for running the app on a cloud
- Pulling historical data from various resources to improve and enrich analysis
- Creating a more complicated database
- Various sql queries for different analysis
- Different visualisations like trending topics over time, daily or monthly visualisations, sentiment analysis of titles etc.
- More professional README

## Contributors
- Alper Carpan 
