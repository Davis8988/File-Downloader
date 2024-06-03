import requests
import os
import time
import logging
import sys

# Configuration variables
SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS = int(os.getenv("SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS", "10"))  # Default: 10 seconds
CHECK_INTERNET_CONNECTION_TIMEOUT    = int(os.getenv("SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS", "9"))  # Default: 9 seconds
SRC_FILE_TO_DOWNLOAD_URL             = os.getenv("SRC_FILE_TO_DOWNLOAD_URL", "https://raw.githubusercontent.com/Davis8988/birthday-dashboard/main/data/birthdays.csv")
DEST_DOWNLOAD_DIR_PATH               = os.getenv("DEST_DOWNLOAD_DIR_PATH", "/data")
DEST_DOWNLOAD_FILE_NAME              = os.getenv("DEST_DOWNLOAD_FILE_NAME", "birthdays.csv")
LOG_LEVEL                            = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())

# Set up logging
logging.basicConfig(stream=sys.stdout, level=LOG_LEVEL, format='%(asctime)s - %(levelname)s: %(message)s')

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
        logging.info("Downloading now...")
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
    logging.info(f"  CHECK_INTERNET_CONNECTION_TIMEOUT    : {CHECK_INTERNET_CONNECTION_TIMEOUT}")
    logging.info(f"  SRC_FILE_TO_DOWNLOAD_URL             : {SRC_FILE_TO_DOWNLOAD_URL}")
    logging.info(f"  DEST_DOWNLOAD_DIR_PATH               : {DEST_DOWNLOAD_DIR_PATH}")
    logging.info(f"  DEST_DOWNLOAD_FILE_NAME              : {DEST_DOWNLOAD_FILE_NAME}")
    logging.info(f"  LOG_LEVEL                            : {LOG_LEVEL}")
    logging.info("")

def print_dest_dir_contents():
    # Print contents of destination directory
    logging.info(f"Contents of destination directory: {DEST_DOWNLOAD_DIR_PATH}")
    for root, dirs, files in os.walk(DEST_DOWNLOAD_DIR_PATH):
        for file in files:
            logging.info(f" - {os.path.join(root, file)}")
    logging.info("")


def print_dest_file_content():
    # Print content of specified file in destination directory
    file_path = os.path.join(DEST_DOWNLOAD_DIR_PATH, DEST_DOWNLOAD_FILE_NAME)
    logging.info(f"Attempting to read the content of file: {DEST_DOWNLOAD_FILE_NAME}:")
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                logging.info(line.strip())
    else:
        logging.warning(f"File {DEST_DOWNLOAD_FILE_NAME} does not exist in the destination directory.")


if __name__ == "__main__":
    # Ensure the destination directory exists
    if not os.path.exists(DEST_DOWNLOAD_DIR_PATH):
        os.makedirs(DEST_DOWNLOAD_DIR_PATH)

    logging.info("Starting download script...")
    print_vars()

    attempt_count = 1

    while True:
        try:
            logging.info("")
            logging.info(" ==> Attempt %d", attempt_count)
            logging.info("")
            print_dest_dir_contents()  # <-- Print contents of destination directory before next attempt
            print_dest_file_content()  # Print content of file "{DEST_DOWNLOAD_FILE_NAME}" before next attempt
            if not check_internet_connection():
                logging.warning("Attempt %d: No internet connection available. Skipping download attempt.", attempt_count)
            else:
                logging.info("OK - Internet connection available. Proceeding with download...")

                logging.info("Downloading file from URL: %s", SRC_FILE_TO_DOWNLOAD_URL)
                download_file(SRC_FILE_TO_DOWNLOAD_URL, os.path.join(DEST_DOWNLOAD_DIR_PATH, DEST_DOWNLOAD_FILE_NAME))
                
            logging.info("Waiting for %d seconds before next download attempt...", SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS)
            time.sleep(SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS)

            attempt_count += 1
        except Exception as e:
            logging.error(f"Error occurred during download attempt: {e}")
            logging.error("Skipping this download attempt.")
