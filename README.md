# MarkAI - Advanced AI Assistant

## 🚀 Overview

MarkAI is a sophisticated enterprise-grade AI assistant built with Google's Gemini API at its core. It features advanced cognitive capabilities, comprehensive memory management, and a professional modular architecture designed for extensibility and production use.

## 🌟 Key Features

### 🧠 Advanced Intelligence
- **Multi-type Reasoning**: Analytical, creative, strategic, and ethical reasoning modes
- **Cognitive Architecture**: Chain-of-thought processing with meta-cognition
- **Memory Networks**: Episodic and semantic memory with consolidation
- **Multi-modal Processing**: Text, images, documents, and voice inputs
- **Adaptive Learning**: Personalization based on user interactions

### 🏗️ Enterprise Architecture
- **Professional Package Structure**: Clean `src/markai/` package layout
- **Memory Management**: Advanced conversation and context management with SQLite persistence
- **Plugin Ecosystem**: Extensible system with enterprise-grade plugins
- **Multiple Interfaces**: CLI, Web UI, and REST API
- **Real-time Monitoring**: Cognitive state monitoring and analytics

### 🔧 Production Ready
- **Scalable Design**: Modular architecture for enterprise deployment
- **Security**: Encrypted communications and data protection
- **Configuration Management**: YAML-based configuration system
- **Comprehensive Logging**: Structured logging with multiple levels
- **Testing Framework**: Unit tests and integration testing

## 🏗️ Project Structure

```
MarkAI/
├── src/markai/              # Main package source code
│   ├── __init__.py         # Package initialization
│   ├── main.py             # Application entry point
│   ├── core/               # Core AI engine components
│   │   ├── __init__.py
│   │   ├── advanced_ai_engine.py    # Main AI engine
│   │   └── ai_engine.py             # Base engine
│   ├── memory/             # Memory and context management
│   │   ├── __init__.py
│   │   ├── conversation_manager.py  # Conversation persistence
│   │   └── context_manager.py       # Context and memory
│   ├── api/                # Web API and server
│   │   ├── __init__.py
│   │   ├── advanced_server.py       # FastAPI server
│   │   └── server.py               # Base server
│   ├── cli/                # Command line interfaces
│   │   ├── __init__.py
│   │   ├── advanced_interface.py   # Rich CLI interface
│   │   └── interface.py            # Basic CLI
│   ├── plugins/            # Plugin system
│   │   ├── __init__.py
│   │   ├── plugin_manager.py       # Plugin management
│   │   └── advanced_plugins.py     # Core plugins
│   └── utils/              # Utilities and helpers
│       ├── __init__.py
│       ├── config.py              # Configuration management
│       ├── logger.py              # Logging utilities
│       └── helpers.py             # General helpers
├── config/                 # Configuration files
├── data/                   # Data storage (conversations, cache)
├── tests/                  # Test suite
├── examples/               # Usage examples
├── docs/                   # Documentation
├── main.py                 # Main entry point
├── setup.py               # Package setup
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
└── README.md             # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key
- 4GB+ RAM recommended for optimal performance

### Quick Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/MarkAI.git
   cd MarkAI
   ```

2. **Install core dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Or install minimal dependencies:
   ```bash
   pip install google-generativeai faiss-cpu sentence-transformers rich fastapi uvicorn
   ```

3. **Set up configuration:**
   ```bash
   # Copy example configuration
   cp config/config.example.yaml config/config.yaml
   
   # Edit config.yaml with your Google Gemini API key
   # Set other preferences as needed
   ```

4. **Test the installation:**
   ```bash
   python main.py --banner
   ```

### 🎯 Usage Options

#### CLI Interface (Recommended)
```bash
# Start advanced CLI with rich formatting
python main.py cli

# CLI with specific reasoning mode
python main.py cli --mode deep --monitor

# Get CLI help
python main.py cli --help
```

