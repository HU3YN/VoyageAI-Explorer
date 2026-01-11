# itinerary_agent.py - WITH IMPROVED GEOGRAPHIC SORTING AND .ENV SUPPORT
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ItineraryAgent:
    """Agent responsible for building day-by-day itineraries and distributing days across cities"""
    
    # Define geographic regions and countries
    REGIONS = {
        'East Asia': ['Japan', 'South Korea', 'China', 'Taiwan', 'Hong Kong', 'Macau', 'Mongolia'],
        'Southeast Asia': ['Thailand', 'Vietnam', 'Malaysia', 'Singapore', 'Indonesia', 'Philippines', 
                          'Cambodia', 'Laos', 'Myanmar', 'Brunei'],
        'South Asia': ['India', 'Nepal', 'Sri Lanka', 'Bangladesh', 'Pakistan', 'Bhutan', 'Maldives'],
        'Middle East': ['United Arab Emirates', 'Turkey', 'Israel', 'Jordan', 'Saudi Arabia', 'Qatar', 
                       'Oman', 'Lebanon', 'Iran', 'Iraq'],
        'Western Europe': ['France', 'Spain', 'Portugal', 'United Kingdom', 'Ireland', 'Belgium', 
                          'Netherlands', 'Luxembourg', 'Monaco'],
        'Central Europe': ['Germany', 'Austria', 'Switzerland', 'Czech Republic', 'Poland', 'Hungary', 
                          'Slovakia', 'Slovenia', 'Liechtenstein'],
        'Southern Europe': ['Italy', 'Greece', 'Croatia', 'Malta', 'Cyprus', 'Albania', 'Montenegro', 
                           'Serbia', 'Bosnia and Herzegovina'],
        'Northern Europe': ['Norway', 'Sweden', 'Finland', 'Denmark', 'Iceland', 'Estonia', 'Latvia', 'Lithuania'],
        'Eastern Europe': ['Russia', 'Ukraine', 'Romania', 'Bulgaria', 'Belarus', 'Moldova'],
        'North America': ['United States', 'Canada', 'Mexico'],
        'Central America': ['Costa Rica', 'Panama', 'Guatemala', 'Belize', 'Honduras', 'Nicaragua', 'El Salvador'],
        'Caribbean': ['Jamaica', 'Cuba', 'Dominican Republic', 'Puerto Rico', 'Bahamas', 'Barbados', 
                     'Trinidad and Tobago', 'Aruba', 'Turks and Caicos', 'Cayman Islands', 'Antigua and Barbuda',
                     'St. Lucia', 'St. Barts', 'St. Barthélemy', 'Anguilla'],
        'South America': ['Brazil', 'Argentina', 'Chile', 'Peru', 'Colombia', 'Ecuador', 'Bolivia', 
                         'Uruguay', 'Paraguay', 'Venezuela'],
        'Oceania': ['Australia', 'New Zealand', 'Fiji', 'French Polynesia', 'Cook Islands'],
        'Africa North': ['Morocco', 'Egypt', 'Tunisia', 'Algeria', 'Libya'],
        'Africa East': ['Kenya', 'Tanzania', 'Ethiopia', 'Uganda', 'Rwanda'],
        'Africa South': ['South Africa', 'Botswana', 'Zimbabwe', 'Namibia', 'Mozambique'],
        'Africa West': ['Ghana', 'Nigeria', 'Senegal', 'Ivory Coast', 'Cameroon'],
        'Pacific Islands': ['Seychelles', 'Mauritius', 'Maldives'],
    }
    
    def __init__(self):
        # Initialize OpenAI client
        if not OPENAI_API_KEY:
            print("[WARNING] Itinerary Agent: OPENAI_API_KEY not set, AI features disabled")
            self.client = None
        else:
            try:
                self.client = OpenAI(api_key=OPENAI_API_KEY)
                print("✅ Itinerary Agent: AI initialized")
            except Exception as e:
                print(f"[WARNING] Itinerary Agent: Could not initialize AI - {e}")
                self.client = None

    def get_region(self, country):
        """Get the geographic region for a country"""
        for region, countries in self.REGIONS.items():
            if country in countries:
                return region
        return 'Other'

    def sort_by_geography(self, cities):
        """Sort cities to minimize travel distance between them"""
        if len(cities) <= 1:
            return cities
        
        print(f"\n[GEO] Sorting {len(cities)} cities by travel efficiency...")
        
        # Start with the city that has highest score
        sorted_cities = []
        remaining = cities.copy()
        
        # Pick starting city (highest score)
        start_city = max(remaining, key=lambda x: x["score"])
        sorted_cities.append(start_city)
        remaining.remove(start_city)
        
        # Greedy algorithm: always go to nearest region/country
        while remaining:
            current = sorted_cities[-1]
            current_region = self.get_region(current["country"])
            
            # Find next city in same region, then same continent, then nearest region
            same_region = [c for c in remaining if self.get_region(c["country"]) == current_region]
            if same_region:
                # Within same region, pick by score
                same_region.sort(key=lambda x: x["score"], reverse=True)
                next_city = same_region[0]
            else:
                # Go to next closest region
                remaining.sort(key=lambda x: (
                    0 if self.get_region(x["country"]) in self.get_nearby_regions(current_region) else 1,
                    -x["score"]  # Higher score first
                ))
                next_city = remaining[0]
            
            sorted_cities.append(next_city)
            remaining.remove(next_city)
            print(f"[GEO]   → Added {next_city['destination']} ({self.get_region(next_city['country'])})")
        
        print(f"[GEO] Geographic sorting complete! Optimized route:")
        for i, city in enumerate(sorted_cities):
            print(f"[GEO]   {i+1}. {city['destination']}, {city['country']} ({self.get_region(city['country'])})")
        print()
        
        return sorted_cities

    def get_nearby_regions(self, region):
        """Define which regions are near each other"""
        region_groups = {
            'Southeast Asia': ['East Asia', 'South Asia', 'Oceania'],
            'East Asia': ['Southeast Asia', 'South Asia'],
            'South Asia': ['Southeast Asia', 'Middle East'],
            'Oceania': ['Southeast Asia'],
            'Middle East': ['South Asia', 'Africa North', 'Eastern Europe'],
            'Africa North': ['Middle East', 'Africa West', 'Africa East', 'Africa South'],
            'Africa West': ['Africa North', 'Africa East', 'Africa South'],
            'Africa East': ['Africa North', 'Africa West', 'Africa South', 'Middle East'],
            'Africa South': ['Africa North', 'Africa West', 'Africa East'],
            'Western Europe': ['Central Europe', 'Southern Europe', 'Northern Europe'],
            'Central Europe': ['Western Europe', 'Southern Europe', 'Eastern Europe', 'Northern Europe'],
            'Southern Europe': ['Western Europe', 'Central Europe', 'Eastern Europe', 'Middle East'],
            'Northern Europe': ['Western Europe', 'Central Europe', 'Eastern Europe'],
            'Eastern Europe': ['Central Europe', 'Southern Europe', 'Northern Europe', 'Middle East'],
            'North America': ['Central America', 'Caribbean'],
            'Central America': ['North America', 'South America', 'Caribbean'],
            'Caribbean': ['North America', 'Central America', 'South America'],
            'South America': ['Central America', 'Caribbean'],
        }
        return region_groups.get(region, [])

    def calculate_days_per_city(self, total_days):
        """Calculate optimal number of cities and days per city"""
        if total_days <= 3:
            num_cities = total_days
            days_per_city = 1
        elif total_days <= 7:
            num_cities = max(2, total_days // 2)
            days_per_city = total_days / num_cities
        elif total_days <= 14:
            num_cities = max(3, total_days // 3)
            days_per_city = total_days / num_cities
        else:
            num_cities = max(4, total_days // 4)
            days_per_city = total_days / num_cities
        
        print(f"[PLAN] Itinerary Agent: Planning {num_cities} cities with ~{days_per_city:.1f} days each")
        return days_per_city, num_cities

    def build_itinerary(self, ranked_cities, total_days, interests):
        """Build complete itinerary with day distribution and geographic sorting"""
        print(f"\n[BUILD] Itinerary Agent: Building {total_days}-day itinerary...")
        
        days_per_city, num_cities = self.calculate_days_per_city(total_days)
        
        # Select top cities
        selected_cities = ranked_cities[:num_cities]
        
        # Sort by geography to minimize travel
        sorted_cities = self.sort_by_geography(selected_cities)
        
        itinerary = []
        matched_interests_list = []
        activity_interest_map_list = []
        
        days_assigned = 0
        
        for i, city_data in enumerate(sorted_cities):
            # Calculate days for this city
            if i == len(sorted_cities) - 1:
                city_days = total_days - days_assigned
            else:
                city_days = int(days_per_city)
                if days_assigned + city_days < total_days:
                    remaining = total_days - days_assigned - city_days
                    cities_left = len(sorted_cities) - i - 1
                    if cities_left > 0 and remaining / cities_left > days_per_city:
                        city_days += 1
            
            days_assigned += city_days
            
            # Generate itinerary suggestion for multi-day stays
            itinerary_suggestion = self._generate_itinerary_suggestion(
                city_data, city_days, interests
            )
            
            itinerary.append({
                "destination": city_data["destination"],
                "country": city_data["country"],
                "description": city_data["description"],
                "activities": city_data["activities"],
                "score": city_data["score"],
                "days": city_days,
                "itinerary_suggestion": itinerary_suggestion,
                "region": self.get_region(city_data["country"]),  # Add region info
                "matched": city_data["matched"],
                "activity_matches": city_data.get("activity_matches", {})
            })
            matched_interests_list.append(city_data["matched"])
            activity_interest_map_list.append(city_data.get("activity_matches", {}))
        
        print(f"✅ Itinerary Agent: Created geographically optimized itinerary for {len(itinerary)} cities")
        return itinerary, matched_interests_list, activity_interest_map_list

    def _generate_itinerary_suggestion(self, city_data, days, interests):
        """Generate day-by-day itinerary suggestion"""
        if days == 1:
            return None
        
        if self.client:
            return self._generate_with_ai(city_data, days, interests)
        else:
            return self._generate_generic(city_data["destination"], days)

    def _generate_with_ai(self, city_data, days, interests):
        """Use AI to generate personalized itinerary with ALL days"""
        try:
            activities_sample = ', '.join(city_data['activities'][:3]) if city_data['activities'] else 'typical activities'
            
            prompt = f"""Create a {days}-day itinerary for {city_data['destination']} based on these interests: {', '.join(interests[:4])}.

Available activities: {activities_sample}

Format: Day 1: [activity]. Day 2: [activity]. Day 3: [activity]...
Cover ALL {days} days. Keep each day to 8-10 words maximum."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                temperature=0.8,
                max_tokens=120
            )
            
            suggestion = response.choices[0].message.content.strip()
            print(f"[AI] Itinerary Agent: Generated {days}-day plan for {city_data['destination']}")
            return suggestion
                
        except Exception as e:
            print(f"[WARNING] Itinerary Agent: AI failed - {e}, using generic")
            return self._generate_generic(city_data["destination"], days)

    def _generate_generic(self, city_name, days):
        """Fallback generic itinerary that covers ALL days"""
        if days == 2:
            return "Day 1: Explore major attractions and landmarks. Day 2: Experience local culture and cuisine."
        elif days == 3:
            return "Day 1: Visit top sights. Day 2: Focus on your interests. Day 3: Discover hidden gems."
        elif days == 4:
            return "Day 1: Main attractions. Day 2: Cultural experiences. Day 3: Your interests. Day 4: Relaxation and local neighborhoods."
        elif days == 5:
            return "Day 1: Iconic landmarks. Day 2: Museums and culture. Day 3: Your favorite activities. Day 4: Day trip or nature. Day 5: Shopping and farewell."
        else:
            return f"Spend {days} days exploring {city_name}: Mix major sights (Days 1-2), your interests (Days 3-4), and local experiences (remaining days)."