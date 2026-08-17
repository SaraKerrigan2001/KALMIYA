// KALMIYA Reactive Neural Interface Engine
let ws = null;
let voiceEnabled = true;

const orb = document.getElementById('neuralOrb');
const coreLabel = document.getElementById('coreLabel');
const statePill = document.getElementById('statePill');
const connStatus = document.getElementById('connStatus');
const auditFeed = document.getElementById('auditFeed');
const messagesContainer = document.getElementById('messagesContainer');
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const voiceToggle = document.getElementById('voiceToggle');
const clearChatBtn = document.getElementById('clearChat');

// Connect WebSocket
function initWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;

    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        connStatus.textContent = '● CONECTADO';
        connStatus.style.color = 'var(--green)';
        connStatus.style.borderColor = 'rgba(6, 214, 160, 0.3)';
        addAudit('Enlace neural WebSocket establecido.', 'info');
    };

    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            handleIncomingEvent(data);
        } catch (e) {
            console.error('Error parsing WS message:', e);
        }
    };

    ws.onclose = () => {
        connStatus.textContent = '○ DESCONECTADO (Reintentando...)';
        connStatus.style.color = 'var(--red)';
        connStatus.style.borderColor = 'rgba(239, 71, 111, 0.3)';
        setOrbState('idle');
        setTimeout(initWebSocket, 3000);
    };

    ws.onerror = (err) => {
        console.error('WS Error:', err);
    };
}

// Handle Incoming Server Events
function handleIncomingEvent(data) {
    if (data.type === 'state_change') {
        const status = data.state.status || 'idle';
        setOrbState(status, data.state.last_tool);
    } else if (data.type === 'response') {
        renderMessage(data.text, 'assistant');
        setOrbState('idle');
        if (voiceEnabled) {
            speakResponse(data.text);
        }
    }
}

// Dynamic State Controller
function setOrbState(state, toolName = null) {
    orb.className = 'neural-orb';
    
    switch (state) {
        case 'thinking':
            orb.classList.add('state-thinking');
            coreLabel.textContent = 'NEURAL CORE: PROCESANDO';
            coreLabel.style.color = 'var(--purple)';
            statePill.textContent = 'MODO: PENSANDO';
            statePill.className = 'status-pill state-pill highlight-purple';
            break;
            
        case 'tool_execution':
            orb.classList.add('state-tool');
            coreLabel.textContent = `EJECUTANDO: ${toolName || 'TOOL'}`;
            coreLabel.style.color = 'var(--gold)';
            statePill.textContent = `HERRAMIENTA: ${toolName || 'ACTIVA'}`;
            statePill.className = 'status-pill state-pill highlight-gold';
            addAudit(`Tool Call ejecutado: [${toolName}]`, 'tool');
            break;
            
        case 'speaking':
            orb.classList.add('state-speaking');
            coreLabel.textContent = 'NEURAL CORE: TRANSMITIENDO';
            coreLabel.style.color = 'var(--green)';
            statePill.textContent = 'MODO: HABLANDO';
            statePill.className = 'status-pill state-pill highlight-green';
            break;
            
        case 'idle':
        default:
            orb.classList.add('state-idle');
            coreLabel.textContent = 'NEURAL CORE: IDLE';
            coreLabel.style.color = 'var(--cyan)';
            statePill.textContent = 'MODO: ESPERA';
            statePill.className = 'status-pill state-pill';
            break;
    }
}

// Add Audit Item
function addAudit(text, type = 'info') {
    const item = document.createElement('div');
    item.className = `audit-item ${type}`;
    const time = new Date().toLocaleTimeString();
    item.textContent = `[${time}] ${text}`;
    auditFeed.appendChild(item);
    auditFeed.scrollTop = auditFeed.scrollHeight;
}

// Render Messages
function renderMessage(text, role = 'user') {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = role === 'assistant' ? 'K' : 'S';
    
    const content = document.createElement('div');
    content.className = 'msg-content';
    
    const header = document.createElement('div');
    header.className = 'msg-header';
    header.textContent = role === 'assistant' ? 'KALMIYA Neural System' : 'Sara (Tú)';
    
    const body = document.createElement('div');
    body.className = 'msg-body';
    
    if (role === 'assistant' && window.marked) {
        body.innerHTML = marked.parse(text);
    } else {
        body.textContent = text;
    }
    
    content.appendChild(header);
    content.appendChild(body);
    msgDiv.appendChild(avatar);
    msgDiv.appendChild(content);
    
    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Send Message
function sendMessage(text) {
    if (!text || !ws || ws.readyState !== WebSocket.OPEN) return;
    
    renderMessage(text, 'user');
    setOrbState('thinking');
    ws.send(JSON.stringify({ text }));
    userInput.value = '';
}

// Speech Synthesis (TTS Feedback)
function speakResponse(text) {
    if (!('speechSynthesis' in window)) return;
    
    window.speechSynthesis.cancel();
    
    // Clean text for speech
    const cleanText = text.replace(/[*_#`\[\]]/g, '').slice(0, 300);
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = 'es-ES';
    utterance.rate = 1.05;
    utterance.pitch = 1.0;

    utterance.onstart = () => {
        setOrbState('speaking');
    };

    utterance.onend = () => {
        setOrbState('idle');
    };

    window.speechSynthesis.speak(utterance);
}

// Event Listeners
chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    sendMessage(userInput.value.trim());
});

voiceToggle.addEventListener('click', () => {
    voiceEnabled = !voiceEnabled;
    voiceToggle.classList.toggle('active', voiceEnabled);
    voiceToggle.textContent = voiceEnabled ? '🔊 TTS Activado' : '🔇 TTS Silenciado';
    if (!voiceEnabled && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        setOrbState('idle');
    }
});

clearChatBtn.addEventListener('click', () => {
    messagesContainer.innerHTML = '';
    addAudit('Terminal de conversación limpiada.', 'info');
});

// Quick Prompts Helper
window.sendQuickPrompt = function(promptText) {
    sendMessage(promptText);
};

// Initialize on Load
window.addEventListener('DOMContentLoaded', () => {
    initWebSocket();
});
