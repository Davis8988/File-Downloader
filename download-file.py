import requests
import os
import time
import logging
import sys

# Configuration variables
SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS = int(os.getenv("SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS", "10"))  # Default: 10 seconds
REQUESTS_TIMEOUT_SEC                 = int(os.getenv("REQUESTS_TIMEOUT_SEC", "9"))  # Default: 9 seconds
READ_CONTENT_TIMEOUT_SEC             = int(os.getenv("READ_CONTENT_TIMEOUT_SEC", "30"))  # Default: 30 seconds
SRC_FILE_TO_DOWNLOAD_URL             = os.getenv("SRC_FILE_TO_DOWNLOAD_URL", "https://drive.google.com/uc?id=1NMct4riX9-Ip689GzVPl3ILm3ylABoX4")  # Link to: https://drive.google.com/file/d/1NMct4riX9-Ip689GzVPl3ILm3ylABoX4/view?usp=drive_link
DEST_DOWNLOAD_DIR_PATH               = os.getenv("DEST_DOWNLOAD_DIR_PATH", "/data")
DEST_DOWNLOAD_FILE_NAME              = os.getenv("DEST_DOWNLOAD_FILE_NAME", "birthdays.csv")
LOG_LEVEL                            = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())

# Set up logging
logging.basicConfig(stream=sys.stdout, level=LOG_LEVEL, format='%(asctime)s - %(levelname)s: %(message)s')

# def check_internet_connection():
#     try:
#         logging.info(f"Checking if URL adderss is available: {SRC_FILE_TO_DOWNLOAD_URL}")
#         logging.info(f"set timeout to: {REQUESTS_TIMEOUT_SEC} sec")
#         response = requests.head(SRC_FILE_TO_DOWNLOAD_URL, timeout=REQUESTS_TIMEOUT_SEC)
#         if response.status_code == 200:
#             logging.info("OK - Address is available.")
#             return True
#     except requests.ConnectionError as err_msg:
#         logging.error(err_msg)
#     logging.warning("No internet connection available.")
#     return False

import logging
import os
import requests

REQUESTS_TIMEOUT_SEC = 10  # Example timeout, replace with actual value
READ_CONTENT_TIMEOUT_SEC = 5  # Example timeout, replace with actual value

def download_file(url, local_path):
    logging.info(f"Downloading file: '{url}' to: {local_path}")
    try:
        logging.info(f"Set timeout to: {REQUESTS_TIMEOUT_SEC} sec")
        logging.info(f"Reading content from: {url}")
        
        # Download the new content
        response = requests.get(url, timeout=(REQUESTS_TIMEOUT_SEC, READ_CONTENT_TIMEOUT_SEC), allow_redirects=True)
        new_content = response.content
        logging.info(f"OK got new content")
        # Check if the file exists
        logging.info(f"Checking if file already exists: {local_path}")
        if os.path.exists(local_path):
            logging.info(" Yes")
            logging.info(" Reading existing file to compare it's content")
            # Read the existing file's content
            with open(local_path, 'rb') as f:
                existing_content = f.read()

            logging.info(" Got existing the file content")
            # Compare the existing content to the new content
            logging.info(" Comparing now..")
            if existing_content == new_content:
                logging.info("The file already exists and the content is the same. No need to overwrite.")
                return
            logging.info(" Content is new !")
            logging.info(" Continuing to write..")

        # Write the new content if the file doesn't exist or if the content is different
        with open(local_path, 'wb') as f:
            f.write(new_content)
            logging.info("OK - File written successfully.")

    except Exception as e:
        logging.error(f"Error occurred during download: {e}")
        logging.error("Download failed.")


def print_vars():
    # Print defined variables
    logging.info("")
    logging.info("Configuration Variables:")
    logging.info(f"  SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS : {SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS}")
    logging.info(f"  REQUESTS_TIMEOUT_SEC                 : {REQUESTS_TIMEOUT_SEC}")
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
        logging.info(f"Content:")
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
            # if not check_internet_connection():
            #     logging.warning("Attempt %d: No internet connection available. Skipping download attempt.", attempt_count)
            # else:
            #     logging.info("OK - Internet connection available. Proceeding with download...")

            logging.info("Downloading file from URL: %s", SRC_FILE_TO_DOWNLOAD_URL)
            download_file(SRC_FILE_TO_DOWNLOAD_URL, os.path.join(DEST_DOWNLOAD_DIR_PATH, DEST_DOWNLOAD_FILE_NAME))
            logging.info("")
            print_dest_file_content()  # Print content of file "{DEST_DOWNLOAD_FILE_NAME}" before next attempt
            logging.info("")
            print_dest_dir_contents()
                
            logging.info("Waiting for %d seconds before next download attempt...", SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS)
            time.sleep(SLEEP_BETWEEN_DOWNLOAD_TRIES_SECONDS)

            attempt_count += 1
        except Exception as e:
            logging.error(f"Error occurred during download attempt: {e}")
            logging.error("Skipping this download attempt.")
