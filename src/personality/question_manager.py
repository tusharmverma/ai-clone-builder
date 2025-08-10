"""
Dynamic Question Management System
Handles adding, removing, and versioning questions for AI clone creation
"""

import json
import os
from typing import Dict, Any, List, Tuple
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

console = Console()

class QuestionManager:
    """Manages dynamic questions with versioning and update capabilities"""
    
    def __init__(self, questions_file: str = "data/questions.json"):
        self.questions_file = questions_file
        self.questions_data = self.load_questions()
    
    def load_questions(self) -> Dict[str, Any]:
        """Load questions from JSON file"""
        try:
            with open(self.questions_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            console.print(f"[red]Questions file not found: {self.questions_file}[/red]")
            return self._create_default_questions()
    
    def save_questions(self):
        """Save questions to JSON file"""
        with open(self.questions_file, 'w') as f:
            json.dump(self.questions_data, f, indent=2)
    
    def get_current_version(self) -> str:
        """Get current question version"""
        return self.questions_data.get("version", "1.0")
    
    def get_categories(self) -> Dict[str, Any]:
        """Get all question categories"""
        return self.questions_data.get("categories", {})
    
    def add_question(self, category: str, key: str, question_data: Dict[str, Any]) -> bool:
        """Add a new question to a category"""
        try:
            # Ensure category exists
            if category not in self.questions_data["categories"]:
                self.questions_data["categories"][category] = {}
            
            # Add the question
            self.questions_data["categories"][category][key] = question_data
            
            # Update version and changelog
            new_version = self._increment_version()
            self._add_changelog_entry(new_version, f"Added question: {category}.{key}", [f"{category}.{key}"], [])
            
            self.save_questions()
            console.print(f"[green]Added question '{key}' to category '{category}'[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]Error adding question: {e}[/red]")
            return False
    
    def remove_question(self, category: str, key: str) -> bool:
        """Remove a question from a category"""
        if category not in self.questions_data["categories"] or key not in self.questions_data["categories"][category]:
            console.print(f"[yellow]Question '{category}.{key}' not found[/yellow]")
            return False
        
        try:
            del self.questions_data["categories"][category][key]
            self.save_questions()
            console.print(f"[green]Removed question '{key}' from category '{category}'[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Error removing question: {e}[/red]")
            return False
    
    def show_questions(self):
        """Display all questions in a formatted table"""
        console.print(Panel.fit(
            f"[bold blue]Question Management (Version {self.get_current_version()})[/bold blue]",
            border_style="blue"
        ))
        
        for category, questions in self.get_categories().items():
            console.print(f"\n[bold cyan]{category.title()}:[/bold cyan]")
            
            if not questions:
                console.print("  [dim]No questions[/dim]")
                continue
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Key", style="cyan")
            table.add_column("Text", style="white")
            table.add_column("Type", style="yellow")
            table.add_column("Required", style="green")
            table.add_column("Options", style="dim")
            
            for key, q_data in questions.items():
                options = str(q_data.get("options", []))[:50]
                if len(str(q_data.get("options", []))) > 50:
                    options += "..."
                
                required = "Yes" if q_data.get("required", False) else "No"
                
                table.add_row(
                    key,
                    q_data.get("text", "")[:40] + ("..." if len(q_data.get("text", "")) > 40 else ""),
                    q_data.get("type", "unknown"),
                    required,
                    options
                )
            
            console.print(table)
    
    def get_version_diff(self, old_version: str, new_version: str = None) -> Dict[str, List[str]]:
        """Get differences between two versions"""
        if new_version is None:
            new_version = self.get_current_version()
        
        # Find changelog entries between versions
        changes = {"added": [], "removed": []}
        
        for entry in self.questions_data.get("changelog", []):
            if self._version_is_newer(entry["version"], old_version):
                changes["added"].extend(entry.get("questions_added", []))
                changes["removed"].extend(entry.get("questions_removed", []))
        
        return changes
    
    def get_missing_questions(self, personality_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Get questions that a personality hasn't answered yet"""
        personality_version = personality_data.get("question_version", "0.0")
        current_version = self.get_current_version()
        
        if personality_version == current_version:
            return {}
        
        # Get version differences
        diff = self.get_version_diff(personality_version, current_version)
        missing_questions = {}
        
        # Find the actual question data for added questions
        for question_path in diff["added"]:
            if "." in question_path:
                category, key = question_path.split(".", 1)
                if category in self.questions_data["categories"] and key in self.questions_data["categories"][category]:
                    if category not in missing_questions:
                        missing_questions[category] = {}
                    missing_questions[category][key] = self.questions_data["categories"][category][key]
        
        return missing_questions
    
    def interactive_add_question(self):
        """Interactive interface to add a new question"""
        console.print("\n[bold green]➕ Adding New Question[/bold green]")
        
        # Choose category
        categories = list(self.get_categories().keys())
        console.print("Available categories:")
        for i, cat in enumerate(categories, 1):
            console.print(f"  {i}. {cat.replace('_', ' ').title()}")
        console.print(f"  {len(categories) + 1}. Create new category")
        
        try:
            choice = int(Prompt.ask("Choose category")) - 1
            if choice == len(categories):
                category = Prompt.ask("Enter new category name").replace(" ", "_").lower()
            else:
                category = categories[choice]
        except (ValueError, IndexError):
            console.print("[red]Invalid choice[/red]")
            return
        
        # Get question details
        key = Prompt.ask("Question key (e.g., 'favorite_color')").replace(" ", "_").lower()
        question_text = Prompt.ask("Question text")
        
        question_type = Prompt.ask(
            "Question type", 
            choices=["text", "multiple_choice"], 
            default="text"
        )
        
        question_data = {
            "type": question_type,
            "text": question_text, # Changed from "question" to "text"
            "required": Confirm.ask("Is this question required?", default=True)
        }
        
        if question_type == "multiple_choice":
            console.print("Enter options (one per line, empty line to finish):")
            options = []
            while True:
                option = Prompt.ask(f"Option {len(options) + 1} (or press Enter to finish)", default="")
                if not option:
                    break
                options.append(option)
            
            if len(options) < 2:
                console.print("[red]Multiple choice questions need at least 2 options[/red]")
                return
            
            question_data["options"] = options
        
        # Add the question
        self.add_question(category, key, question_data)
    
    def interactive_remove_question(self):
        """Interactive interface to remove a question"""
        console.print("\n[bold red]➖ Removing Question[/bold red]")
        
        # Choose category
        categories = list(self.get_categories().keys())
        console.print("Available categories:")
        for i, cat in enumerate(categories, 1):
            console.print(f"  {i}. {cat.replace('_', ' ').title()}")
        
        try:
            choice = int(Prompt.ask("Choose category")) - 1
            category = categories[choice]
        except (ValueError, IndexError):
            console.print("[red]Invalid choice[/red]")
            return
        
        # Choose question
        questions = list(self.get_categories()[category].keys())
        console.print(f"Questions in {category}:")
        for i, q in enumerate(questions, 1):
            console.print(f"  {i}. {q}")
        
        try:
            choice = int(Prompt.ask("Choose question to remove")) - 1
            key = questions[choice]
        except (ValueError, IndexError):
            console.print("[red]Invalid choice[/red]")
            return
        
        if Confirm.ask(f"Are you sure you want to remove '{key}' from '{category}'?"):
            self.remove_question(category, key)
    
    def _increment_version(self) -> str:
        """Increment version number"""
        current = self.get_current_version()
        major, minor = map(int, current.split("."))
        new_version = f"{major}.{minor + 1}"
        self.questions_data["version"] = new_version
        self.questions_data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        return new_version
    
    def _add_changelog_entry(self, version: str, changes: str, added: List[str], removed: List[str]):
        """Add entry to changelog"""
        entry = {
            "version": version,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "changes": changes,
            "questions_added": added,
            "questions_removed": removed
        }
        self.questions_data["changelog"].append(entry)
    
    def _version_is_newer(self, version1: str, version2: str) -> bool:
        """Check if version1 is newer than version2"""
        v1_parts = list(map(int, version1.split(".")))
        v2_parts = list(map(int, version2.split(".")))
        return v1_parts > v2_parts
    
    def _create_default_questions(self) -> Dict[str, Any]:
        """Create default questions structure if file doesn't exist"""
        return {
            "version": "1.0",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "categories": {},
            "changelog": []
        } 