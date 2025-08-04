#!/usr/bin/env python3
"""
Quick Start Script
Get up and running with AI clones in minutes!
"""

import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

# Add src to path
sys.path.append('src')

console = Console()

def quick_start():
    """Quick start guide"""
    console.print(Panel.fit(
        "[bold blue]🚀 ai-clone-builder Quick Start[/bold blue]\n"
        "Let's get you up and running with AI clones in 3 steps!",
        border_style="blue"
    ))
    
    # Step 1: Test setup
    console.print("\n[bold]Step 1: Testing setup...[/bold]")
    
    try:
        from ai_clone.clone import test_clone_response
        console.print("✅ System test passed!")
    except Exception as e:
        console.print(f"❌ Setup issue: {e}")
        console.print("\nRun: python test_setup.py for detailed diagnostics")
        return
    
    # Step 2: Choose path
    console.print("\n[bold]Step 2: Choose your path[/bold]")
    console.print("1. 🎭 Quick Demo - Watch two AI clones chat (30 seconds)")
    console.print("2. 🧠 Create Your Clone - Build a personality (5 minutes)")
    console.print("3. 🎮 Full CLI - Access all features")
    
    choice = input("\nWhat would you like to do? (1/2/3): ").strip()
    
    if choice == "1":
        # Quick demo
        console.print("\n[bold blue]🎭 Running Quick Demo...[/bold blue]")
        try:
            from ai_clone.conversation import run_demo_conversation
            run_demo_conversation()
            console.print("\n[green]🎉 Demo complete! You just saw two AI clones having a natural conversation![/green]")
        except Exception as e:
            console.print(f"❌ Demo failed: {e}")
    
    elif choice == "2":
        # Create personality
        console.print("\n[bold blue]🧠 Let's create your AI clone...[/bold blue]")
        try:
            from personality.questionnaire import create_personality_interactive
            personality_data, filename = create_personality_interactive()
            
            if filename:
                console.print(f"\n[green]✅ Your AI clone is ready! Saved as: {filename}[/green]")
                
                # Quick test
                if Confirm.ask("Want to test a quick chat with your clone?"):
                    from ai_clone.clone import AIClone
                    clone = AIClone(personality_data)
                    
                    console.print(f"\n[bold]{clone.name}[/bold]: Hi! I'm your AI clone. Ask me anything!")
                    
                    for _ in range(3):  # 3 quick exchanges
                        user_input = input("\nYou: ")
                        if user_input.lower() in ['quit', 'bye']:
                            break
                        response = clone.respond(user_input)
                        console.print(f"{clone.name}: {response}")
                    
                    console.print(f"\n[green]🎉 Your clone {clone.name} is working perfectly![/green]")
            
        except Exception as e:
            console.print(f"❌ Error creating clone: {e}")
    
    elif choice == "3":
        # Full CLI
        console.print("\n[bold blue]🎮 Starting Full CLI...[/bold blue]")
        try:
            from interface.cli import main
            main()
        except Exception as e:
            console.print(f"❌ CLI error: {e}")
    
    else:
        console.print("Invalid choice. Run the script again!")
        return
    
    # Next steps
    console.print("\n" + "="*50)
    console.print("[bold]🔥 Next Steps:[/bold]")
    console.print("• Run: python -m src.interface.cli (Full interface)")
    console.print("• Run: python test_setup.py (System diagnostics)")
    console.print("• Create more clones and watch them interact!")
    console.print("• Check data/personalities/ for saved clones")
    console.print("• Check data/conversations/ for chat logs")

if __name__ == "__main__":
    quick_start() 