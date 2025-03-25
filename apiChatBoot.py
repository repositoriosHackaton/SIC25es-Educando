from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import joblib
import pandas as pd
import json

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

# print("***Cardio Salud ES***")
# print("1) Realizar formulario")
# print("2) Explicame los datos necesarios")
# print("3) Salir")
# print("Nota: Recuerde que estos no son datos oficiales. Consulta con tu medico cualquier sintoma que presentes")
# print("***Previene y cuida tu salud***")
    
@app.post("/HipertensoBot")
async def HipertensoBot(request: Request):
    try:
        #Cargar los modelos
        try:
            model = joblib.load('modelo_XGBClassifier.pkl')
            escalar = joblib.load('modelo_escalado.pkl')
        except Exception as e:
            print(f"Error al cargar el modelo: {str(e)}")
            return {
                "tipo_usuario": "Chatboot",
                "mensaje": "Error al cargar el modelo: " +str(e),
                "type": "false"
            }

        # obtenemos lo enviado que es un diccionaro
        data = await request.json()
        
        # obtenemos el mensaje, [disponible para hacer lo que se desee]
        mensaje = data['mensaje']
    
        # data del formulario
        form_keys = data['formKeys']

        cadena = ''

        
        if len(form_keys) > 0:
           
            try:
                # sobreescribiendo el diccionario
                dict_modelo = {
                    'age': form_keys['edad'], 
                    'sex': form_keys['genero'], 
                    'cp': form_keys['dolor'],  
                    'trestbps': form_keys['presion_sangre'],
                    'chol': form_keys['colesterol'],  
                    'fbs': form_keys['nivel_azucar'],  
                    'thalach': form_keys['frecuencia_cardiaca'],
                    'exang': form_keys['dolor_present_pecho']  
                }

                print("*"*90)
                print(form_keys)
                print(dict_modelo)
                print(type(form_keys))
                print("*"*90)
            
                #hacer lo que se debe
                columnas = ['age','sex','cp','trestbps','chol','fbs','thalach','exang']

                #Convertir a df
                df = pd.DataFrame([dict_modelo.values()], columns=columnas)

                #Escalar datos
                datos_escalados = escalar.transform(df)

                #Prediccion
                cadena = model.predict(datos_escalados)

                if cadena == 1:
                    cadena = 'EL riesgo de hipertension es alto!'
                else:
                    cadena = 'El riesgo de hipertension es bajo!'
            except Exception as e:
          
                return {
                    "tipo_usuario": "Chatboot",
                    "mensaje": "Error al convertir el dataframe " +str(e),
                    "type": "false"
                } 
    
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
            respuesta = chatbot.get_response(user_input)

        # Devolver la respuesta en el formato deseado
        # la respuesta mandarlo todo en un solo string no mandar diccionario array etc...
        return {
            "tipo_usuario": "Chatboot",
            "mensaje": respuesta+ ' ' + cadena,
            "type": "insert"
        }
        
        
        
    except Exception as e:
        return {
            "tipo_usuario": "Chatboot",
            "mensaje": str(e),
            "type": "false"
        }
    
    
    
    
     