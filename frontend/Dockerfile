# Use Node.js with security patches (bookworm version)
FROM node:18-bookworm

# Set working directory inside container
WORKDIR /app

# Copy package.json and package-lock.json, then install dependencies
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy the rest of the frontend files
COPY . .

# Set environment variable for production
ENV NODE_ENV=production

# Build the CRA app (outputs to 'build' folder)
RUN npm run build

# Install a static server to serve the production build
RUN npm install -g serve

# Expose port 3000
EXPOSE 3000

# Serve the production build (CRA uses 'build', not 'dist')
CMD ["serve", "-s", "build", "-l", "3000"]
