import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Medical Myth Buster API",
    description="An API to debunk medical myths using AI chatbot",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (change this for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Define request body model
class ChatRequest(BaseModel):
    message: str

@app.post("/chat", tags=["Chatbot"])
async def chat(request: ChatRequest):
    """
    Chat with the Medical Myth Buster Bot.
    
    - **message**: The user's question
    - **Returns**: AI-generated response
    """
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mixtral-8x7b-32768",
            "messages": [
                {"role": "system", "content": "You are a medical myth buster chatbot."},
                {"role": "user", "content": request.message}
            ]
        }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=data, headers=headers)
        response_data = response.json()

        return {"response": response_data["choices"][0]["message"]["content"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