#### Web Interface
```bash
# Start web server (default: localhost:8000)
python main.py web

# Custom host and port
python main.py web --host 0.0.0.0 --port 8080

# Get web interface help
python main.py web --help
```

#### Show Capabilities
```bash
# Display full feature banner
python main.py --banner

# Show version and system info
python main.py --version

# Enable debug logging
python main.py --debug cli
```

## 💡 Advanced Usage Examples

### CLI Interface Features
```bash
# Start interactive CLI with all features
python main.py cli

# Enable cognitive monitoring
python main.py cli --monitor

# Use specific reasoning modes
python main.py cli --mode analytical    # For logical analysis
python main.py cli --mode creative      # For creative tasks
python main.py cli --mode strategic     # For planning
python main.py cli --mode ethical       # For ethical reasoning

# Process files and documents
python main.py cli --file document.pdf
python main.py cli --image photo.jpg
```

### Web Interface Features
```bash
# Start full-featured web server
python main.py web --host 0.0.0.0 --port 8080

# Enable development mode with hot reload
python main.py web --debug --reload
```

### Memory System Usage
The advanced memory system automatically:
- **Conversation Persistence**: Stores all conversations in SQLite database
- **Context Management**: Manages context windows and memory consolidation  
- **Export Capabilities**: Export conversations to various formats
- **Search & Analytics**: Search through conversation history

### Plugin Development
```python
# Example custom plugin
from markai.plugins.plugin_manager import BasePlugin

class MyCustomPlugin(BasePlugin):
    def get_name(self) -> str:
        return "My Custom Plugin"
    
    async def process(self, input_data: str) -> str:
        # Your custom processing logic
        return f"Processed: {input_data}"
```

### API Integration
```python
import requests
import asyncio

# Basic chat API
response = requests.post("http://localhost:8000/chat", json={
    "message": "Explain quantum computing",
    "conversation_id": "user_123",
    "reasoning_mode": "analytical"
})
print(response.json())

# Advanced API with file upload
files = {"file": open("document.pdf", "rb")}
data = {"conversation_id": "user_123"}
response = requests.post("http://localhost:8000/process_file", files=files, data=data)
print(response.json())

# WebSocket for real-time communication
import websocket

def on_message(ws, message):
    print(f"Received: {message}")

ws = websocket.WebSocketApp("ws://localhost:8000/ws",
                          on_message=on_message)
ws.run_forever()
```

## 🔧 Configuration & Customization

### Configuration Files
The system uses YAML configuration files in the `config/` directory:

```yaml
# config/config.yaml (main configuration)
gemini:
  api_key: "your_api_key_here"
  model: "gemini-1.5-pro"
  
memory:
  max_context_length: 8000
  context_window_overlap: 200
  memory_decay_rate: 0.95
  
plugins:
  enabled: 
    - "web_research"
    - "code_analysis"
    - "document_processor"
    
interface:
  cli_theme: "dark"
  web_host: "localhost"
  web_port: 8000
  
logging:
  level: "INFO"
  file: "logs/markai.log"
```

### Advanced Settings
- **Memory Management**: Control context windows and memory consolidation
- **Reasoning Modes**: Configure different reasoning strategies  
- **Plugin System**: Enable/disable specific plugins
- **Performance Tuning**: Adjust batch sizes and processing limits
- **Security**: Configure encryption and access controls
## 🏗️ Architecture & Components

### Core Components

#### 🧠 Advanced AI Engine (`src/markai/core/`)
- **AdvancedMarkAICore**: Main AI engine with cognitive capabilities
- **Multi-modal Processing**: Handle text, images, documents
- **Reasoning Types**: Analytical, creative, strategic, ethical
- **Chain-of-thought**: Advanced reasoning with meta-cognition
- **Learning & Adaptation**: Continuous improvement from interactions

#### 💾 Memory System (`src/markai/memory/`)
- **ConversationManager**: SQLite-based conversation persistence
  - Store and retrieve conversation history
  - Export conversations (JSON, Markdown, CSV)
  - Search and analytics capabilities
  - Conversation statistics and insights
