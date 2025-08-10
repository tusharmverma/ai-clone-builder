#!/usr/bin/env python3
"""
Quick Start Script for AI Clone Builder

This script provides a user-friendly entry point to the AI Clone Builder system,
allowing users to quickly get started with creating and testing AI clones.

Features:
- Quick demo of AI clone conversations
- Interactive personality creation wizard
- Full CLI access for advanced users
- System setup validation

Usage:
    python quick_start.py

Author: AI Clone Builder Team
Version: 1.0.0
"""

import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import json

# Add src to path for imports
sys.path.append('src')

console = Console()

def main():
    """
    Main quick start function that orchestrates the user experience.
    
    This function serves as the primary entry point, providing users with
    three main options: running a quick demo, creating a new AI clone,
    or accessing the full CLI interface. It also performs basic system
    validation to ensure all dependencies are properly installed.
    
    The function handles user input, manages the flow between different
    features, and provides error handling for common setup issues.
    
    Returns:
        None
        
    Raises:
        Exception: If there are critical system setup issues
    """
    
    # Quick start entry point
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
        _run_quick_demo()
    elif choice == "2":
        _create_user_clone()
    elif choice == "3":
        _launch_full_cli()

def _run_quick_demo():
    """
    Run a quick demonstration of AI clone conversations.
    
    This function launches a pre-configured demo conversation between
    two AI clones to showcase the system's capabilities. The demo
    is designed to be brief (approximately 30 seconds) and gives
    users a taste of what the system can do.
    
    Returns:
        None
        
    Raises:
        Exception: If the demo fails to run
    """
    console.print("\n[bold blue]Running Quick Demo...[/bold blue]")
    try:
        from src.ai_clone.conversation import run_demo_conversation
        run_demo_conversation()
    except Exception as e:
        console.print(f"Demo failed: {e}")

def _create_user_clone():
    """
    Guide the user through creating their own AI clone.
    
    This function provides an interactive wizard for creating a new
    AI clone personality. It uses the QuestionnaireManager to collect
    information about the user's desired personality traits, communication
    style, interests, and background. The process typically takes about
    5 minutes and results in a fully functional AI clone.
    
    The created personality is automatically saved to the data/personalities
    directory and can be immediately tested with a sample conversation.
    
    Returns:
        None
        
    Raises:
        Exception: If there's an error during personality creation
    """
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

def _launch_full_cli():
    """
    Launch the full command-line interface for advanced users.
    
    This function provides access to the complete CLI system, which
    includes all features of the AI Clone Builder such as advanced
    personality management, memory operations, conversation history,
    and system configuration options.
    
    Returns:
        None
        
    Raises:
        Exception: If there's an error launching the CLI
    """
    console.print("\n[bold blue]Launching Full CLI...[/bold blue]")
    try:
        from src.interface.cli import main as cli_main
        cli_main()
    except Exception as e:
        console.print(f"CLI error: {e}")

if __name__ == "__main__":
    main() 