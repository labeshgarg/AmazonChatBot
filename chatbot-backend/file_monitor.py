import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

CHAT_LOG_PATH = 'chat_log.json'
CONVERSATION_COUNT_PATH = 'conversation_count.txt'
CONVERSATION_THRESHOLD = 5  

class ChatLogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(CHAT_LOG_PATH):
            print(f"Detected changes in {event.src_path}. Checking for new conversations...")
            if check_new_conversations():
                run_pipeline()

def get_current_conversation_count():
    with open(CHAT_LOG_PATH, 'r') as file:
        data = json.load(file)
    return len(data)

def get_previous_conversation_count():
    try:
        with open(CONVERSATION_COUNT_PATH, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

def update_conversation_count(count):
    with open(CONVERSATION_COUNT_PATH, 'w') as file:
        file.write(str(count))

def check_new_conversations():
    current_count = get_current_conversation_count()
    previous_count = get_previous_conversation_count()
    
    if current_count - previous_count >= CONVERSATION_THRESHOLD:
        print(f"{current_count - previous_count} new conversations detected. Running pipeline...")
        update_conversation_count(current_count)
        return True
    else:
        print(f"Only {current_count - previous_count} new conversations detected. Waiting for more.")
        return False

def run_pipeline():
    try:
       
        print("Running data preprocessing...")
        subprocess.run(["python", "data_preprocessing.py"], check=True)

        print("Training intent classification model...")
        subprocess.run(["python", "intent_classification.py"], check=True)

        print("Training response classification model...")
        subprocess.run(["python", "response_classification.py"], check=True)

        print("Pipeline completed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error during pipeline execution: {e}")

if __name__ == "__main__":
    if get_previous_conversation_count() == 0:
        update_conversation_count(get_current_conversation_count())
    
    path_to_watch = "."  
    event_handler = ChatLogHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    print(f"Monitoring changes in {path_to_watch}...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
