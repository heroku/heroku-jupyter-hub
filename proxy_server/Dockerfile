FROM node:lts-alpine3.18

# Set labels based on the OCI
LABEL org.opencontainers.image.authors="Jupyter Project <jupyter@googlegroups.com>"
LABEL org.opencontainers.image.source="https://github.com/jupyterhub/configurable-http-proxy"
LABEL org.opencontainers.image.url="https://github.com/jupyterhub/configurable-http-proxy/blob/HEAD/Dockerfile"

# Install nginx and debugging tools
RUN apk upgrade --no-cache && \
    apk add --no-cache \
    curl \
    jq \
    nginx

# Install specific version of configurable-http-proxy
RUN npm install -g configurable-http-proxy@4.5.1

# Copy our files
COPY start_proxy /
COPY nginx.conf /etc/nginx/nginx.conf

# Make start script executable
RUN chmod +x /start_proxy

# Switch to non-root user
USER 65534

# Start command with debug output
ENTRYPOINT ["sh", "-x", "/start_proxy"]