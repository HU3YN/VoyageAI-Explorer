# fix_activities.py - Add missing activities to cities
import sqlite3

conn = sqlite3.connect('travel_data.db')
cursor = conn.cursor()

print("\n[FIX] Checking for cities with missing or generic activities...\n")

# Get all cities with their activities
cursor.execute('''
    SELECT c.id, c.name, c.country, c.keywords, 
           (SELECT COUNT(*) FROM activities WHERE city_id = c.id) as activity_count
    FROM cities c
''')

cities = cursor.fetchall()

fixed_count = 0

for city_id, name, country, keywords, activity_count in cities:
    # Get existing activities
    cursor.execute('SELECT activity FROM activities WHERE city_id = ?', (city_id,))
    existing_activities = [row[0] for row in cursor.fetchall()]
    
    # Check if city has no activities or only generic ones
    needs_fix = False
    
    if activity_count == 0:
        print(f"[NO ACTIVITIES] {name}, {country}")
        needs_fix = True
    elif activity_count < 4:
        print(f"[FEW ACTIVITIES] {name}, {country} (only {activity_count})")
        needs_fix = True
    
    if needs_fix:
        # Create activities based on keywords
        keywords_list = keywords.split(',') if keywords else []
        new_activities = []
        
        # Food activities
        if any(kw in keywords_list for kw in ['food', 'sushi', 'japanese', 'culinary', 'ramen', 'asian']):
            new_activities.append(("Try authentic local cuisine at renowned restaurants.", "food,culinary"))
            new_activities.append(("Take a food tour to sample street food and local specialties.", "food,culture"))
        
        # Skiing activities
        if any(kw in keywords_list for kw in ['skiing', 'snow', 'winter', 'ski']):
            new_activities.append(("Hit the slopes for world-class skiing and snowboarding.", "skiing,adventure,winter"))
            new_activities.append(("Enjoy après-ski at cozy mountain lodges and restaurants.", "nightlife,relaxation,food"))
            new_activities.append(("Take scenic gondola rides for breathtaking mountain views.", "nature,adventure"))
        
        # Beach activities
        if any(kw in keywords_list for kw in ['beaches', 'ocean', 'tropical', 'coastal']):
            new_activities.append(("Relax on pristine beaches and swim in crystal-clear waters.", "beaches,relaxation"))
            new_activities.append(("Try water sports like snorkeling, diving, or kayaking.", "adventure,beaches"))
            new_activities.append(("Watch spectacular sunsets over the ocean.", "beaches,nature,relaxation"))
        
        # Hiking/Nature activities
        if any(kw in keywords_list for kw in ['hiking', 'mountains', 'nature', 'outdoor']):
            new_activities.append(("Explore scenic hiking trails and mountain landscapes.", "hiking,nature,adventure"))
            new_activities.append(("Enjoy outdoor activities and connect with nature.", "nature,outdoor,adventure"))
        
        # Culture activities
        if any(kw in keywords_list for kw in ['culture', 'history', 'museums', 'temples']):
            new_activities.append(("Visit historic landmarks and cultural sites.", "culture,history"))
            new_activities.append(("Explore museums and art galleries.", "culture,art,museums"))
        
        # Car/Automotive activities
        if any(kw in keywords_list for kw in ['cars', 'automotive', 'racing']):
            new_activities.append(("Visit automotive museums showcasing classic and modern vehicles.", "cars,museums"))
            new_activities.append(("Tour car manufacturing facilities or racing circuits.", "cars,automotive,adventure"))
        
        # Shopping activities
        if any(kw in keywords_list for kw in ['shopping']):
            new_activities.append(("Shop at local markets and boutiques for unique souvenirs.", "shopping,culture"))
        
        # Nightlife activities
        if any(kw in keywords_list for kw in ['nightlife', 'party']):
            new_activities.append(("Experience vibrant nightlife at bars and clubs.", "nightlife,entertainment"))
        
        # Add generic activities if still too few
        if len(new_activities) < 4:
            new_activities.append(("Explore the city's main attractions and landmarks.", "culture,sightseeing"))
            new_activities.append(("Discover local neighborhoods and hidden gems.", "culture,exploration"))
            new_activities.append(("Experience authentic local culture and traditions.", "culture"))
        
        # Remove duplicates and limit to 6 activities
        seen = set(existing_activities)
        activities_to_add = []
        
        for activity, act_keywords in new_activities:
            if activity not in seen and len(activities_to_add) < 6:
                activities_to_add.append((activity, act_keywords))
                seen.add(activity)
        
        # Insert new activities
        for activity, act_keywords in activities_to_add:
            cursor.execute(
                'INSERT INTO activities (city_id, activity, keywords) VALUES (?, ?, ?)',
                (city_id, activity, act_keywords)
            )
        
        if activities_to_add:
            print(f"  [FIXED] Added {len(activities_to_add)} activities to {name}, {country}")
            fixed_count += 1

conn.commit()

# Show final stats
cursor.execute('SELECT COUNT(*) FROM cities WHERE id IN (SELECT city_id FROM activities GROUP BY city_id HAVING COUNT(*) > 0)')
cities_with_activities = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM cities')
total_cities = cursor.fetchone()[0]

conn.close()

print(f"\n{'='*60}")
print(f"[SUCCESS] Activities fix complete!")
print(f"{'='*60}")
print(f"Statistics:")
print(f"  * Fixed: {fixed_count} cities")
print(f"  * Cities with activities: {cities_with_activities}/{total_cities}")
print(f"{'='*60}\n")