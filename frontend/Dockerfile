# Build stage
FROM node:20-bullseye-slim AS build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install minimal build dependencies for native modules
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 build-essential git \
    && rm -rf /var/lib/apt/lists/*

# Install npm packages
RUN npm install --silent

# Copy app files
COPY . .

# Build the app
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
