import os
import json
from datetime import datetime

log_file_path = os.getenv('LOG_FILE_PATH', 'chat_logs.json')
def log_chat(conversation_id, user_id, role, message):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "role": role,
        "message": message
    }
    try:
        with open('chat_logs.json', 'r') as f:
            chat_logs = json.load(f)
    except FileNotFoundError:
        chat_logs = {}

    if conversation_id not in chat_logs:
        chat_logs[conversation_id] = {"user_id": user_id, "messages": [], "feedback": None}
    chat_logs[conversation_id]["messages"].append(log_entry)

    with open('chat_logs.json', 'w') as f:
        json.dump(chat_logs, f, indent=4)
