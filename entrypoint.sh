#!/bin/bash

# Start Nginx in the background
nginx -g 'daemon off;' &

# Start the FastAPI backend
uvicorn photos_api.app:app --host 0.0.0.0 --port 8000

