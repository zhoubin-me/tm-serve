# Trademark Indexing AI System

## Overview

This project implements an AI-powered trademark indexing system for GovTech Singapore's Multimodal AI Team. The system automates the extraction and processing of text from trademark images, generating structured indexing data for both English and Chinese text, and providing trademark descriptions.

## Solution Architecture

### System Components

The trademark indexing system consists of the following key components:

1. **FastAPI Web Service**: A lightweight, high-performance API service that handles HTTP requests and responses, providing endpoints for health checks and trademark processing.

2. **InternVL Vision-Language Model**: A fine-tuned multimodal model (`bzhouxyz/internvl-2d5-4B-lora-ft-tm`) specifically trained to process trademark images and extract relevant information.

3. **VLLM Inference Server**: An optimized inference engine that serves the vision-language model with GPU acceleration for efficient processing of trademark images.

4. **Docker Container**: A containerized environment that packages all dependencies and components into a reproducible deployment unit.

### Data Flow

1. **Request Processing**:
   - The client sends a POST request to the `/invoke` endpoint with a base64-encoded trademark image.
   - The FastAPI service validates the request and prepares the image data for processing.

2. **AI Model Inference**:
   - The image is sent to the fine-tuned InternVL model via the OpenAI-compatible API interface provided by VLLM.
   - The model processes the image and identifies three key elements with structured output:
     - English words in the trademark (`wordsInMark`)
     - Chinese characters in the trademark (`chineseCharacter`)
     - Description of the trademark device/symbol (`descrOfDevice`)

3. **Response Generation**:
   - The raw model output is post-processed to ensure proper formatting:
     - English text is filtered to include only English letters and spaces
     - Chinese text is filtered to include only valid Chinese characters
   - The structured data is returned as a JSON response to the client

### Technical Stack

- **Backend Framework**: FastAPI (Python)
- **Vision-Language Model**: Fine-tuned InternVL 2.5 4B with LoRA adaptation
- **Inference Optimization**: VLLM for efficient GPU-accelerated inference
- **Containerization**: Docker and Docker Compose
- **Package Management**: UV (Python package manager)

### Deployment Architecture

The system is deployed as a set of containerized services:

1. **VLLM Server**: Runs the large vision-language model on GPU with memory optimization
2. **FastAPI Application**: Provides the HTTP interface for client applications

Both services are orchestrated through Docker Compose, making the solution portable and easy to deploy across different environments with NVIDIA GPU support.

## Installation

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
This step may take a few minutes as it will download my finetuned model ```bzhouxyz/internvl-2d5-4B-lora-ft-tm``` from huggingface

3. Run the container:
   ```bash
   docker-compose up
   ```

You may need to wait for a few minutes for all services to be ready.

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