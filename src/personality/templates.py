"""
Personality Templates
Converts questionnaire data into AI personality prompts
"""

from typing import Dict, Any

class PersonalityTemplate:
    """Converts personality data into AI prompts"""
    
    @staticmethod
    def create_system_prompt(personality_data: Dict[str, Any]) -> str:
        """Create a system prompt from personality data"""
        basic = personality_data["basic_info"]
        comm = personality_data["communication_style"]
        traits = personality_data["personality_traits"]
        interests = personality_data["interests"]
        
        # Build communication style description
        comm_style = PersonalityTemplate._build_communication_style(comm)
        
        # Build personality traits description
        personality_desc = PersonalityTemplate._build_personality_description(traits)
        
        # Build interests description
        interests_desc = PersonalityTemplate._build_interests_description(interests)
        
        system_prompt = f"""You are {basic['name']}, a {basic['age']}-year-old from {basic['location']} who works as {basic['occupation']}.

PERSONALITY CORE:
{personality_desc}

COMMUNICATION STYLE:
{comm_style}

INTERESTS & TOPICS:
{interests_desc}

CONVERSATION GUIDELINES:
- Always stay in character as {basic['name']}
- Be consistent with your personality traits and communication style
- Reference your interests and background naturally
- Remember previous parts of conversations
- Respond as a real person would, not as an AI
- Keep responses natural and human-like
- Don't break character or mention being an AI

Remember: You ARE {basic['name']}. This is your personality, your life, your way of speaking."""

        return system_prompt
    
    @staticmethod
    def _build_communication_style(comm: Dict[str, Any]) -> str:
        """Build communication style description"""
        style_parts = []
        
        # Formality
        formality = comm.get("formality", {}).get("choice", "Neutral")
        if "Very casual" in formality:
            style_parts.append("- Use very casual language (hey, sup, lol, short responses)")
        elif "Casual" in formality:
            style_parts.append("- Use casual, friendly language")
        elif "formal" in formality.lower():
            style_parts.append("- Use more formal, polite language")
        
        # Humor
        humor = comm.get("humor", {}).get("choice", "")
        if humor:
            style_parts.append(f"- Incorporate {humor.lower()} into conversations")
        
        # Expressiveness
        express = comm.get("expressiveness", {}).get("choice", "")
        if "reserved" in express.lower():
            style_parts.append("- Be more reserved and measured in responses")
        elif "expressive" in express.lower():
            style_parts.append("- Be expressive and enthusiastic in responses")
        
        # Response length
        length = comm.get("response_length", {}).get("choice", "")
        if "short" in length.lower():
            style_parts.append("- Keep responses concise and to the point")
        elif "detailed" in length.lower():
            style_parts.append("- Provide detailed, thoughtful responses")
        
        return "\n".join(style_parts) if style_parts else "- Use natural, authentic communication"
    
    @staticmethod
    def _build_personality_description(traits: Dict[str, Any]) -> str:
        """Build personality traits description"""
        trait_parts = []
        
        # Extroversion
        extro = traits.get("extroversion", {}).get("choice", "")
        if "introverted" in extro.lower():
            trait_parts.append("- You're more introverted - prefer meaningful conversations over small talk")
        elif "extroverted" in extro.lower():
            trait_parts.append("- You're extroverted - enjoy meeting new people and socializing")
        
        # Openness
        openness = traits.get("openness", {}).get("choice", "")
        if "cautious" in openness.lower():
            trait_parts.append("- You're cautious about new experiences - prefer familiar things")
        elif "adventurous" in openness.lower():
            trait_parts.append("- You're adventurous and love trying new experiences")
        
        # Emotional style
        emotional = traits.get("emotional_style", {}).get("choice", "")
        if "reserved" in emotional.lower():
            trait_parts.append("- You express emotions subtly and thoughtfully")
        elif "expressive" in emotional.lower():
            trait_parts.append("- You express emotions openly and directly")
        
        # Decision making
        decision = traits.get("decision_making", {}).get("choice", "")
        if "logical" in decision.lower():
            trait_parts.append("- You make decisions based on logic and facts")
        elif "intuitive" in decision.lower():
            trait_parts.append("- You trust your gut and make intuitive decisions")
        
        return "\n".join(trait_parts) if trait_parts else "- You have a balanced, authentic personality"
    
    @staticmethod
    def _build_interests_description(interests: Dict[str, Any]) -> str:
        """Build interests and values description"""
        parts = []
        
        hobbies = interests.get("hobbies", "")
        if hobbies:
            parts.append(f"- Your hobbies include: {hobbies}")
        
        topics = interests.get("topics", "")
        if topics:
            parts.append(f"- You love talking about: {topics}")
        
        values = interests.get("values", "")
        if values:
            parts.append(f"- What matters most to you in relationships: {values}")
        
        starters = interests.get("conversation_starters", "")
        if starters:
            parts.append(f"- Your conversation style: {starters}")
        
        return "\n".join(parts) if parts else "- You have diverse interests and enjoy good conversation"
    
    @staticmethod
    def create_conversation_context(personality_data: Dict[str, Any], recent_history: list = None) -> str:
        """Create conversation context for ongoing chats"""
        name = personality_data["basic_info"]["name"]
        
        context = f"You are continuing a conversation as {name}. "
        
        if recent_history:
            context += "Recent conversation history:\n"
            for msg in recent_history[-5:]:  # Last 5 messages
                speaker = msg.get("speaker", "Unknown")
                content = msg.get("content", "")
                context += f"{speaker}: {content}\n"
        
        context += f"\nRespond as {name} would, staying consistent with your personality."
        
        return context

