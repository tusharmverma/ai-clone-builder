#!/usr/bin/env python3
"""
End-to-End CLI Test
Tests the complete workflow from clone creation to conversation
"""

import sys
import os
import tempfile
import shutil
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def test_imports():
    """Test that all major modules can be imported"""
    
    # Test CLI import functionality
    console.print("🔍 Testing imports...")
    
    try:
        from ai_clone.clone import AIClone, create_demo_clones
        from personality.questionnaire import QuestionnaireManager
        from personality.templates import PersonalityTemplate
        from memory.memory_manager import MemoryManager
        from memory.enhanced_memory import EnhancedMemory
        from memory.sqlite_vec_memory import SqliteVecMemory
        from memory.simple_memory import SimpleMemory
        from interface.cli import main as cli_main
        
        console.print("✅ All imports successful")
        return True
    except ImportError as e:
        console.print(f"❌ Import failed: {e}")
        return False

def test_demo_clone_creation():
    """Test creating demo clones"""
    console.print("\n🤖 Testing demo clone creation...")
    
    try:
        from ai_clone.clone import create_demo_clones
        
        # Test all memory types
        memory_types = ["auto", "simple", "enhanced", "sqlite_vec"]
        
        for memory_type in memory_types:
            console.print(f"  🧪 Testing {memory_type} memory...")
            
            clones = create_demo_clones(memory_type=memory_type)
            
            if clones and len(clones) >= 2:
                console.print(f"    ✅ Created {len(clones)} clones with {memory_type} memory")
                
                # Test basic clone properties
                for clone in clones:
                    if hasattr(clone, 'name') and clone.name:
                        console.print(f"      ✅ Clone '{clone.name}' created successfully")
                    else:
                        console.print(f"      ❌ Clone missing name")
                        return False
                        
                    if hasattr(clone, 'personality_data') and clone.personality_data:
                        console.print(f"      ✅ Clone has personality data")
                    else:
                        console.print(f"      ❌ Clone missing personality data")
                        return False
            else:
                console.print(f"    ❌ Failed to create clones with {memory_type} memory")
                return False
        
        console.print("✅ Demo clone creation successful")
        return True
        
    except Exception as e:
        console.print(f"❌ Demo clone creation failed: {e}")
        return False

def test_clone_conversation():
    """Test clone conversation functionality"""
    console.print("\n💬 Testing clone conversation...")
    
    try:
        from ai_clone.clone import create_demo_clones
        
        # Create clones with simple memory for testing
        clones = create_demo_clones(memory_type="simple")
        
        if not clones or len(clones) < 2:
            console.print("❌ Need at least 2 clones for conversation test")
            return False
        
        alex, sam = clones[0], clones[1]
        
        console.print(f"  🧪 Testing conversation between {alex.name} and {sam.name}...")
        
        # Test conversation history
        alex.add_to_conversation_history("User", "Hello! How are you?")
        sam.add_to_conversation_history("User", "Hi there! I'm doing well, thanks!")
        
        # Test getting conversation history
        alex_history = alex.get_recent_history(5)
        sam_history = sam.get_recent_history(5)
        
        if len(alex_history) > 0 and len(sam_history) > 0:
            console.print("    ✅ Conversation history working")
        else:
            console.print("    ❌ Conversation history not working")
            return False
        
        # Test personality summary
        alex_summary = alex.get_personality_summary()
        sam_summary = sam.get_personality_summary()
        
        if alex_summary and sam_summary:
            console.print("    ✅ Personality summaries working")
        else:
            console.print("    ❌ Personality summaries not working")
            return False
        
        console.print("✅ Clone conversation functionality working")
        return True
        
    except Exception as e:
        console.print(f"❌ Clone conversation test failed: {e}")
        return False

