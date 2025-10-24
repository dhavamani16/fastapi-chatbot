from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
ollama_url = os.getenv("OLLAMA_URL")

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        payload = {
            "model": "mistral",
            "messages": [
                {"role": "user", "content": request.message}
            ]
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{ollama_url}/chat", json=payload)
            response.raise_for_status()
            data = response.json()
            reply = data['choices'][0]['message']['content']
            return ChatResponse(reply=reply)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error talking to Ollama: {e}")
