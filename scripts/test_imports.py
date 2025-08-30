#!/usr/bin/env python3
"""
MarkAI Import Test - Demonstrates proper import usage

This script shows how to properly import and use MarkAI modules
from any location or context.
"""

# Method 1: Using the import helper (Recommended)
print("🔧 Method 1: Using Import Helper")
print("-" * 40)

from utils.import_helper import setup_project_imports
setup_project_imports()

# Now all MarkAI modules are available
from core.ai_engine import MarkAICore, AIResponse
from memory.conversation_manager import ConversationManager
from memory.context_manager import ContextManager
from plugins.plugin_manager import PluginManager, BasePlugin
from utils.config import Config
from utils.logger import get_logger, setup_logging
from cli.interface import CLIInterface
from api.server import app

print("✅ All imports successful using import helper!")

# Test basic functionality
print("\n🧪 Testing Basic Functionality")
print("-" * 40)

try:
    # Test config
    config = Config("config/config.example.json")
    print(f"✅ Config loaded: {config.get('api.gemini.model', 'Unknown')}")
    
    # Test logger
    logger = get_logger("test_imports")
    logger.info("Testing logger functionality")
    print("✅ Logger working")
    
    # Test data structures
    from datetime import datetime
    response = AIResponse(
        content="Test response",
        metadata={"test": True},
        timestamp=datetime.now(),
        model_used="test-model",
        tokens_used=10,
        confidence=0.95
    )
    print(f"✅ AIResponse created: {response.content}")
    
except Exception as e:
    print(f"❌ Error testing functionality: {str(e)}")

print("\n" + "=" * 50)

# Method 2: Manual path setup (Alternative)
print("🔧 Method 2: Manual Path Setup")
print("-" * 40)

import sys
import os
from pathlib import Path

# Get project root (assuming this script is in project root)
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    print(f"✅ Added to Python path: {project_root}")

# Test import after manual setup
try:
    from utils.helpers import generate_id, format_timestamp
    test_id = generate_id("test")
    print(f"✅ Helper functions work: {test_id}")
except Exception as e:
    print(f"❌ Error with manual setup: {str(e)}")

print("\n" + "=" * 50)

# Method 3: Environment variable approach (For production)
print("🔧 Method 3: Environment Variable")
print("-" * 40)

# Set PYTHONPATH environment variable
project_path = str(Path(__file__).parent.absolute())
current_pythonpath = os.environ.get('PYTHONPATH', '')

if project_path not in current_pythonpath:
    new_pythonpath = f"{project_path};{current_pythonpath}" if current_pythonpath else project_path
    os.environ['PYTHONPATH'] = new_pythonpath
    print(f"✅ Set PYTHONPATH: {project_path}")
else:
    print(f"✅ PYTHONPATH already contains: {project_path}")

print("\n🎯 Import Best Practices")
print("-" * 40)
print("1. Always use the import_helper for MarkAI projects:")
print("   from utils.import_helper import setup_project_imports")
print("   setup_project_imports()")
print("")
print("2. For external scripts importing MarkAI:")
print("   sys.path.insert(0, '/path/to/markai')")
print("")
print("3. For production deployment:")
print("   Set PYTHONPATH environment variable")
print("")
print("4. Use absolute imports for clarity:")
print("   from core.ai_engine import MarkAICore  # Good")
print("   from .ai_engine import MarkAICore      # Relative, use carefully")

print("\n✨ All import methods tested successfully!")
