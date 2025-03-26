# Trademark Indexing AI System

## Overview

This project implements an AI-powered trademark indexing system. The system automates the extraction and processing of text from trademark images, generating structured indexing data for both English and Chinese text, and providing trademark descriptions.

## Solution Architecture

### System Architecture

The Trademark Indexing AI System follows a microservices architecture with two main components:

1. **VLLM Inference Server**:
   - Hosts the fine-tuned InternVL 2.5 4B model with LoRA adaptation
   - Exposes an OpenAI-compatible API for vision-language model inference
   - Optimizes GPU memory utilization and throughput using VLLM

2. **FastAPI Application Service**:
   - Provides RESTful API endpoints for client communication
   - Handles request validation, preprocessing, and error handling
   - Processes model outputs and formats responses according to specifications

#### Design Decisions

1. **Model Selection** - InternVL 2.5 4B with LoRA:
   - **Multimodal Capabilities**: Provides strong vision-language understanding
   - **Parameter-Efficient Fine-tuning**: LoRA adaptation enables cost-effective domain adaptation
   - **Size/Performance Balance**: 4B parameter model balances quality and resource requirements
   - **Strong base model**: Original InternVL 2.5 4B has recall around **72.9%** for Chinese trademark OCR without finetuning; after finetuning will reach **84.1%**

2. **Inference Optimization with VLLM**:
   - **Continuous Batching**: Improves throughput for concurrent requests
   - **Memory Optimization**: Efficient GPU memory utilization (set to 50% in configuration)
   - **KV Cache Management**: Optimizes inference for multiple sequential requests

3. **API Design**:
   - **Structured Output Format**: Uses JSON schema to enforce consistent response structure
   - **Post-processing Logic**: Filters extracted text to ensure quality (English, Chinese character validation)
   - **Health Check Endpoint**: Enables monitoring and load balancing

### Solution Selection Rationale and Alternatives

**Model Selection**:
   - **Selected**: InternVL 2.5 4B with LoRA fine-tuning, strong base model, end to end model for this solution
   - **Considered Alternatives**:
     - **CLIP**: Effective for image embeddings but has limitations in text generation
     - **GOT-OCR 2.0**: More suitable for document understanding, but not optimal for trademark OCR
     - **PaddleOCR**: lightwight model for OCR only, but its performance is not as strong as VLM models for trademarks.

**Inference Infrastructure Selection**:
   - **Selected**: vLLM, easy deployment, minimal bugs, support structured output
   - **Considered Alternatives**:
      - **LMDeploy**: Support TurboMind inference engine, faster concurrency, but structured output has bugs.

### Scaling Considerations and Limitations

1. **Scaling Capabilities**:
   - **Horizontal Scaling**: Can deploy multiple container instances behind a load balancer
   - **Vertical Scaling**: Supports larger GPU instances for handling higher throughput
   - **Cloud Deployment**: Compatible with major cloud providers' GPU instances

2. **Limitations**:
   - **Language Support**: Optimized primarily for English and Chinese text
   - **Image Quality Dependency**: Performance degrades with low-resolution or highly stylized text
   - **Complex Trademarks**: May struggle with intricate logos or ambiguous symbols
   - **Repeating response**: May have repeating response, need limit max response token.
   - **Traditional Chinese & Japanese Kanzi**: Trademark may have traditional Chinese and Japanese kanzi, need conversion to Simplified Chinese for indexing.
   - **Scaling Costs**: Linear cost scaling with GPU resources


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

You may need to wait for a few minutes for all services to be ready. Until you see some information like
```
bzhou_ubuntu  | INFO 03-26 04:37:05 [loggers.py:80] Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 1 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
```

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