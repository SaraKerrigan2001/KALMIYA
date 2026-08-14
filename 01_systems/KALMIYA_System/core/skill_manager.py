"""
KALMIYA Skill Manager v3.6
Sistema de gestión centralizada de skills con configuración dinámica
Permite habilitar/deshabilitar skills y personalizar su comportamiento
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, time
import schedule
import threading
import time as time_module

class SkillManager:
    """
    Gestor centralizado de skills JARVIS OS
    Lee configuración desde .skills/config.yml y ejecuta skills según schedule
    """
    
    def __init__(self, config_path: str = None):
        """
        Inicializa el gestor de skills
        
        Args:
            config_path: Ruta al archivo config.yml
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent.parent / ".skills" / "config.yml"
        
        self.config_path = Path(config_path)
        self.config = {}
        self.skills = {}
        self.scheduler_thread = None
        self.is_running = False
        self.focus_mode_active = False
        
        self.load_config()
        print(f"✅ Skill Manager inicializado")
        print(f"📁 Config: {self.config_path}")
    
    def load_config(self):
        """Carga configuración desde YAML"""
        if not self.config_path.exists():
            print(f"⚠️  Config no encontrado: {self.config_path}")
            return False
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            
            print(f"✅ Configuración cargada")
            return True
        except Exception as e:
            print(f"⚠️  Error cargando config: {e}")
            return False
    
    def reload_config(self):
        """Recarga configuración en caliente"""
        print("🔄 Recargando configuración...")
        return self.load_config()
    
    def is_skill_enabled(self, skill_name: str) -> bool:
        """
        Verifica si un skill está habilitado
        
        Args:
            skill_name: Nombre del skill
            
        Returns:
            True si está habilitado
        """
        if skill_name not in self.config:
            return False
        
        skill_config = self.config.get(skill_name, {})
        return skill_config.get('enabled', False)
    
    def get_skill_config(self, skill_name: str) -> Dict:
        """
        Obtiene configuración de un skill
        
        Args:
            skill_name: Nombre del skill
            
        Returns:
            Diccionario de configuración
        """
        return self.config.get(skill_name, {})
    
    def enable_skill(self, skill_name: str):
        """Habilita un skill"""
        if skill_name in self.config:
            self.config[skill_name]['enabled'] = True
            self._save_config()
            print(f"✅ Skill habilitado: {skill_name}")
    
    def disable_skill(self, skill_name: str):
        """Deshabilita un skill"""
        if skill_name in self.config:
            self.config[skill_name]['enabled'] = False
            self._save_config()
            print(f"⏸️  Skill deshabilitado: {skill_name}")
    
    def _save_config(self):
        """Guarda configuración actual al archivo YAML"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            print("💾 Configuración guardada")
        except Exception as e:
            print(f"⚠️  Error guardando config: {e}")
    
    def is_quiet_hours(self) -> bool:
        """Verifica si estamos en horas silenciosas"""
        global_config = self.config.get('global', {})
        quiet_hours = global_config.get('quiet_hours', {})
        
        if not quiet_hours.get('enabled', False):
            return False
        
        now = datetime.now().time()
        start = time.fromisoformat(quiet_hours.get('start', '22:00'))
        end = time.fromisoformat(quiet_hours.get('end', '07:00'))
        
        if start < end:
            return start <= now <= end
        else:  # Cruza medianoche
            return now >= start or now <= end
    
    def enable_focus_mode(self, duration_minutes: int = 90):
        """
        Activa modo focus
        
        Args:
            duration_minutes: Duración en minutos
        """
        self.focus_mode_active = True
        focus_config = self.config.get('focus_mode', {})
        
        # Pausar skills según configuración
        skills_to_pause = focus_config.get('pause_skills', [])
        for skill in skills_to_pause:
            print(f"⏸️  Pausando skill: {skill}")
        
        print(f"🎯 MODO FOCUS ACTIVADO ({duration_minutes} minutos)")
        
        # Programar desactivación
        def disable_after_duration():
            time_module.sleep(duration_minutes * 60)
            self.disable_focus_mode()
        
        threading.Thread(target=disable_after_duration, daemon=True).start()
    
    def disable_focus_mode(self):
        """Desactiva modo focus"""
        self.focus_mode_active = False
        print("✅ Modo focus desactivado")
    
    def schedule_skills(self):
        """Programa ejecución automática de skills"""
        schedule.clear()
        
        for skill_name, skill_config in self.config.items():
            if skill_name in ['global', 'integrations', 'notifications', 'focus_mode', 'backup', 'logging']:
                continue
            
            if not skill_config.get('enabled', False):
                continue
            
            schedule_time = skill_config.get('schedule')
            
            if schedule_time and schedule_time not in ['manual', 'continuous']:
                # Programar skill
                schedule.every().day.at(schedule_time).do(
                    self._execute_skill, skill_name
                )
                print(f"📅 Programado: {skill_name} a las {schedule_time}")
    
    def _execute_skill(self, skill_name: str):
        """
        Ejecuta un skill
        
        Args:
            skill_name: Nombre del skill a ejecutar
        """
        # Verificar condiciones
        if self.focus_mode_active:
            focus_config = self.config.get('focus_mode', {})
            if skill_name in focus_config.get('pause_skills', []):
                print(f"⏸️  Skill pausado por modo focus: {skill_name}")
                return
        
        if self.is_quiet_hours():
            print(f"🌙 Skill omitido (horas silenciosas): {skill_name}")
            return
        
        print(f"▶️  Ejecutando skill: {skill_name}")
        
        # Aquí iría la lógica de ejecución real del skill
        # Por ahora solo registramos la ejecución
        
        # TODO: Importar y ejecutar el módulo del skill correspondiente
        
    def start_scheduler(self):
        """Inicia el scheduler en background"""
        if self.is_running:
            print("⚠️  Scheduler ya está corriendo")
            return
        
        self.is_running = True
        self.schedule_skills()
        
        def run_scheduler():
            while self.is_running:
                schedule.run_pending()
                time_module.sleep(60)  # Verificar cada minuto
        
        self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        print("✅ Scheduler iniciado")
    
    def stop_scheduler(self):
        """Detiene el scheduler"""
        self.is_running = False
        print("⏹️  Scheduler detenido")
    
    def get_status(self) -> Dict:
        """Obtiene estado actual del skill manager"""
        enabled_skills = [name for name, config in self.config.items() 
                         if isinstance(config, dict) and config.get('enabled', False)]
        
        return {
            'scheduler_running': self.is_running,
            'focus_mode_active': self.focus_mode_active,
            'quiet_hours': self.is_quiet_hours(),
            'enabled_skills': enabled_skills,
            'total_skills': len([k for k in self.config.keys() 
                                if k not in ['global', 'integrations', 'notifications', 
                                           'focus_mode', 'backup', 'logging']])
        }


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         KALMIYA SKILL MANAGER v3.6 - DEMO                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    manager = SkillManager()
    
    # Mostrar status
    status = manager.get_status()
    print("\n📊 Estado actual:")
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # Mostrar skills habilitados
    print("\n✅ Skills habilitados:")
    for skill in status['enabled_skills']:
        config = manager.get_skill_config(skill)
        schedule_time = config.get('schedule', 'manual')
        print(f"   • {skill}: {schedule_time}")
    
    # Iniciar scheduler (comentado para demo)
    # manager.start_scheduler()
