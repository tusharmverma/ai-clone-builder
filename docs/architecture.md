# 🏗️ Technical Architecture

## System Overview

ai-clone-builder is built with a modular, extensible architecture designed for rapid iteration and easy scaling.

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACES                          │
├─────────────────────────────────────────────────────────────┤
│  CLI Interface  │  Quick Start  │  Test Scripts  │  Future  │
│   (rich UI)     │   (demos)     │  (diagnostics) │   (web)  │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                   CORE SYSTEMS                              │
├─────────────────────────────────────────────────────────────┤
│           │              │                │                 │
│ Personality│  AI Clone    │ Conversation  │    Memory       │
│  System    │   Engine     │   Manager     │   System        │
│           │              │                │                 │
│ ┌─────────┐│ ┌──────────┐ │ ┌────────────┐│ ┌─────────────┐ │
│ │Question-││ │AIClone   │ │ │CloneConvo  ││ │SimpleMemory │ │
│ │naire    ││ │Class     │ │ │System      ││ │& ConvoMgr   │ │
│ │         ││ │          │ │ │            ││ │             │ │
│ │Template ││ │Personality│ │ │Scenarios   ││ │JSON Storage │ │
│ │Engine   ││ │Prompts   │ │ │Turn Logic  ││ │Context Mgmt │ │
│ └─────────┘│ └──────────┘ │ └────────────┘│ └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                 EXTERNAL SYSTEMS                            │
├─────────────────────────────────────────────────────────────┤
│                              │                              │
│        Ollama + LLaMA        │       File System           │
│                              │                              │
│ ┌──────────────────────────┐ │ ┌──────────────────────────┐ │
│ │                          │ │ │                          │ │
│ │  LLaMA 3.2:3b Model      │ │ │  data/personalities/     │ │
│ │  Local HTTP API          │ │ │  data/conversations/     │ │
│ │  Text Generation         │ │ │  JSON Configuration      │ │
│ │                          │ │ │                          │ │
│ └──────────────────────────┘ │ └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🧩 Core Components

### 1. Personality System (`src/personality/`)

**Purpose**: Convert human personality traits into AI prompts

**Components**:
- `questionnaire.py` - Interactive personality collection
- `templates.py` - Prompt generation from personality data

**Data Flow**:
```
User Input → Questionnaire → Personality JSON → System Prompt
```

**Key Classes**:
```python
PersonalityQuestionnaire
├── run_questionnaire() -> Dict[personality_data]
├── save_personality() -> str[filename]
└── load_personality() -> Dict[personality_data]

PersonalityTemplate
├── create_system_prompt() -> str[prompt]
├── _build_communication_style() -> str
├── _build_personality_description() -> str
└── _build_interests_description() -> str
```

### 2. AI Clone Engine (`src/ai_clone/`)

**Purpose**: Create and manage individual AI personalities

**Components**:
- `clone.py` - Main AIClone class with Ollama integration
- `conversation.py` - Clone-to-clone conversation management

**Data Flow**:
```
Personality Data → AIClone → Ollama API → Response → Memory Update
```

**Key Classes**:
```python
AIClone
├── __init__(personality_data) -> Sets up system prompt
├── respond(message, context) -> str[ai_response]
├── add_to_conversation_history() -> Updates memory
├── get_recent_history() -> List[messages]
└── save_conversation() -> str[filename]

CloneConversation
├── start_conversation(scenario) -> str[conv_id]
├── run_conversation() -> List[conversation_history]
├── _display_message() -> Rich UI output
└── _should_end_conversation() -> bool
```

### 3. Memory System (`src/memory/`)

**Purpose**: Handle conversation history and context

**Components**:
- `simple_memory.py` - JSON-based memory and conversation management

**Data Flow**:
```
Messages → SimpleMemory → JSON Files → Context Retrieval
```

**Key Classes**:
```python
SimpleMemory
├── add_message(speaker, content) -> Stores message
├── get_recent_messages(count) -> List[messages]
├── search_messages(query) -> List[matching_messages]
└── save_memory() -> JSON file

ConversationManager  
├── start_conversation() -> str[conv_id]
├── add_message_to_conversation() -> Updates conversation
├── end_conversation() -> Archives conversation
└── save_conversation_log() -> JSON file
```

### 4. Interface System (`src/interface/`)

**Purpose**: User interaction and system control

**Components**:
- `cli.py` - Full-featured command-line interface

**Data Flow**:
```
User Input → CLI Menu → Core Systems → Rich UI Output
```

**Key Classes**:
```python
AICloneCLI
├── show_main_menu() -> Rich table display
├── create_new_clone() -> Questionnaire workflow
├── chat_with_clone() -> Interactive chat
├── clone_to_clone_conversation() -> Conversation setup
└── run() -> Main application loop
```

## 🔄 Data Flow Diagrams

