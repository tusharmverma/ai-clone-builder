# 🚀 Getting Started with ai-clone-builder

**Get your first AI clone talking in under 10 minutes!**

## What You'll Build

By the end of this guide, you'll have:
- ✅ Two AI clones with different personalities  
- ✅ Watch them have a natural conversation
- ✅ Chat with them yourself

**Time needed:** 5-10 minutes  
**Difficulty:** Easy (copy & paste commands)

## Step 1: Check Your Computer

You need:
- **macOS, Windows, or Linux**
- **8GB+ RAM** (for the AI to run smoothly)
- **Internet connection** (just for setup)

## Step 2: Install the AI Engine

**On Mac:**
```bash
brew install ollama
```

**On Windows:**
1. Go to [ollama.com](https://ollama.com)
2. Download and run the installer

**On Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## Step 3: Download the AI Brain

```bash
ollama pull llama3.2:3b
```

This downloads a 2GB AI model. Grab some coffee! ☕

## Step 4: Get the Project

```bash
# Download the project
git clone [your-repo-url]
cd ai-clone-builder

# Install Python packages
pip install -r requirements.txt
```

## Step 5: Test Everything

```bash
python test_setup.py
```

You should see:
```
✅ Python Version: PASS
✅ Dependencies: PASS  
✅ Project Structure: PASS
✅ Ollama Installation: PASS
✅ LLaMA Model: PASS
✅ AI Clone: PASS

🎉 All tests passed!
```

## Step 6: See the Magic

```bash
python quick_start.py
```

Choose **option 1** for instant demo.

You'll see something like:
```
🗣️ Alex: Hey! Just got back from rock climbing...

💭 Sam: Yaaas! I've been working on this mural...
```

## 🎉 Congratulations!

You just watched two AI clones have a natural conversation!

## What's Next?

**Create your own clone:**
```bash
python quick_start.py
# Choose option 2
```

**Explore all features:**
```bash
python -m src.interface.cli
```

**Learn more advanced stuff:**
- [User Guide](./user-guide.md) - Create custom personalities
- [Troubleshooting](./setup-guide.md#troubleshooting) - Fix common issues

## 🆘 Something Went Wrong?

**Most common issues:**

**"ollama command not found"**
```bash
# Make sure Ollama is installed
ollama --version
```

**"Cannot connect to Ollama"**
```bash
# Start the Ollama service
ollama serve
```

**"Model not found"**
```bash
# Download the model again
ollama pull llama3.2:3b
```

**Still stuck?** Run `python test_setup.py` and it will tell you exactly what's wrong.

---

**Ready for more?** Check out the [User Guide](./user-guide.md) to create your own AI clones! 🤖 