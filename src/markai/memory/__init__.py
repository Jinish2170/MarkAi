"""
MarkAI Memory Package

Handles conversation history, context management, and memory networks
for the MarkAI AI assistant.
"""

__version__ = "1.0.0"
__author__ = "MarkAI Development Team"

from .conversation_manager import ConversationManager, ConversationMessage
from .context_manager import ContextManager

__all__ = [
    'ConversationManager',
    'ConversationMessage', 
    'ContextManager'
]
