# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Define build-time arguments for environment variables
ARG LOGIN
ARG PASSWORD
ARG FROM_EMAIL
ARG TO_EMAIL
ARG SMTP_SERVER
ARG SMTP_PORT
ARG URL_TO_CHECK
ARG TEXT_TO_FIND
ARG MIN_TIME_TO_SLEEP
ARG MAX_TIME_TO_SLEEP
ARG DEBUG

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Python script into the container
COPY monitor_webpage.py ./

# Update package list and install necessary system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    chromium-browser \
    chromium-chromedriver \
    wget && \
    rm -rf /var/lib/apt/lists/*

# Install necessary packages
RUN pip install --no-cache-dir requests selenium webdriver-manager selenium-stealth undetected-chromedriver

# Check Chromium installation path and log for troubleshooting
RUN echo "Checking Chromium installation:" && \
    (which chromium-browser || echo "chromium-browser not found") && \
    (which google-chrome || echo "google-chrome not found")

# Set environment variables
ENV LOGIN=${LOGIN}
ENV PASSWORD=${PASSWORD}
ENV FROM_EMAIL=${FROM_EMAIL}
ENV TO_EMAIL=${TO_EMAIL}
ENV SMTP_SERVER=${SMTP_SERVER}
ENV SMTP_PORT=${SMTP_PORT}
ENV URL_TO_CHECK=${URL_TO_CHECK}
ENV TEXT_TO_FIND=${TEXT_TO_FIND}
ENV MIN_TIME_TO_SLEEP=${MIN_TIME_TO_SLEEP}
ENV MAX_TIME_TO_SLEEP=${MAX_TIME_TO_SLEEP}
ENV DEBUG=${DEBUG}

# Run the monitor script
CMD ["python", "monitor_webpage.py"]
