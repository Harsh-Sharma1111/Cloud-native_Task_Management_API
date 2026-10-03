# Stage 1: Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files and install dependencies cleanly
COPY package*.json ./
RUN npm ci

# Copy the rest of the application source code
COPY . .

# Accept VITE_API_BASE_URL as a build argument and set it as an environment variable
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Build the application
RUN npm run build

# Stage 2: Serve stage
FROM nginx:alpine

# Copy the custom Nginx configuration to support client-side routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the built assets from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
