# CircularTime - Reloj Digital con Listas Circulares Dobles

## Descripción

Este proyecto es una aplicación web completa de reloj digital desarrollada en Python utilizando Flask y listas circulares dobles. La aplicación ofrece una interfaz moderna y estética con funcionalidades avanzadas de gestión del tiempo.

## Características Principales

### 🕐 Reloj Digital
- **Reloj principal**: Muestra la hora local según la zona horaria configurada (por defecto GMT-5, Bogotá)
- **Múltiples zonas horarias**: Posibilidad de añadir relojes adicionales con diferentes zonas horarias
- **Formato configurable**: Soporte para formato 12H y 24H
- **Actualización en tiempo real**: Los relojes se actualizan automáticamente cada segundo

### ⏱️ Cronómetro
- Funcionalidad completa de cronómetro con precisión de centésimas de segundo
- Controles de iniciar, detener y resetear
- Visualización clara del tiempo transcurrido

### ⏳ Temporizador
- **Selector interactivo**: Ajuste visual de tiempo con flechas arriba/abajo
- **Controles intuitivos**: Botones con iconos SVG (play verde, stop rojo, reset naranja)
- **Transición automática**: Cambia de modo configuración a ejecución al iniciar
- **Alerta visual**: Modal Material Design cuando el temporizador llega a cero

### ⚙️ Configuración Avanzada
- **Zona horaria**: Selección entre múltiples zonas horarias predefinidas
- **Formato de hora**: Alternancia entre 12H y 24H
- **Tema visual**: Interruptor Material Design para alternar entre modo claro y oscuro

## Tecnologías Utilizadas

- **Backend**: Python 3 con Flask (solo librerías estándar)
- **Frontend**: HTML5, CSS3 con Material Design, JavaScript vanilla
- **Estructuras de datos**: Listas circulares dobles personalizadas
- **Gestión de tiempo**: Módulo `datetime` y `zoneinfo` de Python
- **Diseño**: Material Design 3 con temas claro y oscuro

## Estructura del Proyecto

```
Taller-Listas-Circulares-Dobles-Reloj/
├── app.py                 # Aplicación principal Flask
├── circular_list.py       # Implementación de ListaCircularDoble
├── clock_logic.py         # Lógica de relojes, cronómetro y temporizador
├── templates/
│   └── index.html         # Plantilla principal HTML
├── static/
│   ├── styles.css         # Estilos CSS con temas claro/oscuro
│   └── script.js          # JavaScript para funcionalidad frontend
└── README.md              # Este archivo
```

## Instalación y Ejecución

### Prerrequisitos
- Python 3.9 o superior (para soporte completo de `zoneinfo`)

### Pasos de Instalación
1. Clona el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd Taller-Listas-Circulares-Dobles-Reloj
   ```

2. Ejecuta la aplicación:
   ```bash
   python3 app.py
   ```

3. Abre tu navegador y ve a `http://127.0.0.1:5001`

## Uso de la Aplicación

### Navegación
- Utiliza la barra de navegación horizontal para cambiar entre las vistas: Reloj, Cronómetro y Temporizador

### Configuración
- Haz clic en el icono de engranaje (⚙️) en la esquina superior derecha para acceder al formulario de configuración
- Configura la zona horaria, formato de hora y tema visual según tus preferencias

### Gestión de Relojes
- En la vista de Reloj, puedes añadir nuevos relojes con diferentes zonas horarias usando el botón "Agregar Reloj"
- Cada reloj muestra la hora en tiempo real para su zona configurada

### Cronómetro y Temporizador
- Utiliza los botones de control para iniciar, detener y resetear estas funciones
- Para el temporizador, establece primero el tiempo deseado antes de iniciarlo

## Implementación Técnica

### Lista Circular Doble
La clase `ListaCircularDoble` implementa una estructura de datos circular que permite:
- Avanzar y retroceder en el ciclo de valores (0-23 para horas, 0-59 para minutos/segundos)
- Obtener el valor actual
- Establecer un valor específico
- Representación circular perfecta para mediciones temporales

### Gestión de Zonas Horarias
- Utiliza el módulo `zoneinfo` de Python para manejo preciso de zonas horarias
- Soporte para zonas horarias de todo el mundo
- Actualización automática considerando cambios de horario de verano

### Interfaz de Usuario
- **Material Design 3**: Implementación completa de las directrices de Material Design
- **Componentes Material**: Botones, tarjetas, modales y switches siguiendo las especificaciones de Material Design
- **Elevación y sombras**: Sistema de elevación con sombras realistas
- **Responsive design**: Adaptable a dispositivos móviles y tablets
- **Transiciones suaves**: Animaciones y efectos de Material Design
- **Tema dinámico**: Modo claro y oscuro con persistencia en localStorage

## Requisitos del Taller

Este proyecto cumple con todos los requisitos especificados:
- ✅ Desarrollo exclusivamente en Python (Flask)
- ✅ Uso de listas circulares dobles
- ✅ Interfaz web estética
- ✅ Funcionalidad de reloj digital
- ✅ Cronómetro y temporizador
- ✅ Configuración de zona horaria y formato 12H/24H
- ✅ Posibilidad de añadir múltiples relojes
- ✅ Formato HORA:MINUTOS
- ✅ Sin librerías externas (solo estándar de Python)

## Contribución

Este proyecto fue desarrollado como parte de un taller académico. Para modificaciones o mejoras, asegúrate de mantener la integridad de la implementación con listas circulares dobles y el uso exclusivo de librerías estándar de Python.
