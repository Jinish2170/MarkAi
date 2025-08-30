#!/usr/bin/env python3
"""
Project Organization Script for MarkAI

This script reorganizes the project structure into a clean, professional layout:
- Consolidates duplicate files
- Organizes documentation
- Creates proper directory structure  
- Removes unnecessary files
- Sets up development environment
"""

import os
import shutil
from pathlib import Path
import sys

def create_clean_structure():
    """Create a clean project structure"""
    
    # Define the clean directory structure
    directories = [
        "src/markai",           # Main source code
        "src/markai/core",      # Core AI engine
        "src/markai/api",       # Web API
        "src/markai/cli",       # CLI interface
        "src/markai/plugins",   # Plugin system
        "src/markai/utils",     # Utilities
        "config",               # Configuration files
        "docs",                 # Documentation
        "tests",                # Test files
        "scripts",              # Utility scripts
        "examples",             # Usage examples
        "data",                 # Data storage (keep existing)
        "logs",                 # Logs (keep existing)
        "exports",              # Export directory
        "static",               # Static files for web interface
        "templates"             # HTML templates
    ]
    
    print("📁 Creating clean directory structure...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created: {directory}/")

def consolidate_source_code():
    """Move and organize source code files"""
    
    print("\n🔧 Organizing source code...")
    
    # Move core files
    source_moves = [
        ("core/", "src/markai/core/"),
        ("api/", "src/markai/api/"), 
        ("cli/", "src/markai/cli/"),
        ("plugins/", "src/markai/plugins/"),
        ("utils/", "src/markai/utils/")
    ]
    
    for src, dst in source_moves:
        if Path(src).exists():
            if Path(dst).exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"   ✅ Moved: {src} → {dst}")

def consolidate_documentation():
    """Consolidate all documentation files"""
    
    print("\n📚 Organizing documentation...")
    
    # Move documentation files to docs/
    doc_files = {
        "README_ADVANCED.md": "docs/README.md",  # Main README
        "HOW_TO_USE.md": "docs/usage.md",
        "QUICKSTART.md": "docs/quickstart.md",
        "QUICK_START.md": None,  # Duplicate, will be deleted
        "PROJECT_SUMMARY.md": "docs/project_summary.md",
        "FIXES_SUMMARY.md": "docs/development_notes.md",
        "IMPORT_SOLUTIONS.md": "docs/troubleshooting.md",
        "IMPORT_FIXED.md": None,  # Duplicate, will be deleted
    }
    
    for src_file, dst_file in doc_files.items():
        if Path(src_file).exists():
            if dst_file:
                shutil.copy2(src_file, dst_file)
                print(f"   ✅ Moved: {src_file} → {dst_file}")
            os.remove(src_file)
            print(f"   🗑️  Removed: {src_file}")

def organize_scripts_and_examples():
    """Organize scripts and example files"""
    
    print("\n🛠️  Organizing scripts and examples...")
    
    # Move scripts
    script_files = {
        "setup_advanced.py": "scripts/setup.py",
        "fix_imports.py": "scripts/fix_imports.py",
        "test_imports.py": "scripts/test_imports.py",
        "test_system.py": "tests/test_system.py",
        "organize_project.py": "scripts/organize_project.py"
    }
    
    for src_file, dst_file in script_files.items():
        if Path(src_file).exists():
            shutil.copy2(src_file, dst_file)
            print(f"   ✅ Moved: {src_file} → {dst_file}")
            if src_file != "organize_project.py":  # Don't delete this file while running
                os.remove(src_file)
    
    # Move examples
    example_files = {
        "demo.py": "examples/demo.py",
        "usage_examples.py": "examples/usage_examples.py"
    }
    
    for src_file, dst_file in example_files.items():
        if Path(src_file).exists():
            shutil.copy2(src_file, dst_file)
            print(f"   ✅ Moved: {src_file} → {dst_file}")
            os.remove(src_file)

