import React, { useState, useEffect } from 'react';
import { motion, useMotionValue, useSpring, useTransform } from 'framer-motion';

const KalmiyaInteractiveAvatar = ({ message, onMessageRead }) => {
  const [isScanning, setIsScanning] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  // Mouse position values for 3D tilt
  const x = useMotionValue(0);
  const y = useMotionValue(0);

  // Smooth springs for the 3D tilt
  const springConfig = { damping: 20, stiffness: 300 };
  const rotateX = useSpring(useTransform(y, [-0.5, 0.5], [15, -15]), springConfig);
  const rotateY = useSpring(useTransform(x, [-0.5, 0.5], [-15, 15]), springConfig);

  const handleMouseMove = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const width = rect.width;
    const height = rect.height;
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;
    
    // Normalize to -0.5 to 0.5
    const xPct = mouseX / width - 0.5;
    const yPct = mouseY / height - 0.5;
    
    x.set(xPct);
    y.set(yPct);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    x.set(0);
    y.set(0);
  };

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  const handleClick = () => {
    setIsScanning(true);
    setTimeout(() => setIsScanning(false), 2000); // Scan lasts 2s
  };

  // Handle Speech Synthesis
  useEffect(() => {
    if (message) {
      window.speechSynthesis.cancel(); // Clear previous speech
      setIsSpeaking(true);
      
      const utterance = new SpeechSynthesisUtterance(message);
      utterance.lang = 'es-ES'; // Spanish voice
      utterance.rate = 1.0;
      utterance.pitch = 1.2;
      
      // Try to get a specific Spanish voice if available
      const voices = window.speechSynthesis.getVoices();
      const spanishVoice = voices.find(v => v.lang.includes('es'));
      if (spanishVoice) {
        utterance.voice = spanishVoice;
      }

      utterance.onend = () => {
        setIsSpeaking(false);
        if (onMessageRead) onMessageRead();
      };
      
      utterance.onerror = (e) => {
        console.warn("Speech synthesis error:", e);
        setIsSpeaking(false);
        if (onMessageRead) onMessageRead();
      };

      window.speechSynthesis.speak(utterance);
      
      return () => {
        window.speechSynthesis.cancel();
      };
    }
  }, [message, onMessageRead]);

  return (
    <div className="interactive-avatar-wrapper" onClick={handleClick}>
      <motion.div 
        className="avatar-3d-container"
        onMouseMove={handleMouseMove}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        style={{
          rotateX,
          rotateY,
          transformStyle: "preserve-3d"
        }}
      >
        <div className={`avatar-glow-container avatar-animate ${isSpeaking ? 'speaking' : ''}`}>
          <img src="/kalmiya_full.png" alt="KALMIYA Avatar" className="kalmiya-avatar" />
          
          {/* Laser Scan Effect */}
          {(isScanning || isSpeaking) && <div className="laser-scan"></div>}
          
          {/* Audio/Speaking Rings (Always active, faster when speaking) */}
          <div className={`audio-ring ring-1 ${isSpeaking ? 'speaking-ring' : ''}`}></div>
          <div className={`audio-ring ring-2 ${isSpeaking ? 'speaking-ring' : ''}`}></div>
        </div>
      </motion.div>
    </div>
  );
};

export default KalmiyaInteractiveAvatar;
