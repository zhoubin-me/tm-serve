from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import re
import json
client = OpenAI(api_key='YOUR_API_KEY', base_url='http://0.0.0.0:8000/v1')
model_name = "bzhouxyz/internvl-2d5-4B-lora-ft-tm"

guide = {
    'type': 'object',
    'properties': {
        'wordsInMark': {'type': 'string'},
        'chineseCharacter': {'type': 'string'},
        'descrOfDevice': {'type': 'string'}
    },
    'required': ['wordsInMark', 'chineseCharacter', 'descrOfDevice']
}

response_format=dict(type='json_schema',  json_schema=dict(name='test',schema=guide))

app = FastAPI()

class InferenceRequest(BaseModel):
    image: str  # Base64 encoded image

class InferenceResponse(BaseModel):
    wordsInMark: str
    chineseCharacter: str
    descrOfDevice: str

@app.get("/ping")
def health_check():
    return "pong"

@app.post("/invoke", response_model=InferenceResponse)
def invoke_model(request: InferenceRequest):
    try:
        # Decode base64 image
        image_data = request.image
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a helpful assistant that extracts Chinese characters, English words on this trademark image, and describes the trademark in short words.'
                },
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'text',
                            'text': '<image>\nExtract Chinese characters, English words on this trademark image, and describe the trademark in short words.',
                        },
                        {
                            'type': 'image_url',
                            'image_url': { 'url': f"data:image/jpeg;base64,{image_data}"},
                        },
                    ],
                }
            ],
            response_format=response_format,
            temperature=0.1,
            top_p=0.9)

        content = response.choices[0].message.content

        if isinstance(content, str):
            # If the content is in a JSON-like structure, try to parse it
            try:
                content = json.loads(content)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Response content is not in expected JSON format.")


        # Filter to allow only English letters and space
        words_in_mark = re.sub(r'[^a-zA-Z\s]', '', content['wordsInMark'])
        # Filter to allow only Chinese characters
        chinese_character = re.sub(r'[^\u4e00-\u9fa5\u3400-\u4DBF]', '', content['chineseCharacter'])
        descr_of_device = content['descrOfDevice']

        return InferenceResponse(
            wordsInMark=words_in_mark,
            chineseCharacter=chinese_character,
            descrOfDevice=descr_of_device
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image data: {str(e)}")