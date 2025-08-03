"""
Command Line Interface
Main CLI for interacting with AI clones
"""

import sys
import os
from typing import List, Dict
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.personality.questionnaire import PersonalityQuestionnaire, create_personality_interactive
from src.ai_clone.clone import AIClone, load_clone_from_file
from src.ai_clone.conversation import CloneConversation, run_demo_conversation
from src.memory.simple_memory import SimpleMemory

console = Console()

class AICloneCLI:
    """Main CLI application for AI clones"""
    
    def __init__(self):
        self.active_clones = {}
        self.personalities_dir = "data/personalities"
        self.conversations_dir = "data/conversations"
        
        # Ensure directories exist
        os.makedirs(self.personalities_dir, exist_ok=True)
        os.makedirs(self.conversations_dir, exist_ok=True)
    
    def show_welcome(self):
        """Show welcome screen"""
        welcome_text = Text()
        welcome_text.append("🧠 fol-ai-match CLI\n", style="bold blue")
        welcome_text.append("Week 1 MVP - AI Clone Creator & Chat System\n\n", style="blue")
        welcome_text.append("Create AI clones with unique personalities and watch them chat!")
        
        console.print(Panel(welcome_text, border_style="blue", expand=False))
    
    def show_main_menu(self):
        """Show main menu options"""
        table = Table(title="🎯 Main Menu", show_header=False, box=None)
        table.add_column("Option", style="cyan")
        table.add_column("Description", style="white")
        
        table.add_row("1", "Create New AI Clone")
        table.add_row("2", "Load Existing Clone")
        table.add_row("3", "List All Clones")
        table.add_row("4", "Chat with Clone")
        table.add_row("5", "Clone-to-Clone Conversation")
        table.add_row("6", "Run Demo Conversation")
        table.add_row("7", "System Test")
        table.add_row("0", "Exit")
        
        console.print(table)
    
    def create_new_clone(self):
        """Create a new AI clone via questionnaire"""
        console.print("\n[bold green]🆕 Creating New AI Clone[/bold green]")
        
        clone_name = Prompt.ask("What should we call this clone?")
        
        try:
            personality_data, filename = create_personality_interactive(clone_name)
            
            if filename:
                console.print(f"[green]✅ Clone personality saved: {filename}[/green]")
                
                # Load the clone
                clone = AIClone(personality_data)
                self.active_clones[clone_name] = clone
                
                console.print(f"[green]🤖 {clone_name} is now active and ready to chat![/green]")
                return clone
            else:
                console.print("[yellow]⚠️ Personality not saved[/yellow]")
                return None
                
        except Exception as e:
            console.print(f"[red]❌ Error creating clone: {e}[/red]")
            return None
    
    def load_existing_clone(self):
        """Load an existing clone from file"""
        console.print("\n[bold green]📂 Loading Existing Clone[/bold green]")
        
        # List available personality files
        personality_files = self.list_personality_files()
        
        if not personality_files:
            console.print("[yellow]No saved personalities found. Create one first![/yellow]")
            return None
        
        console.print("Available personalities:")
        for i, file in enumerate(personality_files, 1):
            console.print(f"  {i}. {file}")
        
        try:
            choice = int(Prompt.ask("Choose a personality")) - 1
            if 0 <= choice < len(personality_files):
                filename = os.path.join(self.personalities_dir, personality_files[choice])
                clone = load_clone_from_file(filename)
                self.active_clones[clone.name] = clone
                
                console.print(f"[green]✅ Loaded {clone.name}: {clone.get_personality_summary()}[/green]")
                return clone
            else:
                console.print("[red]Invalid choice[/red]")
                return None
                
        except (ValueError, Exception) as e:
            console.print(f"[red]Error loading clone: {e}[/red]")
            return None
    
    def list_all_clones(self):
        """List all active and available clones"""
        console.print("\n[bold green]📋 Clone Status[/bold green]")
        
        # Active clones
        if self.active_clones:
            table = Table(title="🟢 Active Clones", show_header=True)
            table.add_column("Name", style="cyan")
            table.add_column("Summary", style="white")
            
            for name, clone in self.active_clones.items():
                table.add_row(name, clone.get_personality_summary())
            
            console.print(table)
        else:
            console.print("[yellow]No active clones[/yellow]")
        
        # Available personalities
        personality_files = self.list_personality_files()
        if personality_files:
            console.print(f"\n[blue]💾 Available personalities: {len(personality_files)} files[/blue]")
            for file in personality_files[:5]:  # Show first 5
                console.print(f"  • {file}")
            if len(personality_files) > 5:
                console.print(f"  ... and {len(personality_files) - 5} more")
    
    def chat_with_clone(self):
        """Chat with a single clone"""
        if not self.active_clones:
            console.print("[yellow]No active clones. Load or create one first![/yellow]")
            return
        
        # Select clone
        clone_names = list(self.active_clones.keys())
        console.print("Available clones:")
        for i, name in enumerate(clone_names, 1):
            console.print(f"  {i}. {name}")
        
        try:
            choice = int(Prompt.ask("Choose a clone to chat with")) - 1
            clone = self.active_clones[clone_names[choice]]
        except (ValueError, IndexError):
            console.print("[red]Invalid choice[/red]")
            return
        
        console.print(f"\n[bold blue]💬 Chatting with {clone.name}[/bold blue]")
        console.print("[dim]Type 'quit' to end the conversation[/dim]")
        
        while True:
            user_input = Prompt.ask(f"\n[green]You[/green]")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                console.print("[blue]👋 Goodbye![/blue]")
                break
            
            # Get AI response
            response = clone.respond(user_input, clone.get_recent_history(5))
            console.print(f"[cyan]{clone.name}[/cyan]: {response}")
            
            # Add to history
            clone.add_to_conversation_history("You", user_input)
            clone.add_to_conversation_history(clone.name, response)
    
    def clone_to_clone_conversation(self):
        """Start a conversation between two clones"""
        if len(self.active_clones) < 2:
            console.print("[yellow]Need at least 2 active clones for conversation![/yellow]")
            return
        
        # Select two clones
        clone_names = list(self.active_clones.keys())
        console.print("Available clones:")
        for i, name in enumerate(clone_names, 1):
            console.print(f"  {i}. {name}")
        
        try:
            choice1 = int(Prompt.ask("Choose first clone")) - 1
            choice2 = int(Prompt.ask("Choose second clone")) - 1
            
            if choice1 == choice2:
                console.print("[red]Please choose two different clones[/red]")
                return
            
            clone1 = self.active_clones[clone_names[choice1]]
            clone2 = self.active_clones[clone_names[choice2]]
            
        except (ValueError, IndexError):
            console.print("[red]Invalid choice[/red]")
            return
        
        # Start conversation
        conversation = CloneConversation(clone1, clone2)
        
        # Optional custom scenario
        custom_scenario = None
        if Confirm.ask("Want to set a custom scenario?", default=False):
            custom_scenario = Prompt.ask("Enter scenario")
        
        # Run conversation
        max_turns = int(Prompt.ask("How many turns?", default="8"))
        conversation.run_conversation(scenario=custom_scenario, max_turns=max_turns)
    
    def run_demo_conversation(self):
        """Run a demo conversation"""
        console.print("\n[bold blue]🎭 Running Demo Conversation[/bold blue]")
        run_demo_conversation()
    
    def run_system_test(self):
        """Run system test"""
        console.print("\n[bold blue]🧪 Running System Test[/bold blue]")
        try:
            # Import and run test
            import subprocess
            result = subprocess.run([sys.executable, "test_setup.py"], capture_output=True, text=True)
            console.print(result.stdout)
            if result.stderr:
                console.print(f"[red]{result.stderr}[/red]")
        except Exception as e:
            console.print(f"[red]Error running test: {e}[/red]")
    
    def list_personality_files(self) -> List[str]:
        """List available personality files"""
        if not os.path.exists(self.personalities_dir):
            return []
        
        files = [f for f in os.listdir(self.personalities_dir) if f.endswith('.json')]
        return sorted(files)
    
    def run(self):
        """Main CLI loop"""
        self.show_welcome()
        
        while True:
            console.print("\n" + "="*50)
            self.show_main_menu()
            
            choice = Prompt.ask("\n[bold]Choose an option[/bold]", default="0")
            
            if choice == "1":
                self.create_new_clone()
            elif choice == "2":
                self.load_existing_clone()
            elif choice == "3":
                self.list_all_clones()
            elif choice == "4":
                self.chat_with_clone()
            elif choice == "5":
                self.clone_to_clone_conversation()
            elif choice == "6":
                self.run_demo_conversation()
            elif choice == "7":
                self.run_system_test()
            elif choice == "0":
                console.print("[blue]👋 Thanks for using fol-ai-match![/blue]")
                break
            else:
                console.print("[red]Invalid option. Please try again.[/red]")

def main():
    """Main entry point"""
    try:
        cli = AICloneCLI()
        cli.run()
    except KeyboardInterrupt:
        console.print("\n[blue]👋 Goodbye![/blue]")
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")

if __name__ == "__main__":
    main() 