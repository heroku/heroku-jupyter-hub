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

# Set up configurable-http-proxy
RUN mkdir -p /srv/configurable-http-proxy
COPY . /srv/configurable-http-proxy/
WORKDIR /srv/configurable-http-proxy

RUN npm install -g configurable-http-proxy

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Switch to non-root user
USER 65534

# Put configurable-http-proxy on path
ENV PATH=/srv/configurable-http-proxy/bin:$PATH

# Start command
ENTRYPOINT ["/srv/configurable-http-proxy/start_proxy"]