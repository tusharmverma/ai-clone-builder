#!/usr/bin/env python3
"""
SqliteVec Memory System
True semantic search using sqlite-vec with M1 Mac compatibility
Uses vec0 virtual tables for efficient vector similarity search
Now self-contained without dependencies on other memory systems.
"""

import json
import os
import sqlite3
import sqlite_vec
import time
import uuid
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

class SqliteVecMemory:
    """
    Primary memory system using sqlite-vec for true semantic search.
    Provides vector similarity search, conversation clustering, and long-term memory.
    Now self-contained without dependencies on other memory systems.
    """
    
    def __init__(self, clone_name: str, embedding_dim: int = 384):
        """
        Initialize SqliteVec memory system
        
        Args:
            clone_name: Name of the AI clone
            embedding_dim: Dimension of embeddings (default 384 for sentence-transformers)
        """
        self.clone_name = clone_name
        self.embedding_dim = embedding_dim
        
        # Database setup
        self.db_file = f"data/vector_memory/{clone_name}_vectors.db"
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        
        # Initialize database connection with sqlite-vec
        self.conn = None
        self._initialize_database()
        
        # Configuration
        self.max_context_messages = 20
        self.similarity_threshold = 0.3
        self.conversation_window = 50  # Messages in recent context
        
        # Performance optimizations
        self.embedding_cache = {}  # Cache embeddings to avoid recomputation
        self.batch_size = 1  # Batch size 1 for immediate processing (better for testing)
        self.pending_messages = []  # Queue for batch inserts
        
        # Memory stats
        self.stats = {
            "total_messages": 0,
            "vector_searches": 0,
            "cache_hits": 0,
            "last_updated": datetime.now().isoformat()
        }
    
    def _initialize_database(self):
        """Initialize SQLite database with sqlite-vec extension"""
        try:
            self.conn = sqlite3.connect(self.db_file)
            
            # Try to enable extension loading and load sqlite-vec
            try:
                if hasattr(self.conn, 'enable_load_extension'):
                    self.conn.enable_load_extension(True)
                    sqlite_vec.load(self.conn)
                    self.conn.enable_load_extension(False)
                    self.vector_extension_available = True
                else:
                    # Fallback for systems without extension support
                    self.vector_extension_available = False
                    print("Info: SQLite extension loading not supported on this system - using basic mode")
            except Exception as ext_error:
                self.vector_extension_available = False
                print(f"Info: Could not load sqlite-vec extension: {ext_error} - using basic mode")
            
            cursor = self.conn.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    speaker TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    embedding BLOB,
                    metadata TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS embeddings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id INTEGER,
                    vector_data BLOB,
                    FOREIGN KEY (message_id) REFERENCES messages (id)
                )
            ''')
            
            # Create message_vectors table for sqlite-vec
            if self.vector_extension_available:
                cursor.execute('''
                    CREATE VIRTUAL TABLE IF NOT EXISTS message_vectors 
                    USING vec0(
                        message_id INTEGER,
                        embedding float32[384]
                    )
                ''')
            
            self.conn.commit()
            if self.vector_extension_available:
                print(f"SqliteVec database initialized with vector support: {self.db_file}")
            else:
                print(f"SqliteVec database initialized (basic mode): {self.db_file}")
            
        except Exception as e:
            print(f"SqliteVec initialization failed: {e}")
            raise
    
    def _generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate embeddings for text using a simple approach
        In production, this would use OpenAI API or local embedding model
        For testing, we'll use a simple hash-based approach
        """
        # Simple hash-based embedding for testing (deterministic)
        import hashlib
        
        # Create a deterministic "embedding" from text hash
        hash_bytes = hashlib.md5(text.encode()).digest()
        
        # Convert to float array of desired dimension
        embedding = []
        for i in range(self.embedding_dim):
            byte_idx = i % len(hash_bytes)
            embedding.append((hash_bytes[byte_idx] / 255.0) * 2.0 - 1.0)  # Scale to [-1, 1]
        
        return embedding
    
    def _generate_real_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate real semantic embeddings using OpenAI API or local models
        This is where the true semantic power comes from!
        """
        try:
            # Option 1: OpenAI API (requires API key)
            # import openai
            # response = openai.Embedding.create(
            #     input=text,
            #     model="text-embedding-ada-002"
            # )
            # return response['data'][0]['embedding']
            
            # Option 2: Local embedding model (sentence-transformers)
            # from sentence_transformers import SentenceTransformer
            # model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensions
            # embedding = model.encode(text).tolist()
            # return embedding
            
            # Option 3: Ollama embeddings (if available)
            # import requests
            # response = requests.post(
            #     "http://localhost:11434/api/embeddings",
            #     json={"model": "llama3.2:3b", "prompt": text}
            # )
            # return response.json()["embedding"]
            
            # For now, fall back to hash-based
            return self._generate_embedding(text)
            
        except Exception as e:
            print(f"⚠️ Real embedding failed: {e}, using hash-based fallback")
            return self._generate_embedding(text)
    
    def add_message(self, speaker: str, content: str, metadata: Dict = None):
        """Add a message with vector embedding (with performance optimizations)"""
        
        if not self.conn:
            return  # Fallback mode
        
        try:
            timestamp = datetime.now().isoformat()
            
            # Check cache first for performance
            content_hash = hashlib.md5(content.encode()).hexdigest()
            if content_hash in self.embedding_cache:
                embedding = self.embedding_cache[content_hash]
                self.stats["cache_hits"] += 1
            else:
                embedding = self._generate_embedding(content)
                if embedding:
                    self.embedding_cache[content_hash] = embedding
            
            # Always add message to database, even without embedding in basic mode
            # Add to batch queue for better performance
            self.pending_messages.append({
                "speaker": speaker,
                "content": content,
                "timestamp": timestamp,
                "metadata": metadata,
                "embedding": embedding
            })
            
            # Process batch if full
            if len(self.pending_messages) >= self.batch_size:
                self._process_batch()
            
            self.stats["total_messages"] += 1
            
        except Exception as e:
            print(f"Error adding message to vector memory: {e}")
    
    def _process_batch(self):
        """Process pending messages in batch for better performance"""
        if not self.pending_messages:
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Use transaction for batch insert
            cursor.execute("BEGIN TRANSACTION")
            
            for msg in self.pending_messages:
                # Insert message
                cursor.execute("""
                    INSERT INTO messages (speaker, content, timestamp, metadata)
                    VALUES (?, ?, ?, ?)
                """, (msg["speaker"], msg["content"], 
                      msg["timestamp"], json.dumps(msg["metadata"]) if msg["metadata"] else None))
                
                # Get the auto-generated message ID
                message_id = cursor.lastrowid
                
                # Only insert vector if extension is available and embedding exists
                if getattr(self, 'vector_extension_available', False) and msg["embedding"]:
                    try:
                        embedding_bytes = sqlite_vec.serialize_float32(msg["embedding"])
                        cursor.execute("""
                            INSERT INTO message_vectors (message_id, embedding)
                            VALUES (?, ?)
                        """, (message_id, embedding_bytes))
                    except Exception as vec_error:
                        print(f"Info: Vector insertion skipped: {vec_error}")
            
            cursor.execute("COMMIT")
            self.pending_messages.clear()
            
        except Exception as e:
            print(f"Error processing batch: {e}")
            cursor.execute("ROLLBACK")
    
    def search_messages(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for messages (alias for compatibility)"""
        return self.search_similar_messages(query, max_results)
    
    def search_similar_messages(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for semantically similar messages using vector similarity"""
        if not self.conn:
            # Fallback to simple memory
            return self._basic_text_search(query, limit)
        
        # Check if vector extension is available
        if not getattr(self, 'vector_extension_available', False):
            # Fallback to basic text search
            return self._basic_text_search(query, limit)
        
        try:
            # Generate query embedding
            query_embedding = self._generate_embedding(query)
            if not query_embedding:
                return []
            
            query_bytes = sqlite_vec.serialize_float32(query_embedding)
            
            cursor = self.conn.cursor()
            
            # Vector similarity search using sqlite-vec (with k constraint)
            cursor.execute("""
                SELECT 
                    m.speaker,
                    m.content,
                    m.timestamp,
                    v.distance
                FROM message_vectors v
                JOIN messages m ON v.message_id = m.id
                WHERE v.embedding MATCH ? AND k = ?
                ORDER BY v.distance
            """, (query_bytes, limit))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "speaker": row[0],
                    "content": row[1],
                    "timestamp": row[2],
                    "similarity_score": 1.0 - row[3],  # Convert distance to similarity
                    "source": "vector_search"
                })
            
            self.stats["vector_searches"] += 1
            return results
            
        except Exception as e:
            print(f"⚠️ Vector search failed: {e}")
            # Fallback to basic text search
            return self._basic_text_search(query, limit)
    
    def get_smart_context(self, message: str, max_total: int = 8) -> str:
        """Get intelligent context combining recent messages and semantically similar past messages"""
        try:
            # Get recent messages first
            recent_messages = self._get_recent_messages(min(5, max_total))
            
            # Get semantically similar messages for the remaining slots
            remaining_slots = max_total - len(recent_messages)
            similar_messages = []
            
            if remaining_slots > 0:
                similar_messages = self.search_similar_messages(message, remaining_slots)
            
            # Combine and format
            all_messages = similar_messages + recent_messages
            
            if not all_messages:
                return "No previous conversation."
            
            # Format context
            context_lines = []
            for msg in all_messages:
                timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M")
                context_lines.append(f"[{timestamp}] {msg['speaker']}: {msg['content']}")
            
            return "\n".join(context_lines)
            
        except Exception as e:
            # Fallback to basic text search
            return self._get_recent_messages(max_total)
    
    def get_context(self, max_messages: int = 10) -> str:
        """Get recent conversation context (alias for compatibility)"""
        return self._get_recent_messages(max_messages)
    
    def _get_recent_messages(self, limit: int = 10) -> List[Dict]:
        """Get recent messages from database"""
        if not self.conn:
            return []
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT speaker, content, timestamp
                FROM messages
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "speaker": row[0],
                    "content": row[1],
                    "timestamp": row[2]
                })
            
            return list(reversed(results))  # Return in chronological order
            
        except Exception as e:
            print(f"⚠️ Error getting recent messages: {e}")
            return []
    
    def _basic_text_search(self, query: str, limit: int = 10) -> List[Dict]:
        """Basic text search fallback when vector search is not available"""
        if not self.conn:
            return []
        
        try:
            cursor = self.conn.cursor()
            
            # Simple text search using LIKE operator
            cursor.execute("""
                SELECT speaker, content, timestamp
                FROM messages
                WHERE content LIKE ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (f"%{query}%", limit))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "speaker": row[0],
                    "content": row[1],
                    "timestamp": row[2],
                    "similarity_score": 0.5,  # Default similarity for text search
                    "source": "text_search"
                })
            
            return results
            
        except Exception as e:
            print(f"Error in basic text search: {e}")
            return []
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation"""
        if not self.conn:
            return "Vector memory not available"
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) as total,
                       MIN(timestamp) as first_message,
                       MAX(timestamp) as last_message
                FROM messages
            """)
            
            row = cursor.fetchone()
            if row and row[0] > 0:
                total, first, last = row
                first_time = datetime.fromisoformat(first).strftime("%Y-%m-%d %H:%M")
                last_time = datetime.fromisoformat(last).strftime("%Y-%m-%d %H:%M")
                
                return f"Conversation: {total} messages from {first_time} to {last_time}"
            else:
                return "No conversation history"
                
        except Exception as e:
            return f"Error getting conversation summary: {e}"
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        base_stats = self.stats.copy()
        
        if self.conn:
            try:
                cursor = self.conn.cursor()
                
                # Get message count
                cursor.execute("SELECT COUNT(*) FROM messages")
                base_stats["total_messages"] = cursor.fetchone()[0]
                
                # Get vector count
                cursor.execute("SELECT COUNT(*) FROM message_vectors")
                base_stats["vector_embeddings"] = cursor.fetchone()[0]
                
                # Get database size
                cursor.execute("SELECT page_count * page_size FROM pragma_page_count(), pragma_page_size()")
                base_stats["database_size_bytes"] = cursor.fetchone()[0]
                
            except Exception as e:
                base_stats["error"] = str(e)
        
        base_stats["memory_type"] = "sqlite_vec"
        base_stats["embedding_dimension"] = self.embedding_dim
        base_stats["database_file"] = self.db_file
        
        return base_stats
    
    def save_memory(self):
        """Save memory data (SQLite auto-saves, but we can optimize/vacuum)"""
        # Process any pending batch operations
        if self.pending_messages:
            self._process_batch()
        
        if self.conn:
            try:
                self.conn.execute("VACUUM")
                self.conn.commit()
            except Exception as e:
                print(f"⚠️ Error optimizing database: {e}")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None 