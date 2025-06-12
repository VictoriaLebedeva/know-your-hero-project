FROM node:18

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

# Expose the Vite dev server port
EXPOSE 5173

# Start the frontend in development mode
CMD ["npm", "run", "dev", "--", "--host"]