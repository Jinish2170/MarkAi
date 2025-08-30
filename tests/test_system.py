"""
Test script for MarkAI - Quick functionality tests
"""

import asyncio
import sys
import os
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.config import Config
from utils.logger import setup_logging, get_logger
from core.ai_engine import MarkAICore
from memory.conversation_manager import ConversationManager
from memory.context_manager import ContextManager
from plugins.plugin_manager import PluginManager


@pytest.mark.asyncio
async def test_config():
    """Test configuration loading"""
    print("🔧 Testing Configuration...")
    try:
        config = Config("config/config.example.json")
        print(f"  ✓ Config loaded: {config.gemini_model}")
        print(f"  ✓ Server: {config.server_host}:{config.server_port}")
        return True
    except Exception as e:
        print(f"  ❌ Config error: {str(e)}")
        return False


@pytest.mark.asyncio
async def test_logging():
    """Test logging system"""
    print("📝 Testing Logging...")
    try:
        setup_logging(log_level="INFO", log_file="logs/test.log")
        logger = get_logger("test")
        logger.info("Test log message")
        print("  ✓ Logging system working")
        return True
    except Exception as e:
        print(f"  ❌ Logging error: {str(e)}")
        return False


@pytest.mark.asyncio
async def test_memory_managers():
    """Test memory management systems"""
    print("🧠 Testing Memory Managers...")
    try:
        config = Config("config/config.example.json")
        
        # Test conversation manager
        conv_manager = ConversationManager(config)
        user_id = "test_user"
        conv_id = conv_manager.create_conversation(user_id, "Test Conversation")
        print(f"  ✓ Created conversation: {conv_id}")
        
        # Test context manager
        context_manager = ContextManager(config)
        context = await context_manager.get_user_context(user_id)
        print(f"  ✓ Got user context: {context['user_id']}")
        
        return True
    except Exception as e:
        print(f"  ❌ Memory manager error: {str(e)}")
        return False


@pytest.mark.asyncio
async def test_plugin_system():
    """Test plugin system"""
    print("🔌 Testing Plugin System...")
    try:
        config = Config("config/config.example.json")
        plugin_manager = PluginManager(config)
        
        # Wait a moment for plugins to load
        await asyncio.sleep(0.5)
        
        plugins = plugin_manager.list_plugins()
        print(f"  ✓ Loaded {len(plugins)} plugins")
        
        for plugin in plugins:
            print(f"    - {plugin['name']}: {plugin['description']}")
        
        # Test calculator plugin
        response = await plugin_manager.handle_message("calculate 2 + 2", "test_user")
        if response:
            print(f"  ✓ Calculator plugin works: {response.get('content', 'No content')}")
        
        await plugin_manager.shutdown()
        return True
    except Exception as e:
        print(f"  ❌ Plugin system error: {str(e)}")
        return False


@pytest.mark.asyncio
async def test_ai_engine():
    """Test AI engine (without API key)"""
    print("🤖 Testing AI Engine...")
    try:
        config = Config("config/config.example.json")
        
        # Override API key to empty for testing
        config.set('api.gemini.api_key', '')
        
        # This should initialize but fail on actual API call
        ai_engine = MarkAICore(config)
        print("  ✓ AI Engine initialized")
        
        # Test health status
        health = await ai_engine.get_health_status()
        print(f"  ✓ Health status: {health['status']}")
        
        await ai_engine.shutdown()
        return True
    except Exception as e:
        print(f"  ❌ AI Engine error: {str(e)}")
        return False


@pytest.mark.asyncio
async def test_utilities():
    """Test utility functions"""
    print("🛠️  Testing Utilities...")
    try:
        from utils.helpers import (
            generate_id, safe_json_loads, format_timestamp,
            truncate_text, calculate_similarity, Timer
        )
        
        # Test ID generation
        test_id = generate_id("test", 8)
        print(f"  ✓ Generated ID: {test_id}")
        
        # Test JSON handling
        data = safe_json_loads('{"test": "value"}')
        print(f"  ✓ JSON parsing: {data}")
        
        # Test text utilities
        timestamp = format_timestamp()
        print(f"  ✓ Timestamp: {timestamp}")
        
        truncated = truncate_text("This is a long text", 10)
        print(f"  ✓ Text truncation: {truncated}")
        
        similarity = calculate_similarity("hello world", "hello earth")
        print(f"  ✓ Text similarity: {similarity:.2f}")
        
        # Test timer
        with Timer("Test operation") as timer:
            await asyncio.sleep(0.1)
        print(f"  ✓ Timer: {timer}")
        
        return True
    except Exception as e:
        print(f"  ❌ Utilities error: {str(e)}")
        return False


async def main():
    """Main test function"""
    print("🚀 MarkAI System Tests")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_config),
        ("Logging", test_logging),
        ("Memory Managers", test_memory_managers),
        ("Plugin System", test_plugin_system),
        ("AI Engine", test_ai_engine),
        ("Utilities", test_utilities),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
            print()  # Add spacing
        except Exception as e:
            print(f"  ❌ Unexpected error in {test_name}: {str(e)}")
            results.append((test_name, False))
            print()
    
    # Summary
    print("=" * 50)
    print("📊 Test Results:")
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
        
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {passed + failed} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! MarkAI is ready to use.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check the configuration and dependencies.")
    
    return failed == 0


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        sys.exit(1)
