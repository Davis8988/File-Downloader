# Use an official Python runtime as a parent image
FROM python:3.9-slim

# PYTHONUNBUFFERED=1 to allow immediate printings of logs
ENV PYTHONUNBUFFERED=1

# Create a directory for the script
WORKDIR /usr/src/app

COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY download-file.py .

# Run the script
CMD [ "python", "./download-file.py" ]
