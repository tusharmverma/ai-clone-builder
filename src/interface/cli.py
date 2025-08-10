"""
Command Line Interface
Main CLI for interacting with AI clones
"""

import sys
import os
import json
from typing import List, Dict
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.personality.questionnaire import QuestionnaireManager
from src.personality.question_manager import QuestionManager
from src.ai_clone.clone import AIClone, load_clone_from_file
from src.ai_clone.conversation import CloneConversation, run_demo_conversation

console = Console()

class AICloneCLI:
    """Main CLI application for AI clones"""
    
    # Main CLI interface for AI clone management
    
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
        welcome_text.append("AI Clone Builder CLI\n", style="bold blue")
        welcome_text.append("AI Clone Creator & Chat System\n\n", style="blue")
        welcome_text.append("Create AI clones with unique personalities and watch them chat!")
        
        console.print(Panel(welcome_text, border_style="blue", expand=False))
    
    def show_main_menu(self):
        """Show main menu options"""
        table = Table(title="Main Menu", show_header=False, box=None)
        table.add_column("Option", style="cyan")
        table.add_column("Description", style="white")
        
        table.add_row("1", "Create New AI Clone")
        table.add_row("2", "Load Existing Clone")
        table.add_row("3", "List All Clones")
        table.add_row("4", "Chat with Clone")
        table.add_row("5", "Clone-to-Clone Conversation")
        table.add_row("6", "Run Demo Conversation") 
        table.add_row("7", "Question Management")
        table.add_row("8", "System Test")
        table.add_row("q", "Exit")
        
        console.print(table)
    
    def create_new_clone(self):
        """Create a new AI clone via questionnaire"""
        console.print("\n[bold green]Creating New AI Clone[/bold green]")
        
        clone_name = Prompt.ask("What should we call this clone?")
        
        try:
            questionnaire_manager = QuestionnaireManager()
            personality_data = questionnaire_manager.create_personality(clone_name)
            
            # Save personality
            filename = f"data/personalities/{clone_name.lower().replace(' ', '_')}_personality.json"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w') as f:
                json.dump(personality_data, f, indent=2)
            
            console.print(f"[green]Clone personality saved: {filename}[/green]")
            
            # Load the clone
            clone = AIClone(personality_data)
            self.active_clones[clone_name] = clone
            
            console.print(f"[green]{clone_name} is now active and ready to chat![/green]")
            return clone
                
        except Exception as e:
            console.print(f"[red]Error creating clone: {e}[/red]")
            return None
    
    def load_existing_clone(self):
        """Load an existing clone from file"""
        console.print("\n[bold green]Loading Existing Clone[/bold green]")
        
        personality_files = self.list_personality_files()
        
        if not personality_files:
            console.print("[yellow]No saved personalities found.[/yellow]")
            return None
        
        console.print("\nAvailable personalities:")
        for i, filename in enumerate(personality_files, 1):
            clone_name = os.path.basename(filename).replace('_personality.json', '')
            console.print(f"{i}. {clone_name}")
        
        try:
            choice = int(Prompt.ask("\nSelect a clone (number)")) - 1
            if 0 <= choice < len(personality_files):
                selected_file = personality_files[choice]
                clone = load_clone_from_file(selected_file)
                
                if clone:
                    self.active_clones[clone.name] = clone
                    console.print(f"[green]Loaded {clone.name}![/green]")
                    return clone
                else:
                    console.print("[red]Failed to load clone[/red]")
                    return None
            else:
                console.print("[red]Invalid selection[/red]")
                return None
        except ValueError:
            console.print("[red]Please enter a valid number[/red]")
            return None
    
    def list_all_clones(self):
        """List all available clones"""
        console.print("\n[bold green]Available Clones[/bold green]")
        
        personality_files = self.list_personality_files()
        
        if not personality_files:
            console.print("[yellow]No saved personalities found.[/yellow]")
            return
        
        table = Table(title="Saved Clones")
        table.add_column("Name", style="cyan")
        table.add_column("File", style="white")
        
        for filename in personality_files:
            clone_name = os.path.basename(filename).replace('_personality.json', '')
            table.add_row(clone_name, filename)
        
        console.print(table)
    
    def chat_with_clone(self):
        """Chat with a selected clone"""
        console.print("\n[bold green]Chat with Clone[/bold green]")
        
        if not self.active_clones:
            console.print("[yellow]No clones loaded. Create or load a clone first.[/yellow]")
            return
        
        console.print("\nActive clones:")
        for i, (name, clone) in enumerate(self.active_clones.items(), 1):
            console.print(f"{i}. {name}")
        
        try:
            choice = int(Prompt.ask("\nSelect a clone to chat with (number)")) - 1
            clone_names = list(self.active_clones.keys())
            
            if 0 <= choice < len(clone_names):
                clone_name = clone_names[choice]
                clone = self.active_clones[clone_name]
                
                console.print(f"\n[bold]Chatting with {clone.name}[/bold]")
                console.print("Type 'quit' to end the conversation\n")
                
                while True:
                    user_input = Prompt.ask("You")
                    if user_input.lower() in ['quit', 'bye', 'exit']:
                        break
                    
                    response = clone.respond(user_input)
                    console.print(f"{clone.name}: {response}")
            else:
                console.print("[red]Invalid selection[/red]")
        except ValueError:
            console.print("[red]Please enter a valid number[/red]")
    
    def clone_to_clone_conversation(self):
        """Start a conversation between two clones"""
        console.print("\n[bold green]Clone-to-Clone Conversation[/bold green]")
        
        if len(self.active_clones) < 2:
            console.print("[yellow]Need at least 2 clones loaded. Create or load more clones first.[/yellow]")
            return
        
        clone_names = list(self.active_clones.keys())
        
        console.print("\nSelect two clones to chat:")
        for i, name in enumerate(clone_names, 1):
            console.print(f"{i}. {name}")
        
        try:
            choice1 = int(Prompt.ask("\nSelect first clone (number)")) - 1
            choice2 = int(Prompt.ask("Select second clone (number)")) - 1
            
            if (0 <= choice1 < len(clone_names) and 
                0 <= choice2 < len(clone_names) and 
                choice1 != choice2):
                
                clone1_name = clone_names[choice1]
                clone2_name = clone_names[choice2]
                
                clone1 = self.active_clones[clone1_name]
                clone2 = self.active_clones[clone2_name]
                
                console.print(f"\n[bold]Starting conversation between {clone1.name} and {clone2.name}[/bold]")
                
                conversation = CloneConversation(clone1, clone2)
                conversation.start_conversation()
                
            else:
                console.print("[red]Invalid selection or same clone selected[/red]")
        except ValueError:
            console.print("[red]Please enter valid numbers[/red]")
    
    def run_demo_conversation(self):
        """Run the demo conversation"""
        console.print("\n[bold green]Running Demo Conversation[/bold green]")
        run_demo_conversation()
    
    def run_system_test(self):
        """Run system diagnostics"""
        console.print("\n[bold green]Running System Test[/bold green]")
        
        try:
            import subprocess
            result = subprocess.run([sys.executable, "test_setup.py"], 
                                  capture_output=True, text=True)
            console.print(result.stdout)
            if result.stderr:
                console.print(f"[red]Errors: {result.stderr}[/red]")
        except Exception as e:
            console.print(f"[red]Test failed: {e}[/red]")
    
    def question_management_menu(self):
        """Show question management options"""
        console.print("\n[bold green]Question Management[/bold green]")
        
        try:
            question_manager = QuestionManager()
            
            console.print("1. View all questions")
            console.print("2. Add new question")
            console.print("3. Edit existing question")
            console.print("4. Delete question")
            console.print("5. Back to main menu")
            
            choice = Prompt.ask("\nSelect option", choices=["1", "2", "3", "4", "5"])
            
            if choice == "1":
                self._show_question_history(question_manager)
            elif choice == "2":
                question_manager.add_question_interactive()
            elif choice == "3":
                question_manager.edit_question_interactive()
            elif choice == "4":
                question_manager.delete_question_interactive()
            elif choice == "5":
                return
            
        except Exception as e:
            console.print(f"[red]Question management error: {e}[/red]")
    
    def _show_question_history(self, question_manager: QuestionManager):
        """Show question history"""
        questions = question_manager.get_all_questions()
        
        if not questions:
            console.print("[yellow]No questions found.[/yellow]")
            return
        
        table = Table(title="Question History")
        table.add_column("ID", style="cyan")
        table.add_column("Question", style="white")
        table.add_column("Category", style="green")
        table.add_column("Stage", style="yellow")
        
        for q in questions:
            table.add_row(str(q["id"]), q["question"], q["category"], str(q["stage"]))
        
        console.print(table)
    
    def list_personality_files(self) -> List[str]:
        """List all personality files"""
        if not os.path.exists(self.personalities_dir):
            return []
        
        files = [f for f in os.listdir(self.personalities_dir) 
                if f.endswith('_personality.json')]
        return [os.path.join(self.personalities_dir, f) for f in files]
    
    def run(self):
        """Main application loop"""
        while True:
            try:
                self.show_welcome()
                self.show_main_menu()
                
                choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4", "5", "6", "7", "8", "q"])
                
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
                    self.question_management_menu()
                elif choice == "8":
                    self.run_system_test()
                elif choice == "q":
                    console.print("\n[green]Goodbye![/green]")
                    break
                
                if choice != "q":
                    input("\nPress Enter to continue...")
                    console.clear()
                    
            except KeyboardInterrupt:
                console.print("\n\n[green]Goodbye![/green]")
                break
            except Exception as e:
                console.print(f"\n[red]Unexpected error: {e}[/red]")
                input("Press Enter to continue...")

def main():
    """Main entry point"""
    cli = AICloneCLI()
    cli.run()

if __name__ == "__main__":
    main() 