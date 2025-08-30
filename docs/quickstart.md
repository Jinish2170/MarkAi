# MarkAI - Quick Start Guide

Welcome to MarkAI! This guide will help you get started quickly.

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Your Gemini API Key
1. Go to [Google AI Studio](https://ai.google.dev/)
2. Create an account or sign in
3. Generate a new API key
4. Keep it safe - you'll need it in the next step

### Step 2: Run the Setup Script
```bash
python setup.py
```
This will:
- Install all dependencies
- Create necessary directories
- Set up your configuration
- Prompt for your Gemini API key

### Step 3: Start MarkAI
```bash
# Web interface (recommended)
python main.py

# Command line interface
python main.py --cli
```

### Step 4: Open Your Browser
- Go to http://localhost:8000
- Start chatting with MarkAI!

## 🔧 Manual Setup (if needed)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Configuration
```bash
# Copy the example config
cp config/config.example.json config/config.json

# Edit config.json and add your Gemini API key
```

### 3. Create Directories
```bash
mkdir -p data logs memory/vectors plugins/custom exports
```

## 💡 Features Overview

### Core Features
- **Smart Conversations**: Context-aware responses with memory
- **Plugin System**: Extensible with built-in calculator, file manager, etc.
- **Multi-Interface**: Web UI, CLI, and REST API
- **User Preferences**: Learns your communication style
- **Conversation History**: Persistent storage and search

### Built-in Plugins
- **Calculator**: Perform mathematical calculations
- **File Manager**: Basic file operations
- **Code Analyzer**: Analyze code snippets
- **Task Manager**: Simple task tracking
- **Weather**: Weather information (requires API key)

## 📱 Usage Examples

### Web Interface
1. Open http://localhost:8000
2. Type your message
3. Get intelligent responses with context awareness

### CLI Interface
```bash
python main.py --cli

# Available commands:
/help      - Show help
/history   - View conversation history
/stats     - Show your statistics
/plugins   - List available plugins
/preferences - Manage your preferences
/quit      - Exit MarkAI
```

### API Usage
```python
import requests

response = requests.post('http://localhost:8000/api/chat', json={
    'message': 'Hello, MarkAI!',
    'user_id': 'your_user_id'
})

print(response.json()['response'])
```

## 🔍 Testing Your Installation

Run the system test to verify everything is working:
```bash
python test_system.py
```

This will test:
- Configuration loading
- Memory management
- Plugin system
- Core utilities

## 🎛️ Configuration Options

Edit `config/config.json` to customize:

```json
{
  "api": {
    "gemini": {
      "model": "gemini-1.5-pro-latest",
      "temperature": 0.7,
      "max_tokens": 8192
    }
  },
  "server": {
    "host": "localhost",
    "port": 8000
  },
  "memory": {
    "max_conversations": 1000,
    "max_tokens_per_conversation": 50000
  },
  "features": {
    "voice_enabled": true,
    "image_processing": true,
    "plugin_system": true
  }
}
```

## 🔌 Creating Custom Plugins

Create a new file in `plugins/custom/`:

```python
from plugins.plugin_manager import BasePlugin

class MyPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "my_plugin"
    
    @property
    def description(self) -> str:
        return "My custom plugin"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def triggers(self) -> List[str]:
        return ["my command"]
    
    async def process_message(self, message, user_id, context=None):
        if "my command" in message.lower():
            return {
                'content': "Hello from my custom plugin!",
                'metadata': {'plugin': self.name}
            }
        return None
```

## 🛠️ Troubleshooting

### Common Issues

**"Configuration validation failed"**
- Check your Gemini API key in `config/config.json`
- Ensure the file exists and is valid JSON

**"Module not found" errors**
- Run `pip install -r requirements.txt`
- Ensure you're using Python 3.8 or higher

**"Port already in use"**
- Change the port in config: `"port": 8001`
- Or kill the process using the port

**Memory/database errors**
- Delete the `data/` directory to reset
- Restart MarkAI

### Getting Help

1. Check the logs in `logs/markai.log`
2. Run `python test_system.py` to diagnose issues
3. Check your configuration file
4. Ensure your Gemini API key is valid

## 📚 Advanced Usage

### Environment Variables
You can override config with environment variables:
```bash
export GEMINI_API_KEY="your-api-key"
export MARKAI_PORT=9000
python main.py
```

### Docker (future feature)
```bash
docker build -t markai .
docker run -p 8000:8000 -e GEMINI_API_KEY="your-key" markai
```

### API Documentation
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 🎯 Tips for Best Results

1. **Be specific**: The more context you provide, the better the responses
2. **Use plugins**: Try "calculate 2+2" or "list files" 
3. **Set preferences**: Use `/preferences` in CLI to customize responses
4. **Regular conversations**: MarkAI learns from your interaction style
5. **Explore commands**: Try different CLI commands to discover features

## 🔐 Security Notes

- Keep your API key secure
- Don't share your configuration file
- MarkAI stores conversation data locally
- Use environment variables for sensitive data

## 🚀 What's Next?

- Explore all the plugins
- Try the API endpoints
- Customize your preferences
- Create custom plugins
- Join the community (if applicable)

---

**Need help?** Run `python main.py --help` or check the full documentation in the `docs/` directory.

**Happy chatting with MarkAI! 🤖**