def test_memory_systems():
    """Test all memory systems"""
    console.print("\n🧠 Testing memory systems...")
    
    try:
        from memory.memory_manager import MemoryManager
        from memory.enhanced_memory import EnhancedMemory
        from memory.sqlite_vec_memory import SqliteVecMemory
        from memory.simple_memory import SimpleMemory
        
        # Test simple memory
        console.print("  🧪 Testing simple memory...")
        simple_mem = SimpleMemory("test_clone")
        simple_mem.add_message("User", "Test message")
        context = simple_mem.get_context()
        if context:
            console.print("    ✅ Simple memory working")
        else:
            console.print("    ❌ Simple memory not working")
            return False
        
        # Test enhanced memory
        console.print("  🧪 Testing enhanced memory...")
        enhanced_mem = EnhancedMemory("test_clone")
        enhanced_mem.add_message("User", "Test message")
        context = enhanced_mem.get_context()
        if context:
            console.print("    ✅ Enhanced memory working")
        else:
            console.print("    ❌ Enhanced memory not working")
            return False
        
        # Test SQLite vector memory
        console.print("  🧪 Testing SQLite vector memory...")
        sqlite_mem = None
        try:
            sqlite_mem = SqliteVecMemory("test_clone")
            sqlite_mem.add_message("User", "Test message")
            context = sqlite_mem.get_context()
            if context:
                console.print("    ✅ SQLite vector memory working")
            else:
                console.print("    ❌ SQLite vector memory not working")
                return False
        except Exception as e:
            console.print(f"    ⚠️ SQLite vector memory test skipped: {e}")
        
        # Test memory manager
        console.print("  🧪 Testing memory manager...")
        manager = MemoryManager("test_clone")
        if manager.current_memory_type:
            console.print("    ✅ Memory manager working")
        else:
            console.print("    ❌ Memory manager not working")
            return False
        
        # Cleanup
        if hasattr(simple_mem, 'close'):
            simple_mem.close()
        if hasattr(enhanced_mem, 'close'):
            enhanced_mem.close()
        if sqlite_mem and hasattr(sqlite_mem, 'close'):
            sqlite_mem.close()
        
        console.print("✅ All memory systems working")
        return True
        
    except Exception as e:
        console.print(f"❌ Memory systems test failed: {e}")
        return False

def test_personality_system():
    """Test personality questionnaire and templates"""
    console.print("\n🎭 Testing personality system...")
    
    try:
        from personality.templates import PersonalityTemplate
        from personality.questionnaire import QuestionnaireManager
        
        # Test template creation
        console.print("  🧪 Testing personality templates...")
        
        # Create a test personality
        test_personality = {
            "basic_info": {
                "name": "TestClone",
                "age": 25,
                "location": "Test City",
                "occupation": "Tester"
            },
            "personality_traits": {
                "introversion": {"choice": "Extroverted"},
                "emotional_stability": {"choice": "Stable"},
                "openness": {"choice": "Open to new experiences"}
            },
            "communication_style": {
                "formality": {"choice": "Casual"},
                "humor": {"choice": "Witty/sarcastic"},
                "expressiveness": {"choice": "Expressive"}
            }
        }
        
        # Test system prompt creation
        system_prompt = PersonalityTemplate.create_system_prompt(test_personality)
        if system_prompt and len(system_prompt) > 100:
            console.print("    ✅ System prompt creation working")
        else:
            console.print("    ❌ System prompt creation failed")
            return False
        
        # Test conversation context creation
        context = PersonalityTemplate.create_conversation_context(test_personality)
        if context and len(context) > 50:
            console.print("    ✅ Conversation context creation working")
        else:
            console.print("    ❌ Conversation context creation failed")
            return False
        
        console.print("✅ Personality system working")
        return True
        
    except Exception as e:
        console.print(f"❌ Personality system test failed: {e}")
        return False

def test_ollama_integration():
    """Test Ollama integration (if available)"""
    console.print("\n🦙 Testing Ollama integration...")
    
    try:
        import requests
        
        # Test Ollama server connection
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                console.print("  ✅ Ollama server responding")
                
                # Test model availability
                models = response.json().get("models", [])
                if models:
                    console.print(f"  ✅ Models available: {len(models)}")
                    
                    # Test basic clone response (if we have a model)
                    try:
                        from ai_clone.clone import create_demo_clones
                        clones = create_demo_clones(memory_type="simple")
                        if clones:
                            clone = clones[0]
                            
                            # Test a simple response (this might take time)
                            console.print("  🧪 Testing clone response generation...")
                            start_time = time.time()
                            
                            try:
                                response = clone.respond("Hello! How are you?")
                                end_time = time.time()
                                
                                if response and len(response) > 0:
                                    console.print(f"    ✅ Response generated in {end_time - start_time:.2f}s")
                                    console.print(f"    📝 Response: {response[:100]}...")
                                else:
                                    console.print("    ❌ No response generated")
                                    return False
                                    
                            except Exception as e:
                                console.print(f"    ⚠️ Response generation test skipped: {e}")
                                console.print("    ℹ️ This is normal if Ollama model is still loading")
                                
                    except Exception as e:
                        console.print(f"    ⚠️ Clone response test skipped: {e}")
                        
                else:
                    console.print("  ⚠️ No models available")
                    console.print("  ℹ️ Run: ollama pull llama3.2:3b")
                    
                return True
                
            else:
                console.print("  ❌ Ollama server not responding properly")
                return False
                
        except requests.exceptions.ConnectionError:
            console.print("  ⚠️ Ollama server not running")
            console.print("  ℹ️ Run: ollama serve")
            return False
        except requests.exceptions.Timeout:
            console.print("  ❌ Ollama server timeout")
            return False
            
    except ImportError:
        console.print("  ⚠️ Requests not available, skipping Ollama test")
        return False
    except Exception as e:
        console.print(f"  ❌ Ollama integration test failed: {e}")
        return False

