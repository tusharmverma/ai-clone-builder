# 🎮 User Guide

Complete guide to using ai-clone-builder AI clone system.

## 🚀 Getting Started

### First Time Setup
1. **Complete installation**: Follow [Setup Guide](./setup-guide.md)
2. **Run system test**: `python test_setup.py`
3. **Try quick demo**: `python quick_start.py` → option 1

### Launch the Application
```bash
# Full CLI interface
python -m src.interface.cli

# Quick start wizard  
python quick_start.py

# Individual components
python -m src.personality.questionnaire
```

## 🧠 Creating Your First AI Clone

### Method 1: Interactive Questionnaire (Recommended)

**Launch the questionnaire:**
```bash
python -m src.interface.cli
# Choose option 1: "Create New AI Clone"
```

**The Process:**
```
🧠 AI Clone Personality Questionnaire
Creating personality for: YourClone
This will take about 5-10 minutes.

📋 Basic Information
├── Name: What's your name?
├── Age: What's your age? 
├── Location: Where are you from?
└── Occupation: What do you do for work/study?

💬 Communication Style  
├── Formality: Casual vs formal conversation?
├── Humor: Sarcastic, playful, dry, etc.
├── Expressiveness: Reserved vs expressive?
└── Response Length: Short vs detailed responses?

🧠 Personality Traits
├── Extroversion: Social vs alone time energy?
├── Openness: Cautious vs adventurous?
├── Emotional Style: How you express emotions?
└── Decision Making: Logical vs intuitive?

🎯 Interests & Values
├── Hobbies: Main interests (comma separated)
├── Topics: Love talking about (comma separated)
├── Values: Important in relationships?
└── Conversation Starters: How you meet people?
```

**Tips for Better Results:**
- **Be specific**: "hiking, photography, coffee" vs "outdoor stuff"
- **Be honest**: The AI works best with authentic personalities
- **Think examples**: How would you actually respond?
- **Consider context**: Dating/social scenarios specifically

### Method 2: Quick Demo Clones

**Use pre-built personalities:**
```bash
python quick_start.py
# Choose option 1 for instant demo with Alex & Sam
```

**Demo Personalities:**
- **Alex**: 25, SF, Developer - Casual, witty, tech-focused
- **Sam**: 28, Austin, Artist - Very casual, creative, expressive

## 💬 Chatting with AI Clones

### One-on-One Chat

**Start a conversation:**
```bash
python -m src.interface.cli
# Choose option 4: "Chat with Clone"
```

**Sample Conversation:**
```
💬 Chatting with Alex
Type 'quit' to end the conversation

You: Hey! What do you like to do on weekends?

Alex: Hey! I'm usually either out on a climbing route somewhere in the Bay Area or 
messing around with a new coding project. Last weekend I was working on this photo 
organization app while my coffee got cold, which is pretty typical for me lol. 
What about you?

You: I love hiking too! Any favorite spots?

Alex: Nice! Yeah, I'm obsessed with the trails around Mount Tam - the views are 
insane and it's got that perfect mix of challenge and accessibility. Castle Rock 
is another go-to if I want something closer to the city. Have you done much 
hiking around here?
```

**Chat Features:**
- **Memory**: Remembers previous messages in conversation
- **Personality**: Consistent style and interests
- **Context**: References earlier topics naturally
- **Natural Flow**: Realistic conversation patterns

### Conversation Commands
```
quit / exit / bye  → End conversation
help              → Show available commands  
history           → Show recent messages
save              → Save conversation to file
```

## 🗨️ Clone-to-Clone Conversations

### Setting Up Clone Conversations

**Basic Setup:**
```bash
python -m src.interface.cli
# Choose option 5: "Clone-to-Clone Conversation"
```

**Advanced Setup:**
```
Available clones:
  1. Alex
  2. Sam

Choose first clone: 1
Choose second clone: 2

Want to set a custom scenario? [y/N]: y
Enter scenario: You're both at a weekend farmer's market

How many turns? [8]: 10

🗨️ Starting Conversation
Participants: Alex & Sam  
Scenario: You're both at a weekend farmer's market
```

### Built-in Scenarios

**Dating Scenarios:**
- Coffee shop first meeting
- Restaurant first date  
- Mutual friend's party
- Airport delayed flight
- Bookstore browsing
- Food truck line

**Custom Scenarios:**
- Weekend farmer's market
- Art gallery opening
- Tech meetup networking
- Hiking trail encounter
- Music festival
- Beach volleyball game

### Example Clone Conversation
```
🗣️ Alex:
Hey, have you tried those honey lavender pastries? They smell incredible.

💭 Sam:
Omg yes! I was just eyeing those - the vendor said they're made with local honey from 
Sonoma. I'm such a sucker for anything lavender, it's like edible aromatherapy you know?

🗣️ Alex:
Haha exactly! I'm usually more of a coffee and basic croissant person, but these 
farmers markets always make me want to try new things. Are you here every week?

💭 Sam:
Pretty much! I love the energy here, plus I've been getting obsessed with sourcing 
ingredients for this painting series I'm working on - sounds weird but different 
foods inspire different color palettes for me.

🗣️ Alex:
That's actually really cool! I never thought about food as color inspiration. 
What kind of paintings are you working on?
```

**Conversation Features:**
- **Realistic turn-taking**: Natural back-and-forth
- **Personality consistency**: Each clone stays in character
- **Scenario awareness**: Responses fit the setting
- **Natural endings**: Conversations end organically
- **Auto-save**: All conversations logged automatically

