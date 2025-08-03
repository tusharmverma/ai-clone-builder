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

console = Console()

class PersonalityQuestionnaire:
    def __init__(self):
        self.questions = {
            "basic_info": {
                "name": "What's your name?",
                "age": "What's your age?",
                "location": "Where are you from? (city/country)",
                "occupation": "What do you do for work/study?"
            },
            "communication_style": {
                "formality": {
                    "question": "Do you prefer casual or formal conversation?",
                    "options": ["Very casual (hey, sup, lol)", "Casual (hi, cool, nice)", "Neutral", "Somewhat formal", "Very formal"]
                },
                "humor": {
                    "question": "How would you describe your sense of humor?",
                    "options": ["Sarcastic/witty", "Playful/silly", "Dry/deadpan", "Dad jokes", "Not much humor", "Dark humor"]
                },
                "expressiveness": {
                    "question": "Are you more reserved or expressive?",
                    "options": ["Very reserved", "Somewhat reserved", "Balanced", "Quite expressive", "Very expressive"]
                },
                "response_length": {
                    "question": "Do you prefer short or detailed responses?",
                    "options": ["Very short (1-2 words)", "Short (1 sentence)", "Medium", "Detailed", "Very detailed"]
                }
            },
            "personality_traits": {
                "extroversion": {
                    "question": "Do you gain energy from socializing or alone time?",
                    "options": ["Strongly introverted", "Somewhat introverted", "Balanced", "Somewhat extroverted", "Strongly extroverted"]
                },
                "openness": {
                    "question": "How open are you to new experiences?",
                    "options": ["Very cautious", "Somewhat cautious", "Balanced", "Quite adventurous", "Very adventurous"]
                },
                "emotional_style": {
                    "question": "How do you typically express emotions?",
                    "options": ["Very reserved", "Subtle hints", "Direct but calm", "Openly emotional", "Very expressive"]
                },
                "decision_making": {
                    "question": "Are you more logical or intuitive in decisions?",
                    "options": ["Very logical", "Mostly logical", "Balanced", "Mostly intuitive", "Very intuitive"]
                }
            },
            "interests": {
                "hobbies": "What are your main hobbies/interests? (separate with commas)",
                "topics": "What topics do you love talking about? (separate with commas)",
                "values": "What's most important to you in relationships?",
                "conversation_starters": "What kind of things do you usually talk about when meeting someone new?"
            }
        }
    
    def run_questionnaire(self, clone_name: str = None) -> Dict[str, Any]:
        """Run the complete personality questionnaire"""
        console.print(Panel.fit(
            "[bold blue]🧠 AI Clone Personality Questionnaire[/bold blue]\n"
            f"Creating personality for: {clone_name or 'New Clone'}\n"
            "This will take about 5-10 minutes.",
            border_style="blue"
        ))
        
        personality_data = {
            "clone_name": clone_name,
            "basic_info": {},
            "communication_style": {},
            "personality_traits": {},
            "interests": {}
        }
        
        # Basic Info
        console.print("\n[bold green]📋 Basic Information[/bold green]")
        for key, question in self.questions["basic_info"].items():
            if key == "name" and clone_name:
                personality_data["basic_info"][key] = clone_name
                continue
            personality_data["basic_info"][key] = Prompt.ask(f"[cyan]{question}[/cyan]")
        
        # Communication Style
        console.print("\n[bold green]💬 Communication Style[/bold green]")
        for key, question_data in self.questions["communication_style"].items():
            if isinstance(question_data, dict):
                choice = self._ask_multiple_choice(question_data["question"], question_data["options"])
                personality_data["communication_style"][key] = {
                    "choice": choice,
                    "index": question_data["options"].index(choice)
                }
            else:
                personality_data["communication_style"][key] = Prompt.ask(f"[cyan]{question_data}[/cyan]")
        
        # Personality Traits
        console.print("\n[bold green]🧠 Personality Traits[/bold green]")
        for key, question_data in self.questions["personality_traits"].items():
            choice = self._ask_multiple_choice(question_data["question"], question_data["options"])
            personality_data["personality_traits"][key] = {
                "choice": choice,
                "index": question_data["options"].index(choice)
            }
        
        # Interests
        console.print("\n[bold green]🎯 Interests & Values[/bold green]")
        for key, question in self.questions["interests"].items():
            personality_data["interests"][key] = Prompt.ask(f"[cyan]{question}[/cyan]")
        
        return personality_data
    
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