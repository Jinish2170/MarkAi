"""
Plugin Manager for MarkAI - Extensible plugin system for additional capabilities
"""

import asyncio
import importlib
import importlib.util
import inspect
import re
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from ..utils.logger import get_logger


class BasePlugin(ABC):
    """Base class for all MarkAI plugins"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = get_logger(self.__class__.__name__)
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Plugin description"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version"""
        pass
    
    @property
    def triggers(self) -> List[str]:
        """Keywords or patterns that trigger this plugin"""
        return []
    
    @property
    def capabilities(self) -> List[str]:
        """List of capabilities this plugin provides"""
        return []
    
    async def initialize(self):
        """Initialize the plugin (called on startup)"""
        pass
    
    async def shutdown(self):
        """Cleanup when shutting down"""
        pass
    
    @abstractmethod
    async def process_message(
        self,
        message: str,
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Process a message and return response if this plugin should handle it
        
        Returns:
            None if plugin doesn't handle the message
            Dict with response data if plugin handles the message
        """
        pass
    
    def should_handle(self, message: str) -> bool:
        """Check if this plugin should handle the given message"""
        if not self.triggers:
            return False
        
        message_lower = message.lower()
        return any(trigger.lower() in message_lower for trigger in self.triggers)


class PluginManager:
    """Manages all plugins for MarkAI"""
    
    def __init__(self, config):
        self.config = config
        self.logger = get_logger(__name__)
        self.plugins: Dict[str, BasePlugin] = {}
        self.plugin_dir = Path("plugins")
        
        # Initialize plugin system
        asyncio.create_task(self._load_plugins())
        
        self.logger.info("PluginManager initialized")
    
    async def _load_plugins(self):
        """Load all plugins from the plugins directory"""
        if not self.plugin_dir.exists():
            self.plugin_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info("Created plugins directory")
            return
        
        # Load built-in plugins first
        await self._load_builtin_plugins()
        
        # Then load external plugins
        await self._load_external_plugins()
        
        self.logger.info(f"Loaded {len(self.plugins)} plugins")
    
    async def _load_builtin_plugins(self):
        """Load built-in plugins"""
        builtin_plugins = [
            CalculatorPlugin,
            WeatherPlugin,
            FileManagerPlugin,
            CodeAnalyzerPlugin,
            TaskManagerPlugin
        ]
        
        for plugin_class in builtin_plugins:
            try:
                plugin = plugin_class(self.config.get('plugins', {}).get(plugin_class.__name__, {}))
                await plugin.initialize()
                self.plugins[plugin.name] = plugin
                self.logger.info(f"Loaded built-in plugin: {plugin.name}")
            except Exception as e:
                self.logger.error(f"Failed to load built-in plugin {plugin_class.__name__}: {str(e)}")
    
    async def _load_external_plugins(self):
        """Load external plugins from the plugins directory"""
        for plugin_file in self.plugin_dir.glob("*.py"):
            if plugin_file.name.startswith("__"):
                continue
            
            try:
                spec = importlib.util.spec_from_file_location(
                    f"plugins.{plugin_file.stem}", plugin_file
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find plugin classes in the module
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, BasePlugin) and 
                        obj != BasePlugin):
                        
                        plugin = obj(self.config.get('plugins', {}).get(name, {}))
                        await plugin.initialize()
                        self.plugins[plugin.name] = plugin
                        self.logger.info(f"Loaded external plugin: {plugin.name}")
                        
            except Exception as e:
                self.logger.error(f"Failed to load plugin from {plugin_file}: {str(e)}")
    
    async def handle_message(
        self,
        message: str,
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Check if any plugin should handle the message"""
        
        for plugin in self.plugins.values():
            if plugin.should_handle(message):
                try:
                    response = await plugin.process_message(message, user_id, context)
                    if response:
                        self.logger.info(f"Plugin {plugin.name} handled message")
                        return response
                except Exception as e:
                    self.logger.error(f"Plugin {plugin.name} error: {str(e)}")
        
        return None
    
    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """Get a plugin by name"""
        return self.plugins.get(name)
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all loaded plugins"""
        return [
            {
                'name': plugin.name,
                'description': plugin.description,
                'version': plugin.version,
                'triggers': plugin.triggers,
                'capabilities': plugin.capabilities
            }
            for plugin in self.plugins.values()
        ]
    
    async def shutdown(self):
        """Shutdown all plugins"""
        for plugin in self.plugins.values():
            try:
                await plugin.shutdown()
            except (IOError, OSError, RuntimeError) as e:
                self.logger.error(f"Error shutting down plugin {plugin.name}: {str(e)}")
        
        self.logger.info("PluginManager shut down")


# Built-in plugins

class CalculatorPlugin(BasePlugin):
    """Simple calculator plugin"""
    
    @property
    def name(self) -> str:
        return "calculator"
    
    @property
    def description(self) -> str:
        return "Performs mathematical calculations"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def triggers(self) -> List[str]:
        return ["calculate", "math", "=", "+", "-", "*", "/"]
    
    @property
    def capabilities(self) -> List[str]:
        return ["basic_math", "calculations"]
    
    async def process_message(
        self,
        message: str,
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Process mathematical expressions"""
        
        # Look for mathematical expressions
        math_patterns = [
            r'calculate\s+(.+)',
            r'what\s+is\s+(.+)',
            r'(\d+(?:\.\d+)?\s*[+\-*/]\s*\d+(?:\.\d+)?(?:\s*[+\-*/]\s*\d+(?:\.\d+)?)*)',
        ]
        
        for pattern in math_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                expression = match.group(1).strip()
                
                try:
                    # Basic safety check
                    if re.match(r'^[\d\s+\-*/().]+$', expression):
                        # Use safe evaluation instead of eval
                        result = self._safe_eval(expression)
                        return {
                            'content': f"The result is: {result}",
                            'metadata': {
                                'plugin': self.name,
                                'expression': expression,
                                'result': result
                            }
                        }
                except (ValueError, ZeroDivisionError, ArithmeticError) as e:
                    return {
                        'content': f"Sorry, I couldn't calculate that: {str(e)}",
                        'metadata': {'plugin': self.name, 'error': str(e)}
                    }
        
        return None
    
    def _safe_eval(self, expression: str) -> float:
        """Safely evaluate mathematical expressions"""
        # Replace with a simple parser for basic math
        allowed_chars = set('0123456789+-*/.()')
        if not all(c in allowed_chars or c.isspace() for c in expression):
            raise ValueError("Invalid characters in expression")
        
        # For now, use eval but with restricted input
        # In production, use a proper math expression parser
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return float(result)
        except Exception as e:
            raise ValueError(f"Cannot evaluate expression: {str(e)}")  # pylint: disable=raise-missing-from


class WeatherPlugin(BasePlugin):
    """Weather information plugin (mock implementation)"""
    
    @property
    def name(self) -> str:
        return "weather"
    
    @property
    def description(self) -> str:
        return "Provides weather information"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def triggers(self) -> List[str]:
        return ["weather", "temperature", "forecast", "rain", "sunny"]
    
    async def process_message(
        self,
        message: str,
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Provide weather information (mock)"""
        
        if "weather" in message.lower():
            # Mock weather response
            return {
                'content': "I'd love to help with weather information! However, I need to be configured with a weather API key. Please check the plugin configuration.",
                'metadata': {
                    'plugin': self.name,
                    'requires_api': True
                }
            }
        
        return None


class FileManagerPlugin(BasePlugin):
    """File management plugin"""
    
    @property
    def name(self) -> str:
        return "file_manager"
    
    @property
    def description(self) -> str:
        return "Helps with file operations"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def triggers(self) -> List[str]:
        return ["file", "folder", "directory", "create file", "list files"]
    
    async def process_message(
        self,
        message: str,
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Handle file operations"""
        
        message_lower = message.lower()
        
        if "list files" in message_lower:
            try:
                current_dir = Path.cwd()
                files = [f.name for f in current_dir.iterdir() if f.is_file()]
                folders = [f.name for f in current_dir.iterdir() if f.is_dir()]
                
                response = f"Current directory: {current_dir}\n\n"
                if folders:
                    response += f"Folders: {', '.join(folders[:10])}\n"
                if files:
                    response += f"Files: {', '.join(files[:10])}"
                
                return {
                    'content': response,
                    'metadata': {
                        'plugin': self.name,
                        'operation': 'list_files',
                        'file_count': len(files),
                        'folder_count': len(folders)
                    }
                }
            except (OSError, IOError) as e:
                return {
                    'content': f"Error listing files: {str(e)}",
                    'metadata': {'plugin': self.name, 'error': str(e)}
                }
        
        return None


class CodeAnalyzerPlugin(BasePlugin):
    """Code analysis plugin"""
    
    @property
    def name(self) -> str:
        return "code_analyzer"
    
    @property
    def description(self) -> str:
        return "Analyzes code snippets"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def triggers(self) -> List[str]:
        return ["analyze code", "review code", "code review", "```"]
    
    async def process_message(
        self,
        message: str,
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Analyze code snippets"""
        
        import re
        
        # Look for code blocks
        code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', message, re.DOTALL)
        
        if code_blocks or "analyze code" in message.lower():
            analysis = []
            
            for lang, code in code_blocks:
                lang = lang or "unknown"
                lines = len(code.strip().split('\n'))
                chars = len(code)
                
                analysis.append(f"- Code block ({lang}): {lines} lines, {chars} characters")
            
            if analysis:
                response = "Code Analysis:\n" + "\n".join(analysis)
                response += "\n\nI can provide more detailed analysis if you specify what you'd like me to focus on!"
            else:
                response = "I'd be happy to analyze code for you! Please share the code you'd like me to review."
            
            return {
                'content': response,
                'metadata': {
                    'plugin': self.name,
                    'code_blocks_found': len(code_blocks)
                }
            }
        
        return None


class TaskManagerPlugin(BasePlugin):
    """Simple task management plugin"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.tasks: Dict[str, List[Dict[str, Any]]] = {}
    
    @property
    def name(self) -> str:
        return "task_manager"
    
    @property
    def description(self) -> str:
        return "Simple task management"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def triggers(self) -> List[str]:
        return ["task", "todo", "remind", "add task", "list tasks"]
    
    async def process_message(
        self,
        message: str,
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Handle task management"""
        
        message_lower = message.lower()
        
        if user_id not in self.tasks:
            self.tasks[user_id] = []
        
        if "add task" in message_lower:
            # Extract task from message
            task_match = re.search(r'add task:?\s*(.+)', message, re.IGNORECASE)
            if task_match:
                task = task_match.group(1).strip()
                self.tasks[user_id].append({
                    'task': task,
                    'created': datetime.now().isoformat(),
                    'completed': False
                })
                
                return {
                    'content': f"Added task: {task}",
                    'metadata': {
                        'plugin': self.name,
                        'operation': 'add_task',
                        'task_count': len(self.tasks[user_id])
                    }
                }
        
        elif "list tasks" in message_lower:
            user_tasks = self.tasks.get(user_id, [])
            
            if not user_tasks:
                response = "You have no tasks yet. Use 'add task: [description]' to add one!"
            else:
                pending_tasks = [t for t in user_tasks if not t['completed']]
                response = f"Your tasks ({len(pending_tasks)} pending):\n"
                
                for i, task in enumerate(pending_tasks[:10], 1):
                    response += f"{i}. {task['task']}\n"
            
            return {
                'content': response,
                'metadata': {
                    'plugin': self.name,
                    'operation': 'list_tasks',
                    'task_count': len(user_tasks)
                }
            }
        
        return None
