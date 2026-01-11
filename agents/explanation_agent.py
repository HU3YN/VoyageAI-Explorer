# explanation_agent.py

class ExplanationAgent:
    """Agent responsible for generating explanations of why destinations were selected"""
    
    def __init__(self):
        print("✅ Explanation Agent: Initialized")

    def generate_explanations(self, itinerary, matched_interests_list):
        """Generate explanations for each destination in the itinerary"""
        print(f"✅ Explanation Agent: Generating explanations for {len(itinerary)} destinations...")
        explanations = []
        
        for i, city in enumerate(itinerary):
            matched = matched_interests_list[i] if i < len(matched_interests_list) else []
            
            explanation = self._create_explanation(
                city["destination"],
                city["country"],
                matched,
                city["score"]
            )
            
            explanations.append(explanation)
        
        return explanations

    def _create_explanation(self, destination, country, matched_interests, score):
        """Create a detailed explanation for a single destination"""
        if matched_interests and len(matched_interests) > 0:
            interests_str = ", ".join(matched_interests[:3])
            
            if score >= 80:
                return f"{destination}, {country} is an excellent match ({score}% confidence) for your interests in {interests_str}."
            elif score >= 60:
                return f"{destination}, {country} is a great match ({score}% confidence) based on your interests in {interests_str}."
            elif score >= 40:
                return f"{destination}, {country} is a good match ({score}% confidence) for {interests_str}."
            else:
                return f"{destination}, {country} was selected as a popular destination ({score}% confidence)."
        else:
            return f"{destination}, {country} is a highly-rated destination that offers diverse experiences for travelers."

    def explain_single(self, destination, preferences, score):
        """Legacy method for single destination explanation"""
        matched = [p for p in preferences if p in destination.lower()]
        if not matched:
            matched = preferences
        
        return f"{destination} was selected because it matches your interests in {', '.join(matched)} (confidence: {score}%)."