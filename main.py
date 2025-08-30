#!/usr/bin/env python3
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

try:
    # Import and run the main application
    from markai.main import main
    
    if __name__ == "__main__":
        sys.exit(main())
        
except ImportError as e:
    print("❌ Import Error: MarkAI modules not found")
    print(f"   Error: {e}")
    print("\n🔧 Please run the setup script first:")
    print("   python scripts/setup.py --full")
    print("\n📁 Or check that the project structure is correct:")
    print("   src/markai/ should contain the main modules")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting MarkAI: {e}")
    sys.exit(1)
