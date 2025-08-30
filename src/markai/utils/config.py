"""
Configuration Manager for MarkAI
"""

import json
import os
from typing import Any, Optional
from pathlib import Path

from .logger import get_logger


class Config:
    """Configuration management for MarkAI"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.logger = get_logger(__name__)
        
        if config_path is None:
            config_path = "config/config.json"
            
        self.config_path = Path(config_path)
        self._config_data = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self._config_data = json.load(f)
                self.logger.info(f"Configuration loaded from {self.config_path}")
            else:
                # Try to load from example config
                example_path = self.config_path.parent / "config.example.json"
                if example_path.exists():
                    with open(example_path, 'r', encoding='utf-8') as f:
                        self._config_data = json.load(f)
                    self.logger.warning(f"Using example config from {example_path}")
                else:
                    self._load_default_config()
                    self.logger.warning("Using default configuration")
                    
        except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
            self.logger.error(f"Error loading configuration: {str(e)}")
            self._load_default_config()
    
    def _load_default_config(self):
        """Load default configuration"""
        self._config_data = {
            "api": {
                "gemini": {
                    "api_key": "",
                    "model": "gemini-1.5-pro-latest",
                    "temperature": 0.7,
                    "max_tokens": 8192
                }
            },
            "server": {
                "host": "localhost",
                "port": 8000,
                "debug": False
            },
            "database": {
                "url": "sqlite:///./markai.db"
            },
            "memory": {
                "max_conversations": 1000,
                "max_tokens_per_conversation": 50000
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self._config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config = self._config_data
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self):
        """Save configuration to file"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config_data, f, indent=2)
            self.logger.info(f"Configuration saved to {self.config_path}")
        except (IOError, OSError) as e:
            self.logger.error(f"Error saving configuration: {str(e)}")
    
    # Convenient property accessors
    @property
    def gemini_api_key(self) -> str:
        return self.get('api.gemini.api_key', os.getenv('GEMINI_API_KEY', ''))
    
    @property
    def gemini_model(self) -> str:
        return self.get('api.gemini.model', 'gemini-1.5-pro-latest')
    
    @property
    def gemini_temperature(self) -> float:
        return self.get('api.gemini.temperature', 0.7)
    
    @property
    def gemini_max_tokens(self) -> int:
        return self.get('api.gemini.max_tokens', 8192)
    
    @property
    def server_host(self) -> str:
        return self.get('server.host', 'localhost')
    
    @property
    def server_port(self) -> int:
        return self.get('server.port', 8000)
    
    @property
    def server_debug(self) -> bool:
        return self.get('server.debug', False)
    
    @property
    def database_url(self) -> str:
        return self.get('database.url', 'sqlite:///./markai.db')
    
    @property
    def max_conversations(self) -> int:
        return self.get('memory.max_conversations', 1000)
    
    @property
    def max_tokens_per_conversation(self) -> int:
        return self.get('memory.max_tokens_per_conversation', 50000)
    
    @property
    def vector_db_path(self) -> str:
        return self.get('memory.vector_db_path', './memory/vectors')
    
    @property
    def embedding_model(self) -> str:
        return self.get('memory.embedding_model', 'all-MiniLM-L6-v2')
    
    def validate(self) -> bool:
        """Validate configuration"""
        required_keys = [
            'api.gemini.api_key'
        ]
        
        for key in required_keys:
            if not self.get(key):
                self.logger.error(f"Missing required configuration: {key}")
                return False
        
        return True
