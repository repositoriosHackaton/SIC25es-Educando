from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import random
from fastapi.staticfiles import StaticFiles

# levantar el servidor, si es en modo local
# uvicorn apiChatBoot:app --reload

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)


@app.post("/HipertensoBot")
async def HipertensoBot(request: Request):
    # obtenemos lo enviado que es un diccionaro
    data = await request.json()
    
    # obtenemos el mensaje, [disponible para hacer lo que se desee]
    mensaje = data['mensaje']
   
    
    # devolvemos una respuesta
    return {"tipo_usuario": 'Chatboot',"mensaje": mensaje }
     
     
# para imagenes de cada chat
# app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/assets", StaticFiles(directory="static"), name="static")
