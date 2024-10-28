# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Define build-time arguments
ARG LOGIN
ARG PASSWORD
ARG FROM_EMAIL
ARG TO_EMAIL
ARG SMTP_SERVER
ARG SMTP_PORT
ARG URL_TO_CHECK
ARG TEXT_TO_FIND
ARG TIME_TO_SLEEP

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY monitor_webpage.py ./

# Install necessary packages
RUN pip install --no-cache-dir requests

# Environment variables
ENV LOGIN=${LOGIN}
ENV PASSWORD=${PASSWORD}
ENV FROM_EMAIL=${FROM_EMAIL}
ENV TO_EMAIL=${TO_EMAIL}
ENV SMTP_SERVER=${SMTP_SERVER}
ENV SMTP_PORT=${SMTP_PORT}
ENV URL_TO_CHECK=${URL_TO_CHECK}
ENV TEXT_TO_FIND=${TEXT_TO_FIND}
ENV TIME_TO_SLEEP=${TIME_TO_SLEEP}

# Run monitor_webpage.py when the container launches
CMD ["python", "monitor_webpage.py"]
