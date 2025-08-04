"""
Personality Questionnaire System
Collects user personality data to create AI clone personalities
"""

import json
from typing import Dict, Any
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text
from datetime import datetime

# Import the new question manager
try:
    from .question_manager import QuestionManager
except ImportError:
    from question_manager import QuestionManager

console = Console()

class PersonalityQuestionnaire:
    def __init__(self):
        self.question_manager = QuestionManager()
        self.questions = self.question_manager.get_categories()
    
    def run_questionnaire(self, clone_name: str = None) -> Dict[str, Any]:
        """Run the complete personality questionnaire"""
        console.print(Panel.fit(
            "[bold blue]🧠 AI Clone Personality Questionnaire[/bold blue]\n"
            f"Creating personality for: {clone_name or 'New Clone'}\n"
            f"Question Version: {self.question_manager.get_current_version()}\n"
            "This will take about 5-10 minutes.",
            border_style="blue"
        ))
        
        personality_data = {
            "clone_name": clone_name,
            "question_version": self.question_manager.get_current_version(),
            "created_at": datetime.now().isoformat(),
        }
        
        # Initialize all categories from dynamic questions
        for category in self.questions.keys():
            personality_data[category] = {}
        
        # Process all categories dynamically
        for category, category_questions in self.questions.items():
            # Category display names
            category_names = {
                "basic_info": "📋 Basic Information",
                "communication_style": "💬 Communication Style", 
                "personality_traits": "🧠 Personality Traits",
                "interests": "🎯 Interests & Values"
            }
            
            display_name = category_names.get(category, f"📝 {category.replace('_', ' ').title()}")
            console.print(f"\n[bold green]{display_name}[/bold green]")
            
            for key, question_data in category_questions.items():
                # Handle special case for name field
                if key == "name" and clone_name:
                    personality_data[category][key] = clone_name
                    continue
                
                # Handle different question types
                if isinstance(question_data, dict):
                    question_text = question_data.get("question", "")
                    question_type = question_data.get("type", "text")
                    
                    if question_type == "multiple_choice" and "options" in question_data:
                        choice = self._ask_multiple_choice(question_text, question_data["options"])
                        personality_data[category][key] = {
                            "choice": choice,
                            "index": question_data["options"].index(choice)
                        }
                    else:
                        # Text question
                        personality_data[category][key] = Prompt.ask(f"[cyan]{question_text}[/cyan]")
                else:
                    # Legacy format (string question)
                    personality_data[category][key] = Prompt.ask(f"[cyan]{question_data}[/cyan]")
        
        return personality_data
    
    def update_clone_with_new_questions(self, personality_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing clone with new questions from newer versions"""
        missing_questions = self.question_manager.get_missing_questions(personality_data)
        
        if not missing_questions:
            console.print("[green]✅ Clone is up to date with latest questions![/green]")
            return personality_data
        
        console.print(Panel.fit(
            f"[bold yellow]📝 Updating Clone: {personality_data.get('clone_name', 'Unknown')}[/bold yellow]\n"
            f"From version {personality_data.get('question_version', '0.0')} to {self.question_manager.get_current_version()}\n"
            f"New questions to answer: {sum(len(qs) for qs in missing_questions.values())}",
            border_style="yellow"
        ))
        
        updated_data = personality_data.copy()
        
        # Ask new questions by category
        for category, category_questions in missing_questions.items():
            if category not in updated_data:
                updated_data[category] = {}
            
            category_names = {
                "basic_info": "📋 Basic Information",
                "communication_style": "💬 Communication Style", 
                "personality_traits": "🧠 Personality Traits",
                "interests": "🎯 Interests & Values"
            }
            
            display_name = category_names.get(category, f"📝 {category.replace('_', ' ').title()}")
            console.print(f"\n[bold blue]New questions in {display_name}[/bold blue]")
            
            for key, question_data in category_questions.items():
                question_text = question_data.get("question", "")
                question_type = question_data.get("type", "text")
                
                if question_type == "multiple_choice" and "options" in question_data:
                    choice = self._ask_multiple_choice(question_text, question_data["options"])
                    updated_data[category][key] = {
                        "choice": choice,
                        "index": question_data["options"].index(choice)
                    }
                else:
                    # Text question
                    updated_data[category][key] = Prompt.ask(f"[cyan]{question_text}[/cyan]")
        
        # Update version and timestamp
        updated_data["question_version"] = self.question_manager.get_current_version()
        updated_data["updated_at"] = datetime.now().isoformat()
        
        console.print(f"[green]✅ Clone updated to version {updated_data['question_version']}![/green]")
        return updated_data
    
    def _ask_multiple_choice(self, question: str, options: list) -> str:
        """Ask a multiple choice question"""
        console.print(f"\n[cyan]{question}[/cyan]")
        for i, option in enumerate(options, 1):
            console.print(f"  {i}. {option}")
        
        while True:
            try:
                choice_num = int(Prompt.ask("Choose a number")) - 1
                if 0 <= choice_num < len(options):
                    return options[choice_num]
                else:
                    console.print("[red]Invalid choice. Please try again.[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")
    
    def save_personality(self, personality_data: Dict[str, Any], filename: str = None) -> str:
        """Save personality data to JSON file"""
        if not filename:
            name = personality_data["basic_info"].get("name", "unknown")
            filename = f"data/personalities/{name.lower().replace(' ', '_')}_personality.json"
        
        with open(filename, 'w') as f:
            json.dump(personality_data, f, indent=2)
        
        console.print(f"[green]✅ Personality saved to {filename}[/green]")
        return filename
    
    def load_personality(self, filename: str) -> Dict[str, Any]:
        """Load personality data from JSON file"""
        with open(filename, 'r') as f:
            return json.load(f)

def create_personality_interactive(clone_name: str = None) -> Dict[str, Any]:
    """Main function to create a personality interactively"""
    questionnaire = PersonalityQuestionnaire()
    personality_data = questionnaire.run_questionnaire(clone_name)
    
    # Preview the personality
    console.print(Panel.fit(
        f"[bold green]✅ Personality Created for {personality_data['basic_info']['name']}[/bold green]\n"
        f"Age: {personality_data['basic_info']['age']}\n"
        f"Style: {personality_data['communication_style']['formality']['choice']}, "
        f"{personality_data['communication_style']['humor']['choice']}\n"
        f"Interests: {personality_data['interests']['hobbies'][:50]}...",
        title="Personality Summary"
    ))
    
    if Confirm.ask("Save this personality?"):
        filename = questionnaire.save_personality(personality_data)
        return personality_data, filename
    
    return personality_data, None

if __name__ == "__main__":
    # Test the questionnaire
    create_personality_interactive("Test Clone") 