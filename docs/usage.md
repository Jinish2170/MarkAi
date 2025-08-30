# 🚀 How to Use MarkAI - Complete Guide

## 🎯 Quick Start (3 Steps)

### Step 1: Setup Configuration
```bash
cd d:\files\coding\genAi\MarkAi
python setup.py
```
This will:
- Install dependencies
- Create configuration files
- Set up your Gemini API key
- Create necessary directories

### Step 2: Choose Your Interface

#### Option A: Web Interface (Recommended for beginners)
```bash
python main.py
# Opens server at http://localhost:8000
```

#### Option B: Command Line Interface
```bash
python main.py --cli
```

#### Option C: API Server for Development
```bash
python main.py --mode server --host 0.0.0.0 --port 8000
```

### Step 3: Start Chatting!
Your MarkAI assistant is now ready to help with various tasks!

---

## 🌐 Web Interface Usage

### Starting the Web Server
```bash
python main.py
```

### What You Can Do:
1. **Chat with AI**: Type messages and get intelligent responses
2. **Use Plugins**: Built-in calculator, weather, file manager, code analyzer, task manager
3. **View History**: See your conversation history
4. **Manage Preferences**: Customize your experience
5. **Export Conversations**: Save your chats

### Example Web Conversations:
- "Calculate 15% tip on $42.50"
- "What's the weather like today?"
- "Help me analyze this Python code: [paste code]"
- "Create a task list for my project"
- "Summarize this document for me"

---

## 💻 Command Line Interface Usage

### Starting CLI Mode
```bash
python main.py --cli
```

### CLI Commands:
- `/help` - Show all available commands
- `/history` - View conversation history
- `/stats` - Show usage statistics
- `/plugins` - List available plugins
- `/preferences` - Manage settings
- `/context` - Show current context
- `/export` - Export conversation
- `/new` - Start new conversation
- `/clear` - Clear screen
- `/quit` - Exit MarkAI

### Example CLI Session:
```
MarkAI > Hello! How can I help you today?

You > Calculate the square root of 144

MarkAI > Using the calculator plugin:
The square root of 144 is 12.0

You > /plugins
Available Plugins:
- calculator: Performs mathematical calculations
- weather: Provides weather information  
- file_manager: Helps with file operations
- code_analyzer: Analyzes code snippets
- task_manager: Simple task management

You > What can the code analyzer do?

MarkAI > The code analyzer plugin can help you:
- Analyze Python, JavaScript, and other code snippets
- Identify potential issues and improvements
- Explain code functionality
- Suggest optimizations
- Check for common coding patterns
```

---

## 🔌 Plugin System Usage

MarkAI comes with 5 built-in plugins:

### 1. Calculator Plugin
```
You: "What's 15% of $250?"
AI: "15% of $250 is $37.50"

You: "Calculate compound interest: $1000 at 5% for 3 years"
AI: "Using compound interest formula: $1,157.63"
```

### 2. Weather Plugin
```
You: "What's the weather like?"
AI: "I'll help you get weather information. What city would you like to check?"

You: "Weather in New York"
AI: "[Weather information for New York]"
```

### 3. File Manager Plugin
```
You: "List files in my documents folder"
AI: "[Lists files and provides file management options]"

You: "Create a new folder called 'AI_Projects'"
AI: "Folder 'AI_Projects' created successfully"
```

### 4. Code Analyzer Plugin
```python
You: "Analyze this code:
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)"

AI: "This is a recursive Fibonacci implementation. Here's my analysis:
- Function: Calculates Fibonacci numbers
- Issue: Inefficient for large numbers (exponential time)
- Suggestion: Use dynamic programming or memoization
- Alternative implementation: [provides optimized version]"
```

### 5. Task Manager Plugin
```
You: "Create a task: Finish MarkAI documentation"
AI: "Task created: 'Finish MarkAI documentation' with ID task_001"

You: "List my tasks"
AI: "Your tasks:
1. Finish MarkAI documentation (Pending)
2. Test import functionality (Completed)"
```

---

## 🛠️ API Usage for Developers

### Start API Server
```bash
python main.py --mode server
```

### API Endpoints:

#### Chat with AI
```python
import requests

response = requests.post('http://localhost:8000/api/chat', json={
    'message': 'Hello, how are you?',
    'user_id': 'user123',
    'conversation_id': 'conv456'  # optional
})

print(response.json())
```

