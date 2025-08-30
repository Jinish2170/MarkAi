"""
Conversation Manager - Advanced conversation history management

This module provides sophisticated conversation management capabilities including:
- Persistent conversation storage
- Conversation threading and branching  
- Message metadata tracking
- Context preservation
- Export/import functionality
"""

import asyncio
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

from ..utils.logger import get_logger
from ..utils.config import Config


@dataclass
class ConversationMessage:
    """Represents a single message in a conversation"""
    id: str
    conversation_id: str
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime
    metadata: Dict[str, Any]
    tokens_used: Optional[int] = None
    processing_time: Optional[float] = None
    confidence: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationMessage':
        """Create from dictionary"""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)


class ConversationManager:
    """
    Advanced conversation management system
    
    Features:
    - Persistent storage with SQLite
    - Conversation threading and branching
    - Message search and filtering
    - Export in multiple formats
    - Context window management
    - Performance analytics
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = get_logger(__name__)
        self.db_path = Path(config.get('database.path', 'data/conversations.db'))
        self.max_conversations = config.get('memory.max_conversations', 1000)
        self.max_messages_per_conversation = config.get('memory.max_messages_per_conversation', 1000)
        
        # Ensure database directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        asyncio.create_task(self._init_database())
    
    async def _init_database(self):
        """Initialize the database schema"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create conversations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT DEFAULT '{}'
                )
            """)
            
            # Create messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT DEFAULT '{}',
                    tokens_used INTEGER,
                    processing_time REAL,
                    confidence REAL,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                )
            """)
            
            # Create indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)")
            
            conn.commit()
            conn.close()
            
            self.logger.info("Database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}")
            raise
    
    async def create_conversation(self, user_id: str, title: Optional[str] = None) -> str:
        """Create a new conversation"""
        conversation_id = str(uuid.uuid4())
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO conversations (id, user_id, title, metadata)
                VALUES (?, ?, ?, ?)
            """, (conversation_id, user_id, title or f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}", "{}"))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Created conversation {conversation_id} for user {user_id}")
            return conversation_id
            
        except Exception as e:
            self.logger.error(f"Error creating conversation: {e}")
            raise
    
    async def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        tokens_used: Optional[int] = None,
        processing_time: Optional[float] = None,
        confidence: Optional[float] = None
    ) -> str:
        """Add a message to a conversation"""
        message_id = str(uuid.uuid4())
        message_metadata = metadata or {}
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO messages (id, conversation_id, role, content, metadata, tokens_used, processing_time, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                message_id,
                conversation_id, 
                role,
                content,
                json.dumps(message_metadata),
                tokens_used,
                processing_time,
                confidence
            ))
            
            # Update conversation timestamp
            cursor.execute("""
                UPDATE conversations 
                SET updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (conversation_id,))
            
            conn.commit()
            conn.close()
            
            self.logger.debug(f"Added message {message_id} to conversation {conversation_id}")
            return message_id
            
        except Exception as e:
            self.logger.error(f"Error adding message: {e}")
            raise
    
    async def get_conversation_history(
        self,
        conversation_id: str,
        limit: Optional[int] = None,
        include_metadata: bool = True
    ) -> List[ConversationMessage]:
        """Get conversation history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """
                SELECT id, conversation_id, role, content, timestamp, metadata, 
                       tokens_used, processing_time, confidence
                FROM messages 
                WHERE conversation_id = ?
                ORDER BY timestamp ASC
            """
            
            if limit:
                query += f" LIMIT {limit}"
            
            cursor.execute(query, (conversation_id,))
            rows = cursor.fetchall()
            conn.close()
            
            messages = []
            for row in rows:
                message = ConversationMessage(
                    id=row[0],
                    conversation_id=row[1],
                    role=row[2],
                    content=row[3],
                    timestamp=datetime.fromisoformat(row[4]),
                    metadata=json.loads(row[5]) if include_metadata else {},
                    tokens_used=row[6],
                    processing_time=row[7],
                    confidence=row[8]
                )
                messages.append(message)
            
            return messages
            
        except Exception as e:
            self.logger.error(f"Error getting conversation history: {e}")
            raise
    
    async def get_user_conversations(
        self,
        user_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get all conversations for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """
                SELECT id, title, created_at, updated_at, metadata
                FROM conversations 
                WHERE user_id = ?
                ORDER BY updated_at DESC
            """
            
            if limit:
                query += f" LIMIT {limit}"
            
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            conn.close()
            
            conversations = []
            for row in rows:
                conversation = {
                    'id': row[0],
                    'title': row[1],
                    'created_at': row[2],
                    'updated_at': row[3],
                    'metadata': json.loads(row[4])
                }
                conversations.append(conversation)
            
            return conversations
            
        except Exception as e:
            self.logger.error(f"Error getting user conversations: {e}")
            raise
    
    async def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation and all its messages"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete messages first (foreign key constraint)
            cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
            
            # Delete conversation
            cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Deleted conversation {conversation_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting conversation: {e}")
            return False
    
    async def search_messages(
        self,
        user_id: str,
        query: str,
        limit: int = 50
    ) -> List[ConversationMessage]:
        """Search messages across all user conversations"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            sql_query = """
                SELECT m.id, m.conversation_id, m.role, m.content, m.timestamp, 
                       m.metadata, m.tokens_used, m.processing_time, m.confidence
                FROM messages m
                JOIN conversations c ON m.conversation_id = c.id
                WHERE c.user_id = ? AND m.content LIKE ?
                ORDER BY m.timestamp DESC
                LIMIT ?
            """
            
            cursor.execute(sql_query, (user_id, f"%{query}%", limit))
            rows = cursor.fetchall()
            conn.close()
            
            messages = []
            for row in rows:
                message = ConversationMessage(
                    id=row[0],
                    conversation_id=row[1],
                    role=row[2],
                    content=row[3],
                    timestamp=datetime.fromisoformat(row[4]),
                    metadata=json.loads(row[5]),
                    tokens_used=row[6],
                    processing_time=row[7],
                    confidence=row[8]
                )
                messages.append(message)
            
            return messages
            
        except Exception as e:
            self.logger.error(f"Error searching messages: {e}")
            return []
    
    async def get_conversation_stats(self, conversation_id: str) -> Dict[str, Any]:
        """Get statistics for a conversation"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get message count and token usage
            cursor.execute("""
                SELECT 
                    COUNT(*) as message_count,
                    SUM(tokens_used) as total_tokens,
                    AVG(tokens_used) as avg_tokens,
                    SUM(processing_time) as total_processing_time,
                    AVG(confidence) as avg_confidence
                FROM messages 
                WHERE conversation_id = ?
            """, (conversation_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            stats = {
                'message_count': row[0] or 0,
                'total_tokens': row[1] or 0,
                'avg_tokens': row[2] or 0,
                'total_processing_time': row[3] or 0,
                'avg_confidence': row[4] or 0
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting conversation stats: {e}")
            return {}
    
    async def export_conversation(
        self,
        conversation_id: str,
        format: str = 'json'
    ) -> str:
        """Export conversation in specified format"""
        try:
            messages = await self.get_conversation_history(conversation_id)
            
            if format.lower() == 'json':
                data = [msg.to_dict() for msg in messages]
                return json.dumps(data, indent=2)
            
            elif format.lower() == 'markdown':
                lines = [f"# Conversation {conversation_id}\n"]
                for msg in messages:
                    role = "**User**" if msg.role == "user" else "**Assistant**"
                    lines.append(f"{role}: {msg.content}\n")
                return '\n'.join(lines)
            
            else:
                raise ValueError(f"Unsupported export format: {format}")
                
        except Exception as e:
            self.logger.error(f"Error exporting conversation: {e}")
            raise
    
    async def cleanup_old_conversations(self, days: int = 30) -> int:
        """Clean up conversations older than specified days"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get old conversation IDs
            cursor.execute("""
                SELECT id FROM conversations 
                WHERE updated_at < datetime('now', '-{} days')
            """.format(days))
            
            old_conversation_ids = [row[0] for row in cursor.fetchall()]
            
            # Delete old messages and conversations
            for conv_id in old_conversation_ids:
                cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conv_id,))
                cursor.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Cleaned up {len(old_conversation_ids)} old conversations")
            return len(old_conversation_ids)
            
        except Exception as e:
            self.logger.error(f"Error cleaning up conversations: {e}")
            return 0
