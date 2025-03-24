from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)
app.secret_key = 'clave_segura_dra_cardio_2025'

# Configuración del chatbot
BOT_PROFILE = {
    "name": "Dra. Cardio",
    "emojis": ["❤️", "🩺", "💊", "🏥", "🧠", "💪"],
    "tips": [
        "Caminar 30 minutos diarios reduce el riesgo de hipertensión",
        "Reducir el consumo de sal ayuda a controlar la presión arterial",
        "Meditar 10 minutos diarios baja los niveles de estrés"
    ]
}

RESPONSES = {
    "greeting": "¡Hola! {emoji} Soy {name}, tu asistente cardiovascular",
    "options": ["Evaluar mi riesgo", "Consejos de salud"],
    "methods": ["Modo conversación", "Formulario rápido"]
}

QUESTIONS = [
    {"text": "¿Cuántos años tienes?", "field": "age", "type": "number"},
    {"text": "¿Última medición de presión (ej. 120/80)?", "field": "blood_pressure", "type": "text"},
    {"text": "¿Peso en kg (ej. 70)?", "field": "weight", "type": "number"},
    {"text": "¿Estatura en cm (ej. 165)?", "field": "height", "type": "number"},
    {"text": "¿Antecedentes familiares de hipertensión (sí/no)?", "field": "family_history", "type": "text"},
    {"text": "¿Fumas actualmente (sí/no)?", "field": "smoker", "type": "text"}
]

def format_response(text):
    return text.replace("{name}", BOT_PROFILE["name"]).replace("{emoji}", random.choice(BOT_PROFILE["emojis"]))

def calculate_risk(data):
    risk = 0
    
    try:
        # Age
        age = int(data.get('age', 0))
        if age > 50: risk += 25
        elif age > 40: risk += 15
        
        # Blood pressure
        bp = str(data.get('blood_pressure', '0/0')).split('/')
        if len(bp) == 2:
            systolic, diastolic = map(int, bp)
            if systolic >= 140 or diastolic >= 90: risk += 30
            elif systolic >= 130 or diastolic >= 85: risk += 15
        
        # BMI
        weight = float(data.get('weight', 0))
        height = int(data.get('height', 1))
        if height > 0:
            bmi = weight / ((height/100) ** 2)
            if bmi >= 30: risk += 20
            elif bmi >= 25: risk += 10
        
        # Risk factors (now handling both text and boolean)
        family_history = str(data.get('family_history', '')).lower()
        if family_history in ['sí', 'si', 'yes', 'true']: risk += 15
        
        smoker = str(data.get('smoker', '')).lower()
        if smoker in ['sí', 'si', 'yes', 'true']: risk += 10
        
    except (ValueError, TypeError, AttributeError) as e:
        app.logger.error(f"Error en cálculo de riesgo: {str(e)}")
    
    return min(100, max(5, risk))

@app.route('/')
def home():
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def handle_chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos no recibidos'}), 400

        user_input = data.get('message', '').lower().strip()
        session = data.get('session', {})
        
        # Inicializar sesión
        if not session:
            session = {
                'state': 'welcome',
                'data': {},
                'step': 0
            }
        
        response = {
            'message': '',
            'options': [],
            'session': session,
            'show_form': False,
            'completed': False
        }

        # Máquina de estados
        if session['state'] == 'welcome':
            response['message'] = format_response(RESPONSES["greeting"])
            response['options'] = RESPONSES["options"]
            session['state'] = 'main_menu'
        
        elif session['state'] == 'main_menu':
            if "evaluar" in user_input or "riesgo" in user_input:
                response['message'] = "¿Cómo prefieres realizar la evaluación?"
                response['options'] = RESPONSES["methods"]
                session['state'] = 'method_choice'
            elif "consejos" in user_input:
                response['message'] = "Consejos de salud:\n\n" + "\n".join(f"• {tip}" for tip in BOT_PROFILE["tips"])
                response['options'] = ["Evaluar mi riesgo", "Salir"]
            else:
                response['message'] = "No entendí tu respuesta. Por favor elige una opción:"
                response['options'] = RESPONSES["options"]
        
        elif session['state'] == 'method_choice':
            if "conversación" in user_input:
                session['state'] = 'in_assessment'
                response['message'] = QUESTIONS[0]['text']
            elif "formulario" in user_input:
                session['state'] = 'quick_form'
                response['show_form'] = True
            else:
                response['message'] = "Por favor elige un método de evaluación:"
                response['options'] = RESPONSES["methods"]
        
        elif session['state'] == 'in_assessment':
            current_question = QUESTIONS[session['step']]
            
            # Validación de respuesta
            if current_question['type'] == 'number':
                try:
                    num = float(user_input)
                    if num <= 0:
                        raise ValueError
                    session['data'][current_question['field']] = num
                except ValueError:
                    response['message'] = f"Por favor ingresa un número válido para: {current_question['text']}"
                    return jsonify(response)
            else:
                # Almacenar como texto para evitar problemas con booleanos
                session['data'][current_question['field']] = user_input
            
            # Avanzar o finalizar
            if session['step'] + 1 < len(QUESTIONS):
                session['step'] += 1
                response['message'] = QUESTIONS[session['step']]['text']
            else:
                risk = calculate_risk(session['data'])
                response['message'] = f"🔍 Resultado:\nRiesgo cardiovascular: {risk}%\n\n"
                if risk > 70:
                    response['message'] += "🔴 Riesgo alto - Consulta a un especialista"
                elif risk > 40:
                    response['message'] += "🟠 Riesgo moderado - Recomendamos cambios en tu estilo de vida"
                else:
                    response['message'] += "🟢 Riesgo bajo - ¡Sigue manteniendo hábitos saludables!"
                response['options'] = ["Nueva evaluación", "Salir"]
                session['state'] = 'complete'
        
        return jsonify(response)
    
    except Exception as e:
        app.logger.error(f"Error en /api/chat: {str(e)}")
        return jsonify({
            'message': "Disculpa, ocurrió un error interno. Por favor intenta nuevamente.",
            'options': ["Reiniciar conversación"]
        }), 500

@app.route('/api/assess', methods=['POST'])
def quick_assessment():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos no recibidos'}), 400
        
        # Validación de campos requeridos
        required_fields = ['age', 'systolic', 'diastolic', 'weight', 'height']
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                return jsonify({'error': f'Campo {field} es requerido'}), 400
        
        risk_data = {
            'age': int(data['age']),
            'blood_pressure': f"{data['systolic']}/{data['diastolic']}",
            'weight': float(data['weight']),
            'height': int(data['height']),
            'family_history': str(data.get('family_history', 'no')).lower(),
            'smoker': str(data.get('smoker', 'no')).lower()
        }
        
        risk = calculate_risk(risk_data)
        
        response = {
            'message': f"📊 Resultado:\nRiesgo de hipertensión: {risk}%\n\n",
            'risk': risk,
            'options': ["Evaluar nuevamente", "Salir"]
        }
        
        if risk > 70:
            response['message'] += "🔴 Riesgo alto - Consulta a un cardiólogo"
        elif risk > 40:
            response['message'] += "🟠 Riesgo moderado - Recomendamos cambios en tu estilo de vida"
        else:
            response['message'] += "🟢 Riesgo bajo - ¡Buen trabajo!"
        
        return jsonify(response)
        
    except ValueError as e:
        return jsonify({'error': 'Datos inválidos: ' + str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error en /api/assess: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    app.run(debug=True)