# master_agent.py - FIXED VERSION WITH ACTIVITY MATCHES
from agents.preference_agent import PreferenceAgent
from agents.destination_agent import DestinationAgent
from agents.itinerary_agent import ItineraryAgent
from agents.explanation_agent import ExplanationAgent

class MasterAgent:
    """
    Master Agent coordinates all sub-agents to create personalized travel itineraries
    
    Agent Architecture:
    1. PreferenceAgent - Extracts user interests using AI (minimal tokens)
    2. DestinationAgent - Ranks cities from database based on interests
    3. ItineraryAgent - Distributes days and generates daily plans using AI
    4. ExplanationAgent - Creates reasoning for recommendations
    """
    
    def __init__(self, nlp=None):
        print("\n🚀 Initializing Multi-Agent Travel Planner System...")
        print("=" * 60)
        
        # Initialize all specialized agents
        self.preference_agent = PreferenceAgent()
        self.destination_agent = DestinationAgent()
        self.itinerary_agent = ItineraryAgent()
        self.explanation_agent = ExplanationAgent()
        
        print("=" * 60)
        print("✅ All agents initialized successfully!\n")

    def generate_itinerary(self, user_input, days):
        """
        Main orchestration method - coordinates all agents
        
        Flow:
        1. PreferenceAgent extracts interests from user input
        2. ItineraryAgent calculates optimal city distribution
        3. DestinationAgent ranks cities based on ALL interests
        4. ItineraryAgent builds complete day-by-day itinerary
        """
        print(f"\n{'='*60}")
        print(f"🎯 MASTER AGENT: Planning {days}-day trip")
        print(f"📝 User Input: '{user_input}'")
        print(f"{'='*60}\n")
        
        # Step 1: Extract user preferences (AI Agent)
        if not user_input or user_input.strip() == "":
            print("⚠️ No user input provided, using default recommendations")
            interests = []
        else:
            interests = self.preference_agent.extract_preferences(user_input)
        
        # Step 2: Calculate optimal city distribution
        days_per_city, num_cities = self.itinerary_agent.calculate_days_per_city(days)
        
        # Step 3: Rank cities based on ALL preferences (Database Agent)
        # ⭐ FIX: Pass ALL interests including 'cars', 'beach', etc.
        if interests:
            print(f"🔍 Using ALL {len(interests)} interests for diversity ranking")
            print(f"📋 Full interest list: {interests}\n")
            ranked_cities = self.destination_agent.rank_cities_with_db(interests, num_cities)
        else:
            ranked_cities = self.destination_agent.get_random_cities(num_cities)
        
        # Step 4: Build complete itinerary with day distribution (AI Agent)
        itinerary, matched_interests, activity_map = self.itinerary_agent.build_itinerary(
            ranked_cities, days, interests
        )
        
        print(f"\n{'='*60}")
        print(f"✅ MASTER AGENT: Trip planning complete!")
        print(f"📋 Generated itinerary:")
        for city in itinerary:
            activity_count = sum(len(activities) for activities in city.get("activity_matches", {}).values())
            print(f"   • {city['destination']}, {city['country']}: {city['days']} days (Score: {city['score']}%, Activities: {activity_count})")
        print(f"{'='*60}\n")
        
        return itinerary, matched_interests, activity_map
    
    def plan_trip(self, user_input, days=3):
        """
        Legacy compatibility method with full explanations
        """
        # Generate itinerary using all agents
        itinerary, matched_interests, activity_map = self.generate_itinerary(user_input, days)
        
        # Extract preferences for response
        preferences = self.preference_agent.extract_preferences(user_input)
        
        # Generate explanations (Explanation Agent)
        explanations = self.explanation_agent.generate_explanations(itinerary, matched_interests)
        
        # DEBUG: Print activity matches to see what's happening
        print("\n🔍 DEBUG - Activity Matches:")
        for i, city in enumerate(itinerary):
            activity_matches = city.get("activity_matches", {})
            activity_count = sum(len(activities) for activities in activity_matches.values())
            print(f"  {city['destination']}: {activity_count} activities matched across {len(activity_matches)} interests")
        
        return {
            "preferences": preferences,
            "itinerary": itinerary,
            "explanations": explanations,
            "matched_interests": matched_interests,
            "activity_interest_map": activity_map
        }