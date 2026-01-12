from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable
import importlib
import os
import inspect


# ---------------- META & BASE PLUGIN ------------------

class PluginMeta:
    """Plugin metadata"""

    def __init__(
        self,
        name: str,
        version: str,
        description: str = "",
        dependencies: List[str] = None,
        config_schema: dict = None,
    ):
        self.name = name
        self.version = version
        self.description = description
        self.dependencies = dependencies or []
        self.config_schema = config_schema or {}


class Plugin(ABC):
    """Base plugin interface"""

    @property
    @abstractmethod
    def meta(self) -> PluginMeta:
        pass

    @abstractmethod
    def initialize(self, config: dict) -> None:
        """Called when plugin loads"""
        pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Main plugin operation"""
        pass

    def cleanup(self) -> None:
        """Called when plugin unloads"""
        pass


# ------------------ EVENT SYSTEM --------------------

class EventBus:
    """Simple pub/sub system for plugin communication"""

    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable):
        self.listeners.setdefault(event_name, []).append(callback)

    def emit(self, event_name: str, data: Any):
        for callback in self.listeners.get(event_name, []):
            callback(data)


# ---------------- PLUGIN MANAGER --------------------

class PluginManager:

    def __init__(self, plugin_directory: str):
        self.plugin_directory = plugin_directory
        self.plugins: Dict[str, Plugin] = {}
        self.configs: Dict[str, dict] = {}
        self.event_bus = EventBus()

    # ------------- DISCOVERY -----------------

    def discover_plugins(self) -> List[str]:
        """
        Find all plugin modules inside a directory.
        A plugin file must end with '_plugin.py'
        """
        found = []
        for file in os.listdir(self.plugin_directory):
            if file.endswith("_plugin.py"):
                plugin_name = file[:-3]  # remove .py
                found.append(plugin_name)
        return found

    # ------------- LOADING -------------------

    def load_plugin(self, plugin_module_name: str, config: dict = None) -> bool:
        """
        Load and initialize plugin. Handles dependencies automatically.
        plugin_module_name = file name (without .py)
        """

        # Import module dynamically
        try:
            module = importlib.import_module(
                f"{self.plugin_directory}.{plugin_module_name}"
            )
        except Exception as e:
            print(f"Error importing plugin {plugin_module_name}: {e}")
            return False

        # Find class that extends Plugin
        plugin_class = None
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, Plugin) and obj is not Plugin:
                plugin_class = obj
                break

        if not plugin_class:
            print(f"No Plugin subclass found in {plugin_module_name}")
            return False

        plugin_instance: Plugin = plugin_class()
        meta = plugin_instance.meta

        # --- Load dependencies ---
        for dep in meta.dependencies:
            if dep not in self.plugins:
                print(f"Loading dependency: {dep}")
                if not self.load_plugin(dep):
                    print(f"Failed to load dependency {dep} for {meta.name}")
                    return False

        # Store config
        self.configs[meta.name] = config or {}

        # Initialize plugin
        try:
            plugin_instance.initialize(self.configs[meta.name])
        except Exception as e:
            print(f"Error initializing plugin {meta.name}: {e}")
            return False

        self.plugins[meta.name] = plugin_instance
        print(f"Plugin loaded: {meta.name}")
        return True

    # ------------- UNLOADING -------------------

    def unload_plugin(self, plugin_name: str) -> bool:
        if plugin_name not in self.plugins:
            return False

        try:
            self.plugins[plugin_name].cleanup()
        except Exception as e:
            print(f"Error during cleanup of {plugin_name}: {e}")

        del self.plugins[plugin_name]
        print(f"Plugin unloaded: {plugin_name}")
        return True 

    # ------------- EXECUTION ---------------------

    def execute_plugin(self, plugin_name: str, *args, **kwargs) -> Any:
        if plugin_name not in self.plugins:
            print(f"Plugin {plugin_name} not loaded")
            return None
        return self.plugins[plugin_name].execute(*args, **kwargs)

    # ------------- METADATA -----------------------

    def get_plugin_info(self, plugin_name: str) -> dict:
        if plugin_name not in self.plugins:
            return {}

        meta = self.plugins[plugin_name].meta
        return {
            "name": meta.name,
            "version": meta.version,
            "description": meta.description,
            "dependencies": meta.dependencies,
            "config_schema": meta.config_schema,
        }
