FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Expose port
EXPOSE 2400

# Development command
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "2400"]
