FROM node:20-alpine

WORKDIR /app

# Install npm dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

EXPOSE 3000

# Start Vite and bind to 0.0.0.0 so host port mappings work
CMD ["npm", "run", "dev", "--", "--host"]
