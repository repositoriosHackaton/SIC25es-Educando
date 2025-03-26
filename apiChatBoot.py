from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import joblib
import pandas as pd
import json

# levantar el servidor, si es en modo local
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
                "mensaje": "Error al cargar el modelo: " +str(e)
            }

        # obtenemos lo enviado que es un diccionaro
        data = await request.json()
        
       
    
        # data del formulario
        form_keys = data['formKeys']


        
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

                for col in dict_modelo:
                    try:
                        dict_modelo[col] = int(float(dict_modelo[col]))
                    except ValueError:
                        pass  
   

                #Convertir a df
                # df = pd.DataFrame([dict_modelo], dtype=int)
                df = pd.DataFrame([dict_modelo])

                #Escalar datos numericos
                colnums = ['age','trestbps','chol']
                df_escalado = pd.DataFrame(escalar.fit_transform(df[colnums]), columns=colnums)

                #Combinar de nuevo en un solo DataFrame
                df_restantes = df.drop(columns=colnums)
                df = pd.concat([df_escalado, df_restantes], axis=1)

                #Prediccion
                cadena = model.predict(df)
                cadena = cadena[0]

                if cadena == '1':
                    return {
                        "tipo_usuario": "Chatboot",
                        "mensaje": "EL riesgo de hipertension es alto!"
                    }
                else:
                    return {
                        "tipo_usuario": "Chatboot",
                        "mensaje": "El riesgo de hipertension es bajo!"
                    }
            except Exception as e:
          
                return {
                    "tipo_usuario": "Chatboot",
                    "mensaje": "Error al convertir el dataframe " +str(e)
                } 
        else:
            # obtenemos el mensaje, [disponible para hacer lo que se desee]
            mensaje = data['mensaje']
            
            # Procesar el mensaje
            user_input = mensaje.lower()

            respuesta = ""
            
            if user_input in despedida:
                respuesta = "¡Adiós!"
            elif user_input in op1:
                respuesta = "LINK"
            elif user_input in op2:
                respuesta = """
                DATOS NECESARIOS
                <br> 1. Edad
                <br> 2. Género
                <br> 3. Dolor en el pecho (Anginas)
                <br> 4. Presión en sangre
                <br> 5. Colesterol
                <br> 6. Tiene nivel de azúcar alto?
                <br> 7. Frecuencia cardiaca máxima
                <br> 8. Presenta dolores de pecho al hacer ejercicio? (Anginas)
                """
            else:
                # Usar el chatbot para obtener la respuesta
                respuesta = chatbot.get_response(user_input).text

            return {
                "tipo_usuario": "Chatboot",
                "mensaje": respuesta,
            }
        
        
        
    except Exception as e:
        return {
            "tipo_usuario": "Chatboot",
            "mensaje": "Error: "+ str(e),
        }
    