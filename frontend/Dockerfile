# Use an official Node.js runtime as a parent image
FROM node:16

# Set the working directory to /app
WORKDIR /frontend

# Copy the package.json files to the container
COPY package.json ./


# Install dependencies
RUN npm install
# Copy the rest of the application code to the container
COPY . .

# Build the application
RUN npm run build

# Expose port 3000 to the outside world
EXPOSE 3000

# Start the application
CMD ["npm", "start"]