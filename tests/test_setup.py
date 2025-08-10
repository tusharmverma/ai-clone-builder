#!/usr/bin/env python3
"""
Setup Test Script
Verifies that all components are working correctly
"""

import sys
import subprocess
import requests
import os
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add src to path for imports
sys.path.append('src')

console = Console()

def test_python_version():
    """Test Python version"""
    console.print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        console.print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        console.print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def test_ollama_installation():
    """Test if Ollama is installed and running"""
    console.print("\n🦙 Checking Ollama installation...")
    
    try:
        # Check if ollama command exists
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            console.print("✅ Ollama CLI installed")
        else:
            console.print("❌ Ollama CLI not found")
            return False
    except FileNotFoundError:
        console.print("❌ Ollama not installed. Visit: https://ollama.com/")
        return False
    
    # Check if Ollama server is running
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            console.print("✅ Ollama server is running")
            return True
        else:
            console.print("❌ Ollama server not responding")
            return False
    except requests.exceptions.ConnectionError:
        console.print("❌ Ollama server not running. Run: ollama serve")
        return False
    except requests.exceptions.Timeout:
        console.print("❌ Ollama server timeout")
        return False

def test_ollama_model():
    """Test if LLaMA model is available"""
    console.print("\n🧠 Checking LLaMA model...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model["name"] for model in models]
            
            if "llama3.2:3b" in model_names:
                console.print("✅ LLaMA 3.2:3b model available")
                return True
            else:
                console.print("❌ LLaMA 3.2:3b model not found")
                console.print("Run: ollama pull llama3.2:3b")
                if model_names:
                    console.print(f"Available models: {', '.join(model_names[:3])}")
                return False
        else:
            console.print("❌ Cannot check models")
            return False
    except Exception as e:
        console.print(f"❌ Error checking models: {e}")
        return False

def test_dependencies():
    """Test if all Python dependencies are installed"""
    console.print("\n📦 Checking Python dependencies...")
    
    required_packages = [
        "requests", "rich", "pydantic", "colorama"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            console.print(f"✅ {package}")
        except ImportError:
            console.print(f"❌ {package} - missing")
            missing_packages.append(package)
    
    if missing_packages:
        console.print(f"\nRun: pip install {' '.join(missing_packages)}")
        return False
    
    return True

def test_project_structure():
    """Test if project structure is correct"""
    console.print("\n📁 Checking project structure...")
    
    required_dirs = [
        "src/personality",
        "src/ai_clone", 
        "src/memory",
        "src/interface",
        "data/personalities",
        "data/conversations"
    ]
    
    missing_dirs = []
    
    for directory in required_dirs:
        if os.path.exists(directory):
            console.print(f"✅ {directory}")
        else:
            console.print(f"❌ {directory} - missing")
            missing_dirs.append(directory)
    
    return len(missing_dirs) == 0

def test_ai_clone():
    """Test basic AI clone functionality"""
    console.print("\n🤖 Testing AI clone functionality...")
    
    try:
        # Test imports
        from personality.templates import create_demo_personalities
        from ai_clone.clone import AIClone
        
        console.print("✅ AI clone imports working")
        
        # Try to create a test clone (without Ollama)
        demo_personalities = create_demo_personalities()
        if demo_personalities:
            console.print("✅ Demo personalities created")
            console.print("✅ AI clone test successful (Ollama connection will be tested when available)")
            return True
        else:
            console.print("❌ Failed to create demo personalities")
            return False
        
    except ImportError as e:
        console.print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        console.print(f"❌ AI clone test failed: {e}")
        return False

def run_full_test():
    """Run all tests"""
    console.print(Panel.fit(
        "[bold blue]🚀 ai-clone-builder Setup Test[/bold blue]\n"
        "Checking if everything is ready for Week 1 development...",
        border_style="blue"
    ))
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Project Structure", test_project_structure),
        ("AI Clone", test_ai_clone),
        ("Ollama Installation", test_ollama_installation),
        ("LLaMA Model", test_ollama_model)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            console.print(f"❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    console.print("\n" + "="*50)
    console.print("[bold]📊 Test Results Summary[/bold]")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        console.print(f"{test_name}: {status}")
    
    console.print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        console.print(Panel.fit(
            "[bold green]🎉 All tests passed! You're ready to start building AI clones![/bold green]",
            border_style="green"
        ))
        console.print("\n[bold]Next steps:[/bold]")
        console.print("1. Run: python -m src.personality.questionnaire")
        console.print("2. Or run: python -m src.interface.cli")
    else:
        console.print(Panel.fit(
            "[bold red]⚠️  Some tests failed. Please fix the issues above before proceeding.[/bold red]",
            border_style="red"
        ))
        
        # Provide specific help
        if not any(result for name, result in results if "Ollama" in name):
            console.print("\n[yellow]Ollama Setup Help:[/yellow]")
            console.print("1. Install: https://ollama.com/")
            console.print("2. Run: ollama pull llama3.2:3b")
            console.print("3. Start: ollama serve")

if __name__ == "__main__":
    run_full_test() 