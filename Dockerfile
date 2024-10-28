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

# Install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl wget unzip chromium chromium-driver fonts-liberation \
    libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 \
    libdbus-1-3 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libnss3 libx11-xcb1 \
    libxcomposite1 libxdamage1 libxrandr2 x11-apps && \
    pip install --no-cache-dir requests selenium webdriver-manager && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

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
