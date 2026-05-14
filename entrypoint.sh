#!/bin/bash

alembic upgrade head
exec uvicorn code.src.main:app --host 0.0.0.0 --port 80 --reload
