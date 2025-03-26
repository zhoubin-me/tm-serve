#!/bin/bash

# Start vllm server in the background
uv run vllm serve bzhouxyz/internvl-2d5-4B-lora-ft-tm --gpu-memory-utilization 0.5 &
VLLM_PID=$!

# Start FastAPI app
uv run uvicorn main:app --host 0.0.0.0 --port 1234 --reload &
UVICORN_PID=$!

# Keep the container running
trap "kill $VLLM_PID $UVICORN_PID; exit" SIGTERM SIGINT
wait $VLLM_PID $UVICORN_PID