FROM node:18-alpine

WORKDIR /app

# Copy only package files first to leverage caching
COPY package.json package-lock.json ./
RUN npm install  # Install dependencies

# Now, copy the rest of the project
COPY . . 

EXPOSE 3000

CMD ["npm", "start"]