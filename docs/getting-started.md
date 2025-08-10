# Getting Started Guide

Get AI clones chatting in 5 minutes!

## Quick Start

### 1. Install Dependencies
- Install Python packages: `pip install -r requirements.txt`
- Install Ollama (the AI engine) from [ollama.com](https://ollama.com/)

### 2. Download AI Model
- Download the AI model: `ollama pull llama3.2:3b`

### 3. Run Demo
- Run the quick start script: `python quick_start.py`

That's it! You'll see two AI clones having a natural conversation.

## Detailed Setup

### What You Need
- Python 3.8 or newer - [Download here](https://python.org)
- 8GB or more memory - For smooth AI generation
- Ollama - Local AI engine

### Step-by-Step

#### 1. Test Your Setup
Run the setup test script to check everything is working:

```bash
python tests/test_setup.py
```

This checks:
- Python version
- Ollama installation  
- AI model availability
- Python packages

#### 2. Create Your First Clone
- Use the main interface and choose option 1 to create a clone

## What You Can Do

### Create AI Clones
- 5-minute questionnaire creates unique personalities
- Realistic traits - interests, communication style, background
- Psychology-based questions for authentic personalities

### Chat with Clones
- Natural conversations with consistent personality
- Smart memory remembers everything you discuss
- Three memory systems (SQLite vector memory recommended)

### Watch Clones Chat
- Two clones talk to each other
- Built-in scenarios (coffee shop, restaurant, etc.)
- Automatic logging of all conversations

## Common Issues

"Ollama not found"
- Install Ollama first from [ollama.com](https://ollama.com/)

"Model not found"
- Download the AI model: `ollama pull llama3.2:3b`

"Connection refused"
- Start the Ollama service: `ollama serve`

Still having issues? Run the setup test script for diagnostics.

## Next Steps

1. Create your first clone - Use the main interface
2. Try different memory types - Simple, Enhanced, SQLite Vector
3. Watch clones interact - Start conversations between them
4. Learn more - Check the [Setup Guide](./setup-guide.md)

---

Ready to start? Run the quick start script for the fastest demo! 