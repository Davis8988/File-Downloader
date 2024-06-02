import requests
import os
import time
import logging
import sys

# Configuration variables
SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS = int(os.getenv("SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS", "3600"))  # Default: 60 minutes
SRC_FILE_TO_DOWNLOAD_URL             = os.getenv("SRC_FILE_TO_DOWNLOAD_URL", "https://example.com/file.txt")
DEST_DOWNLOAD_DIR                    = os.getenv("DEST_DOWNLOAD_DIR", "/data")
LOG_LEVEL                            = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())

# Set up logging
logging.basicConfig(stream=sys.stdout, level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

def download_file(url, local_path):
    logging.info("Checking for updates...")
    response = requests.head(url)
    if response.status_code == 200:
        logging.info("File is updated. Downloading...")
        with open(local_path, 'wb') as f:
            response = requests.get(url)
            f.write(response.content)
        logging.info("Download complete.")


def print_vars():
    # Print defined variables
    logging.info("Configuration Variables:")
    logging.info(f"  SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS : {SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS}")
    logging.info(f"  SRC_FILE_TO_DOWNLOAD_URL             : {SRC_FILE_TO_DOWNLOAD_URL}")
    logging.info(f"  DEST_DOWNLOAD_DIR                    : {DEST_DOWNLOAD_DIR}")
    logging.info(f"  LOG_LEVEL                            : {LOG_LEVEL}")


if __name__ == "__main__":
    # Ensure the destination directory exists
    if not os.path.exists(DEST_DOWNLOAD_DIR):
        os.makedirs(DEST_DOWNLOAD_DIR)

    logging.info("Starting download script...")
    print_vars()
    attempt_count = 1

    while True:
        logging.info("Attempt %d: Downloading file from URL: %s", attempt_count, SRC_FILE_TO_DOWNLOAD_URL)
        download_file(SRC_FILE_TO_DOWNLOAD_URL, os.path.join(DEST_DOWNLOAD_DIR, "file.txt"))
        
        logging.info("Attempt %d: Waiting for %d seconds before next download attempt...", attempt_count, SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS)
        time.sleep(SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS)

        attempt_count += 1
