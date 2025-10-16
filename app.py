from flask import Flask, render_template, request, jsonify
import json
from clock_logic import Reloj, Cronometro, Temporizador

app = Flask(__name__)

# Instancias globales
reloj_principal = Reloj()
cronometro = Cronometro()
temporizador = Temporizador()
relojes_adicionales = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/hora_actual')
def hora_actual():
    # El reloj principal muestra segundos
    return jsonify({'hora': reloj_principal.obtener_hora_actual()})

@app.route('/api/cambiar_configuracion', methods=['POST'])
def cambiar_configuracion():
    global reloj_principal, relojes_adicionales
    data = request.get_json()
    zona_horaria = data.get('zona_horaria', 'America/Bogota')
    formato_24h = data.get('formato_24h', True)
    tema_oscuro = data.get('tema_oscuro', False)

    # Actualizar reloj principal
    reloj_principal = Reloj(zona_horaria=zona_horaria, formato_24h=formato_24h)

    # Actualizar todos los relojes adicionales con el nuevo formato
    for i, reloj in enumerate(relojes_adicionales):
        relojes_adicionales[i] = Reloj(zona_horaria=reloj.zona_horaria, formato_24h=formato_24h)

    return jsonify({'success': True, 'tema_oscuro': tema_oscuro})

@app.route('/api/agregar_reloj', methods=['POST'])
def agregar_reloj():
    data = request.get_json()
    zona_horaria = data.get('zona_horaria', 'UTC')
    # Usar el mismo formato que el reloj principal
    formato_24h = reloj_principal.formato_24h

    nuevo_reloj = Reloj(zona_horaria=zona_horaria, formato_24h=formato_24h)
    relojes_adicionales.append(nuevo_reloj)

    return jsonify({'hora': nuevo_reloj.obtener_hora_actual(), 'indice': len(relojes_adicionales) - 1})

@app.route('/api/horas_adicionales')
def horas_adicionales():
    import datetime
    horas = []
    for reloj in relojes_adicionales:
        # Los relojes adicionales no muestran segundos, solo HH:MM
        ahora = datetime.datetime.now(reloj.tz)
        if reloj.formato_24h:
            hora_formateada = ahora.strftime("%H:%M")
        else:
            hora_formateada = ahora.strftime("%I:%M %p").lower()
        horas.append(hora_formateada)
    return jsonify({'horas': horas})

@app.route('/api/quitar_reloj/<int:indice>', methods=['DELETE'])
def quitar_reloj(indice):
    if 0 <= indice < len(relojes_adicionales):
        relojes_adicionales.pop(indice)
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Índice no válido'}), 400

@app.route('/api/cronometro/iniciar', methods=['POST'])
def cronometro_iniciar():
    cronometro.iniciar()
    return jsonify({'success': True})

@app.route('/api/cronometro/detener', methods=['POST'])
def cronometro_detener():
    cronometro.detener()
    return jsonify({'success': True})

@app.route('/api/cronometro/resetear', methods=['POST'])
def cronometro_resetear():
    cronometro.resetear()
    return jsonify({'success': True})

@app.route('/api/cronometro/estado')
def cronometro_estado():
    return jsonify({'iniciado': cronometro.iniciado})

@app.route('/api/cronometro/tiempo')
def cronometro_tiempo():
    return jsonify({'tiempo': cronometro.obtener_tiempo()})

@app.route('/api/temporizador/configuracion')
def temporizador_configuracion():
    return jsonify(temporizador.obtener_configuracion_actual())

@app.route('/api/temporizador/establecer', methods=['POST'])
def temporizador_establecer():
    data = request.get_json()
    horas = min(max(int(data.get('horas', 0)), 0), 23)
    minutos = min(max(int(data.get('minutos', 0)), 0), 59)
    segundos = min(max(int(data.get('segundos', 0)), 0), 59)

    temporizador.establecer_tiempo(horas, minutos, segundos)
    return jsonify(temporizador.obtener_configuracion_actual())

@app.route('/api/temporizador/iniciar', methods=['POST'])
def temporizador_iniciar():
    # No iniciar si el tiempo es 00:00:00 (solo no hacer nada, sin mensaje)
    tiempo_total_segundos = temporizador.tiempo_restante.total_seconds()
    if tiempo_total_segundos <= 0:
        return jsonify({'success': False})

    temporizador.iniciar()
    return jsonify({'success': True})

@app.route('/api/temporizador/detener', methods=['POST'])
def temporizador_detener():
    temporizador.detener()
    return jsonify({'success': True})

@app.route('/api/temporizador/resetear', methods=['POST'])
def temporizador_resetear():
    temporizador.resetear()
    return jsonify({'success': True})

@app.route('/api/temporizador/tiempo')
def temporizador_tiempo():
    terminado = temporizador.actualizar()
    return jsonify({
        'tiempo': temporizador.obtener_tiempo_restante(),
        'terminado': terminado
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)