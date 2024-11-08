from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import subprocess
import datetime
import time

third_job_executed = False #adding flag to run streamlit only once
streamlit_process = None  #to follow up the Streamlit process

def first_job(): 
    print("Pulling news...")
    try:
        subprocess.run(["python", "reporter.py"], check=True)
        print("News delivered successfully.")
    except subprocess.CalledProcessError:
        print("Error in delivering news!")

def second_job():
    print("Updating database...")
    try:
        subprocess.run(["python", "db_update.py"], check=True)
        print(f"Database updated successfully at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        global third_job_executed
        if not third_job_executed:
            third_job()
            third_job_executed = True  # preventing streamlit from running again
    except subprocess.CalledProcessError:
        print("Error in database update!")

def third_job():
    print("Launching Streamlit app...")
    global streamlit_process
    try:
        # launching streamlit
        streamlit_process = subprocess.Popen(["streamlit", "run", "streamlitapp.py"]) 
        print("Streamlit app launched successfully.")
    except Exception as e:
        print(f"Error launching Streamlit app!: {e}")    


def job_listener(event):
    if event.exception:
        print(f"Error in job: {event.job_id}")
    elif event.job_id == 'first_job':  # Only trigger second job if first job succeeded
        second_job()

print ("Starting the scheduler...") 

scheduler = BackgroundScheduler()
# First job to run every 30 minutes
scheduler.add_job(first_job, 'interval', minutes=30, id='first_job', next_run_time=datetime.datetime.now())
# Listener to handle job events
scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

scheduler.start()

try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    print("Shutting down the scheduler...")
    scheduler.shutdown()
    if streamlit_process:
        streamlit_process.terminate()
        streamlit_process.wait()  # make sure the process is completed
        print("Streamlit app stopped.")