### Personality Creation Flow
```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│    User     │───▶│Questionnaire │───▶│Personality  │
│   Input     │    │   System     │    │    JSON     │
└─────────────┘    └──────────────┘    └─────────────┘
                                              │
                                              ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│ AI Clone    │◀───│   Template   │◀───│ System      │
│   Ready     │    │   Engine     │    │  Prompt     │
└─────────────┘    └──────────────┘    └─────────────┘
```

### Conversation Flow
```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Message   │───▶│  AI Clone    │───▶│  Ollama     │
│   Input     │    │  + Context   │    │    API      │
└─────────────┘    └──────────────┘    └─────────────┘
                                              │
                                              ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Memory    │◀───│  Response    │◀───│   LLaMA     │
│  Storage    │    │ Processing   │    │  Response   │
└─────────────┘    └──────────────┘    └─────────────┘
```

### Clone-to-Clone Conversation
```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Clone A   │───▶│Conversation  │───▶│   Clone B   │
│  (Speaker)  │    │   Manager    │    │ (Listener)  │
└─────────────┘    └──────────────┘    └─────────────┘
       ▲                   │                   │
       │                   ▼                   ▼
       │            ┌──────────────┐    ┌─────────────┐
       │            │   Message    │    │   Message   │
       │            │   Storage    │    │ Processing  │
       │            └──────────────┘    └─────────────┘
       │                   │                   │
       │                   ▼                   ▼
       └──────────────────────────────── Response
```

## 🗄️ Data Structures

### Personality Data Schema
```json
{
  "clone_name": "string",
  "basic_info": {
    "name": "string",
    "age": "string", 
    "location": "string",
    "occupation": "string"
  },
  "communication_style": {
    "formality": {"choice": "string", "index": "number"},
    "humor": {"choice": "string", "index": "number"},
    "expressiveness": {"choice": "string", "index": "number"},
    "response_length": {"choice": "string", "index": "number"}
  },
  "personality_traits": {
    "extroversion": {"choice": "string", "index": "number"},
    "openness": {"choice": "string", "index": "number"}, 
    "emotional_style": {"choice": "string", "index": "number"},
    "decision_making": {"choice": "string", "index": "number"}
  },
  "interests": {
    "hobbies": "string",
    "topics": "string", 
    "values": "string",
    "conversation_starters": "string"
  }
}
```

### Conversation History Schema
```json
{
  "id": "string",
  "participants": ["string", "string"],
  "scenario": "string",
  "started_at": "ISO_timestamp",
  "ended_at": "ISO_timestamp", 
  "status": "active|ended",
  "messages": [
    {
      "timestamp": "ISO_timestamp",
      "speaker": "string",
      "content": "string"
    }
  ]
}
```

## ⚙️ Configuration & Settings

### Ollama Configuration
```python
OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "llama3.2:3b"
GENERATION_PARAMS = {
    "temperature": 0.7,
    "top_p": 0.9, 
    "max_tokens": 150
}
```

### File System Layout
```
data/
├── personalities/          # Personality JSON files
│   ├── {name}_personality.json
│   └── .gitkeep
└── conversations/          # Conversation logs
    ├── {clone1}_{clone2}_{timestamp}.json
    ├── conversation_{id}.json
    └── .gitkeep
```

### Error Handling Strategy

**Connection Errors**:
- Ollama connection testing on startup
- Graceful degradation with helpful error messages
- Setup guidance for common issues

**Data Errors**:
- JSON validation for personality files
- Backup conversation data on errors
- Recovery mechanisms for corrupted data

**User Input Errors**:
- Input validation with retry prompts
- Clear error messages with suggested fixes
- Graceful handling of interrupts (Ctrl+C)

## 🔌 Extension Points

### Adding New Memory Systems
```python
# Implement this interface
class MemoryInterface:
    def add_message(self, speaker: str, content: str) -> None
    def get_recent_messages(self, count: int) -> List[Dict]
    def search_messages(self, query: str) -> List[Dict]
```

### Adding New AI Models
```python
# Implement this interface  
class AIModelInterface:
    def respond(self, prompt: str, context: List[Dict]) -> str
    def test_connection(self) -> bool
```

### Adding New Interfaces
```python
# Implement this interface
class InterfaceInterface:
    def show_menu(self) -> None
    def handle_input(self, choice: str) -> None
    def display_response(self, message: str) -> None
```

## 🚀 Performance Considerations

### Memory Usage
- **Personality data**: ~5-50KB per clone
- **Conversation history**: ~1-5KB per message
- **Model memory**: ~4GB for LLaMA 3.2:3b
- **Application memory**: ~50-100MB

### Response Times
- **Cold start**: 5-10 seconds (model loading)
- **Warm responses**: 2-5 seconds per message
- **Context processing**: <1 second
- **File I/O**: <100ms

### Scalability Limits (Current)
- **Concurrent clones**: 2-5 (memory limited)
- **Conversation history**: 1000+ messages per clone
- **Personality files**: 100+ clones
- **Storage growth**: ~1MB per 1000 messages

---

**Next**: Check out the [Setup Guide](./setup-guide.md) for installation instructions! 