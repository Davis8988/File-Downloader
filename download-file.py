import requests
import os
import time
import logging
import sys

# Configuration variables
SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS = int(os.getenv("SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS", "10"))  # Default: 10 seconds
CHECK_INTERNET_CONNECTION_TIMEOUT    = int(os.getenv("SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS", "9"))  # Default: 9 seconds
SRC_FILE_TO_DOWNLOAD_URL             = os.getenv("SRC_FILE_TO_DOWNLOAD_URL", "https://example.com/file.txt")
DEST_DOWNLOAD_DIR                    = os.getenv("DEST_DOWNLOAD_DIR", "/data")
LOG_LEVEL                            = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())

# Set up logging
logging.basicConfig(stream=sys.stdout, level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

def check_internet_connection():
    try:
        logging.info(f"Checking if URL adderss is available: {SRC_FILE_TO_DOWNLOAD_URL}")
        logging.info(f"set timeout to: {CHECK_INTERNET_CONNECTION_TIMEOUT} sec")
        response = requests.head(SRC_FILE_TO_DOWNLOAD_URL, timeout=CHECK_INTERNET_CONNECTION_TIMEOUT)
        if response.status_code == 200:
            logging.info("OK - Address is available.")
            return True
    except requests.ConnectionError as err_msg:
        logging.error(err_msg)
    logging.warning("No internet connection available.")
    return False

def download_file(url, local_path):
    logging.info(f"Downloading file: '{url}' to: {local_path}")
    try:
        logging.info(f"set timeout to: {CHECK_INTERNET_CONNECTION_TIMEOUT} sec")
        logging.info("Downloading...")
        with open(local_path, 'wb') as f:
            response = requests.get(url, timeout=CHECK_INTERNET_CONNECTION_TIMEOUT)
            f.write(response.content)
        logging.info("OK - Download complete.")
    except Exception as e:
        logging.error(f"Error occurred during download: {e}")
        logging.error("Download failed.")

def print_vars():
    # Print defined variables
    logging.info("")
    logging.info("Configuration Variables:")
    logging.info(f"  SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS : {SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS}")
    logging.info(f"  SRC_FILE_TO_DOWNLOAD_URL             : {SRC_FILE_TO_DOWNLOAD_URL}")
    logging.info(f"  DEST_DOWNLOAD_DIR                    : {DEST_DOWNLOAD_DIR}")
    logging.info(f"  LOG_LEVEL                            : {LOG_LEVEL}")
    logging.info("")

def print_dest_dir_contents():
    # Print contents of destination directory
    logging.info(f"Contents of destination directory: {DEST_DOWNLOAD_DIR}")
    for root, dirs, files in os.walk(DEST_DOWNLOAD_DIR):
        for file in files:
            logging.info(os.path.join(root, file))
    logging.info("")


def print_dest_file_content(filename):
    # Print content of specified file in destination directory
    file_path = os.path.join(DEST_DOWNLOAD_DIR, filename)
    logging.info(f"Content of file {filename}:")
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                logging.info(line.strip())
    else:
        logging.warning(f"File {filename} does not exist in the destination directory.")


if __name__ == "__main__":
    # Ensure the destination directory exists
    if not os.path.exists(DEST_DOWNLOAD_DIR):
        os.makedirs(DEST_DOWNLOAD_DIR)

    logging.info("Starting download script...")
    print_vars()

    attempt_count = 1

    while True:
        try:
            logging.info("")
            logging.info("Attempt %d", attempt_count)
            logging.info("")
            if not check_internet_connection():
                logging.warning("Attempt %d: No internet connection available. Skipping download attempt.", attempt_count)
            else:
                logging.info("OK - Internet connection available. Proceeding with download...", attempt_count)
                
                print_dest_dir_contents()  # Print contents of destination directory before next attempt

                logging.info("Downloading file from URL: %s", SRC_FILE_TO_DOWNLOAD_URL)
                download_file(SRC_FILE_TO_DOWNLOAD_URL, os.path.join(DEST_DOWNLOAD_DIR, "file.txt"))
                
                print_dest_file_content("file.txt")  # Print content of file "file.txt" before next attempt
            logging.info("Waiting for %d seconds before next download attempt...", SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS)
            time.sleep(SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS)

            attempt_count += 1
        except Exception as e:
            logging.error(f"Error occurred during download attempt: {e}")
            logging.error("Skipping this download attempt.")
