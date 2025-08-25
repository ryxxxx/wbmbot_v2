# Use a minimal Ubuntu base image
FROM ubuntu:latest

LABEL VERSION="1.0.1"
LABEL MAINTAINER="Vel-San | vel-san@protonmail.com"
LABEL DESCRIPTION="A docker image that has all required dependenices for the bot to run"

# ARGS
ARG DEBIAN_FRONTEND=noninteractive

# Update package lists and install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    nano \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /home

# Copy the Python project files into the container
COPY configs/ /home/configs
COPY logging/ /home/logging
COPY offline_viewings/ /home/offline_viewings
COPY wbmbot_v2/ /home/wbmbot_v2
COPY generate_config_from_env.py /home/

# Create and activate virtual environment, then install dependencies
RUN python3 -m venv /home/venv && \
    /home/venv/bin/pip install --no-cache-dir -r /home/wbmbot_v2/requirements.txt

# Create entrypoint script that generates config from env vars and starts the bot
RUN echo '#!/bin/bash\necho "Generating WBM config from environment variables..."\n/home/venv/bin/python /home/generate_config_from_env.py\necho "Starting WBM bot in headless mode..."\n/home/venv/bin/python /home/wbmbot_v2/main.py -H' > /home/entrypoint.sh && \
    chmod +x /home/entrypoint.sh

# Command to run the entrypoint script
CMD ["/home/entrypoint.sh"]
