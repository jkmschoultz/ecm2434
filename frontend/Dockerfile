FROM node:14.17.3

# Set the working directory to /frontend
WORKDIR /frontend

# Copy the application code to the container
COPY . .

# Install dependencies
RUN npm install

# Build the application
RUN npm run build

# Expose port 3000 to the outside world
EXPOSE 3000

# Start the application
CMD ["npm", "start"]