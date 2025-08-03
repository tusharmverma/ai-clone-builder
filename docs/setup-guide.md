# 🚀 Setup Guide

Complete installation guide for fol-ai-match AI clone system.

## ⚡ Quick Start (5 minutes)

### Option 1: Instant Demo
```bash
# 1. Install Python dependencies  
pip install -r requirements.txt

# 2. Run the quick start
python quick_start.py

# 3. Choose option 1 for demo
```

### Option 2: Full Setup
```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Download AI model
ollama pull llama3.2:3b

# 3. Install Python dependencies
pip install -r requirements.txt  

# 4. Test everything
python test_setup.py

# 5. Start creating clones!
python -m src.interface.cli
```

## 📋 Prerequisites

### System Requirements
- **Operating System**: macOS, Linux, or Windows
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 2GB free space (for AI model)
- **Internet**: Required for initial setup only

### Check Your System
```bash
# Check Python version
python --version
# Should show Python 3.8+

# Check available RAM
# macOS/Linux:
free -h
# Windows:
wmic memorychip get size

# Check free disk space  
df -h  # macOS/Linux
dir   # Windows
```

## 🔧 Detailed Installation

### Step 1: Install Ollama

Ollama runs the AI model locally on your machine.

#### macOS & Linux
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version
```

#### Windows
1. Download from [ollama.com](https://ollama.com/)
2. Run the installer
3. Open command prompt and verify: `ollama --version`

#### Alternative: Docker Installation
```bash
# If you prefer Docker
docker pull ollama/ollama
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### Step 2: Download AI Model

```bash
# Download LLaMA 3.2 (3B parameters)
ollama pull llama3.2:3b

# Verify model is downloaded
ollama list

# Test the model
ollama run llama3.2:3b
# Type "hello" and press enter
# Press Ctrl+D to exit
```

**Model Size**: ~2GB download
**Download Time**: 5-20 minutes (depending on internet speed)

### Step 3: Python Environment Setup

#### Option A: Using pip (Recommended)
```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python -c "import requests, rich, pydantic; print('All packages installed!')"
```

#### Option B: Using conda
```bash
# Create new environment
conda create -n fol-ai-match python=3.9

# Activate environment  
conda activate fol-ai-match

# Install packages
pip install -r requirements.txt
```

#### Option C: Using virtual environment
```bash
# Create virtual environment
python -m venv venv

# Activate environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 4: Project Setup

```bash
# Clone or download the project
git clone [your-repo-url]
cd fol-ai-match

# Create data directories (if not already present)
mkdir -p data/personalities data/conversations

# Make scripts executable (macOS/Linux)
chmod +x quick_start.py test_setup.py

# Run the setup test
python test_setup.py
```

## 🧪 Verify Installation

### Automated Testing
```bash
# Run comprehensive system test
python test_setup.py

# Expected output:
# ✅ Python Version: PASS
# ✅ Dependencies: PASS  
# ✅ Project Structure: PASS
# ✅ Ollama Installation: PASS
# ✅ LLaMA Model: PASS
# ✅ AI Clone: PASS
# 
# Overall: 6/6 tests passed
# 🎉 All tests passed! You're ready to start building AI clones!
```

### Manual Testing
```bash
# Test Ollama connection
curl http://localhost:11434/api/tags

# Test Python imports
python -c "
from src.ai_clone.clone import test_clone_response
test_clone_response()
"

# Test CLI
python -m src.interface.cli
```

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. Ollama Not Found
```
❌ Error: ollama command not found
```

**Solutions**:
```bash
# Check if Ollama is installed
which ollama

# If not found, reinstall:
curl -fsSL https://ollama.com/install.sh | sh

# Add to PATH (if needed)
export PATH=$PATH:/usr/local/bin
```

#### 2. Ollama Server Not Running
```
❌ Error: Cannot connect to Ollama server
```

**Solutions**:
```bash
# Start Ollama service
ollama serve

# Or run in background
nohup ollama serve &

# Check if port 11434 is open
lsof -i :11434
```

#### 3. Model Not Found
```
❌ Error: llama3.2:3b model not found
```

**Solutions**:
```bash
# Download the model
ollama pull llama3.2:3b

# Check available models
ollama list

# Alternative smaller model (if RAM limited)
ollama pull llama3.2:1b
```

#### 4. Python Package Issues
```
❌ Error: No module named 'rich'
```

**Solutions**:
```bash
# Reinstall requirements
pip install -r requirements.txt

# Check Python version
python --version

# Use specific Python version if needed
python3.9 -m pip install -r requirements.txt
```

#### 5. Permission Errors
```
❌ Error: Permission denied
```

**Solutions**:
```bash
# Fix file permissions
chmod +x quick_start.py test_setup.py

# Fix directory permissions
chmod -R 755 data/

# Run with user permissions
python quick_start.py
```

#### 6. Memory Issues
```
❌ Error: Out of memory
```

**Solutions**:
```bash
# Check available RAM
free -h

# Use smaller model
ollama pull llama3.2:1b

# Close other applications
# Restart Ollama service
```

#### 7. Network/Firewall Issues
```
❌ Error: Connection timeout
```

**Solutions**:
```bash
# Check firewall settings
# Allow port 11434 for Ollama

# Test local connection
curl -v http://localhost:11434/api/tags

# Use alternative host
export OLLAMA_HOST=http://127.0.0.1:11434
```

### Platform-Specific Issues

#### macOS
```bash
# Xcode command line tools (if needed)
xcode-select --install

# Homebrew installation of Ollama
brew install ollama

# Python via Homebrew
brew install python@3.9
```

#### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt update

# Install Python pip
sudo apt install python3-pip

# Install curl (if needed)
sudo apt install curl

# Fix locale issues (if any)
sudo locale-gen en_US.UTF-8
```

#### Windows
```powershell
# Install Python from Microsoft Store
# Or download from python.org

# Install Git for Windows (if using git)
# Download from git-scm.com

# Use PowerShell or Command Prompt
# Not Windows Subsystem for Linux (WSL)
```

## 📊 Performance Optimization

### For Limited RAM (< 8GB)
```bash
# Use smaller model
ollama pull llama3.2:1b

# Edit clone.py to use smaller model:
# self.model = "llama3.2:1b"

# Reduce conversation history
# In clone.py, reduce max_messages to 3-5
```

### For Slower Machines
```bash
# Increase timeout in clone.py
# timeout=60  # instead of 30

# Reduce concurrent conversations
# Use one clone at a time

# Close unnecessary applications
```

### For Better Performance
```bash
# Use SSD storage for faster file I/O
# Increase RAM for better model performance
# Use dedicated GPU (future feature)
```

## 🛠️ Development Setup

### Additional Tools for Development
```bash
# Install development dependencies
pip install pytest black flake8 mypy

# Set up pre-commit hooks
pre-commit install

# Run tests
python -m pytest tests/

# Format code
black src/

# Type checking
mypy src/
```

### IDE Configuration
```json
// VS Code settings.json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black"
}
```

## 🎯 Next Steps

### After Successful Installation
1. **Run the demo**: `python quick_start.py` → option 1
2. **Create your first clone**: `python quick_start.py` → option 2  
3. **Explore the CLI**: `python -m src.interface.cli`
4. **Read the user guide**: [User Guide](./user-guide.md)

### If You Had Issues
1. **Join the community**: [GitHub Issues](../README.md)
2. **Check documentation**: [API Reference](./api-reference.md)
3. **Report bugs**: Include output from `python test_setup.py`

---

**Installation complete?** 🎉 Check out the [User Guide](./user-guide.md) to start creating AI clones! 