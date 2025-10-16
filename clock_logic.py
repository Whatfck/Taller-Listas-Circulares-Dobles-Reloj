import datetime
import zoneinfo
from circular_list import ListaCircularDoble

class Reloj:
    def __init__(self, zona_horaria='America/Bogota', formato_24h=True):
        self.zona_horaria = zona_horaria
        self.formato_24h = formato_24h
        self.tz = zoneinfo.ZoneInfo(zona_horaria)

    def obtener_hora_actual(self):
        ahora = datetime.datetime.now(self.tz)
        if self.formato_24h:
            return ahora.strftime("%H:%M:%S")
        else:
            return ahora.strftime("%I:%M:%S %p").lower()

class Cronometro:
    def __init__(self):
        self.iniciado = False
        self.tiempo_inicio = None
        self.tiempo_pausado = datetime.timedelta(0)

    def iniciar(self):
        if not self.iniciado:
            self.tiempo_inicio = datetime.datetime.now()
            self.iniciado = True

    def detener(self):
        if self.iniciado:
            self.tiempo_pausado += datetime.datetime.now() - self.tiempo_inicio
            self.iniciado = False

    def resetear(self):
        self.iniciado = False
        self.tiempo_inicio = None
        self.tiempo_pausado = datetime.timedelta(0)

    def obtener_tiempo(self):
        if self.iniciado:
            tiempo_total = self.tiempo_pausado + (datetime.datetime.now() - self.tiempo_inicio)
        else:
            tiempo_total = self.tiempo_pausado

        horas, resto = divmod(int(tiempo_total.total_seconds()), 3600)
        minutos, segundos = divmod(resto, 60)
        centesimas = int((tiempo_total.total_seconds() - int(tiempo_total.total_seconds())) * 100)
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}.{centesimas:02d}"

class Temporizador:
    def __init__(self):
        self.tiempo_restante = datetime.timedelta(0)
        self.iniciado = False
        self.tiempo_inicio = None
        self.horas_lista = ListaCircularDoble(list(range(24)))
        self.minutos_lista = ListaCircularDoble(list(range(60)))
        self.segundos_lista = ListaCircularDoble(list(range(60)))

    def establecer_tiempo(self, horas, minutos, segundos):
        self.tiempo_restante = datetime.timedelta(hours=horas, minutes=minutos, seconds=segundos)

    def iniciar(self):
        if not self.iniciado and self.tiempo_restante > datetime.timedelta(0):
            self.tiempo_inicio = datetime.datetime.now()
            self.iniciado = True

    def detener(self):
        if self.iniciado:
            tiempo_transcurrido = datetime.datetime.now() - self.tiempo_inicio
            self.tiempo_restante -= tiempo_transcurrido
            if self.tiempo_restante < datetime.timedelta(0):
                self.tiempo_restante = datetime.timedelta(0)
            self.iniciado = False

    def resetear(self):
        self.tiempo_restante = datetime.timedelta(0)
        self.iniciado = False
        self.tiempo_inicio = None

    def actualizar(self):
        if self.iniciado:
            tiempo_transcurrido = datetime.datetime.now() - self.tiempo_inicio
            tiempo_restante_actual = self.tiempo_restante - tiempo_transcurrido
            if tiempo_restante_actual <= datetime.timedelta(0):
                self.tiempo_restante = datetime.timedelta(0)
                self.iniciado = False
                return True  # Temporizador terminado
            return False
        return False

    def obtener_tiempo_restante(self):
        if self.iniciado:
            tiempo_transcurrido = datetime.datetime.now() - self.tiempo_inicio
            tiempo_restante_actual = self.tiempo_restante - tiempo_transcurrido
            if tiempo_restante_actual < datetime.timedelta(0):
                tiempo_restante_actual = datetime.timedelta(0)
        else:
            tiempo_restante_actual = self.tiempo_restante

        total_segundos = int(tiempo_restante_actual.total_seconds())
        horas, resto = divmod(total_segundos, 3600)
        minutos, segundos = divmod(resto, 60)
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    def ajustar_horas(self, direccion):
        if direccion == 'up':
            self.horas_lista.avanzar()
        elif direccion == 'down':
            self.horas_lista.retroceder()
        horas = self.horas_lista.obtener_actual()
        minutos = self.minutos_lista.obtener_actual()
        segundos = self.segundos_lista.obtener_actual()
        self.establecer_tiempo(horas, minutos, segundos)

    def ajustar_minutos(self, direccion):
        if direccion == 'up':
            self.minutos_lista.avanzar()
        elif direccion == 'down':
            self.minutos_lista.retroceder()
        horas = self.horas_lista.obtener_actual()
        minutos = self.minutos_lista.obtener_actual()
        segundos = self.segundos_lista.obtener_actual()
        self.establecer_tiempo(horas, minutos, segundos)

    def ajustar_segundos(self, direccion):
        if direccion == 'up':
            self.segundos_lista.avanzar()
        elif direccion == 'down':
            self.segundos_lista.retroceder()
        horas = self.horas_lista.obtener_actual()
        minutos = self.minutos_lista.obtener_actual()
        segundos = self.segundos_lista.obtener_actual()
        self.establecer_tiempo(horas, minutos, segundos)

    def obtener_configuracion_actual(self):
        return {
            'horas': self.horas_lista.obtener_actual(),
            'minutos': self.minutos_lista.obtener_actual(),
            'segundos': self.segundos_lista.obtener_actual()
        }