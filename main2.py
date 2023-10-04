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


class CompletionRequest(BaseModel):
    prompt: str

# @app.post("/completions")
# async def completions(request: CompletionRequest):
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         # model="gpt-4",
#         messages=[
#             {"role": "user", "content": request.prompt},
#         ],
#         stream=True,
#         max_tokens = 100
#     )
#     return response

    # return response["choices"][0]["delta"]["content"]

    # # Itera a través del generador "response" y accede a los elementos necesarios
    # collected = []
    # for chunk in response:
    #     chunk_message = chunk["choices"][0]["delta"]
    #     collected.append(chunk_message)
    # content = ''.join([m.get('content', '') for m in collected])

    # return content


async def generate_messages(data: dict, websocket: WebSocket):
    # Envía la respuesta como JSON a través de WebSocket
    await websocket.send_json(data)


@app.websocket("/completions")
async def completions(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()

            # Utiliza OpenAI para obtener una respuesta
            prompt = data  # El mensaje del cliente podría servir como el prompt para OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto cuenta cuentos"},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=100
            )

            # Extrae el contenido de la respuesta de OpenAI
            assistant_response = response.choices[0].message["content"]

            data = {"message": assistant_response}

            json_data = json.dumps(data)
            # Envía la respuesta al cliente a través de WebSocket
            await websocket.send_text(json_data)

    except WebSocketDisconnect:
        pass
 


