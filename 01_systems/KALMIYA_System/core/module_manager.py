import os
import sys
import importlib
import inspect
import json

class ModuleManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModuleManager, cls).__new__(cls)
            cls._instance.modules = {}
            cls._instance.instances = {}
            cls._instance.load_all_modules()
        return cls._instance

    def load_all_modules(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        modules_dir = os.path.join(base_dir, 'modules')
        
        if base_dir not in sys.path:
            sys.path.insert(0, base_dir)
            
        if not os.path.exists(modules_dir):
            return

        for filename in os.listdir(modules_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(f"modules.{module_name}")
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if obj.__module__ == f"modules.{module_name}":
                            self.modules[name] = obj
                            try:
                                self.instances[name] = obj()
                            except Exception as e:
                                pass
                except Exception as e:
                    print(f"Error loading module {module_name}: {e}")

    def execute_function(self, function_name, args_json=None):
        args_dict = {}
        if args_json:
            if isinstance(args_json, str):
                try:
                    args_dict = json.loads(args_json)
                except:
                    args_dict = {}
            elif isinstance(args_json, dict):
                args_dict = args_json
                
        for name, instance in self.instances.items():
            if hasattr(instance, function_name):
                func = getattr(instance, function_name)
                if callable(func):
                    try:
                        result = func(**args_dict)
                        return f"Successfully executed {function_name}. Result: {result}"
                    except Exception as e:
                        return f"Error executing {function_name} in {name}: {e}"
        return f"Function {function_name} not found in any loaded module."

    def get_loaded_modules_info(self):
        return {name: [f[0] for f in inspect.getmembers(instance, predicate=inspect.ismethod) if not f[0].startswith('_')] 
                for name, instance in self.instances.items()}

# Global instance
manager = ModuleManager()
