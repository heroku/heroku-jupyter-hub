# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
# These args may not be necessary
ARG JUPYTERHUB_ADMIN
ARG DOCKER_NETWORK_NAME
ARG DOCKER_NOTEBOOK_IMAGE
ARG DOCKER_NOTEBOOK_DIR

# Stage 1: Build dependencies
FROM python:3.10-slim as builder

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --user -r /tmp/requirements.txt

# Stage 2: Final image
FROM python:3.10-slim

# Copy only the installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Create jovyan user first
RUN useradd -m -s /bin/bash -N -u 1000 jovyan

# Create necessary directories and set permissions
RUN mkdir -p /srv/jupyterhub /etc/jupyterhub && \
    chown -R jovyan:users /srv/jupyterhub /etc/jupyterhub

# Set working directory
WORKDIR /srv/jupyterhub

# Copy application files
COPY . .

# Set permissions for copied files
RUN chown -R jovyan:users /srv/jupyterhub

# Switch to jovyan user
USER jovyan

# Make start script executable
RUN chmod +x start_hub

# Expose port
EXPOSE $PORT

# Start the service
CMD ["./start_hub"]
