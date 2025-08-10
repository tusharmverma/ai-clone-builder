# Simple Examples

**See what AI clones can actually do with real examples.**

## Demo Conversation

**Run this to see two AI clones chat:**

Use the quick start script and choose option 1.

**What you'll see:**
```
Alex: Hey! Just got back from rock climbing in Golden Gate Park. 
The view from the top was worth the bruises on my ego!

Sam: Yaaas! I'm super jealous. I've been working on this mural 
for a coffee shop - it's all about spreading positivity vibes, 
you know? I'm really feeling it!

Alex: That sounds amazing! What's the concept behind your mural?

Sam: It's about inner strength and how it manifests in daily life. 
I want people to take a moment for themselves and embrace their 
inner peace...
```

**Alex** (tech-savvy rock climber) and **Sam** (creative artist) stay perfectly in character!

## Create Your Own Clone

**Step 1: Start the questionnaire**
- Use the main interface and choose option 1: Create New AI Clone

**Step 2: Answer questions (5-10 minutes)**
- What's your name? → **Alex**
- How old are you? → **28**
- Where do you live? → **San Francisco**
- What do you do? → **Software Engineer**
- What's your energy level? → **High energy, always moving**
- How do you communicate? → **Casual, uses emojis, short responses**

**Step 3: Test your clone**
- Choose option 4: Chat with Clone
- Select Alex and start chatting!

## Clone-to-Clone Conversations

**Create two clones and watch them chat:**

1. **Create first clone**
   - Use the main interface and choose option 1
   - Create "Alex"

2. **Create second clone**  
   - Use the main interface and choose option 1
   - Create "Sam"

3. **Start conversation**
   - Use the main interface and choose option 5: Clone-to-Clone Conversation
   - Select Alex and Sam

**Built-in scenarios:**
- Coffee shop meetup
- Restaurant dinner
- Park walk
- Museum visit

## Memory Examples

**Three memory types with different behaviors:**

### SQLite Vector Memory
- Understands meaning of conversations
- Finds related topics automatically
- Best for serious conversations

### Enhanced Memory  
- Remembers recent messages plus relevant past ones
- Better context and understanding
- Good for everyday use

### Simple Memory
- Remembers last 10 messages
- Basic but reliable storage
- Good for quick testing

## Real Use Cases

### Dating App Testing
- Create clones with different personalities
- Test conversation flows
- See how different traits interact

### Customer Service Training
- Create customer personality clones
- Train staff on different customer types
- Test response strategies

### Social Experiments
- Watch how different ages communicate
- Test conversation styles
- Understand personality dynamics

## Quick Commands

**Basic Operations:**
```bash
# Run demo
python quick_start.py

# Test setup
python tests/test_setup.py

# Run all tests
python run_tests.py

# Full interface
python -m src.interface.cli
```

**Memory Testing:**
```bash
# Test specific memory type
python tests/test_sqlite_vec_integration.py
python tests/test_intelligent_memory.py
```

## What Makes This Special

**Real Personalities**: Not just random responses - each clone has consistent traits, interests, and communication style.

**Smart Memory**: Clones remember what you talked about and reference previous conversations naturally.

**Local & Private**: Everything runs on your computer. No data sent to the cloud.

**Easy to Use**: Simple questionnaire creates complex personalities in minutes.

**Extensible**: Add new personality types, memory systems, or conversation scenarios. 