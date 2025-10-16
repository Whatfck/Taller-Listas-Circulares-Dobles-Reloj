// Variables globales
let currentView = 'clock';
let clockInterval;
let stopwatchInterval;
let timerInterval;
let additionalClocks = [];

// Elementos DOM
const navTabs = document.querySelectorAll('.nav-tab');
const views = document.querySelectorAll('.view');
const mainClock = document.getElementById('mainClock');
const settingsBtn = document.getElementById('settingsBtn');
const settingsModal = document.getElementById('settingsModal');
const closeSettings = document.getElementById('closeSettings');
const saveSettings = document.getElementById('saveSettings');
const cancelSettings = document.getElementById('cancelSettings');
const addClockBtn = document.getElementById('addClockBtn');
const addClockModal = document.getElementById('addClockModal');
const closeAddClock = document.getElementById('closeAddClock');
const saveAddClock = document.getElementById('saveAddClock');
const cancelAddClock = document.getElementById('cancelAddClock');
const timerFinishedModal = document.getElementById('timerFinishedModal');
const closeTimerFinished = document.getElementById('closeTimerFinished');

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    startClock();
    loadSettings();
    loadTimerConfiguration(); // Cargar configuración inicial del temporizador
});

// Event listeners
function initializeEventListeners() {
    // Navegación
    navTabs.forEach(tab => {
        tab.addEventListener('click', () => switchView(tab.dataset.tab));
    });

    // Configuración
    settingsBtn.addEventListener('click', () => settingsModal.classList.add('show'));
    closeSettings.addEventListener('click', () => settingsModal.classList.remove('show'));
    cancelSettings.addEventListener('click', () => settingsModal.classList.remove('show'));
    saveSettings.addEventListener('click', saveSettingsHandler);

    // Agregar reloj
    addClockBtn.addEventListener('click', () => addClockModal.classList.add('show'));
    closeAddClock.addEventListener('click', () => addClockModal.classList.remove('show'));
    cancelAddClock.addEventListener('click', () => addClockModal.classList.remove('show'));
    saveAddClock.addEventListener('click', addClockHandler);

    // Cronómetro
    document.getElementById('startStopwatch').addEventListener('click', startStopwatch);
    document.getElementById('stopStopwatch').addEventListener('click', stopStopwatch);
    document.getElementById('resetStopwatch').addEventListener('click', resetStopwatch);

    // Temporizador
    document.getElementById('hoursInput').addEventListener('input', updateTimerFromInputs);
    document.getElementById('minutesInput').addEventListener('input', updateTimerFromInputs);
    document.getElementById('secondsInput').addEventListener('input', updateTimerFromInputs);
    document.getElementById('startTimer').addEventListener('click', startTimer);
    document.getElementById('stopTimer').addEventListener('click', stopTimer);
    document.getElementById('resetTimer').addEventListener('click', resetTimer);
    document.getElementById('resetTimerRunning').addEventListener('click', resetTimer);

    // Modal temporizador terminado
    closeTimerFinished.addEventListener('click', () => timerFinishedModal.classList.remove('show'));

    // Tema
    document.getElementById('themeToggle').addEventListener('change', toggleTheme);
}

// Navegación entre vistas
function switchView(viewName) {
    currentView = viewName;

    // Actualizar pestañas
    navTabs.forEach(tab => {
        tab.classList.toggle('active', tab.dataset.tab === viewName);
    });

    // Mostrar vista
    views.forEach(view => {
        view.classList.toggle('active', view.id === `${viewName}-view`);
    });

    // Detener intervalos cuando se cambia de vista
    if (viewName !== 'clock') {
        clearInterval(clockInterval);
    } else {
        startClock();
    }

    if (viewName !== 'stopwatch') {
        clearInterval(stopwatchInterval);
    }

    if (viewName !== 'timer') {
        clearInterval(timerInterval);
    }
}

// Reloj principal
function startClock() {
    updateClock();
    clockInterval = setInterval(updateClock, 1000);
}

function updateClock() {
    fetch('/api/hora_actual')
        .then(response => response.json())
        .then(data => {
            mainClock.textContent = data.hora;
        })
        .catch(error => console.error('Error al actualizar reloj:', error));
}

// Configuración
function loadSettings() {
    const theme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', theme);
    document.getElementById('themeToggle').checked = theme === 'dark';
}

function saveSettingsHandler() {
    const timezone = document.getElementById('timezoneSelect').value;
    const format24h = document.getElementById('formatToggle').checked;
    const darkTheme = document.getElementById('themeToggle').checked;

    fetch('/api/cambiar_configuracion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            zona_horaria: timezone,
            formato_24h: format24h,
            tema_oscuro: darkTheme
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            settingsModal.classList.remove('show');
            if (darkTheme) {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
            }
        }
    })
    .catch(error => console.error('Error al guardar configuración:', error));
}

function toggleTheme() {
    const isDark = document.getElementById('themeToggle').checked;
    const theme = isDark ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}

// Relojes adicionales
function addClockHandler() {
    const timezone = document.getElementById('addTimezoneSelect').value;
    const format24h = document.getElementById('addFormatToggle').checked;

    fetch('/api/agregar_reloj', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            zona_horaria: timezone,
            formato_24h: format24h
        })
    })
    .then(response => response.json())
    .then(data => {
        addClockModal.classList.remove('show');
        renderAdditionalClock(data.hora, timezone, data.indice);
        startAdditionalClocks();
    })
    .catch(error => console.error('Error al agregar reloj:', error));
}