#### Get Conversation History
```python
response = requests.get('http://localhost:8000/api/conversations/conv456/history')
print(response.json())
```

#### Use Plugins via API
```python
response = requests.post('http://localhost:8000/api/chat', json={
    'message': 'Calculate 25 * 4 + 10',
    'user_id': 'user123'
})
# AI will automatically use calculator plugin
```

---

## 🎨 Customization Options

### 1. Configuration Settings
Edit `config/config.json`:
```json
{
  "api": {
    "gemini": {
      "model": "gemini-1.5-pro-latest",
      "temperature": 0.7,
      "max_tokens": 2048
    }
  },
  "server": {
    "host": "localhost",
    "port": 8000,
    "debug": false
  },
  "memory": {
    "max_conversations": 1000,
    "context_window": 10
  }
}
```

### 2. User Preferences
```
You: "/preferences set response_style casual"
AI: "Response style set to casual"

You: "/preferences set max_tokens 1500"
AI: "Maximum tokens set to 1500"
```

### 3. Custom Plugins
Create your own plugins in `plugins/custom/`:
```python
from plugins.plugin_manager import BasePlugin

class MyCustomPlugin(BasePlugin):
    def __init__(self):
        super().__init__(
            name="my_plugin",
            description="My custom functionality",
            version="1.0.0"
        )
    
    async def handle_message(self, message: str, context: dict) -> dict:
        # Your custom logic here
        pass
```

---

## 📝 Real-World Use Cases

### 1. Programming Assistant
```
You: "Help me debug this Python error: KeyError: 'username'"
AI: "This KeyError suggests you're trying to access a dictionary key 'username' that doesn't exist..."

You: "Write a function to validate email addresses"
AI: "[Provides complete email validation function with explanation]"
```

### 2. Data Analysis Helper
```
You: "I have sales data for Q1. Help me calculate growth rate"
AI: "I'll help you calculate the growth rate. Please provide your Q1 and previous quarter data..."

You: "Calculate: January: $50k, February: $65k, March: $78k"
AI: "Your Q1 performance shows strong growth:
- Feb vs Jan: 30% increase
- Mar vs Feb: 20% increase
- Overall Q1 growth: 56%"
```

### 3. Learning and Research
```
You: "Explain machine learning in simple terms"
AI: "[Provides clear explanation with examples]"

You: "What are the pros and cons of microservices architecture?"
AI: "[Detailed analysis of microservices with practical examples]"
```

### 4. Task Planning
```
You: "Help me plan a software deployment"
AI: "Here's a deployment checklist:
1. Code review and testing
2. Database migrations
3. Backup current version
4. Deploy to staging
5. Run integration tests
6. Deploy to production
7. Monitor for issues

Would you like me to elaborate on any step?"
```

---

## 🚀 Advanced Features

### 1. Memory and Context
MarkAI remembers your conversations and learns your preferences:
```
You: "Remember that I prefer Python for backend development"
AI: "I'll remember your preference for Python in backend development"

[Later in conversation]
You: "What's the best language for my API server?"
AI: "Given your preference for Python, I'd recommend FastAPI or Django..."
```

### 2. Multi-turn Conversations
```
You: "I'm building a web app"
AI: "Great! What type of web app are you building?"

You: "An e-commerce platform"
AI: "For an e-commerce platform, you'll need to consider..."

You: "What about payment processing?"
AI: "For payment processing in your e-commerce platform, here are the options..."
```

### 3. Export and Sharing
```bash
# Export conversation to file
/export

# Creates timestamped file: conversation_20250830_165500.txt
```

---

## 🎯 Getting Started Right Now

### Option 1: Quick Test (Web Interface)
```bash
cd d:\files\coding\genAi\MarkAi
python main.py
# Open browser to http://localhost:8000
# Start chatting!
```

### Option 2: CLI Experience
```bash
cd d:\files\coding\genAi\MarkAi
python main.py --cli
# Type: "Hello! Help me get started with MarkAI"
```

### Option 3: Test All Features
```bash
cd d:\files\coding\genAi\MarkAi
python test_system.py  # Verify everything works
python main.py --cli   # Start using it
```

---

## 🆘 Need Help?

- Run `python main.py --help` for all options
- Check `README.md` for detailed documentation
- Use `/help` in CLI mode for commands
- Check `IMPORT_SOLUTIONS.md` if you have import issues
- All configuration is in `config/config.json`

**You're ready to use MarkAI! Start with the web interface for the easiest experience! 🎉**
