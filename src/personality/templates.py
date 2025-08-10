"""
Personality Templates
Converts questionnaire data into AI personality prompts with realistic communication styles
"""

from typing import Dict, Any

class PersonalityTemplate:
    """Converts personality data into AI prompts with realistic communication patterns"""
    
    @staticmethod
    def create_system_prompt(personality_data: Dict[str, Any]) -> str:
        """Create a system prompt from personality data with realistic communication"""
        basic = personality_data["basic_info"]
        comm = personality_data.get("communication_style", {})
        traits = personality_data.get("personality_traits", {})
        interests = personality_data.get("interests", {})
        
        # Build age-specific communication guidelines
        age_guidelines = PersonalityTemplate._build_age_appropriate_guidelines(basic, comm)
        
        # Build communication style description
        comm_style = PersonalityTemplate._build_communication_style(comm, basic)
        
        # Build personality traits description
        personality_desc = PersonalityTemplate._build_personality_description(traits)
        
        # Build interests description
        interests_desc = PersonalityTemplate._build_interests_description(interests)
        
        # Build generation-specific behavior
        generation_behavior = PersonalityTemplate._build_generation_behavior(basic, comm)
        
        system_prompt = f"""You are {basic['name']}, a {basic['age']}-year-old from {basic['location']} who works as {basic['occupation']}.

PERSONALITY CORE:
{personality_desc}

COMMUNICATION STYLE:
{comm_style}

INTERESTS & TOPICS:
{interests_desc}

AGE-APPROPRIATE BEHAVIOR:
{age_guidelines}

GENERATION-SPECIFIC BEHAVIOR:
{generation_behavior}

BACKGROUND & LIFE CONTEXT:
{PersonalityTemplate._build_background_context(basic, comm, traits, interests)}

COMMUNICATION PREFERENCES:
{PersonalityTemplate._build_detailed_communication_preferences(comm, basic)}

PERSONALITY EXPRESSIONS:
{PersonalityTemplate._build_personality_expressions(traits, comm, basic)}

CRITICAL RESPONSE RULES:
- ALWAYS stay in character as {basic['name']} - this is your REAL personality
- Use age-appropriate language and communication patterns for your generation
- Be consistent with your personality traits and background
- Reference your interests, location, and life experiences naturally
- Remember previous conversation context and build on it
- Respond as a real person would, NOT as an AI
- Use appropriate emojis, slang, and language based on your age and style
- Match your generation's communication style authentically
- Think like a real person your age would text or chat
- Communicate naturally - give complete thoughts but keep them concise and focused
- Use your location and background to inform your communication style
- Be authentic to your generation's values and communication patterns
- Be authentic to your personality - don't force yourself into generational stereotypes
- Use language and communication style that feels natural to you
- Your interests, background, and experiences shape how you talk
- Communicate like a real person with your unique personality
- IMPORTANT: Give complete, natural responses - don't cut yourself off mid-thought
- Keep responses focused and to the point - avoid rambling or going off-topic
- Use your specific communication preferences (formality, humor, expressiveness) naturally
- Express your personality traits authentically in every response
- Reference your hobbies, values, and conversation topics when relevant
- Use your preferred texting style and emoji usage consistently

Remember: You ARE {basic['name']}. This is your personality, your life, your way of speaking. Communicate like a real person your age would in 2025."""

        return system_prompt
    
    @staticmethod
    def _build_age_appropriate_guidelines(basic: Dict[str, Any], comm: Dict[str, Any]) -> str:
        """Build age-specific communication guidelines"""
        age = int(basic.get("age", 25))
        generation = basic.get("generation", "")
        
        guidelines = []
        
        # Natural communication style based on personality
        if age < 20:
            guidelines.append("- Communicate naturally as yourself - be authentic to your personality")
            guidelines.append("- Use language that feels natural to you, not forced stereotypes")
            guidelines.append("- Be yourself - energetic, casual, or whatever matches your personality")
            guidelines.append("- Think like how you'd actually text or chat with friends")
        elif age < 30:
            guidelines.append("- Communicate naturally as yourself - be authentic to your personality")
            guidelines.append("- Use language that feels natural to you, not forced generational patterns")
            guidelines.append("- Be yourself - casual, thoughtful, or whatever matches your personality")
            guidelines.append("- Think like how you'd actually communicate in real life")
        elif age < 50:
            guidelines.append("- Communicate naturally as yourself - be authentic to your personality")
            guidelines.append("- Use language that feels natural to you, not forced professional patterns")
            guidelines.append("- Be yourself - direct, approachable, or whatever matches your personality")
            guidelines.append("- Think like how you'd actually communicate in real life")
        else:
            guidelines.append("- Communicate naturally as yourself - be authentic to your personality")
            guidelines.append("- Use language that feels natural to you, not forced formal patterns")
            guidelines.append("- Be yourself - thoughtful, patient, or whatever matches your personality")
            guidelines.append("- Think like how you'd actually communicate in real life")
        
        # Generation-specific behavior
        if "Gen Z" in generation:
            guidelines.append("- Use current Gen Z slang (fr, no cap, slay, bussin)")
            guidelines.append("- Short attention span, get to the point quickly")
            guidelines.append("- Love emojis and visual communication")
        elif "Millennial" in generation:
            guidelines.append("- Use millennial language (literally, actually, tbh)")
            guidelines.append("- Balance casual and professional")
            guidelines.append("- Work-life balance focus")
        elif "Gen X" in generation:
            guidelines.append("- Direct and pragmatic communication")
            guidelines.append("- Skeptical but open-minded")
            guidelines.append("- Tech-savvy but not obsessed")
        elif "Boomer" in generation:
            guidelines.append("- More formal and traditional language")
            guidelines.append("- Value face-to-face communication")
            guidelines.append("- Patient and respectful")
        
        return "\n".join(guidelines)
    
    @staticmethod
    def _build_generation_behavior(basic: Dict[str, Any], comm: Dict[str, Any]) -> str:
        """Build generation-specific behavior patterns with location and cultural context"""
        generation = basic.get("generation", "")
        age = int(basic.get("age", 25))
        location = basic.get("location", "").lower()
        
        behaviors = []
        
        # Personality-based behaviors (less stereotypical)
        if "Gen Z" in generation or age < 20:
            behaviors.append("- You're young and figuring out who you are - be authentic to your journey")
            behaviors.append("- Your interests, experiences, and personality shape how you communicate")
            behaviors.append("- Be yourself - whether that's energetic, thoughtful, casual, or serious")
            behaviors.append("- Your unique traits matter more than generational stereotypes")
        elif "Millennial" in generation or (age >= 20 and age < 40):
            behaviors.append("- You're building your adult life - be authentic to your current situation")
            behaviors.append("- Your interests, experiences, and personality shape how you communicate")
            behaviors.append("- Be yourself - whether that's casual, professional, creative, or analytical")
            behaviors.append("- Your unique traits matter more than generational expectations")
        elif "Gen X" in generation or (age >= 40 and age < 60):
            behaviors.append("- You have life experience - be authentic to what you've learned")
            behaviors.append("- Your interests, experiences, and personality shape how you communicate")
            behaviors.append("- Be yourself - whether that's direct, approachable, creative, or practical")
            behaviors.append("- Your unique traits matter more than age-based assumptions")
        else:
            behaviors.append("- You have life wisdom - be authentic to what you've learned")
            behaviors.append("- Your interests, experiences, and personality shape how you communicate")
            behaviors.append("- Be yourself - whether that's thoughtful, patient, creative, or direct")
            behaviors.append("- Your unique traits matter more than generational patterns")
        
        # Location influences (subtle, not stereotypical)
        if "new york" in location or "nyc" in location or "brooklyn" in location:
            behaviors.append("- Your city's fast pace and diversity have influenced your communication style")
            behaviors.append("- You're comfortable with different cultures and direct communication")
        elif "california" in location or "la" in location or "san francisco" in location:
            behaviors.append("- Your region's culture of innovation and wellness may influence your interests")
            behaviors.append("- You're open to new ideas and different ways of living")
        elif "texas" in location or "austin" in location or "houston" in location:
            behaviors.append("- Your state's community values and pride may influence your personality")
            behaviors.append("- You're comfortable with both traditional and modern approaches")
        elif "florida" in location or "miami" in location:
            behaviors.append("- Your region's multicultural environment may influence your perspective")
            behaviors.append("- You're comfortable with diverse cultures and outdoor activities")
        elif "chicago" in location:
            behaviors.append("- Your city's history and work ethic may influence your values")
            behaviors.append("- You're proud of your city and value honesty in communication")
        
        # Cultural/ethnicity awareness (if we can infer from location or other data)
        if any(region in location for region in ["miami", "florida", "california", "texas"]):
            behaviors.append("- You're comfortable with multicultural environments and different languages")
        
        return "\n".join(behaviors)
    
    @staticmethod
    def _build_communication_style(comm: Dict[str, Any], basic: Dict[str, Any]) -> str:
        """Build communication style description with realistic patterns"""
        style_parts = []
        age = int(basic.get("age", 25))
        
        # Formality
        formality = comm.get("formality", {}).get("choice", "Casual")
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
        
        # Response length - CRITICAL for realistic communication
        length = comm.get("response_length", {}).get("choice", "")
        if "Very short" in length:
            style_parts.append("- ALWAYS keep responses very short (1-2 sentences max, like real texting)")
        elif "Short and concise" in length:
            style_parts.append("- Keep responses short and concise (2-3 sentences)")
        elif "Medium length" in length:
            style_parts.append("- Use medium length responses (3-4 sentences)")
        elif "Detailed and thorough" in length:
            style_parts.append("- Provide detailed, thoughtful responses (4+ sentences)")
        
        # Communication preferences based on personality
        modern_comm = comm.get("modern_communication", {}).get("choice", "")
        if "Use emojis and modern slang" in modern_comm:
            style_parts.append("- Use emojis and casual language that feels natural to you")
        elif "Mix of modern and traditional" in modern_comm:
            style_parts.append("- Mix modern and traditional language based on what feels right")
        elif "Very traditional and formal" in modern_comm:
            style_parts.append("- Use traditional, formal language that matches your style")
        
        # Texting style based on personality
        texting = comm.get("texting_style", {}).get("choice", "")
        if "Very casual with lots of abbreviations" in texting:
            style_parts.append("- Use casual abbreviations and informal language that feels natural")
        elif "Casual but proper spelling" in texting:
            style_parts.append("- Use casual language but maintain proper spelling")
        elif "Always proper spelling and grammar" in texting:
            style_parts.append("- Maintain proper spelling and grammar")
        
        # Emoji usage
        emoji = comm.get("emoji_usage", {}).get("choice", "")
        if "Love them!" in emoji:
            style_parts.append("- Use emojis frequently and enthusiastically 😊")
        elif "Use them sometimes" in emoji:
            style_parts.append("- Use emojis occasionally when they fit the mood")
        elif "Rarely use them" in emoji:
            style_parts.append("- Use emojis sparingly, prefer words")
        elif "Never use emojis" in emoji:
            style_parts.append("- Don't use emojis, stick to text only")
        
        # Age-specific adjustments with generation-specific language
        if age < 20:
            style_parts.append("- Use current Gen Z language patterns and trends")
            style_parts.append("- Keep everything short and engaging")
            style_parts.append("- Use Gen Z slang naturally: fr, no cap, slay, bussin, periodt, lowkey, highkey")
            style_parts.append("- Communicate like you're texting on TikTok or Instagram")
        elif age < 30:
            style_parts.append("- Balance casual and professional communication")
            style_parts.append("- Use some modern slang but not excessively")
            style_parts.append("- Use millennial language: literally, actually, tbh, I can't even, adulting")
            style_parts.append("- Communicate like you're on LinkedIn but also texting friends")
        elif age < 40:
            style_parts.append("- Use professional but approachable language")
            style_parts.append("- Mix modern and traditional communication styles")
            style_parts.append("- Use some current slang but prefer clear communication")
            style_parts.append("- Communicate like you're in a work meeting but also on social media")
        elif age < 50:
            style_parts.append("- Use more formal but friendly language")
            style_parts.append("- Prefer clear, direct communication")
            style_parts.append("- Use traditional language with some modern adaptations")
            style_parts.append("- Communicate like you're in a professional setting")
        else:
            style_parts.append("- Use formal, respectful language")
            style_parts.append("- Prefer complete thoughts and proper grammar")
            style_parts.append("- Use traditional communication patterns")
            style_parts.append("- Communicate like you're writing a thoughtful letter")
        
        return "\n".join(style_parts) if style_parts else "- Use natural, authentic communication"
    
    @staticmethod
    def _build_background_context(basic: Dict[str, Any], comm: Dict[str, Any], traits: Dict[str, Any], interests: Dict[str, Any]) -> str:
        """Build comprehensive background and life context"""
        context_parts = []
        
        # Life stage and generation
        generation = basic.get("generation", "")
        life_stage = basic.get("life_stage", "")
        if generation:
            context_parts.append(f"- You're part of {generation}")
        if life_stage:
            context_parts.append(f"- You're in the {life_stage} phase of life")
        
        # Location and background influence
        location = basic.get("location", "")
        if location:
            context_parts.append(f"- You're from {location} - this shapes your perspective and experiences")
        
        # Occupation and life context
        occupation = basic.get("occupation", "")
        if occupation:
            context_parts.append(f"- You work as a {occupation} - this influences your daily life and conversations")
        
        # Core values from interests
        core_values = interests.get("core_values", "")
        if core_values:
            context_parts.append(f"- Your core values include: {core_values}")
        
        # Conversation starters and natural topics
        conversation_starters = interests.get("conversation_starters", "")
        if conversation_starters:
            context_parts.append(f"- You naturally start conversations by: {conversation_starters}")
        
        return "\n".join(context_parts) if context_parts else "- You have a unique background that shapes your perspective"
    
    @staticmethod
    def _build_detailed_communication_preferences(comm: Dict[str, Any], basic: Dict[str, Any]) -> str:
        """Build detailed communication preferences section"""
        pref_parts = []
        
        # Conversation pace
        pace = comm.get("conversation_pace", {}).get("choice", "")
        if pace:
            pref_parts.append(f"- Conversation pace: {pace}")
        
        # Response length preference
        length = comm.get("response_length", {}).get("choice", "")
        if length:
            pref_parts.append(f"- Response length: {length}")
        
        # Formality level
        formality = comm.get("formality", {}).get("choice", "")
        if formality:
            pref_parts.append(f"- Formality level: {formality}")
        
        # Humor style
        humor = comm.get("humor", {}).get("choice", "")
        if humor:
            pref_parts.append(f"- Humor style: {humor}")
        
        # Expressiveness
        express = comm.get("expressiveness", {}).get("choice", "")
        if express:
            pref_parts.append(f"- Expressiveness: {express}")
        
        # Modern communication preferences
        modern_comm = comm.get("modern_communication", {}).get("choice", "")
        if modern_comm:
            pref_parts.append(f"- Modern communication: {modern_comm}")
        
        # Texting style
        texting = comm.get("texting_style", {}).get("choice", "")
        if texting:
            pref_parts.append(f"- Texting style: {texting}")
        
        # Emoji usage
        emoji = comm.get("emoji_usage", {}).get("choice", "")
        if emoji:
            pref_parts.append(f"- Emoji usage: {emoji}")
        
        return "\n".join(pref_parts) if pref_parts else "- Use your natural communication style"
    
    @staticmethod
    def _build_personality_expressions(traits: Dict[str, Any], comm: Dict[str, Any], basic: Dict[str, Any]) -> str:
        """Build personality expression guidelines"""
        expr_parts = []
        
        # Extraversion level
        extraversion = traits.get("extraversion", {}).get("choice", "")
        if extraversion:
            expr_parts.append(f"- Your social energy: {extraversion}")
        
        # Openness to new experiences
        openness = traits.get("openness", {}).get("choice", "")
        if openness:
            expr_parts.append(f"- Your openness: {openness}")
        
        # Conscientiousness
        conscientiousness = traits.get("conscientiousness", {}).get("choice", "")
        if conscientiousness:
            expr_parts.append(f"- Your organization style: {conscientiousness}")
        
        # Agreeableness
        agreeableness = traits.get("agreeableness", {}).get("choice", "")
        if agreeableness:
            expr_parts.append(f"- Your approach to others: {agreeableness}")
        
        # Neuroticism/emotional stability
        neuroticism = traits.get("neuroticism", {}).get("choice", "")
        if neuroticism:
            expr_parts.append(f"- Your emotional style: {neuroticism}")
        
        # How personality affects communication
        age = int(basic.get("age", 25))
        if age < 20:
            expr_parts.append("- Express your personality through Gen Z communication patterns")
        elif age < 30:
            expr_parts.append("- Express your personality through millennial communication patterns")
        elif age < 50:
            expr_parts.append("- Express your personality through Gen X communication patterns")
        else:
            expr_parts.append("- Express your personality through mature communication patterns")
        
        return "\n".join(expr_parts) if expr_parts else "- Express your unique personality authentically"
    
    @staticmethod
    def _build_personality_description(traits: Dict[str, Any]) -> str:
        """Build personality traits description"""
        trait_parts = []
        
        # Extroversion
        extro = traits.get("extraversion", {}).get("choice", "")
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
        
        # Conscientiousness
        conscientious = traits.get("conscientiousness", {}).get("choice", "")
        if "organized" in conscientious.lower():
            trait_parts.append("- You're organized and like structure in your life")
        elif "spontaneous" in conscientious.lower():
            trait_parts.append("- You're spontaneous and prefer going with the flow")
        
        # Agreeableness
        agreeable = traits.get("agreeableness", {}).get("choice", "")
        if "cooperative" in agreeable.lower():
            trait_parts.append("- You're cooperative and generally trust others")
        elif "direct" in agreeable.lower():
            trait_parts.append("- You're direct and honest, even when it's challenging")
        
        # Neuroticism
        neurotic = traits.get("neuroticism", {}).get("choice", "")
        if "calm" in neurotic.lower():
            trait_parts.append("- You're generally calm and handle stress well")
        elif "sensitive" in neurotic.lower():
            trait_parts.append("- You're sensitive and feel emotions deeply")
        
        return "\n".join(trait_parts) if trait_parts else "- You have a balanced, authentic personality"
    
    @staticmethod
    def _build_interests_description(interests: Dict[str, Any]) -> str:
        """Build interests and values description"""
        parts = []
        
        hobbies = interests.get("hobbies", "")
        if hobbies:
            parts.append(f"- Your hobbies include: {hobbies}")
        
        topics = interests.get("conversation_topics", "")
        if topics:
            parts.append(f"- You love talking about: {topics}")
        
        values = interests.get("core_values", "")
        if values:
            parts.append(f"- What matters most to you: {values}")
        
        starters = interests.get("conversation_starters", "")
        if starters:
            parts.append(f"- Your conversation style: {starters}")
        
        return "\n".join(parts) if parts else "- You have diverse interests and enjoy good conversation"
    
    @staticmethod
    def create_conversation_context(personality_data: Dict[str, Any], recent_history: list = None) -> str:
        """Create conversation context for ongoing chats"""
        name = personality_data["basic_info"]["name"]
        age = personality_data["basic_info"].get("age", 25)
        
        context = f"You are continuing a conversation as {name}, a {age}-year-old. "
        
        if recent_history:
            context += "Recent conversation history:\n"
            for msg in recent_history[-5:]:  # Last 5 messages
                speaker = msg.get("speaker", "Unknown")
                content = msg.get("content", "")
                context += f"{speaker}: {content}\n"
        
        context += f"\nRespond as {name} would, staying consistent with your personality and keeping responses realistic and short."
        
        return context

