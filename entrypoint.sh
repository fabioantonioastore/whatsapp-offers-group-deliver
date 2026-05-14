#!/bin/bash

exec alembic upgrade head
exec uvicorn src.main:app --host 0.0.0.0 --port 80 --reload
