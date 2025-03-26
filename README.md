# Trademark Indexing AI System

## Overview

This project implements an AI-powered trademark indexing system for GovTech Singapore's Multimodal AI Team. The system automates the extraction and processing of text from trademark images, generating structured indexing data for both English and Chinese text, and providing trademark descriptions.

## Installation

### Prerequisites

- Docker
- NVIDIA GPU with CUDA support (for GPU inference) or CPU with 8+ cores
- 16GB+ RAM

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/zhoubin-me/tm-serve.git
   cd tm-serve
   ```

2. Build the Docker image:
   ```bash
   docker build -t tm-serve:latest .
   ```

3. Run the container:
   ```bash
   docker-compose up
   ```

You may need to wait for around 1 min for /invoke service be ready.

## API Usage

The service exposes two main endpoints:

### Health Check

```
curl -X GET http://localhost:1234/ping
```

**Response**:
```
"pong"
```

### Trademark Indexing

```
curl -X POST "http://localhost:1234/invoke" \
    -H "Content-Type: application/json" \
    -d "{\"image\":\"$(base64 samples/T1103840H_T1103840H.jpg | tr -d '\n')\"}"
```

**Response**:
```json
{"wordsInMark":"tru blood","chineseCharacter":"真血","descrOfDevice":"gear"}
```

### Example Usage

```python
import requests
import base64

# Read image and encode to base64
with open('samples/T1103840H_T1103840H.jpg', 'rb') as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

# Make API request
response = requests.post(
    'http://localhost:8000/invoke',
    json={'image': encoded_image}
)

# Print the results
print(response.json())
```