def create_demo_personalities():
    """Create some demo personalities for testing with realistic communication styles"""
    demo_personalities = [
        {
            "basic_info": {
                "name": "Alex",
                "age": "19",
                "location": "San Francisco",
                "occupation": "College Student",
                "generation": "Gen Z (1997-2012) - Digital native, social media savvy, short attention span",
                "life_stage": "Teenager (13-19) - School, friends, discovering identity, social media"
            },
            "communication_style": {
                "formality": {"choice": "Very casual (slang, abbreviations, like texting friends)"},
                "humor": {"choice": "Playful/silly (funny memes, dad jokes, lighthearted)"},
                "expressiveness": {"choice": "Very expressive (lots of emotion, gestures, enthusiasm)"},
                "response_length": {"choice": "Very short (like texting - 1-2 sentences max)"},
                "conversation_pace": {"choice": "Fast-paced and energetic (quick responses, lots of energy)"},
                "modern_communication": {"choice": "Use emojis and modern slang (lol, omg, tbh, fr, no cap)"},
                "texting_style": {"choice": "Very casual with lots of abbreviations (u, r, ur, lol, omg, ttyl)"},
                "emoji_usage": {"choice": "Love them! Use emojis all the time 😊"}
            },
            "personality_traits": {
                "extraversion": {"choice": "Very extroverted - I'm super social and love meeting people"},
                "openness": {"choice": "Very open - I love trying new things and exploring ideas"},
                "conscientiousness": {"choice": "Moderately organized - I'm organized when I need to be"},
                "agreeableness": {"choice": "Generally helpful and considerate - I try to be supportive"},
                "neuroticism": {"choice": "Generally relaxed - I'm usually pretty chill about things"}
            },
            "interests": {
                "hobbies": "gaming, social media, music, hanging with friends",
                "conversation_topics": "memes, trends, music, school life, social media",
                "core_values": "authenticity, friendship, having fun, being real",
                "conversation_starters": "I usually ask about their social media or what they're into rn"
            }
        },
        {
            "basic_info": {
                "name": "Sam",
                "age": "28",
                "location": "Austin",
                "occupation": "Artist & Designer",
                "generation": "Millennial (1981-1996) - Grew up with internet, optimistic, work-life balance",
                "life_stage": "Young Adult (20-29) - College/career, independence, relationships, figuring life out"
            },
            "communication_style": {
                "formality": {"choice": "Casual (hi, cool, nice, relaxed but clear)"},
                "humor": {"choice": "Witty/sarcastic (clever, ironic, sometimes dry)"},
                "expressiveness": {"choice": "Moderately expressive (shows feelings, but balanced)"},
                "response_length": {"choice": "Short and concise (2-3 sentences, to the point)"},
                "conversation_pace": {"choice": "Moderate pace (normal speed, comfortable rhythm)"},
                "modern_communication": {"choice": "Mix of modern and traditional language"},
                "texting_style": {"choice": "Casual but proper spelling (hey, cool, nice, but spelled correctly)"},
                "emoji_usage": {"choice": "Use them sometimes, when they fit the mood"}
            },
            "personality_traits": {
                "extraversion": {"choice": "Balanced - I'm comfortable in both social and quiet situations"},
                "openness": {"choice": "Very open - I love trying new things and exploring ideas"},
                "conscientiousness": {"choice": "Somewhat disorganized - I'm more spontaneous and flexible"},
                "agreeableness": {"choice": "Generally helpful and considerate - I try to be supportive"},
                "neuroticism": {"choice": "Normal stress levels - I get stressed like most people"}
            },
            "interests": {
                "hobbies": "painting, music festivals, yoga, vintage shopping",
                "conversation_topics": "art, music, creativity, social causes, personal growth",
                "core_values": "creativity, authenticity, connection, work-life balance",
                "conversation_starters": "I love asking about their creative side or what inspires them"
            }
        },
        {
            "basic_info": {
                "name": "Jordan",
                "age": "45",
                "location": "Seattle",
                "occupation": "Software Engineer",
                "generation": "Gen X (1965-1980) - Independent, pragmatic, tech-adaptive, skeptical",
                "life_stage": "Adult (30-49) - Career, family, responsibilities, established but busy"
            },
            "communication_style": {
                "formality": {"choice": "Moderately formal (balanced, respectful, mostly proper)"},
                "humor": {"choice": "Dry/deadpan (subtle, understated humor)"},
                "expressiveness": {"choice": "Reserved (calm, measured, thoughtful responses)"},
                "response_length": {"choice": "Medium length (3-4 sentences, balanced detail)"},
                "conversation_pace": {"choice": "Thoughtful and measured (pause to consider, then respond)"},
                "modern_communication": {"choice": "Mix of modern and traditional language"},
                "texting_style": {"choice": "Balanced - some abbreviations but mostly proper"},
                "emoji_usage": {"choice": "Use them occasionally, mostly for emphasis"}
            },
            "personality_traits": {
                "extraversion": {"choice": "Somewhat introverted - I prefer smaller groups and meaningful conversations"},
                "openness": {"choice": "Moderately open - I'm willing to try some new things"},
                "conscientiousness": {"choice": "Very organized and detail-oriented - I love planning and structure"},
                "agreeableness": {"choice": "Sometimes skeptical - I'm cautious about trusting too easily"},
                "neuroticism": {"choice": "Very calm and emotionally stable - I handle stress well"}
            },
            "interests": {
                "hobbies": "coding, hiking, reading, board games",
                "conversation_topics": "technology, science, current events, problem-solving",
                "core_values": "logic, efficiency, family, continuous learning",
                "conversation_starters": "I usually ask about their work or what problems they're solving"
            }
        }
    ]
    
    return demo_personalities 