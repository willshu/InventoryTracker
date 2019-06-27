#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn product_api.wsgi --bind 0.0.0.0:8000 