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
    
    # Manages clone-to-clone conversations with scenarios
    
    def __init__(self, clone1: AIClone, clone2: AIClone):
        self.clone1 = clone1
        self.clone2 = clone2
        self.conversation_manager = ConversationManager()
        self.current_conversation_id = None
        self.conversation_scenarios = [
            # Original dating scenarios (6)
            "You're both at a coffee shop and just met. Start a natural conversation.",
            "You're on a first date at a cozy restaurant. Get to know each other.", 
            "You're both waiting for a delayed flight. Strike up a conversation.",
            "You met at a mutual friend's party. Find common interests.",
            "You're both in a bookstore browsing. Start chatting about books.",
            "You're in line at a food truck. Make conversation while waiting.",
            
            # Expanded dating scenarios (8)
            "You're both at a weekend farmer's market. Start talking about the local produce.",
            "You're waiting in line at a trendy brunch place on Sunday morning.",
            "You're both attending a wine tasting event. Discuss your preferences.",
            "You meet at a dog park while your pets are playing together.",
            "You're both browsing records at a vintage music store.",
            "You're seated next to each other at a cooking class.",
            "You're both volunteering at a community garden on Saturday.",
            "You meet while hiking the same trail on a beautiful morning.",
            
            # Social scenarios (6)
            "You're both at a tech meetup networking event. Find professional connections.",
            "You're waiting for the same yoga class to start. Chat about wellness.",
            "You're both art enthusiasts at a gallery opening. Discuss the exhibits.",
            "You meet at a book club meeting before it starts.",
            "You're both attending a photography workshop. Share your interests.",
            "You're at a board game cafe and decide to play together.",
            
            # Casual encounter scenarios (6)
            "You're both stuck in an elevator for a few minutes. Make small talk.",
            "You're waiting in line at the bank on a busy Friday afternoon.",
            "You're both browsing the same section at a large bookstore.",
            "You meet at a bus stop while waiting for public transport.",
            "You're both shopping for groceries and reach for the same item.",
            "You're sitting next to each other at a coffee shop with laptops.",
            
            # Activity-based scenarios (6)
            "You're both taking a pottery class and working on similar projects.",
            "You meet at a local trivia night and decide to team up.",
            "You're both at a rooftop bar watching the sunset.",
            "You're attending the same concert and start chatting during intermission.",
            "You meet while browsing at a weekend antique market.",
            "You're both waiting for your orders at a busy lunch spot."
        ]
    
    def start_conversation(self, max_turns: int = 10):
        """
        Start a conversation between two AI clones.
        
        This method initiates a conversation between the two clones, taking turns
        to respond to each other. It handles the conversation flow and displays
        messages in a formatted way.
        
        Args:
            max_turns (int): Maximum number of conversation turns (default: 10)
        """
        console.print(Panel.fit(
            f"[bold blue]Starting Conversation[/bold blue]\n"
            f"{self.clone1.name} and {self.clone2.name} will chat for up to {max_turns} turns",
            border_style="blue"
        ))
        
        # Initial greeting
        console.print(f"\n[bold]{self.clone1.name}:[/bold] Hello! How are you doing today?")
        
        turn_count = 0
        current_speaker = self.clone2
        last_speaker = self.clone1
        
        while turn_count < max_turns:
            try:
                # Get response from current speaker
                response = current_speaker.respond(
                    f"Continue the conversation naturally. You're chatting with {last_speaker.name}."
                )
                
                # Display response
                console.print(f"[bold]{current_speaker.name}:[/bold] {response}")
                
                # Switch speakers
                last_speaker = current_speaker
                current_speaker = self.clone1 if current_speaker == self.clone2 else self.clone2
                
                turn_count += 1
                
                # Small delay to make conversation feel natural
                time.sleep(1)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Conversation interrupted by user[/yellow]")
                break
            except Exception as e:
                console.print(f"\n[red]Error in conversation: {e}[/red]")
                break
        
        console.print(f"\n[bold green]Conversation Complete[/bold green]\n")
        console.print(f"Total turns: {turn_count}")
        console.print(f"Messages saved to memory for both clones")
    
    def run_conversation(self, scenario: str = None, max_turns: int = 10, delay: float = 2.0):
        """
        Run a full conversation between clones with scenario context.
        
        This method creates a more structured conversation by providing a specific
        scenario context and managing the conversation flow through the conversation
        manager. It handles turn-taking and saves the conversation to memory.
        
        Args:
            scenario (str, optional): A specific scenario to set the conversation context
            max_turns (int): Maximum number of conversation turns (default: 10)
            delay (float): Delay between messages in seconds (default: 2.0)
            
        Returns:
            List[Dict]: The complete conversation history
        """
        # Start conversation and get conversation ID
        conv_id = self.conversation_manager.start_conversation(self.clone1.name, self.clone2.name, scenario)
        
        # Initial message from clone1
        initial_prompt = f"Scenario: {scenario or 'General conversation'}\nStart a natural conversation. Be yourself and engage authentically."
        
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
            response = current_speaker.respond(context_prompt)
            
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
        """
        Display a message with appropriate styling based on the speaker.
        
        This method formats and displays messages with color coding to distinguish
        between different speakers in the conversation.
        
        Args:
            speaker (str): The name of the person speaking
            message (str): The message content to display
        """
        if speaker == self.clone1.name:
            color = "blue"
        elif speaker == self.clone2.name:
            color = "green"
        else:
            color = "white"
        
        console.print(f"\n[bold {color}]{speaker}:[/bold {color}]")
        console.print(f"[{color}]{message}[/{color}]")
    
    def _build_context_prompt(self, recent_history: List[Dict], initial_context: str) -> str:
        """
        Build a context prompt for the AI based on recent conversation history.
        
        This method creates a prompt that gives the AI context about what was
        recently said, helping maintain conversation continuity.
        
        Args:
            recent_history (List[Dict]): Recent conversation messages
            initial_context (str): The initial scenario or context
            
        Returns:
            str: A formatted prompt with conversation context
        """
        if not recent_history:
            return "Continue the conversation naturally."
        
        last_message = recent_history[-1]
        other_speaker = last_message["speaker"]
        last_content = last_message["content"]
        
        prompt = f"{other_speaker} just said: \"{last_content}\"\n\nRespond naturally as yourself. Keep the conversation going."
        
        return prompt
    
    def _should_end_conversation(self, response: str, turn: int) -> bool:
        """
        Determine if the conversation should end naturally.
        
        This method analyzes the response content and turn number to decide
        if the conversation has reached a natural conclusion.
        
        Args:
            response (str): The last response from a clone
            turn (int): The current turn number
            
        Returns:
            bool: True if the conversation should end, False otherwise
        """
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
        """
        Get a summary of the current conversation.
        
        This method retrieves metadata about the active conversation including
        the conversation ID, participants, total message count, and the last
        message exchanged.
        
        Returns:
            Dict[str, Any]: Summary containing conversation metadata, or error dict if no active conversation
        """
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
    """
    Run a demo conversation with pre-built AI clones.
    
    This function creates two demo AI clones with predefined personalities
    and runs a conversation between them to showcase the system's capabilities.
    The demo includes scenario-based conversation with natural turn-taking
    and displays the conversation in real-time.
    
    Returns:
        List[Dict]: The complete conversation history, or None if the demo fails
    """
    console.print(Panel.fit(
        "[bold blue]Demo Conversation[/bold blue]\n"
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
            console.print("[red]Need at least 2 clones for conversation[/red]")
            return
        
        # Start conversation
        conversation = CloneConversation(clones[0], clones[1])
        
        # Show clone info
        console.print(f"\n[bold]{clones[0].name}:[/bold] {clones[0].get_personality_summary()}")
        console.print(f"[bold]{clones[1].name}:[/bold] {clones[1].get_personality_summary()}")
        
        # Run conversation
        history = conversation.run_conversation(max_turns=8, delay=1.5)
        
        return history
        
    except Exception as e:
        console.print(f"[red]Error running demo conversation: {e}[/red]")
        return None

def interactive_conversation_setup():
    """
    Interactive setup for clone conversations.
    
    This function provides an interactive interface for users to set up
    conversations between their saved AI clones. It currently defaults
    to running the demo conversation but is designed to be extended
    with user personality selection and custom scenario creation.
    
    Returns:
        List[Dict]: The conversation history from the selected conversation type
    """
    console.print(Panel.fit(
        "[bold blue]Interactive Conversation Setup[/bold blue]\n"
        "Set up a conversation between your AI clones",
        border_style="blue"
    ))
    
    # This would integrate with saved personalities
    # For now, just run demo
    return run_demo_conversation()

if __name__ == "__main__":
    run_demo_conversation() 