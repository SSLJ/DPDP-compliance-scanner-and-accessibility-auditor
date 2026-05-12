FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5173
# Use --host to allow external access to the Vite server
CMD ["npm", "run", "dev", "--", "--host"]
