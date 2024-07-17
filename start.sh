#!/bin/bash

uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 2

# NUM_WORKERS=$(($(nproc) * 2 + 1))
# uvicorn main:app --host 0.0.0.0 --port 8000 --workers $NUM_WORKERS