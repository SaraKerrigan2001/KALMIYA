import React, { useState } from 'react'
import Kalmiya3DAvatar from './Kalmiya3DAvatar'
import './index.css'

function App() {
  const [inputValue, setInputValue] = useState('');
  const [avatarMessage, setAvatarMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    setAvatarMessage(`Procesando solicitud: ${inputValue}`);
    setInputValue('');
  };

  return (
    <>
      {/* Background Orbs */}
      <div className="bg-orbs">
        <div className="orb orb-1"></div>
        <div className="orb orb-2"></div>
        <div className="orb orb-3"></div>
      </div>

      {/* 3D Interactive Avatar Layer */}
      <Kalmiya3DAvatar 
        message={avatarMessage} 
        onMessageRead={() => setAvatarMessage('')} 
      />

      {/* Chat Interface Overlay */}
      <div className="chat-overlay">
        <div className="chat-glass-panel">
          <form onSubmit={handleSubmit} className="chat-form">
            <input 
              type="text" 
              className="chat-input" 
              placeholder="Habla con KALMIYA..." 
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
            />
            <button type="submit" className="chat-submit-btn">ENVIAR</button>
          </form>
        </div>
      </div>
    </>
  )
}

export default App