- **ContextManager**: Advanced context and memory management
  - Context window management with overlap
  - Memory consolidation and cleanup  
  - Long-term and working memory storage
  - Context summarization and key point extraction

#### � Plugin System (`src/markai/plugins/`)
- **BasePlugin**: Foundation for custom plugins
- **PluginManager**: Load, manage, and execute plugins
- **Built-in Plugins**:
  - Web Research Plugin
  - Code Analysis Plugin  
  - Document Processing Plugin
  - File System Plugin
  - Database Query Plugin

#### 🌐 Interfaces (`src/markai/cli/` & `src/markai/api/`)
- **Advanced CLI**: Rich terminal interface with formatting
- **Web Interface**: FastAPI-based web server
- **REST API**: Comprehensive API endpoints
- **WebSocket Support**: Real-time communication

#### 🛠️ Utilities (`src/markai/utils/`)
- **Configuration Management**: YAML-based config system
- **Logging System**: Structured logging with multiple levels
- **Helper Functions**: Common utilities and tools

### 📊 Performance Features
- **Async Processing**: Non-blocking operations throughout
- **Memory Optimization**: Efficient context management
- **Caching**: Intelligent caching of responses and embeddings
- **Batch Processing**: Optimize bulk operations
- **Resource Monitoring**: Track memory and CPU usage

## � Dependencies & Requirements

### Core Dependencies
```bash
# Essential AI & ML libraries
google-generativeai>=0.3.2    # Google Gemini API
sentence-transformers>=2.2.2   # Text embeddings
faiss-cpu>=1.7.4              # Vector similarity search
networkx>=3.0                 # Graph algorithms

# Web framework & API
fastapi>=0.104.0              # Modern web framework
uvicorn>=0.24.0               # ASGI server
websockets>=12.0              # WebSocket support

# CLI & interface
rich>=13.0.0                  # Rich terminal formatting
click>=8.0.0                  # CLI framework
prompt-toolkit>=3.0.0         # Interactive prompts

# Data processing
pandas>=2.0.0                 # Data manipulation
numpy>=1.24.0                 # Numerical computing
SQLAlchemy>=2.0.0            # Database ORM

# Additional capabilities
PyYAML>=6.0                   # Configuration files
requests>=2.28.0              # HTTP client
Pillow>=9.0.0                 # Image processing
```

### Development Dependencies
```bash
pytest>=7.0.0                 # Testing framework
black>=23.0.0                 # Code formatting
flake8>=6.0.0                 # Linting
mypy>=1.0.0                   # Type checking
```

## 🚀 Development & Deployment

### Local Development
```bash
# Clone and setup
git clone <repository>
cd MarkAI
pip install -r requirements.txt

# Run in development mode
python main.py --debug cli

# Run tests
pytest tests/

# Code formatting
black src/
flake8 src/
```

### Production Deployment
```bash
# Install production dependencies
pip install -r requirements.txt --no-dev

# Configure for production
export MARKAI_CONFIG_PATH="/etc/markai/config.yaml"
export MARKAI_LOG_LEVEL="INFO"

# Run web server
python main.py web --host 0.0.0.0 --port 8000

# Or use gunicorn for production
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.markai.api.advanced_server:app
```

## 🧪 Testing & Quality

### Running Tests
```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/test_memory.py      # Memory system tests
pytest tests/test_ai_engine.py   # AI engine tests
pytest tests/test_plugins.py     # Plugin system tests

# Coverage report
pytest --cov=src/markai tests/
```

### Code Quality
- **Type Hints**: Full type annotation coverage
- **Documentation**: Comprehensive docstrings
- **Testing**: Unit and integration tests
- **Linting**: Enforced code style with flake8
- **Formatting**: Consistent formatting with black

## � Security & Privacy

