#!/usr/bin/env python3
"""
MarkAI Advanced Setup Script

This script helps you set up MarkAI with all advanced features including:
- Environment setup and dependency installation
- Configuration generation with API key setup
- Database initialization 
- Plugin system setup
- Advanced feature configuration
- System validation and testing

Usage:
    python setup_advanced.py --install    # Install all dependencies
    python setup_advanced.py --configure  # Configure system
    python setup_advanced.py --full       # Full setup (install + configure)
    python setup_advanced.py --test       # Test installation
"""

import os
import sys
import json
import subprocess
import asyncio
from pathlib import Path
from typing import Dict, List, Any
import shutil

def print_banner():
    """Print setup banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║    🧠 MarkAI Advanced Setup                              ║
    ║                                                          ║
    ║    Setting up enterprise-grade AI assistant with:       ║
    ║    • Advanced cognitive reasoning                        ║
    ║    • Memory networks & learning                          ║
    ║    • Multi-modal processing                              ║
    ║    • Enterprise plugin ecosystem                         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_command(command: str, description: str = None) -> bool:
    """Run a command and return success status"""
    if description:
        print(f"📦 {description}...")
    
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            check=True
        )
        if description:
            print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description or command}: {e}")
        if e.stdout:
            print(f"   stdout: {e.stdout}")
        if e.stderr:
            print(f"   stderr: {e.stderr}")
        return False


def create_directories():
    """Create necessary directories"""
    directories = [
        'data',
        'logs', 
        'exports',
        'plugins',
        'custom_plugins',
        'config',
        'static',
        'templates',
        'tests',
        'docs'
    ]
    
    print("📁 Creating directory structure...")
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ Created {directory}/")


def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Not in a virtual environment. Consider using one.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            return False
    
    # Install core requirements
    if not run_command("pip install --upgrade pip", "Upgrading pip"):
        return False
    
    requirements_file = Path("requirements.txt")
    if requirements_file.exists():
        if not run_command(f"pip install -r {requirements_file}", "Installing dependencies from requirements.txt"):
            return False
    else:
        # Install essential packages individually
        essential_packages = [
            "google-generativeai>=0.3.2",
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "rich>=13.7.0",
            "sentence-transformers>=2.2.2",
            "faiss-cpu>=1.7.4",
            "networkx>=3.0.0",
            "pandas>=2.0.0",
            "matplotlib>=3.7.0",
            "pillow>=10.0.0"
        ]
        
        for package in essential_packages:
            if not run_command(f"pip install {package}", f"Installing {package}"):
                print(f"❌ Failed to install {package}")
                return False
    
    print("✅ All dependencies installed successfully!")
    return True


def setup_configuration():
    """Setup configuration files"""
    print("⚙️  Setting up configuration...")
    
    # Create config directory
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    # Check if advanced config exists
    advanced_config_path = config_dir / "advanced_config.json"
    
    if advanced_config_path.exists():
        print("   ℹ️  Advanced configuration already exists")
        response = input("   Overwrite existing configuration? (y/N): ")
        if response.lower() != 'y':
            return True
    
    # Get API key from user
    print("\n🔑 API Key Configuration")
    print("   MarkAI requires a Google Gemini API key.")
    print("   Get your API key from: https://makersuite.google.com/app/apikey")
    
    api_key = input("\n   Enter your Gemini API key (or press Enter to configure later): ").strip()
    
    if not api_key:
        api_key = "${GEMINI_API_KEY}"
        print("   ⚠️  API key not provided. Please set GEMINI_API_KEY environment variable")
        print("   or update the configuration file later.")
    
    # Create advanced configuration
    advanced_config = {
        "ai": {
            "provider": "gemini",
            "model_name": "gemini-pro",
            "api_key": api_key,
            "temperature": 0.7,
            "max_tokens": 8192,
            "top_p": 0.9,
            "top_k": 40
        },
        "advanced_ai": {
            "enable_advanced_reasoning": True,
            "enable_chain_of_thought": True,
            "enable_meta_cognition": True,
            "enable_memory_networks": True,
            "enable_adaptive_learning": True,
            "default_processing_mode": "balanced",
            "default_reasoning_type": "analytical",
            "confidence_threshold": 0.7,
            "max_reasoning_steps": 10,
            "enable_multimodal": True,
            "enable_safety_assessment": True
        },
        "memory": {
            "enable_episodic_memory": True,
            "enable_semantic_memory": True,
            "enable_procedural_memory": True,
            "memory_retention_days": 30,
            "max_memories_per_type": 10000,
            "similarity_threshold": 0.8,
            "vector_dimension": 384,
            "use_faiss": True,
            "memory_consolidation_interval": 3600
        },
        "plugins": {
            "enable_plugin_system": True,
            "plugin_directories": ["plugins", "custom_plugins"],
            "enabled_plugins": [
                "web_research",
                "code_intelligence", 
                "data_science",
                "creative_content"
            ],
            "plugin_timeout_seconds": 30,
            "max_plugin_memory_mb": 512
        },
        "web_interface": {
            "host": "127.0.0.1",
            "port": 8000,
            "enable_websocket": True,
            "enable_file_upload": True,
            "max_file_size_mb": 10,
            "enable_real_time_monitoring": True,
            "session_timeout_minutes": 30
        },
        "logging": {
            "level": "INFO",
            "file": "logs/markai.log",
            "max_file_size_mb": 100,
            "backup_count": 5,
            "enable_console_logging": True
        },
        "database": {
            "type": "sqlite",
            "path": "data/markai.db",
            "enable_connection_pooling": True,
            "max_connections": 20
        },
        "security": {
            "enable_rate_limiting": True,
            "requests_per_minute": 60,
            "enable_input_validation": True,
            "enable_output_filtering": True,
            "enable_content_safety": True,
            "safety_threshold": 0.8
        }
    }
    
    # Save configuration
    with open(advanced_config_path, 'w', encoding='utf-8') as f:
        json.dump(advanced_config, f, indent=4)
    
    print(f"   ✅ Advanced configuration saved to {advanced_config_path}")
    
    # Create environment file template
    env_file = Path(".env")
    if not env_file.exists():
        env_content = f"""# MarkAI Environment Variables