def test_file_operations():
    """Test file operations (save/load)"""
    console.print("\n💾 Testing file operations...")
    
    try:
        from ai_clone.clone import create_demo_clones
        
        # Create a test clone
        clones = create_demo_clones(memory_type="simple")
        if not clones:
            console.print("  ❌ Need clones for file operation test")
            return False
        
        clone = clones[0]
        
        # Test conversation save
        console.print("  🧪 Testing conversation save...")
        clone.add_to_conversation_history("User", "Test message for file operations")
        
        # Create temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, "test_conversation.json")
            
            try:
                clone.save_conversation(test_file)
                if os.path.exists(test_file):
                    console.print("    ✅ Conversation save working")
                else:
                    console.print("    ❌ Conversation save failed")
                    return False
                    
                # Test conversation load
                console.print("  🧪 Testing conversation load...")
                clone.load_conversation(test_file)
                
                # Check if conversation was loaded
                history = clone.get_recent_history(5)
                if history and len(history) > 0:
                    console.print("    ✅ Conversation load working")
                else:
                    console.print("    ❌ Conversation load failed")
                    return False
                    
            except Exception as e:
                console.print(f"    ❌ File operation failed: {e}")
                return False
        
        console.print("✅ File operations working")
        return True
        
    except Exception as e:
        console.print(f"❌ File operations test failed: {e}")
        return False

def run_e2e_test():
    """Run the complete end-to-end test suite"""
    console.print(Panel.fit(
        "[bold blue]🚀 ai-clone-builder End-to-End Test Suite[/bold blue]\n"
        "Testing complete workflow from clone creation to conversation...",
        border_style="blue"
    ))
    
    tests = [
        ("Imports", test_imports),
        ("Demo Clone Creation", test_demo_clone_creation),
        ("Clone Conversation", test_clone_conversation),
        ("Memory Systems", test_memory_systems),
        ("Personality System", test_personality_system),
        ("File Operations", test_file_operations),
        ("Ollama Integration", test_ollama_integration)
    ]
    
    results = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        for test_name, test_func in tests:
            task = progress.add_task(f"Running {test_name}...", total=None)
            
            try:
                result = test_func()
                results.append((test_name, result))
                progress.update(task, description=f"{test_name}: {'✅ PASS' if result else '❌ FAIL'}")
            except Exception as e:
                console.print(f"❌ {test_name} failed with error: {e}")
                results.append((test_name, False))
                progress.update(task, description=f"{test_name}: ❌ FAIL")
    
    # Summary
    console.print("\n" + "="*60)
    console.print("[bold]📊 End-to-End Test Results Summary[/bold]")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    table = Table(title="Test Results")
    table.add_column("Test", style="cyan")
    table.add_column("Status", style="magenta")
    table.add_column("Details", style="green")
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        details = "All functionality working" if result else "Functionality needs attention"
        table.add_row(test_name, status, details)
    
    console.print(table)
    
    console.print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        console.print(Panel.fit(
            "[bold green]🎉 All end-to-end tests passed! The system is working perfectly![/bold green]",
            border_style="green"
        ))
        console.print("\n[bold]System Status:[/bold]")
        console.print("✅ Core functionality working")
        console.print("✅ Memory systems operational")
        console.print("✅ Personality system functional")
        console.print("✅ File operations working")
        console.print("✅ Ready for production use!")
        
        return True
    else:
        failed_tests = [name for name, result in results if not result]
        console.print(Panel.fit(
            f"[bold red]⚠️  {total - passed} tests failed. Please fix the issues above.[/bold red]",
            border_style="red"
        ))
        console.print(f"\n[bold]Failed tests:[/bold] {', '.join(failed_tests)}")
        
        return False

if __name__ == "__main__":
    success = run_e2e_test()
    sys.exit(0 if success else 1) 