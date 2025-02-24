# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM quay.io/jupyterhub/jupyterhub

# Copy application files
COPY start_hub jupyterhub_config.py create_proxy.py heroku_tools.py /srv/jupyterhub/
COPY proxy_server/ /srv/jupyterhub/proxy_server


# Install git and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir \
    dockerspawner \
    jupyterhub-nativeauthenticator \
    psycopg2-binary

# Make start script executable
RUN chmod +x /srv/jupyterhub/start_hub

# Start command
CMD ["sh", "-c", "jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py", "--port=${PORT}"]
