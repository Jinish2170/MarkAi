"""
Advanced Web Interface - Enterprise-grade web application

Features:
- Real-time AI conversations with WebSocket support
- Multi-modal interface (text, image, file upload)
- Advanced cognitive state visualization
- Interactive reasoning process display
- Plugin ecosystem management UI
- Advanced analytics and conversation insights
- Responsive modern design with dark/light themes
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, HTTPException, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Any, Optional
import asyncio
import json
import uuid
from datetime import datetime
import base64
from pathlib import Path
import logging

from pydantic import BaseModel, Field

# Setup imports
# from utils.import_helper import setup_project_imports
# setup_project_imports()

from ..core.advanced_ai_engine import AdvancedMarkAICore, ProcessingMode, ReasoningType
from ..utils.config import Config
from ..utils.logger import get_logger


# Pydantic models for API
class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    processing_mode: Optional[str] = "balanced"
    reasoning_type: Optional[str] = "analytical"
    include_reasoning: bool = False
    multimodal_data: Optional[Dict[str, Any]] = None


class ConversationSettings(BaseModel):
    processing_mode: str = "balanced"
    reasoning_type: str = "analytical"
    monitoring_enabled: bool = False
    auto_save: bool = True
    export_format: str = "markdown"


class PluginRequest(BaseModel):
    plugin_name: str
    action: str  # enable, disable, configure
    parameters: Optional[Dict[str, Any]] = None


class WebSocketManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_sessions: Dict[str, Dict] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.user_sessions[user_id] = {
            'connected_at': datetime.now(),
            'conversation_id': None,
            'settings': ConversationSettings()
        }
    
    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]
    
    async def send_message(self, user_id: str, message: Dict[str, Any]):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(json.dumps(message))
    
    async def broadcast(self, message: Dict[str, Any]):
        for user_id in self.active_connections:
            await self.send_message(user_id, message)


class AdvancedWebInterface:
    """Advanced Web Interface with enterprise features"""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = get_logger(__name__)
        
        # Initialize FastAPI app
        self.app = FastAPI(
            title="MarkAI Advanced Web Interface",
            description="Enterprise-grade AI assistant with advanced cognitive capabilities",
            version="1.0.0"
        )
        
        # Initialize components
        self.ai_engine = AdvancedMarkAICore(config)
        self.websocket_manager = WebSocketManager()
        
        # Setup middleware
        self._setup_middleware()
        
        # Setup routes
        self._setup_routes()
        
        # Setup static files and templates
        self._setup_static_files()
    
    def _setup_middleware(self):
        """Setup FastAPI middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure appropriately for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def _setup_routes(self):
        """Setup all API routes"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
            """Serve the main web interface"""
            return self.templates.TemplateResponse("index.html", {"request": request})
        
        @self.app.post("/api/chat")
        async def chat_endpoint(chat_request: ChatMessage):
            """Main chat endpoint for AI conversations"""
            try:
                # Generate user ID if not provided
                user_id = str(uuid.uuid4())
                
                # Create conversation if needed
                if not chat_request.conversation_id:
                    chat_request.conversation_id = await self.ai_engine.conversation_manager.create_conversation(user_id)
                
                # Process message with advanced engine
                response = await self.ai_engine.process_advanced_message(
                    message=chat_request.message,
                    user_id=user_id,
                    conversation_id=chat_request.conversation_id,
                    processing_mode=ProcessingMode(chat_request.processing_mode),
                    reasoning_type=ReasoningType(chat_request.reasoning_type)
                )
                
                # Prepare response
                response_data = {
                    "response": response.content,
                    "conversation_id": chat_request.conversation_id,
                    "confidence": response.confidence,
                    "reasoning_steps": [asdict(step) for step in response.reasoning_steps] if chat_request.include_reasoning else [],
                    "metadata": response.metadata,
                    "safety_assessment": response.safety_assessment
                }
                
                return JSONResponse(content=response_data)
                
            except Exception as e:
                self.logger.error(f"Chat endpoint error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.websocket("/ws/{user_id}")
        async def websocket_endpoint(websocket: WebSocket, user_id: str):
            """WebSocket endpoint for real-time communication"""
            await self.websocket_manager.connect(websocket, user_id)
            
            try:
                # Send welcome message
                await self.websocket_manager.send_message(user_id, {
                    "type": "welcome",
                    "message": "Connected to MarkAI Advanced Interface",
                    "capabilities": await self._get_capabilities_info()
                })
                
                while True:
                    # Receive message from client
                    data = await websocket.receive_text()
                    message_data = json.loads(data)
                    
                    # Handle different message types
                    await self._handle_websocket_message(user_id, message_data)
                    
            except WebSocketDisconnect:
                self.websocket_manager.disconnect(user_id)
            except Exception as e:
                self.logger.error(f"WebSocket error: {e}")
                await self.websocket_manager.send_message(user_id, {
                    "type": "error",
                    "message": str(e)
                })
        
        @self.app.get("/api/cognitive-status")
        async def get_cognitive_status():
            """Get current cognitive status"""
            try:
                status = await self.ai_engine.get_cognitive_status()
                return JSONResponse(content=status)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/conversations/{conversation_id}")
        async def get_conversation(conversation_id: str):
            """Get conversation history"""
            try:
                history = await self.ai_engine.conversation_manager.get_history(conversation_id)
                return JSONResponse(content={"history": history})
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/conversations/{conversation_id}/export")
        async def export_conversation(conversation_id: str, export_format: str = "markdown"):
            """Export conversation in various formats"""
            try:
                # Get conversation history
                history = await self.ai_engine.conversation_manager.get_history(conversation_id)
                
                # Export based on format
                if export_format == "markdown":
                    content = await self._export_markdown(history, conversation_id)
                    media_type = "text/markdown"
                elif export_format == "json":
                    content = json.dumps(history, indent=2)
                    media_type = "application/json"
                else:
                    raise HTTPException(status_code=400, detail="Unsupported export format")
                
                return JSONResponse(
                    content={"content": content, "filename": f"conversation_{conversation_id}.{export_format}"},
                    media_type=media_type
                )
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/plugins")
        async def manage_plugins(plugin_request: PluginRequest):
            """Manage AI plugins"""
            try:
                if plugin_request.action == "list":
                    plugins = await self.ai_engine.plugin_manager.get_available_plugins()
                    return JSONResponse(content={"plugins": plugins})
                elif plugin_request.action == "enable":
                    await self.ai_engine.plugin_manager.enable_plugin(plugin_request.plugin_name)
                    return JSONResponse(content={"message": f"Plugin {plugin_request.plugin_name} enabled"})
                elif plugin_request.action == "disable":
                    await self.ai_engine.plugin_manager.disable_plugin(plugin_request.plugin_name)
                    return JSONResponse(content={"message": f"Plugin {plugin_request.plugin_name} disabled"})
                else:
                    raise HTTPException(status_code=400, detail="Invalid plugin action")
                    
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/upload")
        async def upload_file(file: UploadFile = File(...)):
            """Handle file uploads for multimodal processing"""
            try:
                # Read file content
                content = await file.read()
                
                # Process based on file type
                if file.content_type.startswith('image/'):
                    # Process image
                    result = await self.ai_engine.multimodal_processor.process_image(content)
                elif file.content_type == 'application/pdf':
                    # Process PDF
                    result = await self.ai_engine.multimodal_processor.process_pdf(content)
                else:
                    # Process as text document
                    text_content = content.decode('utf-8')
                    result = await self.ai_engine.multimodal_processor.process_document(text_content)
                
                return JSONResponse(content={
                    "filename": file.filename,
                    "content_type": file.content_type,
                    "processed_content": result
                })
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/analytics/{conversation_id}")
        async def get_conversation_analytics(conversation_id: str):
            """Get advanced conversation analytics"""
            try:
                analytics = await self._generate_conversation_analytics(conversation_id)
                return JSONResponse(content=analytics)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def _setup_static_files(self):
        """Setup static files and templates"""
        # Create directories if they don't exist
        static_dir = Path("static")
        templates_dir = Path("templates")
        static_dir.mkdir(exist_ok=True)
        templates_dir.mkdir(exist_ok=True)
        
        # Mount static files
        self.app.mount("/static", StaticFiles(directory="static"), name="static")
        
        # Setup Jinja2 templates
        self.templates = Jinja2Templates(directory="templates")
        
        # Create basic template if it doesn't exist
        self._create_default_template()
    
    def _create_default_template(self):
        """Create default HTML template"""
        template_path = Path("templates/index.html")
        if not template_path.exists():
            template_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarkAI - Advanced AI Assistant</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        }
        h1 {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #00f5ff, #0080ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            text-align: center;
            opacity: 0.8;
            margin-bottom: 30px;
        }
        .chat-container {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            min-height: 400px;
            max-height: 600px;
            overflow-y: auto;
        }
        .input-container {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        input[type="text"] {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 25px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 16px;
        }
        input[type="text"]::placeholder {
            color: rgba(255, 255, 255, 0.6);
        }
        button {
            padding: 15px 25px;
            border: none;
            border-radius: 25px;
            background: linear-gradient(45deg, #00f5ff, #0080ff);
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        .message {
            margin: 15px 0;
            padding: 15px;
            border-radius: 15px;
            animation: fadeIn 0.3s ease-in;
        }
        .user-message {
            background: linear-gradient(45deg, #00f5ff, #0080ff);
            margin-left: 20%;
            text-align: right;
        }
        .ai-message {
            background: rgba(255, 255, 255, 0.1);
            margin-right: 20%;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .feature-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .status-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.05);
            padding: 10px 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 MarkAI</h1>
        <p class="subtitle">Advanced AI Assistant with Cognitive Intelligence</p>
        
        <div class="status-bar">
            <div>Status: <span id="connection-status">Connecting...</span></div>
            <div>Mode: <span id="processing-mode">Balanced</span></div>
            <div>Reasoning: <span id="reasoning-type">Analytical</span></div>
        </div>
        
        <div class="chat-container" id="chat-container">
            <div class="ai-message">
                <strong>🤖 MarkAI:</strong> Welcome to the Advanced AI Assistant! I'm powered by sophisticated cognitive architecture with multi-modal reasoning, advanced memory networks, and enterprise-grade capabilities. How can I assist you today?
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="message-input" placeholder="Ask me anything... I can reason, analyze, create, and more!" />
            <button onclick="sendMessage()">Send</button>
        </div>
        
        <div class="features">
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <h3>Advanced Reasoning</h3>
                <p>Multi-type reasoning including analytical, creative, logical, emotional, strategic, and ethical modes</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <h3>Deep Analysis</h3>
                <p>Sophisticated chain-of-thought processing with meta-cognitive awareness and confidence assessment</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h3>Adaptive Processing</h3>
                <p>Multiple processing modes from fast responses to deep analytical thinking based on your needs</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔗</div>
                <h3>Memory Networks</h3>
                <p>Advanced episodic and semantic memory with contextual understanding and learning</p>
            </div>
        </div>
    </div>

    <script>
        let ws;
        let conversationId = null;
        
        function connect() {
            const userId = 'web_user_' + Math.random().toString(36).substr(2, 9);
            ws = new WebSocket(`ws://localhost:8000/ws/${userId}`);
            
            ws.onopen = function(event) {
                document.getElementById('connection-status').textContent = 'Connected';
                document.getElementById('connection-status').style.color = '#00ff00';
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                handleWebSocketMessage(data);
            };
            
            ws.onclose = function(event) {
                document.getElementById('connection-status').textContent = 'Disconnected';
                document.getElementById('connection-status').style.color = '#ff0000';
                // Attempt to reconnect after 3 seconds
                setTimeout(connect, 3000);
            };
        }
        
        function handleWebSocketMessage(data) {
            if (data.type === 'chat_response') {
                addMessage(data.response, 'ai');
                if (data.conversation_id) {
                    conversationId = data.conversation_id;
                }
            } else if (data.type === 'welcome') {
                console.log('Connected to MarkAI Advanced Interface');
            }
        }
        
        function sendMessage() {
            const input = document.getElementById('message-input');
            const message = input.value.trim();
            
            if (!message || !ws) return;
            
            addMessage(message, 'user');
            input.value = '';
            
            ws.send(JSON.stringify({
                type: 'chat',
                message: message,
                conversation_id: conversationId,
                processing_mode: document.getElementById('processing-mode').textContent.toLowerCase(),
                reasoning_type: document.getElementById('reasoning-type').textContent.toLowerCase()
            }));
        }
        
        function addMessage(content, sender) {
            const chatContainer = document.getElementById('chat-container');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            
            if (sender === 'user') {
                messageDiv.innerHTML = `<strong>👤 You:</strong> ${content}`;
            } else {
                messageDiv.innerHTML = `<strong>🤖 MarkAI:</strong> ${content}`;
            }
            
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        // Handle Enter key
        document.getElementById('message-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Connect when page loads
        connect();
    </script>
</body>
</html>
            '''
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(template_content.strip())
    
    async def _handle_websocket_message(self, user_id: str, message_data: Dict[str, Any]):
        """Handle incoming WebSocket messages"""
        message_type = message_data.get("type")
        
        if message_type == "chat":
            await self._handle_websocket_chat(user_id, message_data)
        elif message_type == "settings":
            await self._handle_websocket_settings(user_id, message_data)
        elif message_type == "plugin":
            await self._handle_websocket_plugin(user_id, message_data)
    
    async def _handle_websocket_chat(self, user_id: str, message_data: Dict[str, Any]):
        """Handle chat message via WebSocket"""
        try:
            # Get or create conversation
            conversation_id = message_data.get("conversation_id")
            if not conversation_id:
                conversation_id = await self.ai_engine.conversation_manager.create_conversation(user_id)
            
            # Process message
            response = await self.ai_engine.process_advanced_message(
                message=message_data["message"],
                user_id=user_id,
                conversation_id=conversation_id,
                processing_mode=ProcessingMode(message_data.get("processing_mode", "balanced")),
                reasoning_type=ReasoningType(message_data.get("reasoning_type", "analytical"))
            )
            
            # Send response
            await self.websocket_manager.send_message(user_id, {
                "type": "chat_response",
                "response": response.content,
                "conversation_id": conversation_id,
                "confidence": response.confidence,
                "reasoning_steps": [asdict(step) for step in response.reasoning_steps] if message_data.get("include_reasoning") else [],
                "metadata": response.metadata
            })
            
        except Exception as e:
            await self.websocket_manager.send_message(user_id, {
                "type": "error",
                "message": str(e)
            })
    
    async def _get_capabilities_info(self) -> Dict[str, Any]:
        """Get AI capabilities information"""
        return {
            "processing_modes": [mode.value for mode in ProcessingMode],
            "reasoning_types": [rt.value for rt in ReasoningType],
            "multimodal_support": ["text", "images", "documents", "code"],
            "advanced_features": [
                "chain_of_thought_reasoning",
                "memory_networks", 
                "cognitive_state_monitoring",
                "adaptive_learning",
                "plugin_ecosystem",
                "conversation_branching",
                "advanced_analytics"
            ]
        }
    
    async def _export_markdown(self, history: List[Dict], conversation_id: str) -> str:
        """Export conversation history as markdown"""
        md_content = f"# MarkAI Advanced Conversation\n\n"
        md_content += f"**Conversation ID:** {conversation_id}\n"
        md_content += f"**Export Date:** {datetime.now().isoformat()}\n"
        md_content += f"**Total Exchanges:** {len(history)}\n\n"
        md_content += "---\n\n"
        
        for i, exchange in enumerate(history, 1):
            md_content += f"## Exchange {i}\n\n"
            md_content += f"**You:** {exchange.get('user_message', '')}\n\n"
            md_content += f"**MarkAI:** {exchange.get('ai_response', '')}\n\n"
            md_content += "---\n\n"
        
        return md_content
    
    async def _generate_conversation_analytics(self, conversation_id: str) -> Dict[str, Any]:
        """Generate advanced conversation analytics"""
        try:
            history = await self.ai_engine.conversation_manager.get_history(conversation_id)
            
            # Basic metrics
            total_exchanges = len(history)
            total_tokens = sum(exchange.get('tokens_used', 0) for exchange in history)
            
            # Confidence analysis
            confidences = [exchange.get('confidence', 0) for exchange in history if exchange.get('confidence')]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # Reasoning analysis
            reasoning_types = [exchange.get('reasoning_type') for exchange in history if exchange.get('reasoning_type')]
            reasoning_distribution = {}
            for rt in reasoning_types:
                reasoning_distribution[rt] = reasoning_distribution.get(rt, 0) + 1
            
            return {
                "conversation_id": conversation_id,
                "total_exchanges": total_exchanges,
                "total_tokens": total_tokens,
                "average_confidence": avg_confidence,
                "reasoning_distribution": reasoning_distribution,
                "conversation_duration": "N/A",  # Calculate from timestamps
                "complexity_score": avg_confidence * total_exchanges,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Analytics generation error: {e}")
            return {"error": str(e)}
    
    async def start_server(self, host: str = "127.0.0.1", port: int = 8000):
        """Start the web server"""
        import uvicorn
        
        self.logger.info(f"Starting MarkAI Advanced Web Interface on {host}:{port}")
        
        config = uvicorn.Config(
            app=self.app,
            host=host,
            port=port,
            log_level="info",
            access_log=True
        )
        
        server = uvicorn.Server(config)
        await server.serve()


async def main():
    """Main entry point for web interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MarkAI Advanced Web Interface")
    parser.add_argument("--config", default="config/config.json", help="Configuration file")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = Config(args.config)
        
        # Create and start web interface
        web_interface = AdvancedWebInterface(config)
        await web_interface.start_server(args.host, args.port)
        
    except Exception as e:
        print(f"Error starting MarkAI Advanced Web Interface: {e}")


if __name__ == "__main__":
    asyncio.run(main())
