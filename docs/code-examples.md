# What You Can Do

Simple examples of how to use your AI Clone Builder

## Basic Things You Can Do

### 1. Create AI Clones

<!-- Examples of core functionality -->
- Build unique personalities through questionnaires
- Answer questions about interests, communication style, background
- Each clone gets their own personality file and memory system

### 2. **Chat with Clones**
- Have natural conversations with your clones
- Clones remember what you talked about
- They stay in character based on their personality

### 3. **Watch Clones Chat**
- Two clones can talk to each other
- Built-in scenarios like coffee shop, restaurant, etc.
- Automatic logging of all conversations

## Memory System Examples

### **SQLite Vector Memory** (The Smart One)
- **What it does**: Remembers conversations by meaning, not just words
- **Example**: If you talk about "rock climbing," it remembers conversations about outdoor activities, adventure, etc.
- **Best for**: Everyday use, serious conversations

### **Enhanced Memory** (The Middle Option)
- **What it does**: Stores conversations with extra details like timestamps and metadata
- **Example**: You can search for conversations by topic, date, or other details
- **Best for**: Testing, development, when you need more control

### **Simple Memory** (The Basic One)
- **What it does**: Just saves conversations as simple text
- **Example**: Basic conversation history without fancy features
- **Best for**: Quick testing, simple use cases

## Personality Creation Examples

### **Using the Questionnaire**
1. **Start the questionnaire**: Run the personality creator
2. **Answer questions**: About interests, communication style, background
3. **Save personality**: Your clone gets a unique personality file
4. **Use your clone**: Start chatting with your new AI personality

### **Pre-built Templates**
- **Alex**: Tech-savvy rock climber who loves outdoor activities
- **Sam**: Creative artist who spreads positivity through art

## Conversation Examples

### **One-on-One Chat**
```
You: Hey Alex! What's your favorite weekend activity?

Alex: Hey! I'm usually either out on a climbing route somewhere in the Bay Area or 
messing around with a new coding project. Last weekend I was working on this photo 
organization app while my coffee got cold, which is pretty typical for me lol. 
What about you?
```

### **Clone-to-Clone Conversation**
```
Alex: Just got back from rock climbing! The view was amazing.

Sam: That sounds incredible! I've been working on this mural for a coffee shop - 
it's all about spreading positivity vibes, you know? I'm really feeling it!

Alex: That sounds amazing! What's the concept behind your mural?
```

## Memory Search Examples

### **Finding Related Conversations**
```
# Search for conversations about outdoor activities
memory.find_similar("I love hiking and camping")

# Returns: Previous conversations about rock climbing, nature, adventure
```

### **Context-Aware Responses**
```
# Clone remembers you mentioned rock climbing last week
You: What should I do this weekend?

Alex: Since you mentioned loving rock climbing last time we talked, 
you should check out Castle Rock! The views are insane and it's 
got that perfect mix of challenge and accessibility.
```

## Testing Examples

### **Run System Tests**
```bash
# Test everything works
python run_tests.py

# Test specific components
python tests/test_setup.py
python tests/test_sqlite_vec_integration.py
```

### **Test Memory Systems**
```bash
# Test different memory types
python tests/test_intelligent_memory.py
python tests/test_performance_scaling.py
```

## Integration Examples

### **Custom Personality Creation**
```python
from src.personality.questionnaire import QuestionnaireManager

# Create custom personality
manager = QuestionnaireManager()
personality = manager.create_personality("CustomClone")

# Save to file
import json
with open("custom_personality.json", "w") as f:
    json.dump(personality, f, indent=2)
```

### **Clone Management**
```python
from src.ai_clone.clone import AIClone

# Load personality and create clone
with open("alex_personality.json") as f:
    personality = json.load(f)

clone = AIClone(personality)
response = clone.respond("Hello! Tell me about yourself.")
```

## What Makes This Special

**Real Personalities**: Not just random responses - each clone has consistent traits, interests, and communication style.

**Smart Memory**: Clones remember what you talked about and reference previous conversations naturally.

**Local & Private**: Everything runs on your computer. No data sent to the cloud.

**Easy to Use**: Simple questionnaire creates complex personalities in minutes.

**Extensible**: Add new personality types, memory systems, or conversation scenarios. 