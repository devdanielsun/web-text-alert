# web-text-alert
This project monitors a website for specific text. If the text is no longer found, it sends an email alert. The application is designed to run seamlessly in a Docker container.

## Instructions

1. Install and run Docker
2. Pull this repo and `cd` to it
3. Make sure to change the ENV variables in docker-compose.yml
4. Execute `docker-compose up -d`
5. Check the logs of the container `docker-compose logs -f web-text-alert`
