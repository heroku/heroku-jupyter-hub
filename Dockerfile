# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
# These args may not be necessary
ARG JUPYTERHUB_ADMIN
ARG DOCKER_NETWORK_NAME
ARG DOCKER_NOTEBOOK_IMAGE
ARG DOCKER_NOTEBOOK_DIR

FROM python:3.10-slim

# Install Node.js for configurable-http-proxy
RUN apt-get update && \
    apt-get install -y \
    nodejs \
    npm \
    && npm install -g configurable-http-proxy \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
WORKDIR /srv/jupyterhub
COPY . .

# Make start script executable
RUN chmod +x start_hub

# Use non-root user
RUN useradd -m -d /home/jovyan jovyan
RUN chown -R jovyan:jovyan /srv/jupyterhub
USER jovyan

# Expose the port
EXPOSE $PORT

# Start the hub
CMD ["./start_hub"]