def clean_main_files():
    """Organize main entry point files"""
    
    print("\n🚀 Organizing main files...")
    
    # Keep only the advanced main file and rename it
    if Path("advanced_main.py").exists():
        shutil.copy2("advanced_main.py", "main.py")
        print("   ✅ Renamed: advanced_main.py → main.py")
        os.remove("advanced_main.py")
    
    # Clean up other files
    files_to_remove = [
        "setup.py",  # We have the advanced setup script
        "markai.bat"  # Windows batch file not needed
    ]
    
    for file in files_to_remove:
        if Path(file).exists():
            os.remove(file)
            print(f"   🗑️  Removed: {file}")

def create_package_structure():
    """Create proper Python package structure"""
    
    print("\n📦 Creating Python package structure...")
    
    # Create __init__.py files
    init_files = [
        "src/__init__.py",
        "src/markai/__init__.py",
        "src/markai/core/__init__.py",
        "src/markai/api/__init__.py", 
        "src/markai/cli/__init__.py",
        "src/markai/plugins/__init__.py",
        "src/markai/utils/__init__.py"
    ]
    
    for init_file in init_files:
        init_path = Path(init_file)
        if not init_path.exists():
            with open(init_path, 'w') as f:
                package_name = init_path.parent.name
                f.write(f'"""MarkAI {package_name.title()} Package"""\n')
            print(f"   ✅ Created: {init_file}")

def update_main_entry_point():
    """Update the main entry point to work with new structure"""
    
    print("\n🔧 Updating main entry point...")
    
    main_content = '''#!/usr/bin/env python3
"""
MarkAI - Advanced AI Assistant
Main Entry Point

A sophisticated AI assistant with advanced cognitive capabilities.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the main application
from markai.main import main

if __name__ == "__main__":
    sys.exit(main())
'''
    
    with open("main.py", 'w') as f:
        f.write(main_content)
    
    print("   ✅ Updated main.py entry point")

def create_markai_main():
    """Create the actual main module in the package"""
    
    print("\n📝 Creating markai main module...")
    
    # Copy advanced_main.py content but update imports
    main_module_path = "src/markai/main.py"
    
    if Path("main.py").exists():
        # Read the current main.py (which was advanced_main.py)
        with open("main.py", 'r') as f:
            content = f.read()
        
        # Update imports for new structure
        content = content.replace(
            "from utils.import_helper import setup_project_imports\nsetup_project_imports()",
            "# Import setup handled by package structure"
        )
        content = content.replace(
            "from core.advanced_ai_engine import",
            "from markai.core.advanced_ai_engine import"
        )
        content = content.replace(
            "from cli.advanced_interface import",
            "from markai.cli.advanced_interface import"
        )
        content = content.replace(
            "from api.advanced_server import",
            "from markai.api.advanced_server import"
        )
        content = content.replace(
            "from utils.config import",
            "from markai.utils.config import"
        )
        content = content.replace(
            "from utils.logger import",
            "from markai.utils.logger import"
        )
        
        with open(main_module_path, 'w') as f:
            f.write(content)
        
        print(f"   ✅ Created: {main_module_path}")

def create_setup_py():
    """Create a proper setup.py for the package"""
    
    print("\n📦 Creating setup.py...")
    
    setup_content = '''"""
MarkAI Advanced Setup Configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "docs" / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
req_file = this_directory / "requirements.txt"
if req_file.exists():
    with open(req_file, encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="markai-advanced",
    version="1.0.0",
    description="Advanced AI Assistant with Cognitive Intelligence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MarkAI Development Team",
    author_email="dev@markai.ai",
    url="https://github.com/your-username/markai-advanced",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.10.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "markai=markai.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="ai, assistant, cognitive, reasoning, machine-learning",
    include_package_data=True,
    zip_safe=False,
)
'''
    
    with open("setup.py", 'w') as f:
        f.write(setup_content)
    
    print("   ✅ Created: setup.py")

