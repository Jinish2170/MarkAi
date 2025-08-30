"""
FastAPI Web Server for MarkAI - REST API and Web Interface
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
import asyncio
import json
import uuid

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from ..core.ai_engine import MarkAICore, AIResponse
from ..utils.config import Config
from ..utils.logger import get_logger, setup_logging


# Pydantic models for API
class ChatMessage(BaseModel):
    """Chat message request model"""
    message: str = Field(..., description="User message")
    user_id: str = Field(..., description="User identifier")
    conversation_id: Optional[str] = Field(None, description="Conversation identifier")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    conversation_id: str
    message_id: str
    metadata: Dict[str, Any]
    timestamp: datetime
    model_used: str
    tokens_used: int
    confidence: float
    reasoning_steps: Optional[List[str]] = None


class UserPreferences(BaseModel):
    """User preferences model"""
    preferences: Dict[str, Any]
    expertise_areas: Optional[List[str]] = None
    communication_style: Optional[str] = None


class ConversationSummary(BaseModel):
    """Conversation summary model"""
    id: str
    title: str
    message_count: int
    created_at: datetime
    updated_at: datetime


# Initialize FastAPI app
app = FastAPI(
    title="MarkAI - Advanced AI Assistant",
    description="Sophisticated AI assistant powered by Google Gemini",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Global variables
config: Config = None
ai_engine: MarkAICore = None
logger = None


@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup"""
    global config, ai_engine, logger
    
    # Load configuration
    config = Config()
    if not config.validate():
        raise RuntimeError("Invalid configuration. Please check your config.json file.")
    
    # Setup logging
    setup_logging(
        log_level=config.get('logging.level', 'INFO'),
        log_file=config.get('logging.file'),
        max_size=config.get('logging.max_size', '10MB'),
        backup_count=config.get('logging.backup_count', 5)
    )
    
    logger = get_logger(__name__)
    logger.info("Starting MarkAI server...")
    
    # Initialize AI engine
    ai_engine = MarkAICore(config)
    
    logger.info(f"MarkAI server started on {config.server_host}:{config.server_port}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global ai_engine, logger
    
    if logger:
        logger.info("Shutting down MarkAI server...")
    
    if ai_engine:
        await ai_engine.shutdown()
    
    if logger:
        logger.info("MarkAI server shut down successfully")


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get AI engine
async def get_ai_engine() -> MarkAICore:
    """Dependency to get the AI engine"""
    if ai_engine is None:
        raise HTTPException(status_code=503, detail="AI engine not initialized")
    return ai_engine


# API Routes

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main web interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MarkAI - Advanced AI Assistant</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: white;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
                border: 1px solid rgba(255, 255, 255, 0.18);
            }
            h1 {
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .chat-container {
                height: 400px;
                overflow-y: auto;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                background: rgba(0, 0, 0, 0.1);
            }
            .message {
                margin-bottom: 15px;
                padding: 10px 15px;
                border-radius: 10px;
            }
            .user-message {
                background: rgba(255, 255, 255, 0.2);
                margin-left: 50px;
            }
            .ai-message {
                background: rgba(0, 255, 0, 0.2);
                margin-right: 50px;
            }
            .input-container {
                display: flex;
                gap: 10px;
            }
            input[type="text"] {
                flex: 1;
                padding: 15px;
                border: none;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.2);
                color: white;
                font-size: 16px;
            }
            input[type="text"]::placeholder {
                color: rgba(255, 255, 255, 0.7);
            }
            button {
                padding: 15px 25px;
                background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                border: none;
                border-radius: 10px;
                color: white;
                font-weight: bold;
                cursor: pointer;
                transition: transform 0.2s;
            }
            button:hover {
                transform: scale(1.05);
            }
            .features {
                margin-top: 30px;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
            }
            .feature {
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            .status {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 10px 20px;
                background: rgba(0, 255, 0, 0.8);
                border-radius: 20px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="status" id="status">● Online</div>
        <div class="container">
            <h1>🤖 MarkAI Assistant</h1>
            <div class="chat-container" id="chatContainer">
                <div class="message ai-message">
                    <strong>MarkAI:</strong> Hello! I'm MarkAI, your advanced AI assistant. I'm powered by Google's Gemini AI and equipped with memory, context awareness, and a plugin system. How can I help you today?
                </div>
            </div>
            <div class="input-container">
                <input type="text" id="messageInput" placeholder="Ask me anything..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">Send</button>
            </div>
            
            <div class="features">
                <div class="feature">
                    <h3>🧠 Smart Memory</h3>
                    <p>Remembers context and learns from conversations</p>
                </div>
                <div class="feature">
                    <h3>🔌 Plugin System</h3>
                    <p>Extensible with custom plugins for specialized tasks</p>
                </div>
                <div class="feature">
                    <h3>⚡ Fast Processing</h3>
                    <p>Powered by Google Gemini for quick, accurate responses</p>
                </div>
                <div class="feature">
                    <h3>🎯 Context Aware</h3>
                    <p>Understands your preferences and communication style</p>
                </div>
            </div>
        </div>

        <script>
            const userId = 'user_' + Math.random().toString(36).substr(2, 9);
            let conversationId = null;

            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                if (!message) return;

                input.value = '';
                addMessage('user', message);

                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            message: message,
                            user_id: userId,
                            conversation_id: conversationId
                        })
                    });

                    const data = await response.json();
                    if (response.ok) {
                        conversationId = data.conversation_id;
                        addMessage('ai', data.response);
                        updateStatus('● Online');
                    } else {
                        addMessage('ai', 'Sorry, I encountered an error: ' + data.detail);
                        updateStatus('● Error');
                    }
                } catch (error) {
                    addMessage('ai', 'Sorry, I had trouble connecting. Please try again.');
                    updateStatus('● Offline');
                }
            }

            function addMessage(type, content) {
                const chatContainer = document.getElementById('chatContainer');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${type}-message`;
                messageDiv.innerHTML = `<strong>${type === 'user' ? 'You' : 'MarkAI'}:</strong> ${content}`;
                chatContainer.appendChild(messageDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }

            function updateStatus(status) {
                document.getElementById('status').textContent = status;
            }

            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }

            // Focus on input when page loads
            document.getElementById('messageInput').focus();
        </script>
    </body>
    </html>
    """


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    global ai_engine
    
    if ai_engine:
        status = await ai_engine.get_health_status()
        return {"status": "healthy", "details": status}
    else:
        return {"status": "initializing"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    chat_request: ChatMessage,
    ai: MarkAICore = Depends(get_ai_engine)
) -> ChatResponse:
    """Main chat endpoint"""
    try:
        # Process the message through the AI engine
        ai_response = await ai.process_message(
            message=chat_request.message,
            user_id=chat_request.user_id,
            conversation_id=chat_request.conversation_id,
            context=chat_request.context
        )
        
        # Generate a unique message ID
        message_id = str(uuid.uuid4())
        
        return ChatResponse(
            response=ai_response.content,
            conversation_id=ai_response.metadata.get('conversation_id', 'unknown'),
            message_id=message_id,
            metadata=ai_response.metadata,
            timestamp=ai_response.timestamp,
            model_used=ai_response.model_used,
            tokens_used=ai_response.tokens_used,
            confidence=ai_response.confidence,
            reasoning_steps=ai_response.reasoning_steps
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/conversations/{user_id}")
async def get_conversations(
    user_id: str,
    limit: int = 50,
    ai: MarkAICore = Depends(get_ai_engine)
):
    """Get user's conversation history"""
    try:
        conversations = await ai.conversation_manager.get_user_conversations(user_id, limit)
        return {"conversations": conversations}
    except Exception as e:
        logger.error(f"Error getting conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/conversation/{conversation_id}/history")
async def get_conversation_history(
    conversation_id: str,
    limit: int = 50,
    offset: int = 0,
    ai: MarkAICore = Depends(get_ai_engine)
):
    """Get conversation message history"""
    try:
        history = await ai.conversation_manager.get_history(conversation_id, limit, offset)
        return {"history": history}
    except Exception as e:
        logger.error(f"Error getting conversation history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/user/{user_id}/preferences")
async def update_user_preferences(
    user_id: str,
    preferences: UserPreferences,
    ai: MarkAICore = Depends(get_ai_engine)
):
    """Update user preferences"""
    try:
        await ai.context_manager.update_user_preferences(user_id, preferences.preferences)
        
        if preferences.expertise_areas:
            await ai.context_manager.update_expertise_areas(user_id, preferences.expertise_areas)
        
        if preferences.communication_style:
            await ai.context_manager.update_communication_style(user_id, preferences.communication_style)
        
        return {"message": "Preferences updated successfully"}
    except Exception as e:
        logger.error(f"Error updating preferences: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/user/{user_id}/context")
async def get_user_context(
    user_id: str,
    ai: MarkAICore = Depends(get_ai_engine)
):
    """Get user context and preferences"""
    try:
        context = await ai.context_manager.get_user_context(user_id)
        return {"context": context}
    except Exception as e:
        logger.error(f"Error getting user context: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/plugins")
async def list_plugins(ai: MarkAICore = Depends(get_ai_engine)):
    """List all available plugins"""
    try:
        plugins = ai.plugin_manager.list_plugins()
        return {"plugins": plugins}
    except Exception as e:
        logger.error(f"Error listing plugins: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/sentiment")
async def analyze_sentiment(
    request: Dict[str, str],
    ai: MarkAICore = Depends(get_ai_engine)
):
    """Analyze text sentiment"""
    try:
        text = request.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        analysis = await ai.analyze_sentiment(text)
        return {"analysis": analysis}
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/summarize")
async def summarize_text(
    request: Dict[str, Any],
    ai: MarkAICore = Depends(get_ai_engine)
):
    """Summarize text"""
    try:
        text = request.get("text", "")
        max_length = request.get("max_length", 200)
        
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        summary = await ai.summarize_text(text, max_length)
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Error summarizing text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats/{user_id}")
async def get_user_stats(
    user_id: str,
    ai: MarkAICore = Depends(get_ai_engine)
):
    """Get user statistics"""
    try:
        conversation_stats = await ai.conversation_manager.get_stats(user_id)
        context_stats = await ai.context_manager.get_user_stats(user_id)
        
        return {
            "conversation_stats": conversation_stats,
            "context_stats": context_stats
        }
    except Exception as e:
        logger.error(f"Error getting user stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return {"error": exc.detail, "status_code": exc.status_code}


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return {"error": "Internal server error", "status_code": 500}


# Run the server
if __name__ == "__main__":
    import uvicorn
    
    # Load config for server settings
    config = Config()
    
    uvicorn.run(
        "api.server:app",
        host=config.server_host,
        port=config.server_port,
        reload=config.server_debug,
        log_level="info"
    )