GEMINI_API_KEY={api_key if api_key != "${GEMINI_API_KEY}" else "your_gemini_api_key_here"}

# Optional: Override configuration
# MARKAI_CONFIG=config/advanced_config.json
# MARKAI_LOG_LEVEL=INFO
# MARKAI_HOST=127.0.0.1
# MARKAI_PORT=8000
"""
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print(f"   ✅ Environment template saved to {env_file}")
    
    return True


def initialize_database():
    """Initialize the database"""
    print("🗄️  Initializing database...")
    
    try:
        import sqlite3
        
        db_path = Path("data/markai.db")
        
        # Create database and basic tables
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSON
            )
        """)
        
        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSON,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        """)
        
        # Memory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding BLOB,
                strength REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSON
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("   ✅ Database initialized successfully")
        return True
        
    except Exception as e:
        print(f"   ❌ Database initialization failed: {e}")
        return False


def create_plugin_structure():
    """Create plugin system structure"""
    print("🔌 Setting up plugin system...")
    
    # Create plugin directories
    plugin_dirs = ["plugins", "custom_plugins"]
    for plugin_dir in plugin_dirs:
        Path(plugin_dir).mkdir(exist_ok=True)
        
        # Create __init__.py
        init_file = Path(plugin_dir) / "__init__.py"
        if not init_file.exists():
            with open(init_file, 'w') as f:
                f.write(f'"""MarkAI {plugin_dir.title()} Package"""\n')
    
    print("   ✅ Plugin system structure created")
    return True


def run_validation_tests():
    """Run validation tests"""
    print("🧪 Running validation tests...")
    
    test_results = []
    
    # Test 1: Import validation
    print("   Testing imports...")
    try:
        sys.path.insert(0, str(Path.cwd()))
        from utils.import_helper import setup_project_imports
        setup_project_imports()
        test_results.append(("Import system", True))
        print("   ✅ Import system working")
    except Exception as e:
        test_results.append(("Import system", False, str(e)))
        print(f"   ❌ Import system failed: {e}")
    
    # Test 2: Configuration loading
    print("   Testing configuration...")
    try:
        from utils.config import Config
        config = Config("config/advanced_config.json")
        test_results.append(("Configuration", True))
        print("   ✅ Configuration loading working")
    except Exception as e:
        test_results.append(("Configuration", False, str(e)))
        print(f"   ❌ Configuration loading failed: {e}")
    
    # Test 3: Database connection
    print("   Testing database...")
    try:
        import sqlite3
        conn = sqlite3.connect("data/markai.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        
        if len(tables) >= 3:  # conversations, messages, memories
            test_results.append(("Database", True))
            print("   ✅ Database connection working")
        else:
            test_results.append(("Database", False, "Missing tables"))
            print("   ❌ Database missing required tables")
    except Exception as e:
        test_results.append(("Database", False, str(e)))
        print(f"   ❌ Database connection failed: {e}")
    
    # Test 4: AI engine initialization
    print("   Testing AI engine...")
    try:
        # This is a basic test - full test requires API key
        from core.advanced_ai_engine import AdvancedMarkAICore
        test_results.append(("AI Engine Import", True))
        print("   ✅ AI engine import working")
    except Exception as e:
        test_results.append(("AI Engine Import", False, str(e)))
        print(f"   ❌ AI engine import failed: {e}")
    
    # Summary
    passed = sum(1 for result in test_results if result[1])
    total = len(test_results)
    
    print(f"\n📊 Validation Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All validation tests passed! MarkAI is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False


def show_usage_instructions():
    """Show usage instructions"""
    instructions = """
