# destination_agent.py - FINAL FIXED VERSION WITH DIVERSITY IMPROVEMENTS
import sqlite3
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class DestinationAgent:
    """Agent responsible for ranking cities with SEMANTIC AI understanding"""
    
    def __init__(self):
        self.conn = sqlite3.connect('travel_data.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        if not OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY not set. Please configure environment variable.")
        
        try:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            print("✅ Destination Agent: Database + AI semantic matching ready")
        except Exception as e:
            print(f"⚠️ Destination Agent: AI unavailable - {e}")
            self.client = None

    def rank_cities_with_semantic_ai(self, interests, num_cities):
        """Rank cities with improved keyword matching"""
        print(f"🎯 Destination Agent: Ranking for: {interests}")
        
        self.cursor.execute('SELECT id, name, country, description, keywords FROM cities')
        cities = self.cursor.fetchall()
        
        print(f"   📊 Keyword matching {len(cities)} cities...")
        
        pre_scored = []
        for city in cities:
            city_id, name, country, description, keywords = city
            keywords_list = [k.strip() for k in keywords.split(',')] if keywords else []
            
            exact_score = 0
            matched = []
            
            for interest in interests:
                interest_lower = interest.lower().strip()
                
                # 🔍 IMPROVED MATCHING - Multiple strategies
                if self._keyword_matches(interest_lower, keywords_list, description):
                    match_type, score = self._get_match_score(interest_lower, keywords_list, description)
                    exact_score += score
                    matched.append(interest)
            
            # Normalize to percentage
            max_possible = len(interests) * 100
            normalized_score = int((exact_score / max_possible) * 100) if max_possible > 0 else 0
            
            pre_scored.append({
                'city': city,
                'keyword_score': normalized_score,
                'exact_score': exact_score,
                'matched': list(set(matched))
            })
        
        pre_scored.sort(key=lambda x: (x['keyword_score'], x['exact_score']), reverse=True)
        
        high_matches = [c for c in pre_scored if c['keyword_score'] >= 25]
        all_others = [c for c in pre_scored if c['keyword_score'] < 25]
        
        print(f"   ✅ Found {len(high_matches)} strong keyword matches (≥25%)")
        
        final_scored = []
        
        # Process high matches
        for candidate in high_matches[:60]:
            city_id, name, country, description, keywords = candidate['city']
            
            self.cursor.execute('SELECT activity, keywords FROM activities WHERE city_id = ?', (city_id,))
            activities_data = self.cursor.fetchall()
            activities = [act[0] for act in activities_data]
            
            activity_boost, activity_matches = self._score_activities(activities_data, interests)
            final_score = min(100, candidate['keyword_score'] + activity_boost)
            
            final_scored.append({
                "destination": name,
                "country": country,
                "description": description,
                "activities": activities,
                "score": final_score,
                "matched": candidate['matched'],
                "activity_matches": activity_matches,
                "match_count": len(candidate['matched'])
            })
        
        # AI scoring for lower matches
        if all_others and self.client:
            print(f"   🤖 Using AI for {min(40, len(all_others))} other cities")
            ai_candidates = all_others[:40]
            
            city_summaries = [f"{c['city'][1]}, {c['city'][2]}: {c['city'][3][:80]}" 
                            for c in ai_candidates]
            
            ai_scores = self._ai_score_cities_detailed(city_summaries, interests)
            
            for i, candidate in enumerate(ai_candidates):
                ai_score = ai_scores[i] if i < len(ai_scores) else 0
                
                if ai_score >= 35:
                    city_id, name, country, description, keywords = candidate['city']
                    
                    self.cursor.execute('SELECT activity, keywords FROM activities WHERE city_id = ?', (city_id,))
                    activities_data = self.cursor.fetchall()
                    activities = [act[0] for act in activities_data]
                    
                    activity_boost, activity_matches = self._score_activities(activities_data, interests)
                    final_score = min(100, ai_score + activity_boost)
                    
                    final_scored.append({
                        "destination": name,
                        "country": country,
                        "description": description,
                        "activities": activities,
                        "score": final_score,
                        "matched": candidate['matched'] if candidate['matched'] else interests[:1],
                        "activity_matches": activity_matches,
                        "match_count": max(1, len(candidate['matched']))
                    })
        
        final_scored.sort(key=lambda x: (x["score"], x["match_count"]), reverse=True)
        final_scored = [city for city in final_scored if city["score"] >= 15]
        
        if not final_scored:
            print(f"   ⚠️ No matches found, using top results")
            final_scored = []
            for candidate in (high_matches[:num_cities] if high_matches else pre_scored[:num_cities]):
                city_id, name, country, description, keywords = candidate['city']
                self.cursor.execute('SELECT activity, keywords FROM activities WHERE city_id = ?', (city_id,))
                activities_data = self.cursor.fetchall()
                activities = [act[0] for act in activities_data]
                activity_boost, activity_matches = self._score_activities(activities_data, interests)
                final_scored.append({
                    "destination": name,
                    "country": country,
                    "description": description,
                    "activities": activities,
                    "score": max(15, candidate['keyword_score']),
                    "matched": candidate['matched'],
                    "activity_matches": activity_matches,
                    "match_count": len(candidate['matched'])
                })
        
        print(f"   ⚡ Ranking complete! Top: {final_scored[0]['destination']} ({final_scored[0]['score']}%)")
        print(f"   📊 Total cities: {len(final_scored)}")
        
        return self._apply_diversity(final_scored, interests, num_cities)

    def _keyword_matches(self, interest, keywords_list, description):
        """Check if interest matches any keyword or description"""
        interest_lower = interest.lower()
        
        # Exact match
        if interest_lower in keywords_list:
            return True
        
        # Singular/plural variants
        for kw in keywords_list:
            if len(kw) < 2:
                continue
            # beach <-> beaches, mountain <-> mountains
            if (interest_lower == kw + 's' or interest_lower + 's' == kw or
                interest_lower == kw + 'es' or interest_lower + 'es' == kw):
                return True
            # ski <-> skiing, hike <-> hiking
            if (interest_lower + 'ing' == kw or kw + 'ing' == interest_lower):
                return True
            # Contains match (for longer words)
            if len(interest_lower) > 3 and len(kw) > 3:
                if interest_lower in kw or kw in interest_lower:
                    return True
        
        # Description match
        if interest_lower in description.lower():
            return True
        
        return False

    def _get_match_score(self, interest, keywords_list, description):
        """Get match score based on match type"""
        # Exact match = 100
        if interest in keywords_list:
            return ("exact", 100)
        
        # Singular/plural = 95
        for kw in keywords_list:
            if (interest == kw + 's' or interest + 's' == kw or
                interest == kw + 'es' or interest + 'es' == kw or
                interest + 'ing' == kw or kw + 'ing' == interest):
                return ("variant", 95)
        
        # Substring match = 70
        for kw in keywords_list:
            if len(interest) > 3 and len(kw) > 3:
                if interest in kw or kw in interest:
                    return ("partial", 70)
        
        # Description = 40
        if interest in description.lower():
            return ("description", 40)
        
        return ("none", 0)

    def _score_activities(self, activities_data, interests):
        """Score activities and return which activities matched"""
        boost = 0
        activity_matches = {}
        
        for activity_text, activity_keywords in activities_data:
            act_kw_list = [k.strip() for k in activity_keywords.split(',')] if activity_keywords else []
            for interest in interests:
                if interest.lower() in act_kw_list or interest.lower() in activity_text.lower():
                    boost += 3
                    if interest not in activity_matches:
                        activity_matches[interest] = []
                    activity_matches[interest].append(activity_text)
        
        return min(20, boost), activity_matches

    def _ai_score_cities_detailed(self, city_summaries, interests):
        """AI scoring"""
        if not self.client:
            return [40] * len(city_summaries)
        
        try:
            interests_text = ", ".join(interests)
            all_scores = []
            
            for i in range(0, len(city_summaries), 15):
                batch = city_summaries[i:i+15]
                cities_text = "\n".join([f"{j+1}. {city}" for j, city in enumerate(batch)])
                
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{
                        "role": "system",
                        "content": "Score cities 0-100 for interest match. Return only comma-separated numbers."
                    }, {
                        "role": "user",
                        "content": f"Interests: {interests_text}\nCities:\n{cities_text}\n\nScores:"
                    }],
                    temperature=0.5,
                    max_tokens=100
                )
                
                scores_text = response.choices[0].message.content.strip()
                scores = [min(100, int(s.strip())) for s in scores_text.replace('\n', ',').split(',') 
                         if s.strip().isdigit()]
                
                while len(scores) < len(batch):
                    scores.append(40)
                
                all_scores.extend(scores[:len(batch)])
            
            return all_scores
        except Exception as e:
            print(f"⚠️ AI scoring failed: {e}")
            return [40] * len(city_summaries)

    def _apply_diversity(self, scored_cities, interests, num_cities):
        """Select cities to maximize coverage of ALL interests"""
        print("   🎯 Applying diversity logic to cover all interests...")
        
        selected = []
        interest_coverage = {interest: False for interest in interests}  # Track which interests are covered
        
        # Sort cities by how many UNCOVERED interests they match
        remaining_cities = scored_cities.copy()
        
        # Phase 1: Ensure each interest is covered at least once
        while len(selected) < num_cities and interests:
            best_city = None
            best_new_coverage = 0
            
            for city in remaining_cities:
                # Count how many uncovered interests this city would cover
                uncovered_matched = [
                    interest for interest in city["matched"] 
                    if not interest_coverage.get(interest, False)
                ]
                new_coverage = len(uncovered_matched)
                
                # Prefer cities that cover multiple uncovered interests
                if new_coverage > best_new_coverage:
                    best_new_coverage = new_coverage
                    best_city = city
                elif new_coverage == best_new_coverage and new_coverage > 0:
                    # Tie-break: higher score
                    if not best_city or city["score"] > best_city["score"]:
                        best_city = city
            
            if best_city:
                selected.append(best_city)
                remaining_cities.remove(best_city)
                
                # Update coverage
                for interest in best_city["matched"]:
                    interest_coverage[interest] = True
                
                print(f"   {len(selected)}️⃣ {best_city['destination']} ({best_city['score']}%): {best_city['matched']} [{best_city['match_count']} matches]")
            else:
                break  # No more cities that cover new interests
        
        # Phase 2: If we still need more cities, add best overall matches
        while len(selected) < num_cities and remaining_cities:
            # Sort remaining by score
            remaining_cities.sort(key=lambda x: x["score"], reverse=True)
            best_city = remaining_cities[0]
            selected.append(best_city)
            remaining_cities = remaining_cities[1:]
            print(f"   {len(selected)}️⃣ {best_city['destination']} ({best_city['score']}%): {best_city['matched']} [{best_city['match_count']} matches]")
        
        # Print coverage
        covered_interests = [interest for interest, covered in interest_coverage.items() if covered]
        print(f"\n✅ Coverage: {covered_interests}")
        uncovered = set(interests) - set(covered_interests)
        if uncovered:
            print(f"⚠️ Uncovered: {list(uncovered)}")
        
        return selected

    def rank_cities_with_db(self, interests, num_cities):
        """Main method"""
        return self.rank_cities_with_semantic_ai(interests, num_cities)

    def get_random_cities(self, num_cities):
        """Random cities"""
        self.cursor.execute('SELECT id, name, country, description FROM cities ORDER BY RANDOM() LIMIT ?', (num_cities,))
        cities = self.cursor.fetchall()
        
        result = []
        for city_id, name, country, desc in cities:
            self.cursor.execute('SELECT activity FROM activities WHERE city_id = ?', (city_id,))
            activities = [row[0] for row in self.cursor.fetchall()]
            
            result.append({
                "destination": name,
                "country": country,
                "description": desc,
                "activities": activities,
                "score": 60,
                "matched": [],
                "activity_matches": {},
                "match_count": 0
            })
        
        return result

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()