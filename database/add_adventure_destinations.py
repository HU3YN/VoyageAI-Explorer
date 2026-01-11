# update_adventure_keywords.py - Update existing destinations with adventure keywords
import sqlite3

conn = sqlite3.connect('travel_data.db')
cursor = conn.cursor()

# Cities that should have adventure keywords
adventure_updates = {
    # Format: (city, country): (new_keywords_to_add, updated_description)
    ("Queenstown", "New Zealand"): (
        "adventure,hiking,mountains,nature,skiing,extreme,outdoor",
        "Adventure capital of the world with skiing, bungee jumping, hiking, and extreme sports in stunning landscapes."
    ),
    ("Interlaken", "Switzerland"): (
        "adventure,hiking,mountains,skiing,nature,outdoor,extreme",
        "Alpine adventure capital between two lakes with access to Jungfrau region for hiking and extreme sports."
    ),
    ("Banff", "Canada"): (
        "adventure,hiking,mountains,skiing,nature,outdoor,wildlife,winter",
        "Stunning mountain town in Canadian Rockies with world-class skiing, hiking, and natural beauty."
    ),
    ("Chamonix", "France"): (
        "adventure,hiking,mountains,skiing,extreme,nature,outdoor,winter",
        "Historic alpine town beneath Mont Blanc offering extreme skiing, mountaineering, and hiking."
    ),
    ("Patagonia", "Argentina"): (
        "adventure,hiking,mountains,nature,outdoor,trekking,wildlife",
        "Remote wilderness region offering world-class trekking, glaciers, and dramatic mountain landscapes."
    ),
    ("Patagonia", "Chile"): (
        "adventure,hiking,mountains,nature,outdoor,trekking,wildlife",
        "Southern wilderness with Torres del Paine National Park, glaciers, and trekking adventures."
    ),
    ("Moab", "United States"): (
        "adventure,hiking,mountains,nature,outdoor,desert,climbing",
        "Desert adventure hub near Arches and Canyonlands National Parks with world-class rock climbing."
    ),
    ("Whistler", "Canada"): (
        "adventure,skiing,mountains,winter,outdoor,nature,hiking",
        "Top ski destination hosting Winter Olympics with incredible mountain scenery and summer hiking."
    ),
    ("Kathmandu", "Nepal"): (
        "adventure,hiking,mountains,trekking,nature,culture,outdoor",
        "Gateway to Himalayan trekking, Mt. Everest base camp, and ancient temples."
    ),
    ("Pokhara", "Nepal"): (
        "adventure,hiking,mountains,trekking,nature,outdoor,paragliding",
        "Tranquil lakeside city that serves as the gateway to the Annapurna mountain range trekking."
    ),
    ("Lake Tahoe", "United States"): (
        "adventure,skiing,mountains,winter,beaches,outdoor,nature,hiking",
        "California/Nevada border offering multiple ski resorts, hiking, and beautiful lake beaches."
    ),
    ("Reykjavik", "Iceland"): (
        "adventure,nature,hiking,winter,cold,aurora,outdoor,volcanic",
        "Gateway to geothermal wonders, Northern Lights, glacier hiking, and volcanic landscapes."
    ),
    ("Cairns", "Australia"): (
        "adventure,beaches,diving,tropical,nature,outdoor,reef",
        "Gateway to the Great Barrier Reef and ancient Daintree Rainforest with diving and nature."
    ),
    ("Costa Rica", "Costa Rica"): (
        "adventure,nature,hiking,beaches,wildlife,outdoor,tropical,surfing",
        "Eco-paradise offering Pacific and Caribbean beaches plus rainforest adventures and wildlife."
    ),
}

updated_count = 0
not_found_count = 0

print(" Updating adventure destinations ...\n")

for (city, country), (new_keywords, description) in adventure_updates.items():
    cursor.execute('SELECT id, keywords FROM cities WHERE name = ? AND country = ?', (city, country))
    result = cursor.fetchone()
    
    if result:
        city_id, existing_keywords = result
        
        # Merge keywords (remove duplicates)
        if existing_keywords:
            all_keywords = existing_keywords + ',' + new_keywords
        else:
            all_keywords = new_keywords
        
        # Remove duplicates
        unique_keywords = ','.join(set(all_keywords.split(',')))
        
        # Update city
        cursor.execute(
            'UPDATE cities SET description = ?, keywords = ? WHERE id = ?',
            (description, unique_keywords, city_id)
        )
        
        # Add adventure activities if not present
        cursor.execute('SELECT COUNT(*) FROM activities WHERE city_id = ? AND keywords LIKE "%adventure%"', (city_id,))
        has_adventure = cursor.fetchone()[0] > 0
        
        if not has_adventure:
            adventure_activities = [
                ("Go hiking or trekking in stunning natural landscapes.", "hiking,adventure,nature,outdoor"),
                ("Try extreme sports and adrenaline activities.", "adventure,extreme,outdoor"),
                ("Explore mountains, valleys, and wilderness areas.", "nature,adventure,hiking,mountains"),
            ]
            
            for activity, act_keywords in adventure_activities:
                cursor.execute(
                    'INSERT INTO activities (city_id, activity, keywords) VALUES (?, ?, ?)',
                    (city_id, activity, act_keywords)
                )
        
        updated_count += 1
        print(f" Updated: {city}, {country}")
    else:
        not_found_count += 1
        print(f" Not found in database: {city}, {country}")

conn.commit()

# Show statistics
cursor.execute('SELECT COUNT(*) FROM cities WHERE keywords LIKE "%adventure%" OR keywords LIKE "%hiking%"')
adventure_cities = cursor.fetchone()[0]

conn.close()

print(f"\n{'='*60}")
print(f" Adventure destinations update complete!")
print(f" Statistics:")
print(f"    Destinations updated: {updated_count}")
print(f"    Not found: {not_found_count}")
print(f"    Total adventure destinations: {adventure_cities}")
print(f"{'='*60}")