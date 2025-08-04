# ai-clone-builder

**Create AI clones that talk like real people and watch them chat with each other.**

Perfect for dating apps, social experiments, or just having fun with AI personalities.

## ⚡ Quick Start (5 minutes)

```bash
# 1. Install AI engine
brew install ollama                 # Mac
ollama pull llama3.2:3b

# 2. Install Python packages  
pip install -r requirements.txt

# 3. See the magic
python quick_start.py
# Choose option 1 for instant demo!
```

You'll watch two AI clones have a natural conversation about rock climbing, art, music festivals, and more!

## 🎮 What You Can Do

### ✅ **Create AI Clones**
- 5-10 minute personality questionnaire
- Creates unique AI with specific traits
- Talks exactly like the person you described

### ✅ **Chat with Clones**  
- Have natural conversations
- AI remembers what you talked about
- Consistent personality every time

### ✅ **Watch Clones Chat**
- Two clones talk to each other
- Built-in dating scenarios (coffee shop, restaurant, etc.)
- Completely realistic conversations

## 🔥 Why This is Cool

**🏠 100% Private** - Runs on your computer, no cloud, no data sharing

**💰 Completely Free** - Uses free local AI, no API costs ever

**⚡ Actually Works** - Real conversations, not scripted responses

**🧠 Smart Memory** - Remembers personality and conversation context

## 📚 Documentation

**New to this?** → [Getting Started Guide](./docs/getting-started.md)

**Want examples?** → [Simple Examples](./docs/simple-examples.md)

**Something broken?** → [Troubleshooting](./docs/troubleshooting.md)

**Need more details?** → [Full Documentation](./docs/)

**Continuing work?** → [Project Log](./docs/project-log.md) (development history)

## 🎯 Requirements

- **Computer:** Mac, Windows, or Linux
- **RAM:** 8GB+ (4GB for smaller AI model)
- **Python:** 3.8 or higher
- **Time:** 10 minutes to get running

## 🆘 Quick Help

**Not working?** Run this:
```bash
python test_setup.py
```

It will tell you exactly what to fix.

**Common issues:**
- "ollama not found" → Install Ollama from [ollama.com](https://ollama.com)
- "model not found" → Run `ollama pull llama3.2:3b`
- "connection refused" → Run `ollama serve`

## 🎊 Example Conversation

Here's what you'll see with the demo:

```
🗣️ Alex: Hey! Just got back from rock climbing in Golden Gate Park. 
The view from the top was worth the bruises on my ego!

💭 Sam: Yaaas! I'm super jealous. I've been working on this mural 
for a coffee shop - it's all about spreading positivity vibes, 
you know? I'm really feeling it!

🗣️ Alex: That sounds amazing! What's the concept behind your mural?

💭 Sam: It's about inner strength and how it manifests in daily life. 
I want people to take a moment for themselves and embrace their 
inner peace...
```

Alex (tech-savvy rock climber) and Sam (creative artist) stay perfectly in character throughout the entire conversation!

## 🔮 What's Next

This Week 1 MVP is the foundation for:
- **Week 2:** Better memory with FAISS vector search
- **Week 3-4:** Import real chat data (WhatsApp, Discord)
- **Month 2:** Web interface and matchmaking integration
- **Month 3+:** Voice chat and mobile apps

---

**Ready to create your first AI clone?** Start with the [Getting Started Guide](./docs/getting-started.md)! 🚀
