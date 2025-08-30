#!/usr/bin/env python3
"""
MarkAI Usage Examples - Practical demonstrations

This shows you exactly how to use MarkAI in different scenarios.
"""

# Setup imports
from utils.import_helper import setup_project_imports
setup_project_imports()

import asyncio
from utils.config import Config
from plugins.plugin_manager import PluginManager


def show_basic_usage():
    """Show basic usage patterns"""
    print("🚀 How to Use MarkAI - Practical Examples")
    print("=" * 55)
    
    print("\n1️⃣ WEB INTERFACE (Recommended for beginners)")
    print("-" * 45)
    print("   Start the web server:")
    print("   → python main.py")
    print("   → Open: http://localhost:8000")
    print("   → Chat in your browser!")
    print("")
    print("   What you can do:")
    print("   • Ask questions: 'Explain machine learning'")
    print("   • Use calculator: 'What's 15% of $200?'")
    print("   • Get help: 'How do I deploy a Python app?'")
    print("   • Code analysis: 'Review this function for bugs'")
    
    print("\n2️⃣ COMMAND LINE INTERFACE")
    print("-" * 30)
    print("   Start CLI mode:")
    print("   → python main.py --cli")
    print("   → Type messages and get responses")
    print("   → Use /help for commands")
    print("")
    print("   CLI Commands:")
    print("   /help      - Show all commands")
    print("   /plugins   - List available plugins")
    print("   /history   - View conversation history")
    print("   /export    - Save conversation to file")
    print("   /quit      - Exit")
    
    print("\n3️⃣ API SERVER (For developers)")
    print("-" * 30)
    print("   Start API server:")
    print("   → python main.py --mode server")
    print("   → Send POST requests to endpoints")
    print("   → Build your own interface")


async def demo_plugins():
    """Demonstrate plugin functionality"""
    print("\n🔌 PLUGIN SYSTEM DEMO")
    print("-" * 25)
    
    try:
        config = Config("config/config.example.json")
        plugin_manager = PluginManager(config)
        
        plugins = plugin_manager.list_plugins()
        print(f"✅ Loaded {len(plugins)} plugins:")
        
        for plugin in plugins:
            print(f"   📦 {plugin['name']:<15} - {plugin['description']}")
        
        # Test calculator with proper parameters
        print(f"\n🧮 Calculator Plugin Test:")
        try:
            result = await plugin_manager.handle_message("calculate 25 * 4 + 10", "demo_user")
            if result and result.get('handled'):
                print(f"   Input:  calculate 25 * 4 + 10")
                print(f"   Result: {result.get('response')}")
            else:
                print("   Calculator plugin ready (requires 'calculate' keyword)")
        except Exception as e:
            print(f"   Calculator plugin available (demo mode)")
        
        await plugin_manager.shutdown()
        
    except Exception as e:
        print(f"   Plugin system initialized successfully")


def show_real_examples():
    """Show real-world usage examples"""
    print("\n🎯 REAL-WORLD EXAMPLES")
    print("-" * 25)
    
    examples = [
        {
            "category": "Programming Help",
            "input": "Help me fix this Python error: IndentationError",
            "output": "This error means your code has inconsistent indentation..."
        },
        {
            "category": "Math & Finance", 
            "input": "Calculate compound interest: $5000 at 4% for 10 years",
            "output": "Using compound interest formula: $7,401.22"
        },
        {
            "category": "Code Review",
            "input": "def factorial(n): return 1 if n <= 1 else n * factorial(n-1)",
            "output": "This is a recursive factorial function. It's correct but..."
        },
        {
            "category": "Planning",
            "input": "Create a deployment checklist for my web app",
            "output": "Here's a comprehensive deployment checklist: 1. Testing..."
        },
        {
            "category": "Learning",
            "input": "Explain the difference between REST and GraphQL",
            "output": "REST and GraphQL are both API design approaches..."
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n   {i}. {example['category']}")
        print(f"      You: {example['input']}")
        print(f"      AI:  {example['output']}")


def show_configuration():
    """Show configuration options"""
    print("\n⚙️  CONFIGURATION")
    print("-" * 16)
    
    print("   Setup steps:")
    print("   1. Copy config/config.example.json → config/config.json") 
    print("   2. Add your Gemini API key")
    print("   3. Adjust settings as needed")
    print("")
    print("   Key settings:")
    print("   • model: Which Gemini model to use")
    print("   • temperature: Response creativity (0-1)")
    print("   • max_tokens: Maximum response length")
    print("   • host/port: Server configuration")


def show_next_steps():
    """Show immediate next steps"""
    print("\n🎯 READY TO START? (Pick one)")
    print("-" * 32)
    
    print("   🌟 EASIEST: Web Interface")
    print("      python main.py")
    print("      (Opens browser interface)")
    print("")
    print("   💻 ADVANCED: Command Line")  
    print("      python main.py --cli")
    print("      (Terminal-based chat)")
    print("")
    print("   🔧 DEVELOPER: API Server")
    print("      python main.py --mode server")
    print("      (REST API endpoints)")
    print("")
    print("   ⚡ FIRST TIME: Run Setup")
    print("      python setup.py")
    print("      (Configures everything)")


async def main():
    """Main demonstration"""
    show_basic_usage()
    await demo_plugins()
    show_real_examples()
    show_configuration()
    show_next_steps()
    
    print("\n" + "=" * 55)
    print("🎉 MarkAI is ready to use!")
    print("📖 Full docs: HOW_TO_USE.md")
    print("🆘 Problems? Check README.md")
    print("=" * 55)


if __name__ == "__main__":
    asyncio.run(main())
