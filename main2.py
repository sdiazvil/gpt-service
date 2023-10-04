from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
import openai
import asyncio
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
import json

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


@app.websocket("/completions")
async def completions(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()

            # Utiliza OpenAI para obtener una respuesta
            prompt = data  # El mensaje del cliente podría servir como el prompt para OpenAI
            response_generator = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                stream=True,
                max_tokens=100
            )

            for response in response_generator:
                assistant_response = response.choices[0].text

                data = {"message": assistant_response}

                json_data = json.dumps(data)
                # Envía la palabra al cliente a través de WebSocket
                await websocket.send_text(json_data)

    except WebSocketDisconnect:
        pass
    