def create_demo_personalities():
    """Create some demo personalities for testing"""
    demo_personalities = [
        {
            "clone_name": "Alex",
            "basic_info": {
                "name": "Alex",
                "age": "25",
                "location": "San Francisco",
                "occupation": "Software Developer"
            },
            "communication_style": {
                "formality": {"choice": "Casual (hi, cool, nice)", "index": 1},
                "humor": {"choice": "Sarcastic/witty", "index": 0},
                "expressiveness": {"choice": "Quite expressive", "index": 3},
                "response_length": {"choice": "Medium", "index": 2}
            },
            "personality_traits": {
                "extroversion": {"choice": "Somewhat extroverted", "index": 3},
                "openness": {"choice": "Quite adventurous", "index": 3},
                "emotional_style": {"choice": "Direct but calm", "index": 2},
                "decision_making": {"choice": "Mostly logical", "index": 1}
            },
            "interests": {
                "hobbies": "coding, rock climbing, photography, coffee",
                "topics": "technology, startups, travel, food",
                "values": "honesty, adventure, personal growth",
                "conversation_starters": "I usually ask about their projects or travels"
            }
        },
        {
            "clone_name": "Sam",
            "basic_info": {
                "name": "Sam",
                "age": "28",
                "location": "Austin",
                "occupation": "Artist & Designer"
            },
            "communication_style": {
                "formality": {"choice": "Very casual (hey, sup, lol)", "index": 0},
                "humor": {"choice": "Playful/silly", "index": 1},
                "expressiveness": {"choice": "Very expressive", "index": 4},
                "response_length": {"choice": "Detailed", "index": 3}
            },
            "personality_traits": {
                "extroversion": {"choice": "Balanced", "index": 2},
                "openness": {"choice": "Very adventurous", "index": 4},
                "emotional_style": {"choice": "Openly emotional", "index": 3},
                "decision_making": {"choice": "Very intuitive", "index": 4}
            },
            "interests": {
                "hobbies": "painting, music festivals, yoga, vintage shopping",
                "topics": "art, music, spirituality, social causes",
                "values": "creativity, authenticity, connection",
                "conversation_starters": "I love asking about their creative side or what inspires them"
            }
        }
    ]
    
    return demo_personalities 