function renderAdditionalClock(hora, zona, indice) {
    const additionalClocksContainer = document.getElementById('additionalClocks');
    const clockElement = document.createElement('div');
    clockElement.className = 'additional-clock';
    clockElement.id = `additional-clock-${indice}`;
    clockElement.innerHTML = `
        <div class="clock-display">${hora}</div>
        <div class="clock-label">${zona.split('/').pop().replace('_', ' ')}</div>
    `;
    additionalClocksContainer.appendChild(clockElement);
    additionalClocks.push({ element: clockElement, zona: zona, indice: indice });
}

function startAdditionalClocks() {
    if (currentView === 'clock') {
        setInterval(updateAdditionalClocks, 1000);
    }
}

function updateAdditionalClocks() {
    fetch('/api/horas_adicionales')
        .then(response => response.json())
        .then(data => {
            additionalClocks.forEach((clock, index) => {
                if (data.horas[index]) {
                    clock.element.querySelector('.clock-display').textContent = data.horas[index];
                }
            });
        })
        .catch(error => console.error('Error al actualizar relojes adicionales:', error));
}

// Cronómetro
function startStopwatch() {
    fetch('/api/cronometro/iniciar', { method: 'POST' })
        .then(() => {
            updateStopwatch();
            stopwatchInterval = setInterval(updateStopwatch, 100);
        })
        .catch(error => console.error('Error al iniciar cronómetro:', error));
}

function stopStopwatch() {
    fetch('/api/cronometro/detener', { method: 'POST' })
        .then(() => {
            clearInterval(stopwatchInterval);
            updateStopwatch(); // Actualizar una vez más para mostrar el tiempo final
        })
        .catch(error => console.error('Error al detener cronómetro:', error));
}

function resetStopwatch() {
    fetch('/api/cronometro/resetear', { method: 'POST' })
        .then(() => {
            document.getElementById('stopwatchDisplay').textContent = '00:00:00.00';
            clearInterval(stopwatchInterval);
        })
        .catch(error => console.error('Error al resetear cronómetro:', error));
}

function updateStopwatch() {
    fetch('/api/cronometro/tiempo')
        .then(response => response.json())
        .then(data => {
            document.getElementById('stopwatchDisplay').textContent = data.tiempo;
        })
        .catch(error => console.error('Error al actualizar cronómetro:', error));
}

// Temporizador
function updateTimerFromInputs() {
    const hours = parseInt(document.getElementById('hoursInput').value) || 0;
    const minutes = parseInt(document.getElementById('minutesInput').value) || 0;
    const seconds = parseInt(document.getElementById('secondsInput').value) || 0;

    // Validar límites
    const validHours = Math.min(Math.max(hours, 0), 23);
    const validMinutes = Math.min(Math.max(minutes, 0), 59);
    const validSeconds = Math.min(Math.max(seconds, 0), 59);

    // Actualizar inputs si se excedieron los límites
    document.getElementById('hoursInput').value = validHours;
    document.getElementById('minutesInput').value = validMinutes;
    document.getElementById('secondsInput').value = validSeconds;

    // Enviar al servidor
    fetch('/api/temporizador/establecer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            horas: validHours,
            minutos: validMinutes,
            segundos: validSeconds
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Temporizador establecido:', data);
    })
    .catch(error => console.error('Error al establecer temporizador:', error));
}

function startTimer() {
    fetch('/api/temporizador/iniciar', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('timerSetup').style.display = 'none';
                document.getElementById('timerRunning').style.display = 'block';
                updateTimer();
                timerInterval = setInterval(updateTimer, 1000); // Cambiar a 1000ms (1 segundo)
            } else {
                alert(data.message || 'No se puede iniciar el temporizador');
            }
        })
        .catch(error => console.error('Error al iniciar temporizador:', error));
}

function stopTimer() {
    fetch('/api/temporizador/detener', { method: 'POST' })
        .then(() => {
            clearInterval(timerInterval);
            updateTimer(); // Actualizar una vez más para mostrar el tiempo restante
        })
        .catch(error => console.error('Error al detener temporizador:', error));
}

function resetTimer() {
    fetch('/api/temporizador/resetear', { method: 'POST' })
        .then(() => {
            clearInterval(timerInterval);
            document.getElementById('timerSetup').style.display = 'block';
            document.getElementById('timerRunning').style.display = 'none';
            loadTimerConfiguration();
        })
        .catch(error => console.error('Error al resetear temporizador:', error));
}

function updateTimer() {
    fetch('/api/temporizador/tiempo')
        .then(response => response.json())
        .then(data => {
            document.getElementById('timerDisplay').textContent = data.tiempo;
            if (data.terminado) {
                clearInterval(timerInterval);
                timerFinishedModal.classList.add('show');
                document.getElementById('timerSetup').style.display = 'block';
                document.getElementById('timerRunning').style.display = 'none';
                loadTimerConfiguration();
            }
        })
        .catch(error => console.error('Error al actualizar temporizador:', error));
}

function loadTimerConfiguration() {
    fetch('/api/temporizador/configuracion')
        .then(response => response.json())
        .then(data => {
            document.getElementById('hoursInput').value = data.horas;
            document.getElementById('minutesInput').value = data.minutos;
            document.getElementById('secondsInput').value = data.segundos;
        })
        .catch(error => console.error('Error al cargar configuración del temporizador:', error));
}