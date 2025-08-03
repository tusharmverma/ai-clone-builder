# 🔧 Troubleshooting

**Quick fixes for common problems.**

## 🧪 First Step: Run the Test

Before anything else, run:
```bash
python test_setup.py
```

This will tell you exactly what's wrong. Look for ❌ FAIL messages.

## Common Issues

### 1. "ollama command not found"

**Problem:** Ollama isn't installed or not in your PATH

**Fix:**
```bash
# On Mac
brew install ollama

# On Windows: Download from ollama.com
# On Linux
curl -fsSL https://ollama.com/install.sh | sh

# Test if it worked
ollama --version
```

### 2. "Cannot connect to Ollama server"

**Problem:** Ollama is installed but not running

**Fix:**
```bash
# Start Ollama
ollama serve

# Or start as background service (Mac)
brew services start ollama

# Test if it worked
curl http://localhost:11434/api/tags
```

### 3. "llama3.2:3b model not found"

**Problem:** AI model isn't downloaded

**Fix:**
```bash
# Download the model (2GB download)
ollama pull llama3.2:3b

# Check it downloaded
ollama list
```

### 4. "No module named 'rich'"

**Problem:** Python packages aren't installed

**Fix:**
```bash
# Install required packages
pip install -r requirements.txt

# If that doesn't work, try
pip install requests rich pydantic colorama
```

### 5. Slow Responses or "Out of Memory"

**Problem:** Your computer doesn't have enough RAM

**Fix:**
```bash
# Use smaller model (1GB instead of 2GB)
ollama pull llama3.2:1b

# Then edit src/ai_clone/clone.py
# Change: self.model = "llama3.2:3b"  
# To: self.model = "llama3.2:1b"
```

### 6. AI Responses Are Weird/Generic

**Problem:** Personality isn't specific enough

**Fix:**
- Be more specific in questionnaires
- Add more details about interests
- Use concrete examples instead of general terms

**Example:**
```
❌ "I like sports"
✅ "I'm obsessed with basketball, watch every Lakers game, 
    play pickup on weekends, follow NBA stats religiously"
```

### 7. "Import Error" or "Module Not Found"

**Problem:** Python can't find the project files

**Fix:**
```bash
# Make sure you're in the right directory
cd fol-ai-match

# Check the files are there
ls src/

# Try running from the project root
python -m src.interface.cli
```

### 8. Conversations Don't Save

**Problem:** Permission issues with data folder

**Fix:**
```bash
# Check if data folder exists
ls data/

# Create if missing
mkdir -p data/personalities data/conversations

# Fix permissions (Mac/Linux)
chmod -R 755 data/
```

## Still Stuck?

### Check System Requirements
- **RAM:** 8GB minimum (4GB for smaller model)
- **Storage:** 3GB free space
- **Python:** Version 3.8 or higher
- **Internet:** Only needed for initial setup

### Run Full Diagnostics
```bash
# Detailed system check
python test_setup.py

# Check Python version
python --version

# Check available memory
# Mac: Activity Monitor
# Windows: Task Manager  
# Linux: free -h
```

### Reset Everything
```bash
# Stop Ollama
brew services stop ollama  # Mac
# Or Ctrl+C if running ollama serve

# Restart Ollama  
brew services start ollama

# Re-download model
ollama pull llama3.2:3b

# Test again
python test_setup.py
```

## Performance Tips

### For Slower Computers
```bash
# Use smaller model
ollama pull llama3.2:1b

# Reduce conversation history
# Edit src/ai_clone/clone.py
# Change max_messages from 10 to 3
```

### For Better Quality
```bash
# Use larger model (if you have 16GB+ RAM)
ollama pull llama3.2:8b

# Increase response length
# Edit src/ai_clone/clone.py  
# Change max_tokens from 150 to 250
```

## Common Error Messages

**"Connection refused"** → Ollama isn't running  
**"Model not found"** → Need to download model  
**"Permission denied"** → File permission issues  
**"Out of memory"** → Computer doesn't have enough RAM  
**"Module not found"** → Missing Python packages  
**"Command not found"** → Software not installed or not in PATH

## Quick Health Check

Run this to verify everything is working:
```bash
# 1. Check Ollama
ollama list

# 2. Check Python packages
python -c "import requests, rich; print('Packages OK')"

# 3. Check project structure
ls src/ai_clone/clone.py

# 4. Test AI response
python -c "
import sys; sys.path.append('src')
from ai_clone.clone import test_clone_response
test_clone_response()
"
```

If all these work, you're good to go!

---

**Still having issues?** Make sure to run `python test_setup.py` first - it will tell you exactly what to fix! 🔍 