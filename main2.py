from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import openai
from dotenv import dotenv_values
import json
import os

from langchain.llms import AzureOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

app = FastAPI()

config = dotenv_values(".env")

# Configuración de OpenAI
# openai.api_type = "azure"
# openai.api_key = config["AZURE_API_KEY"]
# openai.api_base = config["AZURE_ENDPOINT"]
# openai.api_version = config["AZURE_API_VERSION"]
#os.environ["OPENAI_API_KEY"] = config["API_KEY"]
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = config["AZURE_API_VERSION"]
os.environ["OPENAI_API_BASE"] = config["AZURE_ENDPOINT"]
os.environ["OPENAI_API_KEY"] = config["AZURE_API_VERSION"]

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

llm = AzureOpenAI(
    deployment_name="chatbot-allocation-argentina",
    model_name="text-davinci-002",
)

llm("Tell me a joke")

# @app.websocket("/completions")
# async def completions(websocket: WebSocket):
#     await websocket.accept()

#     try:
#         while True:
#             data = await websocket.receive_text()

#             # Utiliza OpenAI para obtener una respuesta
#             prompt = data  # El mensaje del cliente podría servir como el prompt para OpenAI
#             response_generator = openai.ChatCompletion.create(
#                 deployment_id="chatbot-allocation-argentina",
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "user", "content": prompt},
#                 ],
#                 # messages=[
#                 #     {"role": "system", "content": "Eres un experto cuenta cuentos"},
#                 #     {"role": "user", "content": prompt},
#                 # ],
#                 stream=True,
#                 # max_tokens=200
#             )

#             # Inicializa una variable de control
#             first_iteration = True

#             for response in response_generator:
#                 if first_iteration:
#                     first_iteration = False
#                     continue  # Salta la primera iteración

#                 if response["choices"][0]['finish_reason']=='stop':
#                     print('cadena finalizada')
#                 else :
#                     assistant_response = response['choices'][0]['delta']['content']

#                     data = {"message": assistant_response}

#                     json_data = json.dumps(data)
#                     # Envía la palabra al cliente a través de WebSocket
#                     await websocket.send_text(json_data)

#     except WebSocketDisconnect:
#         pass