## 💾 Managing Your Clones

### Viewing Clones

**List all clones:**
```bash
python -m src.interface.cli
# Choose option 3: "List All Clones"
```

**Output:**
```
📋 Clone Status

🟢 Active Clones
Name    Summary
Alex    Alex, 25, from San Francisco. Style: Casual, Sarcastic/witty. Interests: coding, rock climbing, photography...
Sam     Sam, 28, from Austin. Style: Very casual, Playful/silly. Interests: painting, music festivals, yoga...

💾 Available personalities: 5 files  
  • alex_personality.json
  • sam_personality.json
  • taylor_personality.json
  • jordan_personality.json
  • riley_personality.json
```

### Loading Existing Clones

**Load from file:**
```bash
python -m src.interface.cli
# Choose option 2: "Load Existing Clone"
```

**File locations:**
```
data/personalities/
├── alex_personality.json     ← Your saved personalities
├── sam_personality.json
└── custom_clone_personality.json
```

### Conversation History

**Automatic saving:**
- Individual chats: `data/conversations/{clone_name}_{timestamp}.json`
- Clone conversations: `data/conversations/conversation_{id}.json`

**View conversation files:**
```bash
ls data/conversations/
# Alex_20231201_143022.json
# conversation_Alex_Sam_20231201_150045.json  
# Sam_20231201_160012.json
```

## 🎯 Tips for Better Conversations

### Creating Realistic Personalities

**Be Specific:**
```
❌ "I like music"
✅ "indie rock, Taylor Swift, Bon Iver, going to small venue concerts"

❌ "I'm funny"  
✅ "Sarcastic wit, dad jokes, self-deprecating humor"

❌ "I like food"
✅ "coffee obsessed, tries new restaurants, loves Italian food, terrible at cooking"
```

**Think in Examples:**
- How would you respond to "What did you do this weekend?"
- What topics do you bring up when meeting someone?
- How do you text vs. talk in person?
- What makes you excited or passionate?

### Conversation Starters

**Good prompts for testing:**
```
"What do you like to do for fun?"
"Tell me about your work"  
"What are you passionate about?"
"Where's your favorite place you've traveled?"
"What's been the highlight of your week?"
"If you could have dinner with anyone, who would it be?"
```

**Dating-specific prompts:**
```
"What's your ideal first date?"
"What are you looking for in a relationship?"
"What's a deal breaker for you?"
"Tell me something that would surprise me about you"
"What's your love language?"
```

### Clone Conversation Ideas

**Personality contrasts:**
- Extrovert + Introvert
- Logical + Creative  
- Adventurous + Cautious
- Formal + Casual

**Interest overlaps:**
- Both love travel (different styles)
- Similar hobbies (different skill levels)
- Complementary interests (art + tech)
- Shared values (different expressions)

## 🔧 Advanced Features

### Personality Editing

**Manual editing:**
```bash
# Edit personality files directly
vim data/personalities/alex_personality.json

# Key sections to modify:
{
  "interests": {
    "hobbies": "Add new hobbies here",
    "topics": "Add conversation topics",
    "values": "Relationship values"
  }
}
```

**Personality refinement:**
1. Run conversations
2. Note responses that feel off
3. Adjust relevant personality sections
4. Test again

### Conversation Analysis

**What to look for:**
- **Consistency**: Does the clone stay in character?
- **Naturalness**: Do responses flow well?
- **Personality**: Can you tell the clones apart?
- **Engagement**: Are conversations interesting?

**Common issues:**
- Generic responses → Add more specific interests
- Out-of-character → Refine personality traits
- Repetitive → Expand conversation topics
- Inconsistent → Check communication style settings

### System Customization

**Model settings** (edit `src/ai_clone/clone.py`):
```python
# Response generation parameters
"temperature": 0.7,  # Higher = more creative
"top_p": 0.9,        # Higher = more diverse
"max_tokens": 150    # Response length limit
```

**Conversation settings** (edit `src/ai_clone/conversation.py`):
```python
delay=2.0           # Pause between responses  
max_turns=10        # Conversation length
```

## 🚨 Troubleshooting

### Common Issues

**Clone not responding:**
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve
```

**Personality not saving:**
```bash
# Check directory permissions
ls -la data/personalities/

# Create directory if missing
mkdir -p data/personalities
```

**Conversations feel generic:**
- Add more specific personality details
- Use more varied conversation topics
- Try different personality combinations

**Response too slow:**
- Use smaller model (`llama3.2:1b`)
- Reduce max_tokens
- Close other applications

### Getting Help

**System diagnostics:**
```bash
python test_setup.py
```

**Check logs:**
```bash
# Enable debugging (add to clone.py)
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Reset everything:**
```bash
# Clear all data (careful!)
rm -rf data/personalities/* data/conversations/*
```

## 🔮 What's Next?

### Week 2+ Features
- **FAISS vector memory**: Better conversation context
- **Chat import**: Use real WhatsApp/Discord data  
- **Voice chat**: Talk to clones with speech
- **Web interface**: Browser-based access
- **Matchmaking**: AI compatibility scoring

### Experiment Ideas
- Create clones of historical figures
- Build family member personalities
- Design ideal partner personality
- Test personality compatibility
- Create conversation scenarios for specific situations

---

**Ready to create amazing AI conversations?** Start with `python quick_start.py` and let your creativity flow! 🚀

**Need help?** Check the [API Reference](./api-reference.md) or [Developer Guide](./developer-guide.md). 