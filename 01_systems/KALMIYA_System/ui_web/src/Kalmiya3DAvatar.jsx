import React, { useRef, useEffect, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { useGLTF, useAnimations, Environment, ContactShadows, OrbitControls } from '@react-three/drei';
import * as THREE from 'three';

// 3D Model Component
const KalmiyaModel = ({ textToSpeak, onFinishedSpeaking }) => {
  const group = useRef();
  // Load the animated GLB model
  const { scene, animations } = useGLTF('/kalmiya_avatar.glb');
  const { actions } = useAnimations(animations, group);
  const [isSpeaking, setIsSpeaking] = useState(false);

  // Apply Purple Hologram Material
  useEffect(() => {
    if (scene) {
      scene.traverse((child) => {
        if (child.isMesh) {
          child.material = new THREE.MeshStandardMaterial({
            color: new THREE.Color(0x8b5cf6), // Purple color
            emissive: new THREE.Color(0x6366f1), // Glowing indigo
            emissiveIntensity: 0.5,
            roughness: 0.2,
            metalness: 0.8,
            transparent: true,
            opacity: 0.9,
          });
        }
      });
    }
  }, [scene]);

  // Play Animation
  useEffect(() => {
    if (actions && Object.keys(actions).length > 0) {
      const actionName = Object.keys(actions)[0];
      actions[actionName].reset().fadeIn(0.5).play();
    }
  }, [actions]);

  // Handle Speech
  useEffect(() => {
    if (textToSpeak) {
      window.speechSynthesis.cancel(); // Clear previous speech
      setIsSpeaking(true);
      
      const utterance = new SpeechSynthesisUtterance(textToSpeak);
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
        if (onFinishedSpeaking) onFinishedSpeaking();
      };
      
      utterance.onerror = (e) => {
        console.warn("Speech synthesis error:", e);
        setIsSpeaking(false);
        if (onFinishedSpeaking) onFinishedSpeaking();
      };

      window.speechSynthesis.speak(utterance);
      
      return () => {
        window.speechSynthesis.cancel();
      };
    }
  }, [textToSpeak, onFinishedSpeaking]);

  // Floating & Speaking animation
  useFrame((state) => {
    const t = state.clock.getElapsedTime();
    if (group.current) {
      // Gentle floating up and down (centered at y = -1)
      group.current.position.y = -1 + (Math.sin(t) * 0.2);
      
      // Gentle swaying rotation so she feels alive
      group.current.rotation.y = Math.sin(t / 2) * 0.1;
      group.current.rotation.x = Math.sin(t / 3) * 0.05;
      
      // If speaking, add a slight pulsing to simulate energy/talking
      if (isSpeaking) {
        const pulse = 1 + (Math.sin(t * 15) * 0.03);
        group.current.scale.set(pulse, pulse, pulse);
      } else {
        // Smooth return to scale 1
        group.current.scale.lerp(new THREE.Vector3(1, 1, 1), 0.1);
      }
    }
  });

  return (
    <group ref={group} dispose={null}>
      {/* Scale might need adjustment for the new GLB */}
      <primitive object={scene} scale={2.5} position={[0, -1, 0]} />
    </group>
  );
};

useGLTF.preload('/kalmiya_avatar.glb');

// Main Canvas Component wrapper
const Kalmiya3DAvatar = ({ message, onMessageRead }) => {
  return (
    <div className="canvas-3d-wrapper" style={{ width: '100%', height: '100vh', position: 'absolute', top: 0, left: 0 }}>
      {/* Camera setup */}
      <Canvas camera={{ position: [0, 1, 5], fov: 40 }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[-5, 5, 5]} intensity={1} castShadow />
        <pointLight position={[0, 2, 2]} intensity={2} color="#6366f1" />
        
        {/* Adds a nice studio/cyberpunk environment reflection */}
        <Environment preset="city" />
        
        <KalmiyaModel textToSpeak={message} onFinishedSpeaking={onMessageRead} />
        
        <ContactShadows position={[0, -0.5, 0]} opacity={0.5} scale={10} blur={2} far={4} />
        
        <OrbitControls 
          enableZoom={true} 
          enablePan={false}
          autoRotate={true}
          autoRotateSpeed={1.5}
          target={[0, 0.5, 0]} 
          minPolarAngle={Math.PI / 3} 
          maxPolarAngle={Math.PI / 1.8} 
        />
      </Canvas>
    </div>
  );
};

export default Kalmiya3DAvatar;