### Security Features
- **API Key Management**: Secure storage of sensitive credentials
- **Input Validation**: Comprehensive input sanitization
- **Rate Limiting**: API request throttling
- **Logging Security**: No sensitive data in logs
- **Encryption**: Data encryption at rest and in transit

### Privacy Considerations
- **Local Processing**: Core processing happens locally
- **Data Control**: Full control over conversation data
- **Export Options**: Easy data export and deletion
- **Anonymization**: Built-in data anonymization options

## 📚 Documentation & Resources

### 📖 Documentation Structure
```
docs/
├── user_guide/              # User documentation
│   ├── installation.md     # Detailed installation guide
│   ├── configuration.md    # Configuration options
│   ├── cli_reference.md    # CLI command reference
│   └── web_interface.md    # Web interface guide
├── developer_guide/         # Developer documentation
│   ├── architecture.md     # System architecture
│   ├── api_reference.md    # API documentation
│   ├── plugin_development.md # Plugin creation guide
│   └── contributing.md     # Contribution guidelines
└── examples/                # Code examples and tutorials
    ├── basic_usage.py      # Basic usage examples
    ├── advanced_features.py # Advanced feature demos
    └── plugin_examples/    # Plugin development examples
```

### 🎓 Learning Resources
- **Getting Started Tutorial**: Step-by-step introduction
- **Video Demonstrations**: Feature walkthrough videos
- **API Examples**: Complete API integration examples
- **Plugin Development**: Custom plugin creation guide
- **Best Practices**: Production deployment guidelines

## 🤝 Contributing

We welcome contributions from the community! Here's how to get involved:

### 🐛 Bug Reports
1. Check existing issues first
2. Create detailed bug reports with reproduction steps
3. Include system information and logs

### ✨ Feature Requests
1. Discuss major changes in issues first
2. Follow the existing code style and patterns
3. Include tests for new functionality
4. Update documentation as needed

### 💻 Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/yourusername/MarkAI.git
cd MarkAI

# Create development environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run tests
pytest
```

### 📋 Contribution Guidelines
- Follow PEP 8 style guidelines
- Write comprehensive tests
- Update documentation
- Use clear commit messages
- Submit focused pull requests

## 🏆 Roadmap & Future Plans

### 🎯 Upcoming Features
- **Multi-Agent Collaboration**: Agent-to-agent communication
- **Advanced Analytics**: Conversation analytics dashboard
- **Cloud Deployment**: Docker and Kubernetes support
- **Mobile Interface**: Mobile-optimized web interface
- **Voice Interface**: Speech-to-text and text-to-speech
- **Integration Hub**: Popular service integrations

### 🚀 Performance Improvements
- **GPU Acceleration**: CUDA support for faster processing
- **Distributed Processing**: Multi-node deployment support
- **Advanced Caching**: Redis integration for scalability
- **Stream Processing**: Real-time data processing

## 📄 License & Legal

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses
- Google Generative AI: Google API Terms of Service
- FastAPI: MIT License
- Rich: MIT License
- See `requirements.txt` for complete dependency list

### Citation
If you use MarkAI in your research or projects, please cite:
```bibtex
@software{markai2025,
  title={MarkAI: Advanced AI Assistant with Cognitive Intelligence},
  author={MarkAI Development Team},
  year={2025},
  url={https://github.com/yourusername/MarkAI}
}
```

## 🙏 Acknowledgments

- **Google**: For the powerful Gemini AI API
- **FastAPI Team**: For the excellent web framework
- **Rich Library**: For beautiful terminal formatting
- **Open Source Community**: For the amazing libraries and tools
- **Contributors**: Everyone who helps improve MarkAI

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/MarkAI?style=social)](https://github.com/yourusername/MarkAI)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/MarkAI?style=social)](https://github.com/yourusername/MarkAI)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/MarkAI)](https://github.com/yourusername/MarkAI/issues)

**Made with ❤️ by the MarkAI Team**

</div>
