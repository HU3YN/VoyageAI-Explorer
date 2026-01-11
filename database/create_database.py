# create_database.py - ALL-IN-ONE DATABASE CREATOR (Windows Safe)
import sqlite3
import json
import os

print("\n" + "="*60)
print("[START] CREATING COMPLETE TRAVEL DATABASE")
print("="*60 + "\n")

# Create database
conn = sqlite3.connect('travel_data.db')
cursor = conn.cursor()

# Drop existing tables
cursor.execute('DROP TABLE IF EXISTS activities')
cursor.execute('DROP TABLE IF EXISTS cities')

# Create tables
cursor.execute('''
CREATE TABLE cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    description TEXT,
    keywords TEXT
)
''')

cursor.execute('''
CREATE TABLE activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_id INTEGER,
    activity TEXT NOT NULL,
    keywords TEXT,
    FOREIGN KEY (city_id) REFERENCES cities(id)
)
''')

print("[OK] Database tables created\n")

# ====================
# PART 1: Load from JSON
# ====================
print("[PART 1] Loading destinations from JSON...")

# Check both possible locations for destinations.json 
json_paths = [
    'destinations.json',  # Root folder
    os.path.join('database', 'destinations.json'),  # Database folder
]

json_file = None
for path in json_paths:
    if os.path.exists(path):
        json_file = path
        print(f"[INFO] Found destinations.json at: {path}")
        break

if json_file:
    with open(json_file, 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    for country_data in countries:
        country = country_data['country']
        for city in country_data['cities']:
            desc = city.get('description', '').lower()
            keywords = []
            
            # Extract themes
            if any(word in desc for word in ['food', 'cuisine', 'dining', 'gastronom', 'culinary']):
                keywords.append('food')
            if any(word in desc for word in ['beach', 'coast', 'ocean', 'sea', 'island']):
                keywords.append('beaches')
            if any(word in desc for word in ['mountain', 'hiking', 'nature', 'outdoor', 'trek']):
                keywords.append('hiking')
            if any(word in desc for word in ['culture', 'history', 'museum', 'heritage', 'art', 'temple']):
                keywords.append('culture')
            if any(word in desc for word in ['night', 'vibrant', 'party', 'entertainment']):
                keywords.append('nightlife')
            if any(word in desc for word in ['shop', 'market', 'boutique']):
                keywords.append('shopping')
            if any(word in desc for word in ['ski', 'snow', 'winter', 'ice', 'cold']):
                keywords.append('skiing')
            
            # Country keywords
            country_kw = {
                "Japan": ['sushi', 'japanese', 'ramen', 'asian', 'anime'],
                "South Korea": ['korean', 'kimchi', 'asian', 'bbq'],
                "Italy": ['pasta', 'pizza', 'italian', 'wine'],
                "Mexico": ['tacos', 'mexican', 'tequila'],
                "Thailand": ['thai', 'pad thai', 'asian', 'tropical'],
                "France": ['french', 'wine', 'croissant'],
                "Spain": ['spanish', 'tapas', 'paella'],
                "Switzerland": ['swiss', 'skiing', 'alps', 'mountains', 'winter'],
                "Austria": ['austrian', 'skiing', 'alps', 'winter'],
                "Norway": ['norwegian', 'fjords', 'skiing', 'winter', 'cold'],
                "Iceland": ['icelandic', 'aurora', 'winter', 'cold'],
                "New Zealand": ['kiwi', 'adventure', 'skiing', 'hiking', 'nature'],
                "Canada": ['canadian', 'skiing', 'mountains', 'winter', 'cold'],
            }
            
            if country in country_kw:
                keywords.extend(country_kw[country])
            
            keywords_str = ','.join(set(keywords))
            
            cursor.execute(
                'INSERT INTO cities (name, country, description, keywords) VALUES (?, ?, ?, ?)',
                (city['name'], country, city.get('description', ''), keywords_str)
            )
            city_id = cursor.lastrowid
            
            # Insert activities
            for activity in city.get('activities', []):
                act_kw = []
                act_lower = activity.lower()
                
                if any(kw in act_lower for kw in ['eat', 'food', 'sushi', 'dining', 'restaurant']):
                    act_kw.append('food')
                if any(kw in act_lower for kw in ['hike', 'mountain', 'climb', 'trail']):
                    act_kw.append('hiking')
                if any(kw in act_lower for kw in ['beach', 'swim', 'ocean', 'coast']):
                    act_kw.append('beaches')
                if any(kw in act_lower for kw in ['museum', 'temple', 'church', 'palace', 'historic']):
                    act_kw.append('culture')
                if any(kw in act_lower for kw in ['shop', 'market', 'boutique']):
                    act_kw.append('shopping')
                if any(kw in act_lower for kw in ['ski', 'snowboard', 'snow']):
                    act_kw.append('skiing')
                
                cursor.execute(
                    'INSERT INTO activities (city_id, activity, keywords) VALUES (?, ?, ?)',
                    (city_id, activity, ','.join(set(act_kw)))
                )
    
    cursor.execute('SELECT COUNT(*) FROM cities')
    count = cursor.fetchone()[0]
    print(f"   [OK] Added {count} cities from JSON\n")
else:
    print("   [WARNING] destinations.json not found, skipping\n")

conn.commit()

# Get final count
cursor.execute('SELECT COUNT(*) FROM cities')
total_cities = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM activities')
total_activities = cursor.fetchone()[0]

conn.close()

print("="*60)
print("[SUCCESS] DATABASE CREATION COMPLETE!")
print("="*60)
print(f"[STATS] Final Statistics:")
print(f"   * Total cities: {total_cities}")
print(f"   * Total activities: {total_activities}")
print(f"   * Database file: travel_data.db")
print("="*60)
print()