def create_project_readme():
    """Create the main project README"""
    
    print("\n📄 Creating main README...")
    
    readme_content = '''# 🧠 MarkAI Advanced

**Enterprise-grade AI Assistant with Advanced Cognitive Intelligence**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Quick Start

```bash
# Install dependencies
python scripts/setup.py --full

# Configure your API key
# Edit config/advanced_config.json and add your Gemini API key

# Start CLI interface
python main.py cli

# Start web interface  
python main.py web
```

## Features

- 🧠 **Advanced Cognitive Reasoning** - Multiple reasoning types and processing modes
- 🔗 **Memory Networks** - Episodic, semantic, and procedural memory systems
- 🎯 **Multi-Modal Processing** - Text, images, documents, and code analysis
- 🔌 **Plugin Ecosystem** - Extensible system with enterprise-grade plugins
- 🖥️ **Rich Interfaces** - Advanced CLI and web interfaces
- 📊 **Real-time Monitoring** - Cognitive state and performance tracking

## Documentation

- [**Usage Guide**](docs/usage.md) - How to use MarkAI effectively
- [**Quick Start**](docs/quickstart.md) - Get up and running quickly  
- [**Configuration**](config/advanced_config.json) - System configuration
- [**Examples**](examples/) - Usage examples and demos

## Project Structure

```
markai-advanced/
├── src/markai/          # Main source code
│   ├── core/           # AI engine and cognitive systems
│   ├── api/            # Web API and server
│   ├── cli/            # Command-line interface
│   ├── plugins/        # Plugin system
│   └── utils/          # Utilities and helpers
├── config/             # Configuration files
├── docs/               # Documentation
├── examples/           # Usage examples
├── scripts/            # Utility scripts
├── tests/              # Test suite
├── main.py            # Main entry point
└── requirements.txt   # Dependencies
```

## License

MIT License - see [LICENSE](LICENSE) for details.
'''
    
    with open("README.md", 'w') as f:
        f.write(readme_content)
    
    print("   ✅ Created: README.md")

def clean_up_cache():
    """Clean up cache and temporary files"""
    
    print("\n🧹 Cleaning up cache and temporary files...")
    
    # Remove Python cache
    if Path("__pycache__").exists():
        shutil.rmtree("__pycache__")
        print("   🗑️  Removed: __pycache__/")
    
    # Remove pytest cache
    if Path(".pytest_cache").exists():
        shutil.rmtree(".pytest_cache")
        print("   🗑️  Removed: .pytest_cache/")

def main():
    """Main organization function"""
    
    print("🚀 MarkAI Project Reorganization")
    print("=" * 50)
    
    try:
        # Step 1: Create clean directory structure
        create_clean_structure()
        
        # Step 2: Consolidate source code
        consolidate_source_code()
        
        # Step 3: Organize documentation  
        consolidate_documentation()
        
        # Step 4: Organize scripts and examples
        organize_scripts_and_examples()
        
        # Step 5: Clean main files
        clean_main_files()
        
        # Step 6: Create package structure
        create_package_structure()
        
        # Step 7: Update entry points
        create_markai_main()
        update_main_entry_point()
        
        # Step 8: Create setup.py
        create_setup_py()
        
        # Step 9: Create main README
        create_project_readme()
        
        # Step 10: Clean up
        clean_up_cache()
        
        print("\n" + "=" * 50)
        print("✅ PROJECT REORGANIZATION COMPLETE!")
        print("\n📁 New Structure:")
        print("   src/markai/     - Main source code")
        print("   config/         - Configuration files")
        print("   docs/           - All documentation")  
        print("   examples/       - Usage examples")
        print("   scripts/        - Utility scripts")
        print("   tests/          - Test files")
        print("   main.py         - Entry point")
        
        print("\n🚀 Next Steps:")
        print("   1. Run: python scripts/setup.py --full")
        print("   2. Configure your API key in config/advanced_config.json")
        print("   3. Start MarkAI: python main.py cli")
        
    except Exception as e:
        print(f"\n❌ Error during reorganization: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
