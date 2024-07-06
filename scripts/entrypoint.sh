#!/bin/sh

cd /app

exec uvicorn app.server:app --host 0.0.0.0 --port 8000 ${@}
