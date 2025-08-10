#!/usr/bin/env python3
"""
Enhanced Questionnaire System - Version 3.0
Supports phased approach based on Social Penetration Theory
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()

class QuestionnaireManager:
    """Manages questionnaire loading and personality creation with phased approach"""
    
    def __init__(self):
        self.questions_file = "data/questions.json"
        self.questions_data = self._load_questions()
    
    def _load_questions(self) -> Dict[str, Any]:
        """Load questions from JSON file"""
        try:
            with open(self.questions_file, 'r') as f:
                self.questions = json.load(f)
                return self.questions
        except FileNotFoundError:
            console.print(f"[red]Questions file not found: {self.questions_file}[/red]")
            return {}
        except json.JSONDecodeError as e:
            console.print(f"[red]Error parsing questions file: {e}[/red]")
            return {}
    
    def create_personality(self, name: str) -> Dict[str, Any]:
        """Create a personality through interactive questionnaire"""
        if not self.questions:
            raise Exception("Questions not loaded or questions file is empty")
        
        # Initialize personality data
        personality_data = {
            "basic_info": {"name": name},
            "communication_style": {},
            "personality_traits": {},
            "interests": {},
            "background": {},
            "goals": {}
        }
        
        # Show welcome
        welcome_text = (
            f"[bold blue]Creating AI Clone: {name}[/bold blue]\n"
            "I'll ask you a series of questions to create a unique personality.\n"
            "Answer naturally - there are no wrong answers!\n\n"
            "[yellow]Tip: Type 'quit' at any time to exit the questionnaire[/yellow]"
        )
        console.print(Panel(welcome_text, border_style="blue", expand=False))
        
        # Process categories (which contain the actual questions)
        categories = self.questions.get("categories", {})
        if not categories:
            raise Exception("No question categories found in questions file")
        
        # Process each category
        for category_key, category_data in categories.items():
            if not self._process_category(category_key, category_data, personality_data):
                break
        
        return personality_data
    
    def _process_category(self, category_key: str, category_data: Dict, personality_data: Dict) -> bool:
        """Process a single question category"""
        category_name = category_data.get("name", category_key.replace("_", " ").title())
        category_desc = category_data.get("description", "")
        
        console.print(f"\n[bold cyan]Category: {category_name}[/bold cyan]")
        if category_desc:
            console.print(f"[dim]{category_desc}[/dim]")
        
        # Show available questions for this category
        questions = category_data.get("questions", [])
        if not questions:
            console.print(f"[yellow]No questions found for category {category_key}[/yellow]")
            return True
        
        console.print(f"\n[bold yellow]Questions in this category:[/bold yellow]")
        for q_data in questions:
            question_id = q_data.get("id", "unknown")
            question_text = q_data.get("text", question_id)
            required = " (required)" if q_data.get("required", False) else ""
            console.print(f"  {question_id}{required}: {question_text}")
        
        # Process each question
        for q_data in questions:
            if not self._process_question_item(category_key, q_data, personality_data):
                return False
        
        console.print(f"\n[bold green]Category {category_name} completed![/bold green]")
        return True
    
    def _process_question(self, stage: str, q_key: str, q_data: Dict, personality_data: Dict) -> bool:
        """Process a single question within a stage"""
        question_text = q_data.get("text", q_key)
        question_type = q_data.get("type", "single_choice")
        
        console.print(f"\n[bold cyan]Question: {question_text}[/bold cyan]")
        
        if q_data.get("required", False):
            console.print("[red]This question is required.[/red]")
        
        if question_type == "single_choice":
            response = self._ask_single_choice(q_data)
        elif question_type == "multiple_choice":
            response = self._ask_multiple_choice(q_data)
        elif question_type == "scale":
            response = self._ask_scale(q_data)
        elif question_type == "combined_choice":
            response = self._ask_combined_choice(q_data)
        elif question_type == "text_input":
            response = self._ask_text_input(q_data)
        elif question_type == "number_input":
            response = self._ask_number_input(q_data)
        else:
            console.print(f"[red]Unknown question type: {question_type}[/red]")
            return False
        
        # Store response in personality_data
        personality_data[stage][q_key] = response
        return True
    
    def _process_question_item(self, category_key: str, question_data: Dict, personality_data: Dict) -> bool:
        """Process a single question item from the new structure"""
        question_id = question_data.get("id", "unknown")
        question_text = question_data.get("text", question_id)
        question_type = question_data.get("type", "single_choice")
        
        console.print(f"\n[bold cyan]Question: {question_text}[/bold cyan]")
        
        if question_data.get("required", False):
            console.print("[red]This question is required.[/red]")
        
        try:
            if question_type == "single_choice":
                response = self._ask_single_choice(question_data)
            elif question_type == "multiple_choice":
                response = self._ask_multiple_choice(question_data)
            elif question_type == "scale":
                response = self._ask_scale(question_data)
            elif question_type == "combined_choice":
                response = self._ask_combined_choice(question_data)
            elif question_type == "text_input":
                response = self._ask_text_input(question_data)
            elif question_type == "number_input":
                response = self._ask_number_input(question_data)
            else:
                console.print(f"[red]Unknown question type: {question_type}[/red]")
                return False
            
            # Store response in personality_data based on category
            if category_key.startswith("stage_0_basic_info"):
                personality_data["basic_info"][question_id] = response
            elif category_key.startswith("stage_0_communication_style"):
                personality_data["communication_style"][question_id] = response
            elif category_key.startswith("stage_0_personality_traits"):
                personality_data["personality_traits"][question_id] = response
            else:
                # For other stages, use the category name as the key
                stage_name = category_key.split("_", 2)[-1] if "_" in category_key else category_key
                if stage_name not in personality_data:
                    personality_data[stage_name] = {}
                personality_data[stage_name][question_id] = response
            
            return True
            
        except Exception as e:
            console.print(f"[red]Error processing question: {e}[/red]")
            return False
    
    def _ask_single_choice(self, question: Dict[str, Any]) -> str:
        """Ask a single choice question"""
        options = question["options"]
        
        # Display options
        for i, option in enumerate(options, 1):
            console.print(f"  {i}. {option}")
        
        # Get user choice
        while True:
            try:
                choice = Prompt.ask(
                    "Select your answer",
                    choices=[str(i) for i in range(1, len(options) + 1)]
                )
                selected_option = options[int(choice) - 1]
                
                # Handle "Other (brief description)" option
                if "Other (brief description)" in selected_option:
                    brief_description = Prompt.ask(
                        "[yellow]Please provide a brief description (1-3 words max):[/yellow]",
                        default=""
                    )
                    if brief_description.strip():
                        return f"Other: {brief_description.strip()}"
                    else:
                        console.print("[yellow]Please provide a description for 'Other' option[/yellow]")
                        continue
                
                return selected_option
            except (ValueError, IndexError):
                console.print("[red]Please enter a valid number[/red]")
    
    def _ask_multiple_choice(self, question: Dict[str, Any]) -> List[str]:
        """Ask a multiple choice question"""
        options = question["options"]
        max_selections = question.get("max_selections", len(options))
        
        console.print(f"[yellow]Select up to {max_selections} options:[/yellow]")
        
        # Display options
        for i, option in enumerate(options, 1):
            console.print(f"  {i}. {option}")
        
        # Get user choices
        selected = []
        while len(selected) < max_selections:
            choice = Prompt.ask(
                f"Select option (or 'done' if finished, {len(selected)}/{max_selections} selected)"
            )
            
            if choice.lower() == "done":
                break
            
            try:
                option_index = int(choice) - 1
                if 0 <= option_index < len(options):
                    selected_option = options[option_index]
                    if selected_option not in selected:
                        # Handle "Other (brief description)" option
                        if "Other (brief description)" in selected_option:
                            brief_description = Prompt.ask(
                                "[yellow]Please provide a brief description (1-3 words max):[/yellow]",
                                default=""
                            )
                            if brief_description.strip():
                                selected.append(f"Other: {brief_description.strip()}")
                                console.print(f"[green]✓ Added: Other: {brief_description.strip()}[/green]")
                            else:
                                console.print("[yellow]Skipping 'Other' option - no description provided[/yellow]")
                        else:
                            selected.append(selected_option)
                            console.print(f"[green]✓ Added: {selected_option}[/green]")
                    else:
                        console.print("[yellow]Already selected[/yellow]")
                else:
                    console.print("[red]Invalid option number[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number[/red]")
        
        return selected
    
    def _ask_scale(self, question: Dict[str, Any]) -> int:
        """Ask a scale question"""
        min_val = question.get("min", 1)
        max_val = question.get("max", 5)
        labels = question.get("labels", {})
        
        console.print(f"[yellow]Rate from {min_val} to {max_val}:[/yellow]")
        
        # Display scale with labels
        for i in range(min_val, max_val + 1):
            label = labels.get(str(i), str(i))
            console.print(f"  {i}. {label}")
        
        # Get user choice
        while True:
            try:
                choice = Prompt.ask(
                    "Select your rating",
                    choices=[str(i) for i in range(min_val, max_val + 1)]
                )
                return int(choice)
            except ValueError:
                console.print("[red]Please enter a valid number[/red]")
    
    def _ask_combined_choice(self, question: Dict[str, Any]) -> Dict[str, str]:
        """Ask a combined choice question (category + reason)"""
        category_options = question["category_options"]
        reason_options = question["reason_options"]
        
        console.print(f"[bold]{question['category_question']}[/bold]")
        for i, option in enumerate(category_options, 1):
            console.print(f"  {i}. {option}")
        
        category_choice = Prompt.ask(
            "Select category",
            choices=[str(i) for i in range(1, len(category_options) + 1)]
        )
        selected_category = category_options[int(category_choice) - 1]
        
        console.print(f"\n[bold]{question['reason_question']}[/bold]")
        for i, option in enumerate(reason_options, 1):
            console.print(f"  {i}. {option}")
        
        reason_choice = Prompt.ask(
            "Select reason",
            choices=[str(i) for i in range(1, len(reason_options) + 1)]
        )
        selected_reason = reason_options[int(reason_choice) - 1]
        
        return {
            "category": selected_category,
            "reason": selected_reason
        }
    
    def _ask_text_input(self, question: Dict[str, Any]) -> str:
        """Ask a text input question"""
        placeholder = question.get("placeholder", "")
        max_length = question.get("max_length", 50)  # Default max 50 characters
        
        if placeholder:
            console.print(f"[dim]{placeholder}[/dim]")
        
        console.print(f"[yellow]Please keep your answer brief (max {max_length} characters)[/yellow]")
        console.print("[dim]Type 'quit' to exit the questionnaire[/dim]")
        
        while True:
            response = Prompt.ask("Your answer")
            if response.lower() == "quit":
                raise KeyboardInterrupt("User quit questionnaire")
            if response.strip():
                if len(response.strip()) <= max_length:
                    return response.strip()
                else:
                    console.print(f"[red]Answer too long! Please keep it under {max_length} characters[/red]")
                    console.print(f"[yellow]Current length: {len(response.strip())} characters[/yellow]")
            else:
                console.print("[red]Please provide an answer[/red]")
    
    def _ask_number_input(self, question: Dict[str, Any]) -> int:
        """Ask a number input question"""
        min_val = question.get("min", 0)
        max_val = question.get("max", 999)
        placeholder = question.get("placeholder", "")
        
        if placeholder:
            console.print(f"[dim]{placeholder}[/dim]")
        
        console.print(f"[yellow]Enter a number between {min_val} and {max_val}:[/yellow]")
        console.print("[dim]Type 'quit' to exit the questionnaire[/dim]")
        
        while True:
            try:
                response = Prompt.ask("Your answer")
                if response.lower() == "quit":
                    raise KeyboardInterrupt("User quit questionnaire")
                number = int(response)
                if min_val <= number <= max_val:
                    return number
                else:
                    console.print(f"[red]Please enter a number between {min_val} and {max_val}[/red]")
            except ValueError:
                if response.lower() == "quit":
                    raise KeyboardInterrupt("User quit questionnaire")
                console.print("[red]Please enter a valid number[/red]")
    
    def update_existing_clones(self, stage: str = "stage_1") -> None:
        """Update existing clones with new questions from a specific stage"""
        console.print(Panel.fit(
            f"[bold blue]Updating Existing Clones[/bold blue]\n"
            f"Adding new questions from {stage} to existing personalities",
            border_style="blue"
        ))
        
        personalities_dir = "data/personalities"
        if not os.path.exists(personalities_dir):
            console.print("[red]No personalities directory found[/red]")
            return
        
        updated_count = 0
        for filename in os.listdir(personalities_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(personalities_dir, filename)
                
                try:
                    with open(filepath, 'r') as f:
                        personality_data = json.load(f)
                    
                    # Check if this stage needs updating
                    if stage not in personality_data.get("stages", {}):
                        console.print(f"\n[bold]Updating {personality_data['basic_info']['name']}...[/bold]")
                        
                        # Complete the missing stage
                        categories = self.get_categories()
                        stage_data = self._complete_stage(stage, categories)
                        
                        # Update personality data
                        if "stages" not in personality_data:
                            personality_data["stages"] = {}
                        personality_data["stages"][stage] = stage_data
                        personality_data["basic_info"]["updated_at"] = datetime.now().isoformat()
                        
                        # Save updated personality
                        with open(filepath, 'w') as f:
                            json.dump(personality_data, f, indent=2)
                        
                        updated_count += 1
                        console.print(f"[green]Updated {personality_data['basic_info']['name']}[/green]")
                
                except Exception as e:
                    console.print(f"[red]Error updating {filename}: {e}[/red]")
        
        console.print(f"\n[bold green]Updated {updated_count} clones![/bold green]")

def main():
    """Main function for questionnaire interaction"""
    manager = QuestionnaireManager()
    
    console.print(Panel.fit(
        "[bold green]AI Clone Personality Creator[/bold green]\n"
        "Create AI clones with phased personality development",
        border_style="green"
    ))
    
    # Show available options
    console.print("\n[bold]Available Actions:[/bold]")
    console.print("1. Create new AI clone")
    console.print("2. Update existing clones with new questions")
    console.print("3. View questionnaire information")
    console.print("q. Quit")
    
    choice = Prompt.ask(
        "What would you like to do?",
        choices=["1", "2", "3", "q"],
        default="1"
    )
    
    if choice == "q":
        console.print("\n[bold blue]Goodbye! 👋[/bold blue]")
        return
    
    if choice == "1":
        name = Prompt.ask("Enter the name for your AI clone")
        try:
            personality_data = manager.create_personality(name)
            
            # Save personality
            filename = f"data/personalities/{name.lower().replace(' ', '_')}.json"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w') as f:
                json.dump(personality_data, f, indent=2)
            
            console.print(f"\n[bold green]AI Clone '{name}' created successfully![/bold green]")
            console.print(f"Saved to: {filename}")
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Questionnaire cancelled. No personality created.[/bold yellow]")
        except Exception as e:
            console.print(f"\n[bold red]Error creating personality: {e}[/bold red]")
    
    elif choice == "2":
        stages = manager.get_stages()
        if len(stages) > 1:
            stage_choice = Prompt.ask(
                "Which stage to add to existing clones?",
                choices=list(stages.keys()),
                default="stage_1"
            )
            manager.update_existing_clones(stage_choice)
        else:
            manager.update_existing_clones()
    
    elif choice == "3":
        console.print(f"\n[bold]Questionnaire Information:[/bold]")
        console.print(f"Version: {manager.get_version()}")
        console.print(f"Stages: {len(manager.get_stages())}")
        console.print(f"Categories: {len(manager.get_categories())}")

if __name__ == "__main__":
    main() 