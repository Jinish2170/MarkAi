"""
Context Manager - Advanced context and memory management

This module provides sophisticated context management capabilities including:
- Long-term and short-term memory
- Context window management
- Semantic context extraction
- Context prioritization
- Memory consolidation
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

from ..utils.logger import get_logger
from ..utils.config import Config


class ContextManager:
    """
    Advanced context management system
    
    Features:
    - Context window management
    - Semantic context extraction  
    - Memory consolidation
    - Context prioritization
    - Long-term memory storage
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = get_logger(__name__)
        
        # Configuration
        self.max_context_length = config.get('memory.max_context_length', 8000)
        self.context_window_overlap = config.get('memory.context_window_overlap', 200)
        self.memory_decay_rate = config.get('memory.memory_decay_rate', 0.95)
        
        # Context storage
        self.short_term_memory = {}  # Recent context
        self.working_memory = {}     # Active context  
        self.context_cache = {}      # Cached context summaries
        
    async def get_context_for_conversation(
        self,
        conversation_id: str,
        max_tokens: Optional[int] = None
    ) -> str:
        """Get relevant context for a conversation"""
        try:
            max_tokens = max_tokens or self.max_context_length
            
            # Get recent messages from conversation
            from .conversation_manager import ConversationManager
            conv_manager = ConversationManager(self.config)
            messages = await conv_manager.get_conversation_history(conversation_id, limit=50)
            
            # Build context from messages
            context_parts = []
            total_length = 0
            
            for message in reversed(messages):  # Start with most recent
                message_text = f"{message.role}: {message.content}"
                message_length = len(message_text)
                
                if total_length + message_length <= max_tokens:
                    context_parts.insert(0, message_text)
                    total_length += message_length
                else:
                    break
            
            context = "\n".join(context_parts)
            
            # Cache the context
            self.context_cache[conversation_id] = {
                'context': context,
                'timestamp': datetime.now(),
                'token_count': total_length
            }
            
            return context
            
        except Exception as e:
            self.logger.error(f"Error getting context for conversation {conversation_id}: {e}")
            return ""
    
    async def extract_key_points(self, text: str) -> List[str]:
        """Extract key points from text for context"""
        try:
            # Simple extraction for now - could be enhanced with NLP
            sentences = text.split('. ')
            
            # Filter for meaningful sentences
            key_points = []
            for sentence in sentences:
                if len(sentence.strip()) > 20 and any(word in sentence.lower() for word in [
                    'important', 'key', 'main', 'primary', 'significant', 'critical',
                    'remember', 'note', 'summary', 'conclusion'
                ]):
                    key_points.append(sentence.strip())
            
            return key_points[:5]  # Return top 5 key points
            
        except Exception as e:
            self.logger.error(f"Error extracting key points: {e}")
            return []
    
    async def update_working_memory(
        self,
        conversation_id: str,
        key: str,
        value: Any,
        importance: float = 1.0
    ):
        """Update working memory with new information"""
        try:
            if conversation_id not in self.working_memory:
                self.working_memory[conversation_id] = {}
            
            self.working_memory[conversation_id][key] = {
                'value': value,
                'timestamp': datetime.now(),
                'importance': importance,
                'access_count': 1
            }
            
            self.logger.debug(f"Updated working memory for {conversation_id}: {key}")
            
        except Exception as e:
            self.logger.error(f"Error updating working memory: {e}")
    
    async def get_working_memory(
        self,
        conversation_id: str,
        key: Optional[str] = None
    ) -> Any:
        """Get information from working memory"""
        try:
            if conversation_id not in self.working_memory:
                return None
            
            if key:
                memory_item = self.working_memory[conversation_id].get(key)
                if memory_item:
                    # Update access count
                    memory_item['access_count'] += 1
                    return memory_item['value']
                return None
            
            # Return all working memory for conversation
            return self.working_memory[conversation_id]
            
        except Exception as e:
            self.logger.error(f"Error getting working memory: {e}")
            return None
    
    async def consolidate_memory(self, conversation_id: str):
        """Consolidate working memory into long-term storage"""
        try:
            if conversation_id not in self.working_memory:
                return
            
            working_mem = self.working_memory[conversation_id]
            
            # Identify important memories to consolidate
            important_memories = {}
            for key, memory_item in working_mem.items():
                # Calculate memory strength based on importance and access
                strength = memory_item['importance'] * memory_item['access_count']
                
                # Only consolidate memories above threshold
                if strength > 2.0:  # Configurable threshold
                    important_memories[key] = {
                        'value': memory_item['value'],
                        'strength': strength,
                        'consolidated_at': datetime.now()
                    }
            
            if important_memories:
                # Store in long-term memory (could be database or file)
                self._store_long_term_memory(conversation_id, important_memories)
                
                self.logger.info(f"Consolidated {len(important_memories)} memories for {conversation_id}")
            
        except Exception as e:
            self.logger.error(f"Error consolidating memory: {e}")
    
    def _store_long_term_memory(self, conversation_id: str, memories: Dict[str, Any]):
        """Store memories in long-term storage"""
        try:
            # Simple file-based storage for now
            memory_dir = Path('data/memory')
            memory_dir.mkdir(parents=True, exist_ok=True)
            
            memory_file = memory_dir / f"{conversation_id}_memory.json"
            
            # Load existing memories
            existing_memories = {}
            if memory_file.exists():
                with open(memory_file, 'r', encoding='utf-8') as f:
                    existing_memories = json.load(f)
            
            # Merge with new memories
            existing_memories.update(memories)
            
            # Save updated memories
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(existing_memories, f, indent=2, default=str)
            
        except Exception as e:
            self.logger.error(f"Error storing long-term memory: {e}")
    
    async def retrieve_long_term_memory(self, conversation_id: str) -> Dict[str, Any]:
        """Retrieve memories from long-term storage"""
        try:
            memory_file = Path('data/memory') / f"{conversation_id}_memory.json"
            
            if memory_file.exists():
                with open(memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return {}
            
        except Exception as e:
            self.logger.error(f"Error retrieving long-term memory: {e}")
            return {}
    
    async def summarize_context(self, text: str, max_length: int = 200) -> str:
        """Create a summary of context for memory storage"""
        try:
            # Simple summarization - could be enhanced with AI
            sentences = text.split('. ')
            
            if len(text) <= max_length:
                return text
            
            # Take first and last sentences plus any key sentences
            summary_parts = []
            
            if sentences:
                summary_parts.append(sentences[0])  # First sentence
                
                # Add key sentences from middle
                for sentence in sentences[1:-1]:
                    if any(word in sentence.lower() for word in [
                        'important', 'key', 'main', 'however', 'therefore', 'conclusion'
                    ]):
                        summary_parts.append(sentence)
                        if len(' '.join(summary_parts)) > max_length * 0.8:
                            break
                
                # Add last sentence if there's room
                if len(sentences) > 1:
                    last_sentence = sentences[-1]
                    if len(' '.join(summary_parts + [last_sentence])) <= max_length:
                        summary_parts.append(last_sentence)
            
            return '. '.join(summary_parts)
            
        except Exception as e:
            self.logger.error(f"Error summarizing context: {e}")
            return text[:max_length] + "..." if len(text) > max_length else text
    
    async def cleanup_old_context(self, days: int = 7):
        """Clean up old context data"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Clean up context cache
            expired_keys = [
                key for key, value in self.context_cache.items()
                if value.get('timestamp', datetime.min) < cutoff_date
            ]
            
            for key in expired_keys:
                del self.context_cache[key]
            
            # Clean up working memory
            for conv_id in list(self.working_memory.keys()):
                working_mem = self.working_memory[conv_id]
                expired_items = [
                    key for key, item in working_mem.items()
                    if item.get('timestamp', datetime.min) < cutoff_date
                ]
                
                for key in expired_items:
                    del working_mem[key]
                
                # Remove empty conversation memories
                if not working_mem:
                    del self.working_memory[conv_id]
            
            self.logger.info(f"Cleaned up context data older than {days} days")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up context: {e}")
    
    async def get_context_stats(self) -> Dict[str, Any]:
        """Get statistics about context usage"""
        try:
            stats = {
                'cached_contexts': len(self.context_cache),
                'active_conversations': len(self.working_memory),
                'total_working_memory_items': sum(
                    len(mem) for mem in self.working_memory.values()
                ),
                'memory_usage_bytes': sum(
                    len(str(value)) for cache in self.context_cache.values()
                    for value in cache.values()
                )
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting context stats: {e}")
            return {}
