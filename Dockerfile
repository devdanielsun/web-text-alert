# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install necessary packages
RUN pip install --no-cache-dir requests

# Environment variables
ENV EMAIL_ADDRESS=your_email@gmail.com
ENV EMAIL_PASSWORD=your_password
ENV TO_EMAIL=recipient_email@gmail.com
ENV SMTP_SERVER=smtp.gmail.com
ENV SMTP_PORT=587
ENV URL_TO_CHECK=https://example.com
ENV TEXT_TO_FIND="important text"
ENV TIME_TO_SLEEP‎=30

# Run monitor_webpage.py when the container launches
CMD ["python", "./monitor_webpage.py"]
