#!/usr/bin/env python3
"""
Quick Start Script
Get up and running with AI clones in minutes!
"""

import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import json

# Add src to path
sys.path.append('src')

console = Console()

def main():
    """Main quick start function"""
    console.print(Panel.fit(
        "[bold blue]AI Clone Builder Quick Start[/bold blue]\n"
        "Get up and running with AI clones in minutes!",
        border_style="blue"
    ))
    
    # Test system setup first
    try:
        # Simple test to check if basic imports work
        from src.ai_clone.clone import AIClone
        from src.personality.questionnaire import QuestionnaireManager
        console.print("✅ System test passed!")
    except Exception as e:
        console.print(f"❌ Setup issue: {e}")
        console.print("Please run setup first: python tests/test_setup.py")
        return
    
    # Show options
    console.print("\n[bold]Quick Start Options:[/bold]")
    console.print("1. Quick Demo - Watch two AI clones chat (30 seconds)")
    console.print("2. Create Your Clone - Build a personality (5 minutes)")
    console.print("3. Full CLI - Access all features")
    
    choice = Prompt.ask(
        "What would you like to do?",
        choices=["1", "2", "3"],
        default="1"
    )
    
    if choice == "1":
        console.print("\n[bold blue]Running Quick Demo...[/bold blue]")
        try:
            from src.ai_clone.conversation import run_demo_conversation
            run_demo_conversation()
        except Exception as e:
            console.print(f"Demo failed: {e}")
    
    elif choice == "2":
        console.print("\n[bold blue]Let's create your AI clone...[/bold blue]")
        try:
            from src.personality.questionnaire import QuestionnaireManager
            manager = QuestionnaireManager()
            personality_data = manager.create_personality("YourClone")
            
            # Save personality
            filename = f"data/personalities/yourclone_personality.json"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w') as f:
                json.dump(personality_data, f, indent=2)
            
            console.print(f"\n[green]Your AI clone is ready! Saved as: {filename}[/green]")
            
            # Test the clone
            from src.ai_clone.clone import AIClone
            clone = AIClone(personality_data)
            response = clone.respond("Hello! Tell me about yourself.")
            console.print(f"\n[bold]{clone.name}:[/bold] {response}")
            
        except Exception as e:
            console.print(f"Error creating clone: {e}")
    
    elif choice == "3":
        console.print("\n[bold blue]Launching Full CLI...[/bold blue]")
        try:
            from src.interface.cli import main as cli_main
            cli_main()
        except Exception as e:
            console.print(f"CLI error: {e}")

if __name__ == "__main__":
    main() 