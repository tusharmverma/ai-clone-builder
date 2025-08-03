"""
AI Clone Implementation
Main class for creating and managing AI clones with personalities
"""

import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import os
import sys

# Handle imports for both package and direct execution
try:
    from ..personality.templates import PersonalityTemplate
except ImportError:
    # Add parent directory to path for direct execution
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    from personality.templates import PersonalityTemplate

class AIClone:
    """An AI clone with personality that can have conversations"""
    
    def __init__(self, personality_data: Dict[str, Any], ollama_host: str = "http://localhost:11434"):
        self.personality_data = personality_data
        self.name = personality_data["basic_info"]["name"]
        self.ollama_host = ollama_host
        self.model = "llama3.2:3b"  # Default model
        self.conversation_history = []
        
        # Create system prompt from personality
        self.system_prompt = PersonalityTemplate.create_system_prompt(personality_data)
        
        # Test connection on initialization
        self._test_ollama_connection()
    
    def _test_ollama_connection(self):
        """Test if Ollama is running and model is available"""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags")
            if response.status_code != 200:
                raise ConnectionError("Ollama server not responding")
            
            models = response.json().get("models", [])
            model_names = [model["name"] for model in models]
            
            if self.model not in model_names:
                print(f"⚠️  Model {self.model} not found. Available models: {model_names}")
                print(f"Run: ollama pull {self.model}")
                
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "❌ Cannot connect to Ollama. Make sure it's running:\n"
                "1. Install Ollama: https://ollama.com/\n"
                "2. Run: ollama pull llama3.2:3b\n"
                "3. Start Ollama service"
            )
    
    def respond(self, message: str, context: List[Dict] = None) -> str:
        """Generate a response to a message"""
        # Prepare conversation context
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add recent context if provided
        if context:
            for msg in context[-5:]:  # Last 5 messages for context
                messages.append({
                    "role": "user" if msg["speaker"] != self.name else "assistant",
                    "content": msg["content"]
                })
        
        # Add the current message
        messages.append({"role": "user", "content": message})
        
        # Make request to Ollama
        try:
            response = requests.post(
                f"{self.ollama_host}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 150
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["message"]["content"].strip()
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            return "⏱️ Response timed out. The model might be processing..."
        except Exception as e:
            return f"❌ Error generating response: {str(e)}"
    
    def add_to_conversation_history(self, speaker: str, message: str):
        """Add a message to conversation history"""
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": speaker,
            "content": message
        })
    
    def get_recent_history(self, count: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        return self.conversation_history[-count:] if self.conversation_history else []
    
    def save_conversation(self, filename: str = None):
        """Save conversation history to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/conversations/{self.name}_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump({
                "clone_name": self.name,
                "personality_summary": {
                    "age": self.personality_data["basic_info"]["age"],
                    "location": self.personality_data["basic_info"]["location"],
                    "style": self.personality_data["communication_style"]["formality"]["choice"]
                },
                "conversation": self.conversation_history
            }, f, indent=2)
        
        return filename
    
    def load_conversation(self, filename: str):
        """Load conversation history from file"""
        with open(filename, 'r') as f:
            data = json.load(f)
            self.conversation_history = data.get("conversation", [])
    
    def get_personality_summary(self) -> str:
        """Get a quick personality summary"""
        basic = self.personality_data["basic_info"]
        comm = self.personality_data["communication_style"]
        interests = self.personality_data["interests"]
        
        return (f"{basic['name']}, {basic['age']}, from {basic['location']}. "
                f"Style: {comm['formality']['choice']}, {comm['humor']['choice']}. "
                f"Interests: {interests['hobbies'][:50]}...")

def load_clone_from_file(personality_file: str) -> AIClone:
    """Load an AI clone from a personality file"""
    with open(personality_file, 'r') as f:
        personality_data = json.load(f)
    
    return AIClone(personality_data)

def create_demo_clones() -> List[AIClone]:
    """Create demo clones for testing"""
    try:
        from personality.templates import create_demo_personalities
    except ImportError:
        try:
            from ..personality.templates import create_demo_personalities
        except ImportError:
            # For direct execution
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sys.path.insert(0, parent_dir)
            from personality.templates import create_demo_personalities
    
    demo_personalities = create_demo_personalities()
    clones = []
    
    for personality_data in demo_personalities:
        clone = AIClone(personality_data)
        clones.append(clone)
    
    return clones

# Quick test function
def test_clone_response():
    """Test function to check if AI clone is working"""
    try:
        from personality.templates import create_demo_personalities
    except ImportError:
        try:
            from ..personality.templates import create_demo_personalities
        except ImportError:
            # For direct execution
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sys.path.insert(0, parent_dir)
            from personality.templates import create_demo_personalities
    
    print("🧪 Testing AI Clone...")
    demo_personalities = create_demo_personalities()
    
    # Create test clone
    alex = AIClone(demo_personalities[0])
    print(f"✅ Created clone: {alex.get_personality_summary()}")
    
    # Test response
    test_message = "Hi! What do you like to do for fun?"
    print(f"\n💬 Test message: {test_message}")
    response = alex.respond(test_message)
    print(f"🤖 {alex.name}: {response}")
    
    return alex

if __name__ == "__main__":
    test_clone_response() 