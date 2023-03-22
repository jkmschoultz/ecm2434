FROM node:14.17.3

# Set the working directory to /frontend
WORKDIR /frontend

# Copy the application code to the container
COPY . .

# Install dependencies
RUN npm install

EXPOSE 3000

CMD ["npm", "start"]