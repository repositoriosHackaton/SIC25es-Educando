#Intalar chat pre entrenado
# pip install chatterbot
# pip install chatterbot_corpus


from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Crear una nueva instancia del chatbot
chatbot = ChatBot("Asistente")

# Entrenar el chatbot con datos en español
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.spanish")

#Entrenar con file
trainer.train("/content/entrenar.json")
trainer.train("/content/preguntas.json")



despedida = ['salir', 'adios', 'chao', 'hasta luego', "3"]
op1 = ['op1','opcion 1','opcion1','1', 'formulario']
op2 = ['op2','2', 'opcion 2','opcion2']


# Chat con el bot
print("***Cardio Salud ES***")
print("1) Realizar formulario")
print("2) Explicame los datos necesarios")
print("3) Salir")
print("Nota: Recuerde que estos no son datos oficiales. Consulta con tu medico cualquier sintoma que presentes")
print("***Previene y cuida tu salud***")

while True:
    user_input = input("Tú: ")
    if user_input.lower() in despedida:
        print("¡Adiós!")
        break
    if user_input.lower() in op1:
        print("LINK")
    if user_input.lower() in op2:
        print("**DATOS NECESARIOS**")
        print("1.Edad")
        print("2.Genero")
        print("3.Dolor en el pecho (Anginas)")
        print("La angina de pecho es un tipo de dolor de pecho causado por la reducción del flujo sanguíneo al corazón. ")
        print("4. Presion en sangre")
        print("La presión arterial es una fuerza que se ejerce en la sangre para que esta pueda recorrer todos los torrentes sanguíneos y así aportarle la vitalidad necesaria a los órganos.")
        print("5. Colesterol")
        print("El colesterol es una sustancia cerosa y parecida a la grasa que se encuentra en todas las células de su cuerpo. Su cuerpo necesita algo de colesterol para funcionar bien. Pero si tiene demasiado colesterol en su sangre, se puede pegar en las paredes de sus arterias, estrechándolas o incluso bloqueándolas")
        print("6. Tiene nivel de azucar alto?")
        print("La glucemia es la cantidad de glucosa que circula en la sangre y sirve como fuente de energía para el cuerpo")
        print("Se considera alta si se encuentra arriba de 120 mg/dl")
        print("7. Frecuencia cardiaca maxima")
        print("Es la cantidad máxima de veces que el corazón puede latir en un minuto")
        print("Puedes medirla con el dedo, el frecuencímetro o la calculadora")
        print("8. Presenta dolores de pecho al hacer ejercicio? (Anginas)")

    response = chatbot.get_response(user_input)
    print(f"Cardio Salud ES: {response}")