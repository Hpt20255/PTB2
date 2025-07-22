# GPTB2 Frontend Dockerfile - Task 3.3
# Multi-stage build: Node.js build → Nginx serve
# Optimized for React SPA with production-ready configuration

# ================================
# Stage 1: Build Stage (Node.js)
# ================================
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Set environment variables for build optimization
ENV NODE_ENV=production \
    GENERATE_SOURCEMAP=false \
    INLINE_RUNTIME_CHUNK=false

# Install system dependencies for node-gyp if needed
RUN apk add --no-cache \
    python3 \
    make \
    g++

# Copy package files first for better Docker layer caching
COPY package*.json ./

# Install dependencies with production optimizations
RUN npm ci --only=production --silent && \
    npm cache clean --force

# Copy source code
COPY . .

# Build the React application
RUN npm run build && \
    # Verify build output
    ls -la build/ && \
    echo "Build completed successfully"

# ================================
# Stage 2: Production Stage (Nginx)
# ================================
FROM nginx:1.25-alpine AS production

# Install curl for health checks
RUN apk add --no-cache curl

# Create nginx user and set permissions
RUN addgroup -g 1001 -S nginx-app && \
    adduser -S nginx-app -G nginx-app

# Copy built React app from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create nginx directories and set permissions
RUN mkdir -p /var/cache/nginx /var/log/nginx && \
    chown -R nginx-app:nginx-app /var/cache/nginx /var/log/nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# Create a simple health check script
RUN echo '#!/bin/sh' > /usr/local/bin/health-check.sh && \
    echo 'curl -f http://localhost/health || exit 1' >> /usr/local/bin/health-check.sh && \
    chmod +x /usr/local/bin/health-check.sh

# Expose port 80
EXPOSE 80

# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD /usr/local/bin/health-check.sh

# Add labels for better container management
LABEL maintainer="GPTB2 Team" \
      version="1.0" \
      description="GPTB2 React Frontend with Nginx" \
      stage="production"

# Switch to non-root user for security
USER nginx-app

# Start nginx
CMD ["nginx", "-g", "daemon off;"]