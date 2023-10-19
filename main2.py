from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
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
            response_generator = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt},
                ],
                # messages=[
                #     {"role": "system", "content": "Eres un experto cuenta cuentos"},
                #     {"role": "user", "content": prompt},
                # ],
                stream=True,
                #max_tokens=200
            )

            for response in response_generator:
                if response["choices"][0]['finish_reason']=='stop':
                    print('cadena finalizada')
                else :
                    assistant_response = response['choices'][0]['delta']['content']

                    data = {"message": assistant_response}

                    json_data = json.dumps(data)
                    # Envía la palabra al cliente a través de WebSocket
                    await websocket.send_text(json_data)
                

    except WebSocketDisconnect:
        pass
