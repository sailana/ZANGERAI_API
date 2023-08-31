from fastapi import FastAPI, File, UploadFile, HTTPException, Form, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
import openai
import json
import asyncio
from pydantic import BaseModel
from typing import List
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



app = FastAPI()

class RequestData(BaseModel):
    message: str
    history: List[str]

@app.post("/generate-response")
def generate_response(request_data: RequestData):
    try:
        logger.info(f"Request type {type(request_data)}")
        logger.info(f"Request {request_data}")
        data = request_data.json
        logger.info(f"Data {data}")
        message = data["message"]
        history = data["history"]
        
        messages = history + [{"role": "user", "content": message}]
        logger.info(f"messages {messages}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=100
        )
        logger.info(f"response {response}")
        logger.info(f"response type {type(response)}")
        
        response_text = response.choices[0].message.content
        return {"response": response_text}
    
    except Exception as e:
        logger.info(f"Error {e}")
        return HTTPException(status_code=500, detail=str(e))
