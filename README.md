# 🤖 AI Clone Builder

**Create AI clones with unique personalities that actually remember conversations!**

## 🚀 Quick Start (3 minutes)

**Step 1: Install the basics**
- Install Python packages by running: `pip install -r requirements.txt`
- Install Ollama (the AI engine) from [ollama.com](https://ollama.com)
- Download an AI model by running: `ollama pull llama3.2:3b`

**Step 2: Try it out**
- Run the demo: `python quick_start.py`

## ✨ What This Does

- **Create AI Clones** - Build unique personalities through simple questionnaires
- **Natural Conversations** - Clones chat like real people with consistent traits
- **Smart Memory** - Uses intelligent storage to remember everything
- **100% Private** - Runs on your computer, no cloud needed

## 🎭 Example Conversation

```
🗣️ Alex: Just got back from rock climbing! The view was amazing.
💭 Sam: That sounds incredible! I've been working on a mural about 
spreading positivity. Rock climbing and art - we're both 
adventurous souls!
```

## 📚 Documentation

- **[Setup Guide](./docs/setup-guide.md)** - How everything works & memory systems
- **[Getting Started](./docs/getting-started.md)** - Step-by-step tutorial
- **[Simple Examples](./docs/simple-examples.md)** - Easy-to-follow examples
- **[Project Overview](./docs/project-overview.md)** - How everything fits together
- **[Troubleshooting](./docs/troubleshooting.md)** - Fix common issues

## 🏗️ How It's Organized

Think of it like a well-organized house:
- **Main Room** - Where AI clones are created and managed
- **Personality Workshop** - Where you design what makes each clone special
- **Memory Storage** - Where all conversations are saved and remembered
- **Front Door** - How you interact with everything

## 🧪 Testing

**Check if everything works:**
- Run all tests: `python run_tests.py`
- Test basic setup: `python tests/test_setup.py`

## 🔧 What You Need

- **Python**: Version 3.8 or newer
- **Memory**: 8GB or more (4GB works for smaller models)
- **Platform**: Works on Mac, Windows, or Linux

## 🆘 Need Help?

**Something not working?** Try this first:
```bash
python tests/test_setup.py
```

**Common fixes:**
- "Ollama not found" → Install from [ollama.com](https://ollama.com)
- "Connection refused" → Start Ollama with `ollama serve`
- "Model not found" → Download with `ollama pull llama3.2:3b`

---

**Ready to build your first AI clone?** Check the [Setup Guide](./docs/setup-guide.md)! 🎯
