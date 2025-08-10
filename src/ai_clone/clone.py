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
    from ..memory.memory_manager import MemoryManager
    from ..memory.sqlite_vec_memory import SqliteVecMemory
    from ..memory.enhanced_memory import EnhancedMemory
    from ..memory.simple_memory import SimpleMemory
except ImportError:
    # Add parent directory to path for direct execution
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    from personality.templates import PersonalityTemplate
    from memory.memory_manager import MemoryManager
    from memory.sqlite_vec_memory import SqliteVecMemory
    from memory.enhanced_memory import EnhancedMemory
    from memory.simple_memory import SimpleMemory

class AIClone:
    """An AI clone with personality that can have conversations"""
    
    def __init__(self, personality_data: Dict[str, Any], ollama_host: str = "http://localhost:11434", memory_type: str = "sqlite_vec"):
        self.personality_data = personality_data
        self.name = personality_data["basic_info"]["name"]
        self.ollama_host = ollama_host
        self.model = "llama3.2:3b"  # Default model
        self.conversation_history = []
        
        # Initialize memory system
        self.memory_type = memory_type
        self.memory = self._initialize_memory()
        
        # Create system prompt from personality
        self.system_prompt = PersonalityTemplate.create_system_prompt(personality_data)
        
        # Test connection on initialization
        self._test_ollama_connection()
    
    def _initialize_memory(self):
        """Initialize the appropriate memory system"""
        try:
            # Check if user wants intelligent memory management
            if self.memory_type == "auto" or self.memory_type == "intelligent":
                return MemoryManager(self.name, auto_select=True)
            
            # Direct memory type selection - prioritize SQLite vector memory
            if self.memory_type == "sqlite_vec" or self.memory_type == "vector":
                try:
                    return SqliteVecMemory(self.name)
                except Exception as e:
                    print(f"⚠️ SQLite vector memory failed: {e}, falling back to enhanced")
                    return EnhancedMemory(self.name)
            elif self.memory_type == "enhanced":
                return EnhancedMemory(self.name)
            elif self.memory_type == "simple":
                return SimpleMemory(self.name)
            else:
                print(f"Warning: Unknown memory type '{self.memory_type}', using SQLite vector memory")
                try:
                    return SqliteVecMemory(self.name)
                except Exception as e:
                    print(f"⚠️ SQLite vector memory failed: {e}, falling back to enhanced")
                    return EnhancedMemory(self.name)
        except Exception as e:
            print(f"Warning: Error initializing memory: {e}, using basic conversation history")
            return None
    
    def _test_ollama_connection(self):
        """Test if Ollama is running and model is available"""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags")
            if response.status_code != 200:
                raise ConnectionError("Ollama server not responding")
            
            models = response.json().get("models", [])
            model_names = [model["name"] for model in models]
            
            if self.model not in model_names:
                print(f"Warning: Model {self.model} not found. Available: {', '.join(model_names[:3])}")
                print(f"Run: ollama pull {self.model}")
        except Exception as e:
            print(f"Warning: Ollama connection test failed: {e}")
            print("Make sure Ollama is running: ollama serve")
    
    def respond(self, message: str, context: List[Dict] = None) -> str:
        """Generate a response to a message"""
        try:
            # Get conversation context
            if context is None:
                context = self.get_recent_history(5)
            
            # Build the prompt
            prompt = self._build_prompt(message, context)
            
            # Get response from Ollama
            response = self._call_ollama(prompt)
            
            # Post-process the response
            processed_response = self._post_process_response(response)
            
            # Add to conversation history
            self.add_to_conversation_history("User", message)
            self.add_to_conversation_history(self.name, processed_response)
            
            return processed_response
            
        except Exception as e:
            error_msg = f"Sorry, I'm having trouble responding right now: {str(e)}"
            print(f"Error in respond(): {e}")
            return error_msg
    
    def _build_prompt(self, message: str, context: List[Dict]) -> str:
        """Build the complete prompt for Ollama"""
        # Start with system prompt
        prompt = f"{self.system_prompt}\n\n"
        
        # Add conversation context if available
        if context and self.memory:
            try:
                context_str = self.memory.get_context()
                if context_str:
                    prompt += f"RECENT CONVERSATION CONTEXT:\n{context_str}\n\n"
            except Exception as e:
                print(f"Warning: Could not get memory context: {e}")
        
        # Add response length instruction based on message complexity and personality
        response_instruction = self._get_response_length_instruction(message)
        if response_instruction:
            prompt += f"RESPONSE STYLE: {response_instruction}\n\n"
        
        # Add the current message
        prompt += f"User: {message}\n{self.name}: "
        
        return prompt
    
    def _get_response_length_instruction(self, message: str) -> str:
        """Get intelligent response length instruction based on message and personality"""
        try:
            # Get personality preferences
            comm_style = self.personality_data.get("communication_style", {})
            response_length_pref = comm_style.get("response_length", {}).get("choice", "")
            age = int(self.personality_data["basic_info"].get("age", 25))
            
            # Get personality traits for more nuanced instructions
            traits = self.personality_data.get("personality_traits", {})
            extraversion = traits.get("extraversion", {}).get("choice", "")
            expressiveness = comm_style.get("expressiveness", {}).get("choice", "")
            
            # Analyze message complexity
            message_lower = message.lower()
            is_question = message.endswith('?')
            is_greeting = any(word in message_lower for word in ['hi', 'hello', 'hey', 'how are you'])
            is_simple = len(message.split()) <= 3
            is_complex = any(word in message_lower for word in ['explain', 'describe', 'tell me about', 'what do you think', 'why', 'how'])
            
            # Build personalized instruction based on personality
            instruction_parts = []
            
            # Base response length
            if "Very short" in response_length_pref:
                instruction_parts.append("Keep your response very brief (1-2 sentences max)")
            elif "Short and concise" in response_length_pref:
                instruction_parts.append("Keep your response short and to the point (2-3 sentences)")
            elif "Medium length" in response_length_pref:
                instruction_parts.append("Use medium length responses (3-4 sentences)")
            elif "Detailed and thorough" in response_length_pref:
                instruction_parts.append("Provide detailed, thoughtful responses (4+ sentences)")
            
            # Add personality-specific guidance
            if "Very extroverted" in extraversion:
                instruction_parts.append("Show your social energy and enthusiasm")
            elif "Somewhat introverted" in extraversion:
                instruction_parts.append("Be thoughtful and measured in your response")
            
            if "Very expressive" in expressiveness:
                instruction_parts.append("Show your emotions and enthusiasm naturally")
            elif "reserved" in expressiveness.lower():
                instruction_parts.append("Keep your response measured and thoughtful")
            
            # Add age-appropriate language guidance
            if age < 20:
                instruction_parts.append("Use Gen Z language patterns and modern slang naturally")
            elif age < 30:
                instruction_parts.append("Balance casual and thoughtful communication")
            elif age < 50:
                instruction_parts.append("Use professional but approachable language")
            else:
                instruction_parts.append("Use mature, thoughtful communication")
            
            # Add context-specific guidance
            if is_greeting or is_simple:
                instruction_parts.append("Keep it casual and friendly")
            elif is_complex:
                instruction_parts.append("Provide a helpful, focused answer")
            else:
                instruction_parts.append("Respond naturally to the conversation flow")
            
            return ". ".join(instruction_parts) + "."
                    
        except Exception as e:
            print(f"Warning: Error getting response instruction: {e}")
            return "Keep your response natural and appropriate to the conversation."
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API to generate response"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 300,  # Reasonable limit, model should follow instructions
                    "repeat_penalty": 1.1,  # Prevent repetitive responses
                    "top_k": 40  # Better response diversity
                }
            }
            
            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                raise Exception(f"Ollama API error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            raise Exception("Request timed out - Ollama is taking too long to respond")
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to Ollama - make sure it's running")
        except Exception as e:
            raise Exception(f"Error calling Ollama: {str(e)}")
    
    def _get_response_length_constraint(self) -> int:
        """Get response length constraint based on personality"""
        try:
            comm_style = self.personality_data.get("communication_style", {})
            response_length = comm_style.get("response_length", {}).get("choice", "")
            
            if "Very short" in response_length:
                return 50
            elif "Short and concise" in response_length:
                return 100
            elif "Medium length" in response_length:
                return 200
            elif "Detailed and thorough" in response_length:
                return 400
            else:
                return 150  # Default
        except:
            return 150
    
    def _post_process_response(self, response: str) -> str:
        """Post-process the AI response to match personality"""
        try:
            # Clean up the response
            response = response.strip()
            
            # Only apply length constraints if the model didn't follow instructions
            # and the response is significantly longer than expected
            comm_style = self.personality_data.get("communication_style", {})
            response_length = comm_style.get("response_length", {}).get("choice", "")
            age = int(self.personality_data["basic_info"].get("age", 25))
            
            # Only truncate if response is way too long (model didn't follow instructions)
            if "Very short" in response_length and len(response) > 150:
                response = self._intelligently_shorten_response(response, 150, age)
            elif "Short and concise" in response_length and len(response) > 250:
                response = self._intelligently_shorten_response(response, 250, age)
            
            # Remove any trailing incomplete sentences (but only if we have multiple sentences)
            if response and not response.endswith(('.', '!', '?', '...')):
                # Find the last complete sentence
                sentences = response.split('. ')
                if len(sentences) > 1 and len(sentences[-1].strip()) > 0:
                    # Only remove if the last part is actually incomplete
                    response = '. '.join(sentences[:-1]) + '.'
            
            return response
            
        except Exception as e:
            print(f"Warning: Error in post-processing: {e}")
            return response.strip()
    
    def _intelligently_shorten_response(self, response: str, max_length: int, age: int) -> str:
        """Intelligently shorten response while maintaining personality"""
        if len(response) <= max_length:
            return response
        
        # Split into sentences
        sentences = response.split('. ')
        
        # If no periods found, treat as single sentence
        if len(sentences) == 1:
            if len(response) <= max_length:
                return response
            else:
                # Shorten by words
                words = response.split()
                shortened = ""
                for word in words:
                    if len(shortened + word + " ") <= max_length:
                        shortened += word + " "
                    else:
                        break
                return shortened.strip()
        
        # Try to keep complete sentences
        shortened = ""
        for sentence in sentences:
            if len(shortened + sentence + '. ') <= max_length:
                shortened += sentence + '. '
            else:
                break
        
        # If still too long, condense individual sentences
        if len(shortened) > max_length:
            shortened = self._condense_sentence(shortened, age)
        
        return shortened.strip()
    
    def _condense_sentence(self, sentence: str, age: int) -> str:
        """Condense a sentence based on age-appropriate language"""
        # Simple condensation for very short responses
        if age < 20:
            # Gen Z style - very concise
            words = sentence.split()
            if len(words) > 8:
                return ' '.join(words[:8]) + '...'
        elif age < 30:
            # Millennial style - moderately concise
            words = sentence.split()
            if len(words) > 12:
                return ' '.join(words[:12]) + '...'
        
        return sentence
    
    def add_to_conversation_history(self, speaker: str, message: str):
        """Add a message to conversation history"""
        timestamp = datetime.now().isoformat()
        entry = {
            "speaker": speaker,
            "content": message,
            "timestamp": timestamp
        }
        
        self.conversation_history.append(entry)
        
        # Also add to memory system if available
        if self.memory:
            try:
                self.memory.add_message(speaker, message)
            except Exception as e:
                print(f"Warning: Could not add to memory: {e}")
    
    def get_recent_history(self, count: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        return self.conversation_history[-count:] if self.conversation_history else []
    
    def save_conversation(self, filename: str = None):
        """Save conversation to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/conversations/{self.name}_{timestamp}_conversation.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        conversation_data = {
            "clone_name": self.name,
            "personality_file": f"{self.name.lower().replace(' ', '_')}_personality.json",
            "conversation_history": self.conversation_history,
            "saved_at": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(conversation_data, f, indent=2)
        
        print(f"Conversation saved to: {filename}")
        return filename
    
    def load_conversation(self, filename: str):
        """Load conversation from file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.conversation_history = data.get("conversation_history", [])
                print(f"Loaded conversation with {len(self.conversation_history)} messages")
        except Exception as e:
            print(f"Error loading conversation: {e}")
    
    def get_personality_summary(self) -> str:
        """Get a brief summary of the clone's personality"""
        basic = self.personality_data["basic_info"]
        return f"{basic['age']}-year-old {basic['occupation']} from {basic['location']}"

def load_clone_from_file(personality_file: str) -> AIClone:
    """Load a clone from a personality file"""
    try:
        with open(personality_file, 'r') as f:
            personality_data = json.load(f)
        return AIClone(personality_data)
    except Exception as e:
        print(f"Error loading clone from {personality_file}: {e}")
        return None

def create_demo_clones(memory_type: str = "sqlite_vec") -> List[AIClone]:
    """Create demo clones for testing"""
    from personality.templates import create_demo_personalities
    
    # Create demo personalities
    demo_personalities = create_demo_personalities()
    if demo_personalities:
        clones = []
        for personality in demo_personalities:
            clone = AIClone(personality, memory_type=memory_type)
            clones.append(clone)
        return clones
    else:
        # Fallback if no demo personalities available
        print("Warning: No demo personalities available")
        return [] 