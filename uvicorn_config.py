import os
import multiprocessing
from dotenv import load_dotenv

load_dotenv()

# Use the port provided by the environment variable from Google Cloud Run
port = int(os.getenv("PORT", 8000)) if os.getenv("ENV") != "development" else 8000

# Determine the number of workers based on the environment
workers = multiprocessing.cpu_count()

config = {
    # https://www.uvicorn.org/deployment/
    "host": "0.0.0.0",
    "port": port,
    "log_level": "info",
    "access_log": True,
    "timeout_keep_alive": 600,  # set timeout to 10 minutes
    "workers": workers,
}

# Check if the environment is development
if os.getenv("ENV") == "development":
    config["reload"] = True

