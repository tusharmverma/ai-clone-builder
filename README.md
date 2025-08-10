# AI Clone Builder

<!-- Main project overview -->

Create AI clones with unique personalities that actually remember conversations!

## Quick Start (3 minutes)

Step 1: Install the basics
- Install Python packages by running: `pip install -r requirements.txt`
- Install Ollama (the AI engine) from [ollama.com](https://ollama.com)
- Download an AI model by running: `ollama pull llama3.2:3b`

Step 2: Try it out
- Run the demo: `python quick_start.py`

## What This Does

- Create AI Clones - Build unique personalities through simple questionnaires
- Natural Conversations - Clones chat like real people with consistent traits
- Smart Memory - Uses intelligent storage to remember everything
- 100% Private - Runs on your computer, no cloud needed

## Example Conversation

```
Alex: Just got back from rock climbing! The view was amazing.
Sam: That sounds incredible! I've been working on a mural about 
spreading positivity. Rock climbing and art - we're both 
adventurous souls!
```

## Documentation

- [Setup Guide](./docs/setup-guide.md) - How everything works & memory systems
- [Getting Started](./docs/getting-started.md) - Step-by-step tutorial
- [Simple Examples](./docs/simple-examples.md) - Easy-to-follow examples
- [Project Overview](./docs/project-overview.md) - How everything fits together
- [Troubleshooting](./docs/troubleshooting.md) - Fix common issues

## How It's Organized

Think of it like a well-organized house:
- Main Room - Where AI clones are created and managed
- Personality Workshop - Where you design what makes each clone special
- Memory Storage - Where all conversations are saved and remembered
- Front Door - How you interact with everything

## Code Structure

Here's how the code is organized for developers:

### Core AI Clone System (`src/ai_clone/`)
- **`clone.py`** - Main `AIClone` class that handles personality, memory, and conversations
- **`conversation.py`** - Manages conversations between multiple clones with scenarios

### Personality System (`src/personality/`)
- **`questionnaire.py`** - Interactive questionnaire for creating clone personalities
- **`templates.py`** - Converts questionnaire data into detailed AI system prompts

### Memory Management (`src/memory/`)
- **`memory_manager.py`** - Intelligent memory system that auto-selects the best storage type
- **`sqlite_vec_memory.py`** - High-performance vector database for semantic search
- **`enhanced_memory.py`** - JSON-based memory with conversation tracking
- **`simple_memory.py`** - Basic conversation history and management

### User Interface (`src/interface/`)
- **`cli.py`** - Command-line interface for interacting with clones

### Entry Points
- **`quick_start.py`** - Main entry point with demo, clone creation, and CLI options
- **`run_tests.py`** - Comprehensive test runner for all functionality

### Data Storage (`data/`)
- **`questions.json`** - Questionnaire structure and questions
- **`personalities/`** - Saved clone personality files
- **`vector_memory/`** - SQLite databases for semantic memory
- **`enhanced_memory/`** - Enhanced memory JSON files

### Testing (`tests/`)
- **`test_e2e_cli.py`** - End-to-end CLI functionality tests
- **`test_intelligent_memory.py`** - Memory system performance tests
- **`test_performance_scaling.py`** - Memory scaling and performance tests
- **`test_sqlite_vec_integration.py`** - Vector memory integration tests
- **`demo_clone_conversation.py`** - Live conversation demonstration system

## Testing

Check if everything works:
- Run all tests: `python run_tests.py`
- Test basic setup: `python tests/test_setup.py`

## What You Need

- Python: Version 3.8 or newer
- Memory: 8GB or more (4GB works for smaller models)
- Platform: Works on Mac, Windows, or Linux

## Development Guide

### Key Classes and Methods

#### AIClone Class (`src/ai_clone/clone.py`)
- **`__init__(personality_data, ollama_host, memory_type)`** - Creates a new AI clone
- **`respond(message, context)`** - Main method for generating personality-driven responses
- **`_get_response_length_instruction(message)`** - Analyzes message complexity and personality for intelligent response guidance
- **`_build_prompt(message, context)`** - Constructs comprehensive prompts with personality and memory context

#### PersonalityTemplate Class (`src/personality/templates.py`)
- **`create_system_prompt(personality_data)`** - Generates detailed system prompts from questionnaire data
- **`_build_background_context()`** - Creates life context and background information
- **`_build_personality_expressions()`** - Formats personality traits for AI instructions

#### MemoryManager Class (`src/memory/memory_manager.py`)
- **`auto_select_memory()`** - Intelligently chooses the best memory system based on data size
- **`get_context()`** - Retrieves relevant conversation context for responses

### Adding New Features

1. **New Personality Traits**: Add questions to `data/questions.json` and update `templates.py`
2. **New Memory Types**: Create new memory class and add to `memory_manager.py`
3. **New Conversation Types**: Extend `conversation.py` with new scenario handling

### Testing Your Changes

```bash
# Run all tests
python run_tests.py

# Run specific test categories
python tests/test_e2e_cli.py
python tests/test_intelligent_memory.py

# Test quick start functionality
python quick_start.py
```

## Need Help?

Something not working? Try this first:
```bash
python tests/test_setup.py
```

Common fixes:
- "Ollama not found" → Install from [ollama.com](https://ollama.com)
- "Connection refused" → Start Ollama with `ollama serve`
- "Model not found" → Download with `ollama pull llama3.2:3b`

---

Ready to build your first AI clone? Check the [Setup Guide](./docs/setup-guide.md)!
