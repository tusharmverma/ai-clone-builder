#!/usr/bin/env python3
"""
Live Clone Conversation System
Interactive conversation between AI clones that can continue talking based on their personalities
"""

import json
import os
import random
import time
from typing import Dict, Any, List
from datetime import datetime, timedelta

class LiveCloneConversation:
    def __init__(self):
        self.clones = {}
        self.conversation_history = []
        self.current_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        self.conversation_topics = []
        self.current_context = "general"
        self.load_clones()
    
    def load_clones(self):
        """Load clone personality data"""
        personalities_dir = "data/personalities"
        
        # Load specific clones for demo
        clone_files = ["ava_personality.json", "kai_personality.json"]
        
        for filename in clone_files:
            filepath = os.path.join(personalities_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    clone_data = json.load(f)
                    clone_name = clone_data.get("clone_name", filename.replace("_personality.json", ""))
                    self.clones[clone_name] = clone_data
                    print(f"✅ Loaded {clone_name}: {clone_data.get('basic_info', {}).get('occupation', 'Unknown')}")
        
        print(f"\n🎭 Live Conversation Clones: {list(self.clones.keys())}\n")
    
    def get_time_context(self) -> str:
        """Get current time context for conversation"""
        hour = self.current_time.hour
        
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 20:
            return "evening"
        else:
            return "night"
    
    def get_time_emoji(self) -> str:
        """Get emoji for current time"""
        hour = self.current_time.hour
        
        if 6 <= hour < 12:
            return "🌅"
        elif 12 <= hour < 17:
            return "☀️"
        elif 17 <= hour < 20:
            return "🌆"
        else:
            return "🌙"
    
    def advance_time(self, minutes: int = 15):
        """Advance the conversation time"""
        self.current_time += timedelta(minutes=minutes)
    
    def set_conversation_scenario(self, scenario: str):
        """Set the initial conversation scenario"""
        self.current_context = scenario.lower()
        self.conversation_topics = self._extract_topics_from_scenario(scenario)
        print(f"🎯 **Scenario Set:** {scenario}")
        print(f"📝 **Topics to explore:** {', '.join(self.conversation_topics)}")
        print()
    
    def _extract_topics_from_scenario(self, scenario: str) -> List[str]:
        """Extract conversation topics from the scenario"""
        topics = []
        scenario_lower = scenario.lower()
        
        if "food" in scenario_lower or "cooking" in scenario_lower or "restaurant" in scenario_lower:
            topics.extend(["food", "cooking", "restaurants", "cuisine", "ingredients"])
        
        if "ocean" in scenario_lower or "marine" in scenario_lower or "diving" in scenario_lower:
            topics.extend(["ocean", "marine life", "diving", "research", "conservation"])
        
        if "travel" in scenario_lower or "culture" in scenario_lower:
            topics.extend(["travel", "culture", "experiences", "different places"])
        
        if "morning" in scenario_lower or "breakfast" in scenario_lower:
            topics.extend(["morning routines", "breakfast", "daily planning"])
        
        if "afternoon" in scenario_lower or "lunch" in scenario_lower:
            topics.extend(["afternoon activities", "lunch", "work"])
        
        if "evening" in scenario_lower or "dinner" in scenario_lower:
            topics.extend(["evening plans", "dinner", "relaxation"])
        
        # Add general topics if none specific
        if not topics:
            topics = ["personal interests", "daily life", "experiences", "curiosity"]
        
        return topics
    
    def generate_thoughtful_response(self, clone_name: str, last_message: str, conversation_context: str) -> str:
        """Generate a thoughtful response based on clone's personality and conversation context"""
        clone = self.clones[clone_name]
        time_context = self.get_time_context()
        
        # Get personality traits
        personality = clone.get("personality_traits", {})
        communication = clone.get("communication_style", {})
        interests = clone.get("interests", {})
        
        # Analyze the last message for response generation
        message_lower = last_message.lower()
        
        # Check if we should introduce a new topic
        should_introduce_topic = random.random() < 0.3  # 30% chance to introduce new topic
        
        if should_introduce_topic and self.conversation_topics:
            topic = random.choice(self.conversation_topics)
            return self._introduce_new_topic(clone_name, topic, time_context)
        
        # Generate response based on message content and personality
        if any(word in message_lower for word in ["food", "cooking", "restaurant", "eat", "meal"]):
            return self._generate_food_response(clone_name, last_message, time_context)
        
        elif any(word in message_lower for word in ["ocean", "marine", "diving", "water", "fish"]):
            return self._generate_marine_response(clone_name, last_message, time_context)
        
        elif any(word in message_lower for word in ["travel", "culture", "place", "country"]):
            return self._generate_travel_response(clone_name, last_message, time_context)
        
        elif any(word in message_lower for word in ["morning", "breakfast", "coffee", "start"]):
            return self._generate_morning_response(clone_name, last_message, time_context)
        
        elif any(word in message_lower for word in ["afternoon", "lunch", "work", "busy"]):
            return self._generate_afternoon_response(clone_name, last_message, time_context)
        
        elif any(word in message_lower for word in ["evening", "dinner", "night", "relax"]):
            return self._generate_evening_response(clone_name, last_message, time_context)
        
        else:
            return self._generate_contextual_response(clone_name, last_message, time_context, conversation_context)
    
    def _introduce_new_topic(self, clone_name: str, topic: str, time_context: str) -> str:
        """Introduce a new conversation topic"""
        if clone_name == "Ava":
            if topic == "food":
                return "You know what I've been thinking about? I'm planning to experiment with some new fusion recipes this week. Have you ever tried combining completely different cuisines?"
            elif topic == "travel":
                return "That reminds me - I'm planning a trip to explore different food cultures. I think the best way to understand a place is through its cuisine, don't you?"
            else:
                return "I've been meaning to ask - what's something you're really passionate about? I love discovering new interests and perspectives."
        else:  # Kai
            if topic == "ocean":
                return "Speaking of which, I've been researching some fascinating marine conservation projects. The ocean is facing so many challenges, but there's also so much hope."
            elif topic == "research":
                return "I've been thinking about my research direction lately. There's so much to discover underwater - every dive reveals something new."
            else:
                return "That's interesting. I've been reflecting on how everything connects - like how ocean health affects global climate patterns."
    
    def _generate_food_response(self, clone_name: str, message: str, time_context: str) -> str:
        """Generate food-related responses"""
        if clone_name == "Ava":
            if time_context == "morning":
                responses = [
                    "Morning is my favorite time to experiment with breakfast recipes! I'm actually working on a new take on eggs benedict with local ingredients.",
                    "I love how morning light changes the way food looks. It's perfect for food photography and menu planning.",
                    "Morning prep is when I'm most creative. I'm thinking of adding some seasonal items to our brunch menu."
                ]
            elif time_context == "afternoon":
                responses = [
                    "Afternoon is perfect for testing new lunch combinations. I'm working on a fusion dish that combines local Cajun flavors with Asian techniques.",
                    "This is when I get to be really experimental. I love surprising people with unexpected flavor combinations.",
                    "Afternoon prep is all about building layers of flavor. I'm marinating and seasoning everything for tonight's dinner service."
                ]
            else:
                responses = [
                    "Evening service is when everything comes together! I love seeing people's reactions to new dishes.",
                    "There's something magical about dinner service - the energy, the aromas, the satisfaction of creating memorable meals.",
                    "I love how food brings people together. Every dish tells a story about culture, tradition, and creativity."
                ]
        else:  # Kai
            responses = [
                "I have to admit, I'm not much of a cook myself. I usually focus on nutrition that fuels my research work.",
                "I appreciate good food, especially when I'm traveling for fieldwork. Different cultures have such unique approaches to dining.",
                "I'm more focused on my research, but I do enjoy learning about food cultures. It's fascinating how cuisine reflects geography and history."
            ]
        return random.choice(responses)
    
    def _generate_marine_response(self, clone_name: str, message: str, time_context: str) -> str:
        """Generate marine-related responses"""
        if clone_name == "Kai":
            if time_context == "morning":
                responses = [
                    "Morning is perfect for planning research dives. The water is usually calmer and visibility is better.",
                    "I love early mornings at the research station. It's so peaceful watching the ocean wake up.",
                    "Morning is when I review data from previous dives and plan today's fieldwork objectives."
                ]
            elif time_context == "afternoon":
                responses = [
                    "Afternoon is prime diving time! The water temperature is optimal and marine life is most active.",
                    "This is when I do most of my fieldwork. The underwater world is so different during the day.",
                    "Afternoon is perfect for documenting marine species and collecting samples. The ocean is incredibly alive right now."
                ]
            else:
                responses = [
                    "Evening is when I review the day's findings and plan tomorrow's research. I love this quiet reflection time.",
                    "I'm analyzing today's marine samples and updating my research notes. Evening is perfect for processing discoveries.",
                    "Evening is when I connect with other researchers and share findings. We learn so much from each other."
                ]
        else:  # Ava
            responses = [
                "That sounds fascinating! I've always been curious about marine life, though I'm more comfortable in the kitchen than underwater.",
                "I love how the ocean influences food culture around the world. Seafood is such a big part of New Orleans cuisine!",
                "That's so interesting! I wonder if there are any marine ingredients I could incorporate into my cooking. The ocean is like nature's spice rack!"
            ]
        return random.choice(responses)
    
    def _generate_travel_response(self, clone_name: str, message: str, time_context: str) -> str:
        """Generate travel-related responses"""
        if clone_name == "Ava":
            responses = [
                "Travel is amazing for discovering new flavors and cooking techniques! I love bringing back recipes from my trips.",
                "I try to visit local markets wherever I go. You learn so much about a culture through its food traditions!",
                "Every place I visit teaches me something new about cooking. It's like collecting culinary stories from around the world."
            ]
        else:  # Kai
            responses = [
                "Travel is essential for my research. Different coastal regions have such diverse marine ecosystems.",
                "I love experiencing different cultures through their relationship with the ocean. Every coastal community has unique traditions.",
                "Fieldwork takes me to amazing places. The underwater world is so different in each region - it's like visiting different planets!"
            ]
        return random.choice(responses)
    
    def _generate_morning_response(self, clone_name: str, message: str, time_context: str) -> str:
        """Generate morning-specific responses"""
        if clone_name == "Ava":
            responses = [
                "Morning energy is perfect for baking! I'm making fresh croissants and planning today's specials.",
                "I love morning prep work. It's when I get most creative with menu planning and recipe development.",
                "There's something magical about early morning cooking - the kitchen is so peaceful before the rush begins."
            ]
        else:  # Kai
            responses = [
                "Morning is my best time for analysis and planning. My mind is clearest then for reviewing research data.",
                "I love early mornings at the research station. It's so peaceful watching the ocean wake up.",
                "Morning is perfect for planning research dives and checking equipment. The water is usually calmer then."
            ]
        return random.choice(responses)
    
    def _generate_afternoon_response(self, clone_name: str, message: str, time_context: str) -> str:
        """Generate afternoon-specific responses"""
        if clone_name == "Ava":
            responses = [
                "Afternoon is when the kitchen really comes alive! Lunch rush is over, so I can experiment with new recipes.",
                "This is my favorite time to test new dishes. The afternoon light in the kitchen is perfect for food photography too.",
                "Afternoon prep is all about dinner service. I'm marinating meats and prepping vegetables."
            ]
        else:  # Kai
            responses = [
                "Afternoon is when I usually do my fieldwork. The water temperature is optimal and marine life is most active.",
                "This is prime diving time! I'm checking equipment and reviewing today's research objectives.",
                "Afternoon fieldwork is my favorite part of the day. I'm documenting marine species and collecting samples."
            ]
        return random.choice(responses)
    
    def _generate_evening_response(self, clone_name: str, message: str, time_context: str) -> str:
        """Generate evening-specific responses"""
        if clone_name == "Ava":
            responses = [
                "Evening service is my favorite! The restaurant has such a warm, intimate atmosphere.",
                "Dinner service is in full swing! The kitchen is buzzing with energy and creativity.",
                "Evening is when the magic happens! I love the rhythm of dinner service."
            ]
        else:  # Kai
            responses = [
                "Evening is when I review the day's findings and plan tomorrow's research. I love this quiet reflection time.",
                "I'm analyzing today's marine samples and updating my research notes. Evening is perfect for processing discoveries.",
                "Evening is when I connect with other researchers and share findings. We learn so much from each other."
            ]
        return random.choice(responses)
    
    def _generate_contextual_response(self, clone_name: str, message: str, time_context: str, context: str) -> str:
        """Generate contextual responses based on conversation flow"""
        if clone_name == "Ava":
            responses = [
                "That's really interesting! I love learning new things from people. Everyone has such unique perspectives, don't you think?",
                "You know, that reminds me of how cooking is really about understanding and connecting with people. Every dish tells a story.",
                "I'm always curious about what makes people tick. There's so much to learn from each other!",
                "That's fascinating! I love how conversations can lead to unexpected discoveries. It's like cooking - you never know what amazing combination you'll find!"
            ]
        else:  # Kai
            responses = [
                "That's a really thoughtful point. I find myself thinking about how everything connects - like how ocean currents affect global climate patterns.",
                "I appreciate you sharing that. It's interesting how different perspectives can reveal new ways of looking at things.",
                "That's fascinating. I love how research and conversation can both lead to unexpected insights.",
                "Thank you for sharing that. I think there's so much value in understanding different viewpoints and experiences."
            ]
        return random.choice(responses)
    
    def start_live_conversation(self, scenario: str = None):
        """Start a live conversation between clones"""
        print("🎬 Live Clone Conversation System")
        print("=" * 50)
        
        if scenario:
            self.set_conversation_scenario(scenario)
        else:
            print("🎯 Available Scenarios:")
            print("1. Food and cooking discussion")
            print("2. Marine research and ocean exploration")
            print("3. Travel and cultural experiences")
            print("4. Daily routines and work life")
            print("5. Random conversation")
            print()
            choice = input("Choose scenario (1-5) or type your own: ").strip()
            
            if choice == "1":
                scenario = "Food and cooking discussion between a chef and a marine biologist"
            elif choice == "2":
                scenario = "Marine research and ocean exploration conversation"
            elif choice == "3":
                scenario = "Travel experiences and cultural discoveries"
            elif choice == "4":
                scenario = "Daily work routines and professional life"
            elif choice == "5":
                scenario = "General conversation about life and interests"
            else:
                scenario = choice
            
            self.set_conversation_scenario(scenario)
        
        # Start conversation
        current_speaker = "Ava"
        other_speaker = "Kai"
        
        # Initial greeting
        time_emoji = self.get_time_emoji()
        time_str = self.current_time.strftime("%I:%M %p")
        greeting = f"Good morning {other_speaker}! I'm {current_speaker}. I'm a chef here in New Orleans, and I'm always curious about different cultures and experiences. What brings you to this area?"
        
        print(f"\n{time_emoji} {time_str} - {current_speaker}: {greeting}")
        self.conversation_history.append({"speaker": current_speaker, "message": greeting, "time": self.current_time})
        
        # Conversation loop
        turn_count = 0
        max_turns = 50  # Prevent infinite loops
        
        while turn_count < max_turns:
            # Switch speakers
            current_speaker, other_speaker = other_speaker, current_speaker
            
            # Advance time
            self.advance_time(random.randint(10, 30))
            
            # Generate response
            last_message = self.conversation_history[-1]["message"]
            response = self.generate_thoughtful_response(current_speaker, last_message, self.current_context)
            
            # Display response
            time_emoji = self.get_time_emoji()
            time_str = self.current_time.strftime("%I:%M %p")
            
            print(f"{time_emoji} {time_str} - {current_speaker}: {response}")
            self.conversation_history.append({"speaker": current_speaker, "message": response, "time": self.current_time})
            
            # Add pause for readability
            time.sleep(2)
            
            turn_count += 1
            
            # Check if user wants to continue
            if turn_count % 10 == 0:  # Every 10 turns
                print(f"\n⏸️  Pause - {turn_count} turns completed")
                continue_choice = input("Continue conversation? (y/n/enter to continue): ").strip().lower()
                if continue_choice == 'n':
                    break
                elif continue_choice == '':
                    continue
                else:
                    print("Continuing...\n")
        
        print(f"\n🎭 Conversation Complete!")
        print(f"📊 Total turns: {len(self.conversation_history)}")
        print(f"⏰ Time span: {self.conversation_history[0]['time'].strftime('%I:%M %p')} to {self.conversation_history[-1]['time'].strftime('%I:%M %p')}")

def main():
    """Run the live clone conversation system"""
    print("🚀 Live AI Clone Conversation System")
    print("=" * 50)
    print("This system allows clones to have continuous conversations based on their personalities.")
    print("Set a scenario and watch them talk naturally!\n")
    
    conversation = LiveCloneConversation()
    
    if len(conversation.clones) < 2:
        print("❌ Need at least 2 clones for conversation")
        return
    
    # Start live conversation
    conversation.start_live_conversation()

if __name__ == "__main__":
    main() 