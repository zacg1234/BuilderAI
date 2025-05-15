import threading
import os
from datetime import datetime

log_lock = threading.Lock()
LOG_FILE = "agent_log.txt"

def write_log_entry(entry: str):
    timestamp = datetime.now().isoformat()
    with log_lock:
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} {entry}\n")

def delete_log_file():
    """Delete the log file if it exists."""
    with log_lock:
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)