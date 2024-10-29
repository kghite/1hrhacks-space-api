#####
# Stage 1: Build the React app
FROM node:18 AS react-build

WORKDIR /nasa-webapp

# Install dependencies
COPY nasa-webapp/package.json nasa-webapp/package-lock.json ./
RUN npm install

# Build the React appapi
COPY nasa-webapp/ .
RUN npm run build

#####
# Stage 2: Build the FastAPI app
FROM python:3.11 AS nasa-api-build

RUN apt-get update && apt-get install -y nginx && apt-get clean

WORKDIR /nasa-api

# Install pipenv and dependencies
COPY nasa-api/Pipfile nasa-api/Pipfile.lock ./
RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

# Copy all app code
COPY nasa-api/ .
COPY --from=react-build /nasa-webapp/build /nasa-webapp/build
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
COPY nginx.conf /etc/nginx/nginx.conf

# Startup
EXPOSE 8000
EXPOSE 3000

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

