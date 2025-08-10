"""
Enhanced Memory System (DEPRECATED - Protected for Future Use)
Provides Week 2-3 memory features without vector dependencies
Uses keyword-based semantic search and conversation summarization

This system is now deprecated in favor of SqliteVecMemory.
It is kept for reference and potential future use.
"""

import json
import os
import re
from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
from collections import Counter, defaultdict

# Protected import - only for reference
try:
    from .simple_memory import SimpleMemory
except ImportError:
    # For direct execution
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from src.memory.simple_memory import SimpleMemory

class EnhancedMemory:
    """Enhanced memory system with semantic features and conversation summarization (DEPRECATED)"""
    
    def __init__(self, clone_name: str):
        print("⚠️  EnhancedMemory is deprecated. Use SqliteVecMemory instead.")
        self.clone_name = clone_name
        self.simple_memory = SimpleMemory(clone_name)
        
        # Enhanced features
        self.keyword_index = defaultdict(list)  # keyword -> [message_ids]
        self.topic_index = defaultdict(list)    # topic -> [message_ids]
        self.speaker_keywords = defaultdict(Counter)  # speaker -> keyword counts
        self.conversation_summaries = []  # Summarized conversation chunks
        
        # Configuration
        self.summary_threshold = 20  # Messages before creating summary
        self.max_context_messages = 50  # Maximum messages to consider for context
        
        # Load enhanced data
        self.enhanced_file = f"data/enhanced_memory/{clone_name}_enhanced.json"
        self.load_enhanced_data()
    
    def add_message(self, speaker: str, content: str, metadata: Dict = None):
        """Add message with enhanced indexing"""
        # Add to simple memory first
        self.simple_memory.add_message(speaker, content, metadata)
        
        # Get the message ID (length of conversation history)
        message_id = len(self.simple_memory.conversation_history) - 1
        
        # Extract and index keywords
        keywords = self._extract_keywords(content)
        for keyword in keywords:
            self.keyword_index[keyword].append(message_id)
        
        # Extract and index topics
        topics = self._extract_topics(content)
        for topic in topics:
            self.topic_index[topic].append(message_id)
        
        # Update speaker keyword profile
        for keyword in keywords:
            self.speaker_keywords[speaker][keyword] += 1
        
        # Check if we need to create a conversation summary
        if len(self.simple_memory.conversation_history) % self.summary_threshold == 0:
            self._create_conversation_summary()
        
        # Save enhanced data periodically
        if len(self.simple_memory.conversation_history) % 5 == 0:
            self.save_enhanced_data()
    
    def get_smart_context(self, current_message: str, max_total: int = 8) -> str:
        """Get intelligent context: recent + relevant past messages"""
        # Get recent messages (always include these)
        recent_count = min(5, max_total)
        recent_messages = self.simple_memory.get_recent_messages(recent_count)
        
        # Get semantically relevant messages from older history
        relevant_count = max_total - len(recent_messages)
        relevant_messages = []
        
        if relevant_count > 0 and len(self.simple_memory.conversation_history) > recent_count:
            relevant_messages = self._find_relevant_messages(current_message, relevant_count)
        
        # Combine and format
        all_messages = relevant_messages + recent_messages
        
        return self._format_context_messages(all_messages)
    
    def get_context(self, max_messages: int = 10) -> str:
        """Get recent conversation context (alias for compatibility)"""
        return self.simple_memory.get_context(max_messages)
    
    def search_messages(self, query: str, max_results: int = 5) -> List[Dict]:
        """Enhanced semantic search using keywords and topics"""
        query_keywords = self._extract_keywords(query)
        query_topics = self._extract_topics(query)
        
        # Score messages based on keyword and topic matches
        message_scores = defaultdict(float)
        
        # Keyword matching
        for keyword in query_keywords:
            for message_id in self.keyword_index.get(keyword, []):
                message_scores[message_id] += 1.0
        
        # Topic matching (higher weight)
        for topic in query_topics:
            for message_id in self.topic_index.get(topic, []):
                message_scores[message_id] += 2.0
        
        # Also include simple text search results
        simple_results = self.simple_memory.search_messages(query, max_results * 2)
        for result in simple_results:
            # Find message_id in conversation history
            for i, msg in enumerate(self.simple_memory.conversation_history):
                if (msg["speaker"] == result["speaker"] and 
                    msg["content"] == result["content"] and
                    msg["timestamp"] == result["timestamp"]):
                    message_scores[i] += 0.5
                    break
        
        # Sort by score and return top results
        sorted_scores = sorted(message_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for message_id, score in sorted_scores[:max_results]:
            if message_id < len(self.simple_memory.conversation_history):
                message = self.simple_memory.conversation_history[message_id].copy()
                message["relevance_score"] = score
                results.append(message)
        
        return results
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation"""
        if not self.conversation_summaries:
            return "No conversation summary available."
        
        # Return the most recent summary or combine multiple summaries
        if len(self.conversation_summaries) == 1:
            return self.conversation_summaries[0]["summary"]
        else:
            # Combine recent summaries
            recent_summaries = self.conversation_summaries[-3:]  # Last 3 summaries
            combined = "Recent conversation highlights:\n"
            for i, summary in enumerate(recent_summaries):
                combined += f"• {summary['summary']}\n"
            return combined
    
    def get_speaker_profile(self, speaker: str) -> Dict[str, Any]:
        """Get a profile of a speaker based on their message history"""
        if speaker not in self.speaker_keywords:
            return {"speaker": speaker, "message_count": 0, "top_topics": [], "communication_style": "unknown"}
        
        speaker_messages = [msg for msg in self.simple_memory.conversation_history if msg["speaker"] == speaker]
        
        # Get top keywords/topics for this speaker
        top_keywords = self.speaker_keywords[speaker].most_common(10)
        
        # Analyze communication style
        total_length = sum(len(msg["content"]) for msg in speaker_messages)
        avg_length = total_length / len(speaker_messages) if speaker_messages else 0
        
        communication_style = "concise" if avg_length < 50 else "detailed" if avg_length > 150 else "moderate"
        
        return {
            "speaker": speaker,
            "message_count": len(speaker_messages),
            "top_topics": [keyword for keyword, count in top_keywords],
            "communication_style": communication_style,
            "avg_message_length": avg_length
        }
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract meaningful keywords from text"""
        # Convert to lowercase and remove punctuation
        clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = clean_text.split()
        
        # Filter out common stop words and modern slang
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your', 'his', 'her', 'its', 'our', 'their',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'can', 'may', 'might', 'must', 'shall',
            'this', 'that', 'these', 'those', 'here', 'there', 'where', 'when', 'why', 'how',
            'yes', 'no', 'not', 'so', 'very', 'too', 'much', 'many', 'more', 'most', 'less', 'least',
            # Modern slang and common words
            'lol', 'omg', 'idk', 'rn', 'fr', 'yaaas', 'def', '2', 'u', 'r', 'ur', 'lowkey', 'highkey',
            'hella', 'lit', 'slay', 'vibe', 'mood', 'cap', 'no cap', 'bet', 'facts', 'periodt',
            'stan', 'tea', 'spill', 'shade', 'thirsty', 'woke', 'bae', 'fomo', 'yolo', 'fml',
            # Common short words that cause warnings
            'hi', 'me', 'go', 'up', 'hi', 'sessions', 'ways', 'obsessed', 'tbh', 'wut', 'btw',
            'omg', 'yeah', 'omg', 'yeah', 'omg', 'yeah', 'omg', 'yeah', 'omg', 'yeah'
        }
        
        # Extract meaningful keywords (length > 1, not stop words)
        keywords = {word for word in words if len(word) > 1 and word not in stop_words}
        
        return keywords
    
    def _extract_topics(self, text: str) -> Set[str]:
        """Extract potential topics from text"""
        # Define topic patterns (can be expanded)
        topic_patterns = {
            'travel': ['travel', 'trip', 'vacation', 'visit', 'country', 'city', 'hotel', 'flight', 'tourism'],
            'technology': ['computer', 'software', 'internet', 'app', 'digital', 'tech', 'programming', 'code'],
            'food': ['food', 'restaurant', 'cooking', 'recipe', 'meal', 'dinner', 'lunch', 'breakfast', 'cuisine'],
            'work': ['work', 'job', 'career', 'office', 'business', 'project', 'meeting', 'colleague', 'boss'],
            'family': ['family', 'parent', 'child', 'brother', 'sister', 'mother', 'father', 'relative'],
            'hobby': ['hobby', 'interest', 'sport', 'music', 'art', 'reading', 'gaming', 'exercise'],
            'relationship': ['friend', 'relationship', 'love', 'dating', 'marriage', 'partner', 'social'],
            'education': ['school', 'university', 'study', 'learn', 'education', 'student', 'teacher', 'course'],
            'health': ['health', 'doctor', 'medical', 'fitness', 'exercise', 'wellness', 'medicine'],
            'entertainment': ['movie', 'show', 'book', 'game', 'entertainment', 'fun', 'party', 'event']
        }
        
        text_lower = text.lower()
        detected_topics = set()
        
        for topic, keywords in topic_patterns.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected_topics.add(topic)
                    break
        
        return detected_topics
    
    def _find_relevant_messages(self, current_message: str, max_count: int) -> List[Dict]:
        """Find messages relevant to the current message"""
        current_keywords = self._extract_keywords(current_message)
        current_topics = self._extract_topics(current_message)
        
        # Score older messages (exclude recent ones)
        recent_count = 5
        older_messages = self.simple_memory.conversation_history[:-recent_count] if len(self.simple_memory.conversation_history) > recent_count else []
        
        if not older_messages:
            return []
        
        message_scores = []
        
        for i, message in enumerate(older_messages):
            score = 0
            msg_keywords = self._extract_keywords(message["content"])
            msg_topics = self._extract_topics(message["content"])
            
            # Keyword overlap
            keyword_overlap = len(current_keywords.intersection(msg_keywords))
            score += keyword_overlap * 1.0
            
            # Topic overlap (higher weight)
            topic_overlap = len(current_topics.intersection(msg_topics))
            score += topic_overlap * 3.0
            
            # Recency bonus (more recent older messages get slight bonus)
            recency_bonus = i / len(older_messages) * 0.5
            score += recency_bonus
            
            if score > 0:
                message_copy = message.copy()
                message_copy["relevance_score"] = score
                message_copy["context_type"] = "relevant_past"
                message_scores.append((score, message_copy))
        
        # Sort by score and return top messages
        message_scores.sort(key=lambda x: x[0], reverse=True)
        
        return [msg for score, msg in message_scores[:max_count]]
    
    def _create_conversation_summary(self):
        """Create a summary of recent conversation"""
        recent_messages = self.simple_memory.get_recent_messages(self.summary_threshold)
        
        if not recent_messages:
            return
        
        # Extract key information
        speakers = set(msg["speaker"] for msg in recent_messages)
        all_keywords = set()
        all_topics = set()
        
        for msg in recent_messages:
            all_keywords.update(self._extract_keywords(msg["content"]))
            all_topics.update(self._extract_topics(msg["content"]))
        
        # Create simple summary
        summary = f"Conversation between {', '.join(speakers)} "
        if all_topics:
            summary += f"discussing {', '.join(list(all_topics)[:3])}"
        elif all_keywords:
            summary += f"about {', '.join(list(all_keywords)[:5])}"
        
        summary_entry = {
            "timestamp": datetime.now().isoformat(),
            "message_range": [recent_messages[0]["timestamp"], recent_messages[-1]["timestamp"]],
            "speakers": list(speakers),
            "topics": list(all_topics),
            "keywords": list(all_keywords)[:10],
            "summary": summary
        }
        
        self.conversation_summaries.append(summary_entry)
        
        # Keep only recent summaries
        if len(self.conversation_summaries) > 10:
            self.conversation_summaries = self.conversation_summaries[-10:]
    
    def _format_context_messages(self, messages: List[Dict]) -> str:
        """Format context messages for AI prompts"""
        if not messages:
            return "No previous conversation."
        
        context_lines = []
        for msg in messages:
            timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M")
            context_type = msg.get("context_type", "")
            
            if context_type == "relevant_past":
                # Mark relevant past messages
                context_lines.append(f"[{timestamp}] (relevant) {msg['speaker']}: {msg['content']}")
            else:
                context_lines.append(f"[{timestamp}] {msg['speaker']}: {msg['content']}")
        
        return "\n".join(context_lines)
    
    def save_enhanced_data(self):
        """Save enhanced memory data"""
        try:
            os.makedirs(os.path.dirname(self.enhanced_file), exist_ok=True)
            
            enhanced_data = {
                "clone_name": self.clone_name,
                "last_updated": datetime.now().isoformat(),
                "keyword_index": dict(self.keyword_index),
                "topic_index": dict(self.topic_index),
                "speaker_keywords": {speaker: dict(counter) for speaker, counter in self.speaker_keywords.items()},
                "conversation_summaries": self.conversation_summaries
            }
            
            with open(self.enhanced_file, 'w') as f:
                json.dump(enhanced_data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving enhanced memory: {e}")
    
    def load_enhanced_data(self):
        """Load enhanced memory data from file"""
        if not os.path.exists(self.enhanced_file):
            return
        
        try:
            with open(self.enhanced_file, 'r') as f:
                enhanced_data = json.load(f)
                
            self.keyword_index = defaultdict(list, enhanced_data.get("keyword_index", {}))
            self.topic_index = defaultdict(list, enhanced_data.get("topic_index", {}))
            self.speaker_keywords = defaultdict(Counter, enhanced_data.get("speaker_keywords", {}))
            self.conversation_summaries = enhanced_data.get("conversation_summaries", [])
            
        except Exception as e:
            print(f"Warning: Error loading enhanced memory: {e}")
    
    def clear_memory(self):
        """Clear all memory data"""
        self.simple_memory.clear_memory()
        
        # Clear enhanced data
        self.keyword_index.clear()
        self.topic_index.clear()
        self.speaker_keywords.clear()
        self.conversation_summaries.clear()
        
        # Remove enhanced file
        if os.path.exists(self.enhanced_file):
            os.remove(self.enhanced_file)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics"""
        simple_stats = self.simple_memory.get_memory_stats()
        
        stats = {
            "memory_type": "enhanced",
            "simple_memory": simple_stats,
            "keyword_count": len(self.keyword_index),
            "topic_count": len(self.topic_index),
            "speakers": len(self.speaker_keywords),
            "conversation_summaries": len(self.conversation_summaries)
        }
        
        return stats
    
    # Delegate methods to simple memory
    def get_recent_messages(self, count: int = 10) -> List[Dict]:
        return self.simple_memory.get_recent_messages(count)
    
    def get_messages_by_speaker(self, speaker: str, count: int = 5) -> List[Dict]:
        return self.simple_memory.get_messages_by_speaker(speaker, count)
    
    def save_memory(self):
        self.simple_memory.save_memory()
        self.save_enhanced_data() 