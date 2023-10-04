from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

# Configuración de OpenAI
openai.api_key = os.getenv("API_KEY")
print(openai.api_key)

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

# Modelo de datos para recibir la petición


class CompletionRequest(BaseModel):
    prompt: str

# Ruta para la petición de completions


# @app.post("/completions")
# async def completions(request: CompletionRequest):
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=request.prompt,
#         max_tokens=256
#     )
#     return response.choices[0].text


@app.post("/completions")
async def completions(request: CompletionRequest):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        #model="gpt-4",
        messages=[
            {"role": "user", "content": request.prompt},
        ]
    )
    return response['choices'][0]['message']['content']

