from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

# Configuración de OpenAI
openai.api_key = os.getenv("API_KEY")

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompletionRequest(BaseModel):
    prompt: str

@app.post("/completions")
async def completions(request: CompletionRequest):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # model="gpt-4",
        messages=[
            {"role": "user", "content": request.prompt},
        ],
        stream=True,
        max_tokens = 100
    )

    # Itera a través del generador "response" y accede a los elementos necesarios
    collected = []
    for chunk in response:
        chunk_message = chunk["choices"][0]["delta"]
        collected.append(chunk_message)
    content = ''.join([m.get('content', '') for m in collected])

    return content

