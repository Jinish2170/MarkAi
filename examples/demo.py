#!/usr/bin/env python3
"""
MarkAI Demo Script - Shows different ways to use the project

This script demonstrates various usage patterns for MarkAI
without requiring API keys for basic demonstration.
"""

# Setup imports first
from utils.import_helper import setup_project_imports
setup_project_imports()

import asyncio
from datetime import datetime
from core.ai_engine import MarkAICore, AIResponse
from utils.config import Config
from utils.logger import get_logger
from plugins.plugin_manager import PluginManager


async def demo_basic_functionality():
    """Demonstrate basic MarkAI functionality"""
    print("🚀 MarkAI Demo - Basic Functionality")
    print("=" * 50)
    
    # Initialize configuration
    config = Config("config/config.example.json")
    logger = get_logger("demo")
    
    print(f"✅ Configuration loaded: {config.get('api.gemini.model')}")
    print(f"✅ Server will run on: {config.get('server.host')}:{config.get('server.port')}")
    
    # Test plugin system
    print("\n🔌 Testing Plugin System:")
    plugin_manager = PluginManager(config)
    plugins = plugin_manager.list_plugins()
    
    for plugin in plugins:
        print(f"  📦 {plugin['name']}: {plugin['description']}")
    
    # Test calculator plugin
    print(f"\n🧮 Calculator Plugin Demo:")
    calc_result = await plugin_manager.handle_message("calculate 15 * 8 + 22")
    if calc_result and calc_result.get('handled'):
        print(f"  Input: calculate 15 * 8 + 22")
        print(f"  Output: {calc_result.get('response')}")
    
    # Create sample AI response
    print(f"\n🤖 Sample AI Response Structure:")
    sample_response = AIResponse(
        content="Hello! I'm MarkAI, your advanced AI assistant. I can help with calculations, code analysis, task management, and much more!",
        metadata={
            "plugins_used": ["greeting"],
            "confidence": 0.95,
            "processing_time": 0.15
        },
        timestamp=datetime.now(),
        model_used="gemini-1.5-pro-latest",
        tokens_used=45,
        confidence=0.95,
        reasoning_steps=[
            "Detected greeting intent",
            "Prepared introduction message", 
            "Listed capabilities"
        ]
    )
    
    print(f"  Content: {sample_response.content[:100]}...")
    print(f"  Model: {sample_response.model_used}")
    print(f"  Confidence: {sample_response.confidence}")
    print(f"  Tokens: {sample_response.tokens_used}")
    
    await plugin_manager.shutdown()


def demo_cli_commands():
    """Show available CLI commands"""
    print("\n💻 CLI Mode Commands:")
    print("-" * 30)
    
    commands = {
        "/help": "Show all available commands",
        "/history": "View conversation history",
        "/stats": "Show usage statistics",
        "/plugins": "List available plugins",
        "/preferences": "Manage user settings",
        "/context": "Show current context",
        "/export": "Export conversation to file",
        "/new": "Start new conversation",
        "/clear": "Clear screen",
        "/quit": "Exit MarkAI"
    }
    
    for cmd, desc in commands.items():
        print(f"  {cmd:<12} - {desc}")


def demo_api_usage():
    """Show API usage examples"""
    print("\n🌐 API Usage Examples:")
    print("-" * 30)
    
    print("📤 Send a chat message:")
    print("""
curl -X POST http://localhost:8000/api/chat \\
  -H "Content-Type: application/json" \\
  -d '{
    "message": "Calculate 25 * 4",
    "user_id": "demo_user",
    "conversation_id": "demo_conv_001"
  }'
    """)
    
    print("📥 Get conversation history:")
    print("""
curl -X GET http://localhost:8000/api/conversations/demo_conv_001/history
    """)
    
    print("🔧 Get user preferences:")
    print("""
curl -X GET http://localhost:8000/api/users/demo_user/preferences
    """)


def demo_use_cases():
    """Show real-world use cases"""
    print("\n🎯 Real-World Use Cases:")
    print("-" * 30)
    
    use_cases = [
        {
            "title": "Programming Assistant",
            "example": "Help me debug this Python error: NameError: name 'x' is not defined",
            "response": "This error means you're trying to use variable 'x' before defining it..."
        },
        {
            "title": "Math & Calculations", 
            "example": "What's 15% tip on $87.50?",
            "response": "15% tip on $87.50 is $13.13, making the total $100.63"
        },
        {
            "title": "Code Analysis",
            "example": "Analyze this function for performance issues",
            "response": "I'll review your code for efficiency, readability, and best practices..."
        },
        {
            "title": "Task Management",
            "example": "Create a task list for my web development project",
            "response": "Here's a structured task list: 1. Setup, 2. Backend, 3. Frontend..."
        },
        {
            "title": "Learning & Explanation",
            "example": "Explain how async/await works in Python",
            "response": "Async/await in Python allows for concurrent programming..."
        }
    ]
    
    for i, case in enumerate(use_cases, 1):
        print(f"\n{i}. {case['title']}:")
        print(f"   You: \"{case['example']}\"")
        print(f"   AI: \"{case['response']}\"")


def demo_getting_started():
    """Show getting started steps"""
    print("\n🚀 Getting Started (Choose Your Path):")
    print("-" * 50)
    
    print("📍 Option 1: Web Interface (Easiest)")
    print("   1. python main.py")
    print("   2. Open browser: http://localhost:8000")
    print("   3. Start chatting!")
    
    print("\n📍 Option 2: Command Line")
    print("   1. python main.py --cli") 
    print("   2. Type your questions")
    print("   3. Use /help for commands")
    
    print("\n📍 Option 3: API Development")
    print("   1. python main.py --mode server")
    print("   2. Use REST API endpoints")
    print("   3. Build your own interface")
    
    print("\n⚠️  First Time Setup:")
    print("   • Run: python setup.py")
    print("   • Add your Gemini API key to config/config.json")
    print("   • Copy config/config.example.json to config/config.json")


async def main():
    """Main demo function"""
    print("🎉 Welcome to MarkAI - Your Advanced AI Assistant!")
    print("=" * 60)
    
    try:
        # Run basic functionality demo
        await demo_basic_functionality()
        
        # Show other usage information
        demo_cli_commands()
        demo_api_usage()
        demo_use_cases()
        demo_getting_started()
        
        print("\n" + "=" * 60)
        print("✨ MarkAI is ready to use! Choose your preferred interface above.")
        print("📚 Check HOW_TO_USE.md for complete documentation.")
        print("🆘 Need help? Check README.md or run with --help flag.")
        
    except Exception as e:
        print(f"❌ Demo error: {str(e)}")
        print("💡 This is just a demo. For full functionality, ensure:")
        print("   • Config file is properly set up")
        print("   • Gemini API key is configured")
        print("   • All dependencies are installed")


if __name__ == "__main__":
    asyncio.run(main())