🚀 MarkAI Advanced Setup Complete!

📋 Quick Start:
   1. Set your API key in config/advanced_config.json or .env file
   2. Start the CLI interface:
      python advanced_main.py cli
   
   3. Or start the web interface:
      python advanced_main.py web
   
   4. For help:
      python advanced_main.py --help

🔧 Configuration:
   • Main config: config/advanced_config.json
   • Environment: .env file
   • Logs: logs/ directory
   • Data: data/ directory

🧠 Advanced Features:
   • Multi-type reasoning modes (analytical, creative, strategic, etc.)
   • Advanced memory networks with learning
   • Chain-of-thought reasoning with confidence scoring
   • Multi-modal processing (text, images, documents)
   • Enterprise plugin ecosystem
   • Real-time cognitive monitoring
   • Conversation analytics and export

📚 Documentation:
   • Configuration guide: docs/configuration.md
   • Plugin development: docs/plugins.md
   • API reference: docs/api.md

🔑 Don't forget to set your Gemini API key!
   Get it from: https://makersuite.google.com/app/apikey
    """
    print(instructions)


def main():
    """Main setup function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MarkAI Advanced Setup Script")
    parser.add_argument("--install", action="store_true", help="Install dependencies")
    parser.add_argument("--configure", action="store_true", help="Configure system")
    parser.add_argument("--full", action="store_true", help="Full setup (install + configure)")
    parser.add_argument("--test", action="store_true", help="Run validation tests")
    parser.add_argument("--dirs", action="store_true", help="Create directories only")
    
    args = parser.parse_args()
    
    if not any([args.install, args.configure, args.full, args.test, args.dirs]):
        print_banner()
        parser.print_help()
        print("\nExample: python setup_advanced.py --full")
        return 0
    
    print_banner()
    
    success = True
    
    if args.full or args.dirs:
        create_directories()
    
    if args.full or args.install:
        if not install_dependencies():
            success = False
    
    if args.full or args.configure:
        if not setup_configuration():
            success = False
        if not initialize_database():
            success = False
        if not create_plugin_structure():
            success = False
    
    if args.test or args.full:
        if not run_validation_tests():
            success = False
    
    if success:
        print("\n🎉 Setup completed successfully!")
        if not args.test:
            show_usage_instructions()
        return 0
    else:
        print("\n❌ Setup completed with errors. Please check the messages above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
