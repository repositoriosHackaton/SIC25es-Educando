from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import random
from fastapi.staticfiles import StaticFiles
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


# levantar el servidor, si es en modo local
# uvicorn apiChatBoot:app --reload

# modificacion levantando en un puerto distinto laravel corre en el 8080
# uvicorn apiChatBoot:app --reload --host 127.0.0.5 --port 5555
# endpoint generado: http://127.0.0.5:5555/HipertensoBot

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)



chatbot = ChatBot("Asistente")

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.spanish")

trainer.train("content\entrenar.json")
trainer.train("content\preguntas.json")


despedida = ['salir', 'adios', 'chao', 'hasta luego', "3"]
op1 = ['op1','opcion 1','opcion1','1', 'formulario']
op2 = ['op2','2', 'opcion 2','opcion2']

print("***Cardio Salud ES***")
print("1) Realizar formulario")
print("2) Explicame los datos necesarios")
print("3) Salir")
print("Nota: Recuerde que estos no son datos oficiales. Consulta con tu medico cualquier sintoma que presentes")
print("***Previene y cuida tu salud***")
    
@app.post("/HipertensoBot")
async def HipertensoBot(request: Request):
    # obtenemos lo enviado que es un diccionaro
    data = await request.json()
    
    # obtenemos el mensaje, [disponible para hacer lo que se desee]
    mensaje = data['mensaje']
   
    form_keys = data['formKeys']
    # llega en este formado, un diccionario
    # {
    #     "edad": "",
    #     "genero": "",
    #     "dolor": "",
    #     "presion_sangre": "",
    #     "colesterol": "",
    #     "nivel_azucar": "",
    #     "frecuencia_cardiaca": "",
    #     "dolor_present_pecho": ""
    # }
  
    if form_keys is not None:
        #hacer lo que se debe
        print(form_keys)
  
        
   
   # Procesar el mensaje
    user_input = mensaje.lower()

    respuesta = ""
    
    if user_input in despedida:
        respuesta = "¡Adiós!"
    elif user_input in op1:
        respuesta = "LINK"
    elif user_input in op2:
        respuesta = """
        **DATOS NECESARIOS**
        1. Edad
        2. Género
        3. Dolor en el pecho (Anginas)
        4. Presión en sangre
        5. Colesterol
        6. Tiene nivel de azúcar alto?
        7. Frecuencia cardiaca máxima
        8. Presenta dolores de pecho al hacer ejercicio? (Anginas)
        """
    else:
        # Usar el chatbot para obtener la respuesta
        # response = chatbot.get_response(user_input)
        respuesta = "Mensaje no encontrado"

    # Devolver la respuesta en el formato deseado
    # la respuesta mandarlo todo en un solo string no mandar diccionario array etc...
    return {
        "tipo_usuario": "Chatboot",
        "mensaje": respuesta,
        "type": "insert",
        "json_form" : form_keys
    }
     
     
# para imagenes de cada chat
app.mount("/assets", StaticFiles(directory="static"), name="static")
