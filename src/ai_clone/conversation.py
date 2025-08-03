"""
Conversation System
Handles conversations between AI clones
"""

import time
import random
import sys
import os
from typing import List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table

# Handle imports for both package and direct execution
try:
    from .clone import AIClone
    from ..memory.simple_memory import ConversationManager
except ImportError:
    # For direct execution
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    from ai_clone.clone import AIClone
    from memory.simple_memory import ConversationManager

console = Console()

class CloneConversation:
    """Manages conversations between two AI clones"""
    
    def __init__(self, clone1: AIClone, clone2: AIClone):
        self.clone1 = clone1
        self.clone2 = clone2
        self.conversation_manager = ConversationManager()
        self.current_conversation_id = None
        self.conversation_scenarios = [
            "You're both at a coffee shop and just met. Start a natural conversation.",
            "You're on a first date at a cozy restaurant. Get to know each other.",
            "You're both waiting for a delayed flight. Strike up a conversation.",
            "You met at a mutual friend's party. Find common interests.",
            "You're both in a bookstore browsing. Start chatting about books.",
            "You're in line at a food truck. Make conversation while waiting."
        ]
    
    def start_conversation(self, scenario: str = None, max_turns: int = 10) -> str:
        """Start a conversation between the two clones"""
        if not scenario:
            scenario = random.choice(self.conversation_scenarios)
        
        # Start conversation
        self.current_conversation_id = self.conversation_manager.start_conversation(
            self.clone1.name, self.clone2.name, scenario
        )
        
        console.print(Panel.fit(
            f"[bold blue]🗨️  Starting Conversation[/bold blue]\n"
            f"Participants: {self.clone1.name} & {self.clone2.name}\n"
            f"Scenario: {scenario}",
            border_style="blue"
        ))
        
        return self.current_conversation_id
    
    def run_conversation(self, scenario: str = None, max_turns: int = 10, delay: float = 2.0):
        """Run a full conversation between clones"""
        conv_id = self.start_conversation(scenario, max_turns)
        
        # Initial message from clone1
        initial_prompt = f"Scenario: {scenario}\nStart a natural conversation. Be yourself and engage authentically."
        
        current_speaker = self.clone1
        other_speaker = self.clone2
        conversation_history = []
        
        # First message
        response = current_speaker.respond(initial_prompt)
        self._display_message(current_speaker.name, response)
        
        # Add to conversation history
        self.conversation_manager.add_message_to_conversation(conv_id, current_speaker.name, response)
        conversation_history.append({"speaker": current_speaker.name, "content": response})
        
        # Continue conversation
        for turn in range(max_turns - 1):
            time.sleep(delay)  # Natural pause
            
            # Switch speakers
            current_speaker, other_speaker = other_speaker, current_speaker
            
            # Get recent history for context
            recent_history = conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history
            
            # Generate response
            context_prompt = self._build_context_prompt(recent_history, conversation_history[0]["content"] if conversation_history else "")
            response = current_speaker.respond(context_prompt, recent_history)
            
            # Display response
            self._display_message(current_speaker.name, response)
            
            # Add to conversation
            self.conversation_manager.add_message_to_conversation(conv_id, current_speaker.name, response)
            conversation_history.append({"speaker": current_speaker.name, "content": response})
            
            # Check if conversation should end naturally
            if self._should_end_conversation(response, turn):
                break
        
        # End conversation
        self.conversation_manager.end_conversation(conv_id)
        
        console.print(Panel.fit(
            f"[bold green]✅ Conversation Complete[/bold green]\n"
            f"Total messages: {len(conversation_history)}\n"
            f"Saved as: conversation_{conv_id}.json",
            border_style="green"
        ))
        
        return conversation_history
    
    def _display_message(self, speaker: str, message: str):
        """Display a message in a nice format"""
        # Color coding for different speakers
        if speaker == self.clone1.name:
            color = "cyan"
            icon = "🗣️"
        else:
            color = "yellow"
            icon = "💭"
        
        console.print(f"\n[bold {color}]{icon} {speaker}:[/bold {color}]")
        console.print(f"[{color}]{message}[/{color}]")
    
    def _build_context_prompt(self, recent_history: List[Dict], initial_context: str) -> str:
        """Build a context prompt for the AI"""
        if not recent_history:
            return "Continue the conversation naturally."
        
        last_message = recent_history[-1]
        other_speaker = last_message["speaker"]
        last_content = last_message["content"]
        
        prompt = f"{other_speaker} just said: \"{last_content}\"\n\nRespond naturally as yourself. Keep the conversation going."
        
        return prompt
    
    def _should_end_conversation(self, response: str, turn: int) -> bool:
        """Determine if conversation should end naturally"""
        ending_indicators = [
            "nice talking to you",
            "i should get going",
            "great meeting you",
            "see you later",
            "have a good",
            "take care",
            "goodbye",
            "bye",
            "gotta run"
        ]
        
        response_lower = response.lower()
        return any(indicator in response_lower for indicator in ending_indicators)
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the current conversation"""
        if not self.current_conversation_id:
            return {"error": "No active conversation"}
        
        history = self.conversation_manager.get_conversation_history(self.current_conversation_id)
        
        return {
            "conversation_id": self.current_conversation_id,
            "participants": [self.clone1.name, self.clone2.name],
            "total_messages": len(history),
            "last_message": history[-1] if history else None
        }

def run_demo_conversation():
    """Run a demo conversation with pre-built clones"""
    console.print(Panel.fit(
        "[bold blue]🎭 Demo Conversation[/bold blue]\n"
        "Creating two AI clones and watching them chat...",
        border_style="blue"
    ))
    
    try:
        # Create demo clones
        try:
            from .clone import create_demo_clones
        except ImportError:
            from ai_clone.clone import create_demo_clones
        
        clones = create_demo_clones()
        
        if len(clones) < 2:
            console.print("[red]❌ Need at least 2 clones for conversation[/red]")
            return
        
        # Start conversation
        conversation = CloneConversation(clones[0], clones[1])
        
        # Show clone info
        console.print(f"\n[bold]👤 {clones[0].name}:[/bold] {clones[0].get_personality_summary()}")
        console.print(f"[bold]👤 {clones[1].name}:[/bold] {clones[1].get_personality_summary()}")
        
        # Run conversation
        history = conversation.run_conversation(max_turns=8, delay=1.5)
        
        return history
        
    except Exception as e:
        console.print(f"[red]❌ Error running demo conversation: {e}[/red]")
        return None

def interactive_conversation_setup():
    """Interactive setup for clone conversations"""
    console.print(Panel.fit(
        "[bold blue]🎮 Interactive Conversation Setup[/bold blue]\n"
        "Set up a conversation between your AI clones",
        border_style="blue"
    ))
    
    # This would integrate with saved personalities
    # For now, just run demo
    return run_demo_conversation()

if __name__ == "__main__":
    run_demo_conversation() 