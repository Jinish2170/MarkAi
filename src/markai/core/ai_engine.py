"""
MarkAI Core Engine - Advanced AI Assistant with Gemini Integration
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from pathlib import Path

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from ..memory.conversation_manager import ConversationManager
from ..memory.context_manager import ContextManager
from ..utils.logger import get_logger
from ..utils.config import Config
from ..plugins.plugin_manager import PluginManager


@dataclass
class AIResponse:
    """Response structure from the AI"""
    content: str
    metadata: Dict[str, Any]
    timestamp: datetime
    model_used: str
    tokens_used: int
    confidence: float
    reasoning_steps: List[str] = None


class MarkAICore:
    """
    Advanced AI Assistant Core Engine
    
    This class manages the main AI functionality using Google's Gemini API
    with advanced features like memory management, context awareness,
    and plugin system integration.
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = get_logger(__name__)
        
        # Initialize Gemini API
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel(
            model_name=config.gemini_model,
            generation_config=genai.types.GenerationConfig(
                temperature=config.gemini_temperature,
                max_output_tokens=config.gemini_max_tokens,
            ),
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
        )
        
        # Initialize core components
        self.conversation_manager = ConversationManager(config)
        self.context_manager = ContextManager(config)
        self.plugin_manager = PluginManager(config)
        
        # AI system prompts
        self.system_prompt = self._load_system_prompt()
        
        self.logger.info("MarkAI Core Engine initialized successfully")
    
    def _load_system_prompt(self) -> str:
        """Load the system prompt that defines the AI's behavior"""
        return """
        You are MarkAI, an advanced AI assistant with the following capabilities:
        
        CORE IDENTITY:
        - You are intelligent, helpful, and adaptive
        - You maintain context across conversations
        - You can learn from interactions and improve responses
        - You have access to various tools and plugins
        
        CAPABILITIES:
        - Multi-modal processing (text, images, documents)
        - Complex reasoning with step-by-step analysis
        - Memory management and context retention
        - Task automation and workflow management
        - Plugin system for extended functionality
        
        BEHAVIOR GUIDELINES:
        - Always be helpful, accurate, and honest
        - Explain your reasoning when solving complex problems
        - Ask clarifying questions when needed
        - Maintain conversation context and user preferences
        - Suggest improvements and optimizations
        - Be proactive in offering assistance
        
        RESPONSE FORMAT:
        - Provide clear, structured responses
        - Include reasoning steps for complex problems
        - Offer multiple solutions when applicable
        - Include confidence levels for your responses
        """
    
    async def process_message(
        self,
        message: str,
        user_id: str,
        conversation_id: Optional[str] = None,
        attachments: Optional[List[Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> AIResponse:
        """
        Process a user message and generate an intelligent response
        
        Args:
            message: User's input message
            user_id: Unique identifier for the user
            conversation_id: Optional conversation identifier
            attachments: Optional file attachments
            context: Additional context information
            
        Returns:
            AIResponse object with the AI's response and metadata
        """
        try:
            start_time = datetime.now()
            
            # Get or create conversation
            if not conversation_id:
                conversation_id = self.conversation_manager.create_conversation(user_id)
            
            # Retrieve conversation history and context
            conversation_history = await self.conversation_manager.get_history(
                conversation_id, limit=20
            )
            user_context = await self.context_manager.get_user_context(user_id)
            
            # Build the prompt with context
            full_prompt = await self._build_prompt(
                message, conversation_history, user_context, attachments, context
            )
            
            # Check for plugin interactions
            plugin_response = await self.plugin_manager.handle_message(message, user_id)
            if plugin_response:
                return plugin_response
            
            # Generate response using Gemini
            response = await self._generate_response(full_prompt)
            
            # Process and enhance the response
            ai_response = await self._process_response(
                response, message, user_id, conversation_id, start_time
            )
            
            # Save to conversation history
            await self.conversation_manager.add_message(
                conversation_id, user_id, message, ai_response.content
            )
            
            # Update context
            await self.context_manager.update_context(user_id, message, ai_response.content)
            
            self.logger.info(f"Processed message for user {user_id}, conversation {conversation_id}")
            return ai_response
            
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            return AIResponse(
                content="I apologize, but I encountered an error processing your request. Please try again.",
                metadata={"error": str(e)},
                timestamp=datetime.now(),
                model_used=self.config.gemini_model,
                tokens_used=0,
                confidence=0.0
            )
    
    async def _build_prompt(
        self,
        message: str,
        history: List[Dict],
        context: Dict,
        attachments: Optional[List[Any]] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build a comprehensive prompt with context"""
        
        prompt_parts = [self.system_prompt]
        
        # Add user context
        if context.get('preferences'):
            prompt_parts.append(f"User Preferences: {json.dumps(context['preferences'], indent=2)}")
        
        if context.get('expertise_areas'):
            prompt_parts.append(f"User's Expertise Areas: {', '.join(context['expertise_areas'])}")
        
        # Add conversation history
        if history:
            prompt_parts.append("Conversation History:")
            for entry in history[-10:]:  # Last 10 messages
                prompt_parts.append(f"User: {entry['user_message']}")
                prompt_parts.append(f"Assistant: {entry['ai_response']}")
        
        # Add additional context
        if additional_context:
            prompt_parts.append(f"Additional Context: {json.dumps(additional_context, indent=2)}")
        
        # Add current message
        prompt_parts.append(f"Current Message: {message}")
        
        # Add instruction for structured response
        prompt_parts.append("""
        Please provide a helpful response. If this is a complex problem, include your reasoning steps.
        Format your response as JSON with the following structure:
        {
            "response": "Your main response here",
            "reasoning_steps": ["Step 1", "Step 2", ...],
            "confidence": 0.95,
            "suggestions": ["Optional suggestion 1", ...]
        }
        """)
        
        return "\n\n".join(prompt_parts)
    
    async def _generate_response(self, prompt: str) -> str:
        """Generate response using Gemini API"""
        try:
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            return response.text
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            raise
    
    async def _process_response(
        self,
        raw_response: str,
        original_message: str,
        user_id: str,
        conversation_id: str,
        start_time: datetime
    ) -> AIResponse:
        """Process and enhance the raw AI response"""
        
        try:
            # Try to parse as JSON for structured response
            response_data = json.loads(raw_response)
            content = response_data.get('response', raw_response)
            reasoning_steps = response_data.get('reasoning_steps', [])
            confidence = response_data.get('confidence', 0.8)
            
        except json.JSONDecodeError:
            # Fallback to plain text response
            content = raw_response
            reasoning_steps = []
            confidence = 0.7
        
        # Calculate processing time and estimate tokens
        processing_time = (datetime.now() - start_time).total_seconds()
        estimated_tokens = len(raw_response.split()) * 1.3  # Rough estimate
        
        metadata = {
            "processing_time": processing_time,
            "conversation_id": conversation_id,
            "user_id": user_id,
            "original_message": original_message,
        }
        
        return AIResponse(
            content=content,
            metadata=metadata,
            timestamp=datetime.now(),
            model_used=self.config.gemini_model,
            tokens_used=int(estimated_tokens),
            confidence=confidence,
            reasoning_steps=reasoning_steps
        )
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze the sentiment of given text"""
        prompt = f"""
        Analyze the sentiment of the following text and provide a detailed analysis:
        
        Text: "{text}"
        
        Provide the analysis as JSON:
        {{
            "sentiment": "positive/negative/neutral",
            "confidence": 0.95,
            "emotions": ["joy", "excitement"],
            "intensity": "low/medium/high",
            "key_phrases": ["phrase1", "phrase2"]
        }}
        """
        
        try:
            response = await self._generate_response(prompt)
            return json.loads(response)
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {str(e)}")
            return {
                "sentiment": "neutral",
                "confidence": 0.0,
                "emotions": [],
                "intensity": "unknown",
                "key_phrases": []
            }
    
    async def summarize_text(self, text: str, max_length: int = 200) -> str:
        """Generate a summary of the given text"""
        prompt = f"""
        Please provide a concise summary of the following text in approximately {max_length} characters:
        
        {text}
        
        Summary:
        """
        
        try:
            response = await self._generate_response(prompt)
            return response.strip()
        except Exception as e:
            self.logger.error(f"Error summarizing text: {str(e)}")
            return "Unable to generate summary."
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Get the health status of the AI engine"""
        return {
            "status": "healthy",
            "model": self.config.gemini_model,
            "components": {
                "conversation_manager": "active",
                "context_manager": "active",
                "plugin_manager": "active"
            },
            "timestamp": datetime.now().isoformat()
        }
    
    async def shutdown(self):
        """Gracefully shutdown the AI engine"""
        self.logger.info("Shutting down MarkAI Core Engine...")
        await self.conversation_manager.shutdown()
        await self.context_manager.shutdown()
        await self.plugin_manager.shutdown()
        self.logger.info("MarkAI Core Engine shut down successfully")
