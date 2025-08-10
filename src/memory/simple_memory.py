"""
Simple Memory System (DEPRECATED - Protected for Future Use)
Basic memory system for AI clones
Stores conversation history and provides basic context retrieval

This system is now deprecated in favor of SqliteVecMemory.
It is kept for reference and potential future use.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

class SimpleMemory:
    """Simple memory system for storing conversation history (DEPRECATED)"""
    
    def __init__(self, clone_name: str):
        print("⚠️  SimpleMemory is deprecated. Use SqliteVecMemory instead.")
        self.clone_name = clone_name
        self.memory_file = f"data/conversations/{clone_name}_memory.json"
        self.conversation_history = []
        self.load_memory()
    
    def add_message(self, speaker: str, content: str, metadata: Dict = None):
        """Add a message to memory"""
        message = {
            "timestamp": datetime.now().isoformat(),
            "speaker": speaker,
            "content": content,
            "metadata": metadata or {}
        }
        self.conversation_history.append(message)
    
    def get_recent_messages(self, count: int = 10) -> List[Dict]:
        """Get the most recent messages"""
        return self.conversation_history[-count:] if self.conversation_history else []
    
    def get_messages_by_speaker(self, speaker: str, count: int = 5) -> List[Dict]:
        """Get recent messages from a specific speaker"""
        speaker_messages = [msg for msg in self.conversation_history if msg["speaker"] == speaker]
        return speaker_messages[-count:] if speaker_messages else []
    
    def search_messages(self, query: str, max_results: int = 5) -> List[Dict]:
        """Simple text search through messages"""
        query_lower = query.lower()
        matching_messages = []
        
        for msg in self.conversation_history:
            if query_lower in msg["content"].lower():
                matching_messages.append(msg)
        
        return matching_messages[-max_results:] if matching_messages else []
    
    def get_conversation_context(self, max_messages: int = 8) -> str:
        """Get formatted conversation context for AI prompts"""
        recent_messages = self.get_recent_messages(max_messages)
        
        if not recent_messages:
            return "No previous conversation."
        
        context_lines = []
        for msg in recent_messages:
            timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M")
            context_lines.append(f"[{timestamp}] {msg['speaker']}: {msg['content']}")
        
        return "\n".join(context_lines)
    
    def get_context(self, max_messages: int = 10) -> str:
        """Get recent conversation context (alias for compatibility)"""
        return self.get_conversation_context(max_messages)
    
    def get_smart_context(self, message: str, max_total: int = 8) -> str:
        """Get smart context (alias for get_context for compatibility)"""
        return self.get_context(max_total)
    
    def save_memory(self):
        """Save memory to file"""
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        
        memory_data = {
            "clone_name": self.clone_name,
            "last_updated": datetime.now().isoformat(),
            "total_messages": len(self.conversation_history),
            "conversation_history": self.conversation_history
        }
        
        with open(self.memory_file, 'w') as f:
            json.dump(memory_data, f, indent=2)
    
    def load_memory(self):
        """Load memory from file"""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                memory_data = json.load(f)
                self.conversation_history = memory_data.get("conversation_history", [])
    
    def clear_memory(self):
        """Clear all conversation history"""
        self.conversation_history = []
        if os.path.exists(self.memory_file):
            os.remove(self.memory_file)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        if not self.conversation_history:
            return {"total_messages": 0, "speakers": [], "date_range": None}
        
        speakers = list(set(msg["speaker"] for msg in self.conversation_history))
        
        timestamps = [datetime.fromisoformat(msg["timestamp"]) for msg in self.conversation_history]
        date_range = {
            "start": min(timestamps).isoformat(),
            "end": max(timestamps).isoformat()
        }
        
        return {
            "total_messages": len(self.conversation_history),
            "speakers": speakers,
            "date_range": date_range
        }

class ConversationManager:
    """Manages conversations between multiple AI clones"""
    
    def __init__(self):
        self.active_conversations = {}
        self.conversation_logs = []
    
    def start_conversation(self, clone1_name: str, clone2_name: str, scenario: str = None) -> str:
        """Start a new conversation between two clones"""
        conv_id = f"{clone1_name}_{clone2_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        conversation = {
            "id": conv_id,
            "participants": [clone1_name, clone2_name],
            "scenario": scenario,
            "messages": [],
            "started_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.active_conversations[conv_id] = conversation
        return conv_id
    
    def add_message_to_conversation(self, conv_id: str, speaker: str, content: str):
        """Add a message to an active conversation"""
        if conv_id in self.active_conversations:
            message = {
                "timestamp": datetime.now().isoformat(),
                "speaker": speaker,
                "content": content
            }
            self.active_conversations[conv_id]["messages"].append(message)
    
    def get_conversation_history(self, conv_id: str, max_messages: int = 10) -> List[Dict]:
        """Get conversation history"""
        if conv_id in self.active_conversations:
            messages = self.active_conversations[conv_id]["messages"]
            return messages[-max_messages:] if messages else []
        return []
    
    def end_conversation(self, conv_id: str):
        """End a conversation and archive it"""
        if conv_id in self.active_conversations:
            conversation = self.active_conversations[conv_id]
            conversation["status"] = "ended"
            conversation["ended_at"] = datetime.now().isoformat()
            
            # Save to logs
            self.save_conversation_log(conversation)
            
            # Archive to file
            self.save_conversation_log(conversation)
            
            # Remove from active
            del self.active_conversations[conv_id]
    
    def save_conversation_log(self, conversation: Dict):
        """Save conversation log to file"""
        log_file = f"data/conversations/conversation_{conversation['id']}.json"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        with open(log_file, 'w') as f:
            json.dump(conversation, f, indent=2)
    
    def get_active_conversations(self) -> List[str]:
        """Get list of active conversation IDs"""
        return list(self.active_conversations.keys()) 