# add_golf_destinations.py - Add world-class golf destinations
import sqlite3
import sys
import os

# Force UTF-8 output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("\n" + "="*60)
print("ADDING GOLF DESTINATIONS")
print("="*60)

# Check if database exists
if not os.path.exists('travel_data.db'):
    print("[ERROR] Database file 'travel_data.db' not found!")
    sys.exit(1)

try:
    conn = sqlite3.connect('travel_data.db')
    cursor = conn.cursor()
except Exception as e:
    print(f"[ERROR] Could not connect to database: {e}")
    sys.exit(1)

# World-class golf destinations
golf_destinations = [
    ("St Andrews", "United Kingdom", "The home of golf, featuring the legendary Old Course and rich golfing heritage.", "golf,sports,scottish,history,links,coastal,outdoor"),
    ("Pebble Beach", "United States", "Iconic California coastal golf destination with breathtaking ocean views.", "golf,luxury,coastal,ocean,scenic,sports,california"),
    ("Pinehurst", "United States", "North Carolina golf resort village with 9 championship courses including Pinehurst No. 2.", "golf,luxury,sports,resort,southern,championship"),
    ("Augusta", "United States", "Home of the Masters Tournament and Augusta National Golf Club.", "golf,sports,championship,masters,southern,prestige"),
    ("Scottsdale", "United States", "Arizona desert golf capital with over 200 courses and luxury resorts.", "golf,luxury,desert,resort,spa,southwestern,sports"),
    ("Hilton Head", "United States", "South Carolina island with championship golf and beautiful beaches.", "golf,beaches,resort,coastal,sports,luxury,relaxation"),
    ("Kiawah Island", "United States", "South Carolina barrier island famous for The Ocean Course and beach golf.", "golf,beaches,luxury,coastal,resort,championship,nature"),
    ("Palm Springs", "United States", "Southern California desert oasis with 100+ golf courses and year-round sunshine.", "golf,desert,luxury,resort,california,spa,mountains"),
    ("Monterey", "United States", "California coastal paradise home to Pebble Beach Golf Links and stunning views.", "golf,coastal,ocean,scenic,luxury,california,nature"),
    ("Algarve", "Portugal", "Portugal's southern coast with world-class golf courses and Mediterranean climate.", "golf,beaches,coastal,european,sunny,luxury,portuguese"),
    ("Marbella", "Spain", "Costa del Sol's golf paradise with luxury resorts and Mediterranean beaches.", "golf,beaches,luxury,spanish,mediterranean,resort,nightlife"),
    ("Mallorca", "Spain", "Balearic island offering championship golf courses and stunning coastline.", "golf,beaches,islands,spanish,mediterranean,luxury,nature"),
    ("Gold Coast", "Australia", "Queensland's beach paradise with excellent golf courses and theme parks.", "golf,beaches,surfing,australian,tropical,adventure,family"),
    ("Phuket", "Thailand", "Tropical island with championship golf courses, beaches, and Thai culture.", "golf,beaches,tropical,asian,thai,resort,food"),
    ("Hua Hin", "Thailand", "Thai beach resort town known for excellent golf courses and royal heritage.", "golf,beaches,thai,resort,royal,relaxation,asian"),
    ("Da Nang", "Vietnam", "Coastal city with world-class golf courses and UNESCO heritage sites nearby.", "golf,beaches,vietnamese,coastal,culture,asian,food"),
    ("Hokkaido", "Japan", "Japan's northern island with scenic golf courses and natural hot springs.", "golf,nature,mountains,japanese,rural,scenic,outdoor"),
    ("Marrakech", "Morocco", "Exotic North African city with luxury golf resorts and desert landscapes.", "golf,culture,desert,luxury,moroccan,exotic,resort"),
    ("Biarritz", "France", "Elegant French Basque coast resort with historic golf courses and surfing.", "golf,beaches,french,basque,luxury,surfing,coastal"),
    ("Cabo San Lucas", "Mexico", "Baja California resort with dramatic coastal golf courses and desert scenery.", "golf,beaches,luxury,mexican,desert,resort,ocean"),
    ("Puerto Vallarta", "Mexico", "Pacific coast resort with jungle and mountain golf courses plus beautiful beaches.", "golf,beaches,tropical,mexican,resort,adventure,jungle"),
    ("Barbados", "Barbados", "Caribbean island offering tropical golf and British colonial charm.", "golf,beaches,tropical,caribbean,luxury,british,relaxation"),
    ("County Kerry", "Ireland", "Home to stunning coastal links courses including Ballybunion and Waterville.", "golf,links,coastal,nature,irish,scenic,outdoor"),
]


added_count = 0
skipped_count = 0

for name, country, description, keywords in golf_destinations:
    try:
        # Check if city already exists
        cursor.execute('SELECT id FROM cities WHERE name = ? AND country = ?', (name, country))
        existing = cursor.fetchone()
        
        if not existing:
            # Insert new city
            cursor.execute(
                'INSERT INTO cities (name, country, description, keywords) VALUES (?, ?, ?, ?)',
                (name, country, description, keywords)
            )
            city_id = cursor.lastrowid
            
            # Add golf-specific activities
            activities = [
                ("Play championship golf courses with stunning views.", "golf,adventure"),
                ("Take golf lessons from professional instructors.", "golf,sports"),
                ("Enjoy golf resort amenities including spas and fine dining.", "golf,luxury,relaxation"),
                ("Experience world-class golf course design.", "golf,nature"),
                ("Join golf tournaments or social golf events.", "golf,sports"),
            ]
            
            for activity, act_keywords in activities:
                cursor.execute(
                    'INSERT INTO activities (city_id, activity, keywords) VALUES (?, ?, ?)',
                    (city_id, activity, act_keywords)
                )
            
            print(f" Added: {name}, {country}")
            added_count += 1
        else:
            print(f" Skipped: {name}, {country}")
            skipped_count += 1
            
    except Exception as e:
        print(f" [ERROR] Failed to add {name}, {country}: {e}")

# Commit changes
try:
    conn.commit()
except Exception as e:
    print(f"\n[ERROR] Failed to commit: {e}")
    sys.exit(1)

# Show statistics
try:
    cursor.execute('SELECT COUNT(*) FROM cities')
    total_cities = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM cities WHERE keywords LIKE "%golf%"')
    golf_cities = cursor.fetchone()[0]
    
    conn.close()

    print(f"\n{'='*60}")
    print(f" Database expansion complete!")
    print(f" Total cities: {total_cities}")
    print(f"  Golf destinations: {golf_cities}")
    print(f"  Added: {added_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"{'='*60}")
    
except Exception as e:
    print(f"\n[ERROR] Failed to get statistics: {e}")
    sys.exit(1)