"""
KALMIYA Plugin Manager v3.6
Sistema modular de plugins con hot-reload
Permite extender KALMIYA sin modificar el core
"""

import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Dict, List, Optional, Callable
import json
from datetime import datetime

class Plugin:
    """Clase base para plugins de KALMIYA"""
    
    def __init__(self):
        self.name = "BasePlugin"
        self.version = "1.0.0"
        self.author = "Unknown"
        self.description = "Plugin base"
        self.enabled = True
    
    def on_load(self):
        """Llamado cuando el plugin se carga"""
        pass
    
    def on_unload(self):
        """Llamado cuando el plugin se descarga"""
        pass
    
    def on_command(self, command: str, args: List[str]) -> Optional[str]:
        """
        Maneja un comando
        
        Args:
            command: Nombre del comando
            args: Argumentos del comando
            
        Returns:
            Respuesta del comando o None
        """
        return None


class PluginManager:
    """
    Gestor de plugins para KALMIYA
    Carga, descarga, y maneja hot-reload de plugins
    """
    
    def __init__(self, plugins_dir: str = None):
        """
        Inicializa el gestor de plugins
        
        Args:
            plugins_dir: Directorio de plugins
        """
        if plugins_dir is None:
            plugins_dir = Path(__file__).parent.parent.parent.parent / ".plugins"
        
        self.plugins_dir = Path(plugins_dir)
        self.plugins_dir.mkdir(exist_ok=True)
        
        self.loaded_plugins: Dict[str, Plugin] = {}
        self.plugin_modules: Dict[str, object] = {}
        self.plugin_metadata: Dict[str, dict] = {}
        
        print(f"🔌 Plugin Manager inicializado")
        print(f"📁 Plugins dir: {self.plugins_dir}")
    
    def discover_plugins(self) -> List[str]:
        """
        Descubre plugins disponibles
        
        Returns:
            Lista de nombres de plugins
        """
        plugins = []
        
        for plugin_dir in self.plugins_dir.iterdir():
            if not plugin_dir.is_dir():
                continue
            
            # Buscar plugin.py o __init__.py
            plugin_file = plugin_dir / "plugin.py"
            if not plugin_file.exists():
                plugin_file = plugin_dir / "__init__.py"
            
            if plugin_file.exists():
                plugins.append(plugin_dir.name)
        
        return plugins
    
    def load_plugin(self, plugin_name: str) -> bool:
        """
        Carga un plugin
        
        Args:
            plugin_name: Nombre del plugin
            
        Returns:
            True si se cargó exitosamente
        """
        if plugin_name in self.loaded_plugins:
            print(f"⚠️  Plugin ya cargado: {plugin_name}")
            return False
        
        plugin_path = self.plugins_dir / plugin_name
        
        if not plugin_path.exists():
            print(f"❌ Plugin no encontrado: {plugin_name}")
            return False
        
        try:
            # Buscar archivo del plugin
            plugin_file = plugin_path / "plugin.py"
            if not plugin_file.exists():
                plugin_file = plugin_path / "__init__.py"
            
            # Cargar módulo
            spec = importlib.util.spec_from_file_location(
                f"kalmiya.plugins.{plugin_name}",
                plugin_file
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            
            # Buscar clase Plugin
            plugin_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, Plugin) and attr != Plugin:
                    plugin_class = attr
                    break
            
            if not plugin_class:
                print(f"❌ No se encontró clase Plugin en {plugin_name}")
                return False
            
            # Instanciar plugin
            plugin_instance = plugin_class()
            
            # Cargar metadata
            metadata_file = plugin_path / "plugin.json"
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    self.plugin_metadata[plugin_name] = json.load(f)
            
            # Guardar plugin
            self.loaded_plugins[plugin_name] = plugin_instance
            self.plugin_modules[plugin_name] = module
            
            # Llamar on_load
            plugin_instance.on_load()
            
            print(f"✅ Plugin cargado: {plugin_name} v{plugin_instance.version}")
            return True
            
        except Exception as e:
            print(f"❌ Error cargando plugin {plugin_name}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """
        Descarga un plugin
        
        Args:
            plugin_name: Nombre del plugin
            
        Returns:
            True si se descargó exitosamente
        """
        if plugin_name not in self.loaded_plugins:
            print(f"⚠️  Plugin no está cargado: {plugin_name}")
            return False
        
        try:
            # Llamar on_unload
            plugin = self.loaded_plugins[plugin_name]
            plugin.on_unload()
            
            # Eliminar del registro
            del self.loaded_plugins[plugin_name]
            if plugin_name in self.plugin_modules:
                del self.plugin_modules[plugin_name]
            if plugin_name in self.plugin_metadata:
                del self.plugin_metadata[plugin_name]
            
            print(f"✅ Plugin descargado: {plugin_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error descargando plugin {plugin_name}: {e}")
            return False
    
    def reload_plugin(self, plugin_name: str) -> bool:
        """
        Recarga un plugin (hot-reload)
        
        Args:
            plugin_name: Nombre del plugin
            
        Returns:
            True si se recargó exitosamente
        """
        print(f"🔄 Recargando plugin: {plugin_name}")
        
        was_loaded = plugin_name in self.loaded_plugins
        
        if was_loaded:
            self.unload_plugin(plugin_name)
        
        return self.load_plugin(plugin_name)
    
    def load_all_plugins(self):
        """Carga todos los plugins disponibles"""
        plugins = self.discover_plugins()
        print(f"\n🔍 Plugins encontrados: {len(plugins)}")
        
        for plugin_name in plugins:
            self.load_plugin(plugin_name)
    
    def get_plugin(self, plugin_name: str) -> Optional[Plugin]:
        """
        Obtiene una instancia de plugin
        
        Args:
            plugin_name: Nombre del plugin
            
        Returns:
            Instancia del plugin o None
        """
        return self.loaded_plugins.get(plugin_name)
    
    def execute_command(self, command: str, args: List[str] = None) -> Optional[str]:
        """
        Ejecuta un comando en todos los plugins
        
        Args:
            command: Nombre del comando
            args: Argumentos del comando
            
        Returns:
            Primera respuesta no-None de los plugins
        """
        if args is None:
            args = []
        
        for plugin_name, plugin in self.loaded_plugins.items():
            if not plugin.enabled:
                continue
            
            try:
                response = plugin.on_command(command, args)
                if response:
                    return response
            except Exception as e:
                print(f"⚠️  Error en plugin {plugin_name}: {e}")
        
        return None
    
    def get_loaded_plugins(self) -> List[str]:
        """Obtiene lista de plugins cargados"""
        return list(self.loaded_plugins.keys())
    
    def get_plugin_info(self, plugin_name: str) -> Optional[dict]:
        """
        Obtiene información de un plugin
        
        Args:
            plugin_name: Nombre del plugin
            
        Returns:
            Diccionario con información
        """
        if plugin_name not in self.loaded_plugins:
            return None
        
        plugin = self.loaded_plugins[plugin_name]
        metadata = self.plugin_metadata.get(plugin_name, {})
        
        return {
            'name': plugin.name,
            'version': plugin.version,
            'author': plugin.author,
            'description': plugin.description,
            'enabled': plugin.enabled,
            'metadata': metadata
        }


# Crear ejemplo de plugin

EXAMPLE_PLUGIN_CODE = """
from core.plugin_manager import Plugin

class WeatherPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = "Weather"
        self.version = "1.0.0"
        self.author = "KALMIYA Team"
        self.description = "Obtiene información del clima"
    
    def on_load(self):
        print("🌤️  Weather Plugin cargado")
    
    def on_unload(self):
        print("👋 Weather Plugin descargado")
    
    def on_command(self, command: str, args: list):
        if command == "weather":
            city = args[0] if args else "Medellín"
            return f"El clima en {city}: Soleado, 24°C"
        return None
"""

if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         KALMIYA PLUGIN MANAGER v3.6 - DEMO                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    manager = PluginManager()
    
    # Descubrir plugins
    plugins = manager.discover_plugins()
    print(f"\n📦 Plugins disponibles: {plugins}")
    
    # Cargar todos
    manager.load_all_plugins()
    
    # Mostrar cargados
    loaded = manager.get_loaded_plugins()
    print(f"\n✅ Plugins cargados: {loaded}")
    
    # Mostrar info
    for plugin_name in loaded:
        info = manager.get_plugin_info(plugin_name)
        if info:
            print(f"\n📋 {plugin_name}:")
            print(f"   Versión: {info['version']}")
            print(f"   Autor: {info['author']}")
            print(f"   Descripción: {info['description']}")
