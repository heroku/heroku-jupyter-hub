FROM python:3.10-slim

# Install Node.js and nginx
RUN apt-get update && \
    apt-get install -y \
    nodejs \
    npm \
    nginx \
    && npm install -g configurable-http-proxy \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
WORKDIR /app
COPY . .

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Make start script executable
RUN chmod +x start_proxy

# Use non-root user
RUN useradd -m -d /home/jovyan jovyan
RUN chown -R jovyan:jovyan /app
USER jovyan

# Expose the port
EXPOSE $PORT

# Start both nginx and configurable-http-proxy
CMD ["./start_proxy"]