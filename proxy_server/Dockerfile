FROM node:lts-alpine3.18
# ref: https://hub.docker.com/_/node?tab=tags&name=lts-alpine

# Set labels based on the Open Containers Initiative (OCI):
# https://github.com/opencontainers/image-spec/blob/main/annotations.md#pre-defined-annotation-keys
#
LABEL org.opencontainers.image.authors="Jupyter Project <jupyter@googlegroups.com>"
LABEL org.opencontainers.image.source="https://github.com/jupyterhub/configurable-http-proxy"
LABEL org.opencontainers.image.url="https://github.com/jupyterhub/configurable-http-proxy/blob/HEAD/Dockerfile"

# Add tools useful for debugging and update packages to patch known
# vulnerabilities if needed.
RUN apk upgrade --no-cache \
 && apk add --no-cache \
        curl \
        jq

# Copy relevant (see .dockerignore)
RUN mkdir -p /srv/configurable-http-proxy
COPY . /srv/configurable-http-proxy/
WORKDIR /srv/configurable-http-proxy

# Install dependencies globally
RUN npm install -g pg configurable-http-proxy \
    && npm cache clean --force

# Switch to non-root user
USER node

# Expose ports for proxy traffic (8000) and API (8001)
EXPOSE 8000 8001

# Put configurable-http-proxy on path for chp-docker-entrypoint
ENV PATH=/srv/configurable-http-proxy/bin:$PATH
ENTRYPOINT ["./start_proxy"]