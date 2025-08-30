"""
MarkAI Import Helper - Solves Python import issues

This module provides utilities to properly configure Python imports
for the MarkAI project, ensuring all modules can find each other.
"""

import sys
import os
from pathlib import Path


def setup_project_imports():
    """
    Add the project root directory to Python's module search path.
    This should be called at the top of any script that needs to import
    MarkAI modules.
    
    Usage:
        from utils.import_helper import setup_project_imports
        setup_project_imports()
        
        # Now you can import any MarkAI module
        from markai.core.ai_engine import MarkAICore
        from markai.memory.conversation_manager import ConversationManager
    """
    # Get the project root directory (parent of utils/)
    project_root = Path(__file__).parent.parent
    project_root_str = str(project_root.absolute())
    
    # Add to Python path if not already there
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)
        print(f"✓ Added project root to Python path: {project_root_str}")
    
    return project_root


def get_project_root():
    """
    Get the project root directory as a Path object.
    
    Returns:
        Path: The project root directory
    """
    return Path(__file__).parent.parent


def debug_imports():
    """
    Debug function to show current Python path and project structure.
    Useful for troubleshooting import issues.
    """
    print("🔍 Python Import Debug Information")
    print("=" * 50)
    
    project_root = get_project_root()
    print(f"Project root: {project_root}")
    print(f"Current working directory: {Path.cwd()}")
    
    print("\n📁 Project structure:")
    for item in sorted(project_root.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            print(f"  📁 {item.name}/")
            # Show Python files in each directory
            for py_file in item.glob("*.py"):
                print(f"    📄 {py_file.name}")
    
    print(f"\n🐍 Python path ({len(sys.path)} entries):")
    project_root_str = str(project_root.absolute())
    for i, path in enumerate(sys.path):
        marker = "✓" if project_root_str in path else " "
        print(f"  {marker} {i+1:2d}. {path}")
    
    print("\n📦 Available MarkAI modules:")
    modules_to_test = [
        "core.ai_engine",
        "memory.conversation_manager", 
        "memory.context_manager",
        "plugins.plugin_manager",
        "utils.config",
        "utils.logger",
        "cli.interface",
        "api.server"
    ]
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"  ✅ {module_name}")
        except (ModuleNotFoundError, ImportError) as e:
            print(f"  ❌ {module_name} - {str(e)}")
        except (AttributeError, SyntaxError) as e:
            print(f"  ⚠️  {module_name} - {str(e)}")


def create_init_files():
    """
    Create __init__.py files in all directories to make them proper Python packages.
    This helps with imports and makes the project structure cleaner.
    """
    project_root = get_project_root()
    
    directories = [
        "core",
        "memory", 
        "plugins",
        "utils",
        "cli",
        "api",
        "config"  # If it exists
    ]
    
    created_files = []
    
    for directory in directories:
        dir_path = project_root / directory
        if dir_path.exists() and dir_path.is_dir():
            init_file = dir_path / "__init__.py"
            if not init_file.exists():
                # Create a simple __init__.py with package info
                init_content = f'"""\n{directory.title()} package for MarkAI\n"""\n\n__version__ = "1.0.0"\n'
                
                with open(init_file, 'w', encoding='utf-8') as f:
                    f.write(init_content)
                
                created_files.append(str(init_file))
                print(f"✓ Created {init_file}")
    
    if created_files:
        print(f"\n📦 Created {len(created_files)} __init__.py files")
    else:
        print("📦 All __init__.py files already exist")
    
    return created_files


if __name__ == "__main__":
    # If run directly, perform debug and setup
    print("🚀 MarkAI Import Helper")
    print("=" * 30)
    
    # Setup imports
    setup_project_imports()
    
    # Create __init__.py files
    create_init_files()
    
    # Debug current state
    debug_imports()
