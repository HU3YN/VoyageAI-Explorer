# preference_agent.py - IMPROVED KEYWORD NORMALIZATION
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class PreferenceAgent:
    """Agent responsible for extracting and understanding user preferences using SEMANTIC AI"""
    
    def __init__(self):
        # Initialize OpenAI client
        if not OPENAI_API_KEY:
            print("⚠️ Preference Agent: OPENAI_API_KEY not set, AI features disabled")
            self.client = None
        else:
            try:
                self.client = OpenAI(api_key=OPENAI_API_KEY)
                print("✅ Preference Agent: AI initialized with SEMANTIC understanding")
            except Exception as e:
                print(f"❌ Preference Agent: Could not initialize AI - {e}")
                self.client = None
        
        # Cache for fast repeated queries
        self.cache = {}
        
        # ⭐ IMPROVED: Map variations to database keywords
        self.keyword_normalization = {
            # Singular -> Plural
            'beach': 'beaches',
            'mountain': 'mountains',
            'temple': 'temples',
            'museum': 'museums',
            'bar': 'bars',
            'club': 'clubs',
            'market': 'markets',
            'boutique': 'boutiques',
            
            # Activity forms
            'ski': 'skiing',
            'hike': 'hiking',
            'dive': 'diving',
            'surf': 'surfing',
            'climb': 'climbing',
            'shop': 'shopping',
            'swim': 'swimming',
            
            # Common variations
            'food': 'food',
            'eat': 'food',
            'dining': 'food',
            'restaurant': 'food',
            'cuisine': 'food',
            
            # Semantic relationships for better matching
            'hiking': 'hiking,trekking,mountains,nature,outdoor',
            'trekking': 'hiking,trekking,mountains',
            'mountains': 'hiking,mountains,nature',
            'nature': 'hiking,nature,outdoor',
            'outdoor': 'hiking,nature,outdoor',
            'sushi': 'sushi,japanese,food,asian',
            'japanese': 'sushi,japanese,food,asian',
            'cars': 'cars,automotive,racing,motor',
            'car': 'cars,automotive,racing,motor',
            'anime': 'anime,japanese,culture,entertainment',
            'pokemon': 'anime,japanese,gaming',
            'ferrari': 'cars,italian,automotive,luxury',
            'wine': 'wine,vineyard,french,italian',
            'coffee': 'coffee,cafe,breakfast',
        }
        
        # Fallback expansions (only used if AI fails)
        self.expansions = {
            "sushi": ["sushi", "japanese", "food", "asian"],
            "ramen": ["ramen", "japanese", "food", "noodles"],
            "korean": ["korean", "food", "asian"],
            "hiking": ["hiking", "mountains", "nature", "outdoor"],
            "beaches": ["beaches", "ocean", "coastal", "tropical"],
            "beach": ["beaches", "ocean", "coastal", "tropical"],
            "culture": ["culture", "history", "museums", "art"],
            "nightlife": ["nightlife", "bars", "clubs", "entertainment"],
            "shopping": ["shopping", "markets", "boutiques"],
            "pasta": ["pasta", "italian", "food"],
            "pizza": ["pizza", "italian", "food"],
            "cars": ["cars", "automotive", "racing", "motor"],
            "car": ["cars", "automotive", "racing", "motor"],
            "mountains": ["hiking", "mountains", "nature", "trekking"],
            "nature": ["hiking", "mountains", "nature", "outdoor"],
            "outdoor": ["hiking", "mountains", "nature", "outdoor"],
            "japanese": ["sushi", "japanese", "food", "asian"],
            "anime": ["anime", "japanese", "culture", "entertainment"],
            "wine": ["wine", "vineyard", "french", "italian"],
            "coffee": ["coffee", "cafe", "breakfast", "morning"],
        }

    def extract_preferences(self, user_input):
        """Extract user preferences - normalize keywords for better matching"""
        print(f"🧠 Preference Agent: Analyzing input...")
        
        # Check cache first
        cache_key = user_input.lower().strip()
        if cache_key in self.cache:
            print(f"   ⚡ Using cached result")
            return self.cache[cache_key]
        
        # Extract words from input - FILTER OUT common verbs
        stop_words = {
            'and', 'the', 'like', 'love', 'want', 'need', 'going', 'drinking', 
            'playing', 'eating', 'watching', 'play', 'drink', 'eat', 'watch', 'go'
        }
        words = [w.strip().lower() for w in user_input.replace(',', ' ').split() 
                 if len(w.strip()) > 2 and w.strip() not in stop_words]
        
        # Check which words are KNOWN keywords vs UNKNOWN
        known_keywords = self._check_database_keywords(words)
        unknown_words = [w for w in words if w not in known_keywords and w not in [self.keyword_normalization.get(w, w) for w in known_keywords]]
        
        result = []
        
        # ⭐ CRITICAL: Add KNOWN keywords directly WITHOUT AI expansion
        if known_keywords:
            result.extend(known_keywords)
            print(f"   ✅ Found exact keywords: {known_keywords}")
        
        # Use AI ONLY for unknown words
        if unknown_words and self.client:
            print(f"   🤖 Using AI for unknown terms: {unknown_words}")
            ai_expansions = self._expand_unknown_with_ai(unknown_words)
            # Only add AI expansions that aren't already in result
            for exp in ai_expansions:
                if exp not in result:
                    result.append(exp)
        elif unknown_words:
            print(f"   ⚠️ Unknown terms (no AI): {unknown_words}")
            for word in unknown_words:
                if word not in result:
                    result.append(word)
        
        # Limit to 7 keywords max
        final = result[:7]
        
        # Cache the result
        self.cache[cache_key] = final
        print(f"   📋 Final interests: {final}")
        return final

    def _check_database_keywords(self, words):
        """Check which words are actual keywords in the database"""
        # Common travel keywords that exist in database
        known_db_keywords = {
            # IMPORTANT: Keep exact food terms
            'sushi', 'ramen', 'pasta', 'pizza', 'tacos', 'curry',
            # Japanese
            'japanese', 'japan', 'asian', 'anime', 'tokyo', 'osaka', 'kyoto',
            # Food (general)
            'food', 'culinary', 'street food',
            # Beaches (PLURAL - what's in database)
            'beaches', 'ocean', 'tropical', 'coastal', 'swimming',
            # Hiking/Nature
            'hiking', 'mountains', 'nature', 'outdoor', 'trekking',
            # Winter
            'skiing', 'ski', 'snow', 'winter', 'cold', 'ice',
            # Culture
            'culture', 'history', 'museums', 'art', 'temples',
            # Nightlife
            'nightlife', 'bars', 'clubs', 'party', 'entertainment',
            # Shopping
            'shopping', 'markets', 'boutiques',
            # Countries/regions
            'italian', 'french', 'spanish', 'mexican', 'thai', 'korean',
            # Cars
            'cars', 'automotive', 'racing', 'motor', 'vehicles',
            # Beverages
            'wine', 'coffee', 'tea', 'chocolate',
            # Activities
            'adventure', 'relaxation', 'luxury', 'budget',
            'diving', 'surfing', 'snorkeling', 'golf',
            # Entertainment
            'gaming', 'movies', 'music', 'concerts',
        }
        
        found = []
        for word in words:
            word_lower = word.lower()
            
            # ⭐ NORMALIZE: Check if word should be converted (beach -> beaches)
            normalized_word = self.keyword_normalization.get(word_lower, word_lower)
            
            # If the normalized word contains multiple keywords (comma separated)
            if ',' in normalized_word:
                keywords = [kw.strip() for kw in normalized_word.split(',')]
                for kw in keywords:
                    if kw in known_db_keywords and kw not in found:
                        found.append(kw)
            # Exact match in known keywords (using normalized form)
            elif normalized_word in known_db_keywords and normalized_word not in found:
                found.append(normalized_word)
            # Check original word too
            elif word_lower in known_db_keywords and word_lower not in found:
                found.append(word_lower)
        
        # Check expansions dict
        for word in words:
            word_lower = word.lower()
            if word_lower in self.expansions:
                for exp in self.expansions[word_lower]:
                    if exp in known_db_keywords and exp not in found:
                        found.append(exp)
        
        return found

    def _expand_unknown_with_ai(self, unknown_words):
        """Use AI ONLY to expand unknown/niche terms like 'Pokemon', 'Ferrari'"""
        try:
            unknown_text = ", ".join(unknown_words)
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "system",
                    "content": """You help identify travel-relevant keywords for niche interests.

Examples:
- "Pokemon" → anime, japanese, gaming, akihabara, tokyo
- "Ferrari" → cars, italian, automotive, luxury, racing
- "Star Wars" → movies, tunisia, ireland, filming locations
- "K-pop" → korean, music, seoul, entertainment

Return ONLY comma-separated travel keywords (no brackets, quotes)."""
                    },
                    {
                        "role": "user",
                        "content": f"What travel keywords match: {unknown_text}"
                    }
                ],
                temperature=0.7,
                max_tokens=40
            )
            
            content = response.choices[0].message.content.strip()
            content = content.replace('[', '').replace(']', '').replace('"', '').replace("'", '')
            keywords = [k.strip().lower() for k in content.split(',') if k.strip()]
            
            print(f"      → AI expansion: {unknown_words} → {keywords}")
            return keywords[:5]
                
        except Exception as e:
            print(f"      ⚠️ AI expansion failed: {e}")
            return unknown_words

    def _extract_with_semantic_ai(self, user_input):
        """Legacy method - now handled by extract_preferences"""
        return self.extract_preferences(user_input)

    def _extract_fallback(self, user_input):
        """Fallback without AI - just use known keywords"""
        words = [w.strip().lower() for w in user_input.replace(',', ' ').split() 
                 if len(w.strip()) > 2]
        return self._check_database_keywords(words)[:5]