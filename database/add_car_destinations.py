# add_car_destinations.py - Add destinations for car/automotive enthusiasts
import sqlite3

conn = sqlite3.connect('travel_data.db')
cursor = conn.cursor()

car_destinations = [
    ("Stuttgart", "Germany", "Home of Mercedes-Benz and Porsche, featuring world-class automotive museums and the famous Nürburgring nearby.", "cars,automotive,german,culture,museums,engineering"),
    ("Munich", "Germany", "BMW headquarters and museum, plus the massive BMW Welt exhibition center showcasing automotive innovation.", "cars,automotive,bmw,german,museums,engineering,technology"),
    ("Detroit", "United States", "Motor City - birthplace of the American automotive industry, home to Henry Ford Museum and GM Renaissance Center.", "cars,automotive,american,history,museums,motor,industry"),
    ("Maranello", "Italy", "Home of Ferrari, featuring the Ferrari Museum and test track where you can experience Italian supercar culture.", "cars,automotive,ferrari,italian,luxury,racing,sports"),
    ("Tokyo", "Japan", "JDM car culture capital with the Nissan Crossing, Toyota Mega Web, and famous Daikoku Parking Area car meets.", "cars,automotive,japanese,jdm,technology,racing,tuning"),
    ("Modena", "Italy", "Birthplace of Enzo Ferrari, home to multiple supercar manufacturers including Pagani and Maserati museums.", "cars,automotive,italian,ferrari,luxury,racing,supercars"),
    ("Le Mans", "France", "Legendary 24 Hours of Le Mans race circuit and automotive museum showcasing racing heritage.", "cars,automotive,racing,french,history,motorsport"),
    ("Monaco", "Monaco", "Monaco Grand Prix circuit, luxury car spotting, and the Prince's vintage car collection.", "cars,automotive,luxury,racing,f1,supercars,monaco"),
    ("Los Angeles", "United States", "Petersen Automotive Museum, car culture, and frequent supercar spotting in Beverly Hills.", "cars,automotive,museums,american,supercars,luxury"),
    ("Turin", "Italy", "Home of Fiat and the National Automobile Museum with 200+ vintage and modern vehicles.", "cars,automotive,italian,museums,history,fiat"),
    ("Goodwood", "United Kingdom", "Goodwood Festival of Speed and Revival - world-famous automotive events and historic racing.", "cars,automotive,racing,british,history,motorsport"),
    ("Dubai", "United Arab Emirates", "Supercars everywhere, luxury car dealerships, and the Dubai Autodrome racing circuit.", "cars,automotive,luxury,supercars,racing,modern"),
    ("São Paulo", "Brazil", "Home of Formula 1 Brazilian Grand Prix at Interlagos circuit and massive car culture.", "cars,automotive,racing,f1,brazilian,motorsport"),
    ("Wolfsburg", "Germany", "Volkswagen's Autostadt - a car-themed park with pavilions from VW brands including Porsche, Lamborghini, and Bugatti.", "cars,automotive,vw,german,museums,technology"),
    ("Nagoya", "Japan", "Toyota City nearby with Toyota Commemorative Museum of Industry and Technology.", "cars,automotive,toyota,japanese,museums,engineering"),
]

added_count = 0
updated_count = 0

print(" Adding car/automotive destinations to database...\n")

for name, country, description, keywords in car_destinations:
    # Check if city exists
    cursor.execute('SELECT id, keywords FROM cities WHERE name = ? AND country = ?', (name, country))
    existing = cursor.fetchone()
    
    if existing:
        city_id, existing_keywords = existing
        # Update existing city to add car keywords
        new_keywords = existing_keywords + ',' + keywords if existing_keywords else keywords
        # Remove duplicates
        unique_keywords = ','.join(set(new_keywords.split(',')))
        
        cursor.execute(
            'UPDATE cities SET description = ?, keywords = ? WHERE id = ?',
            (description, unique_keywords, city_id)
        )
        updated_count += 1
        print(f" Updated: {name}, {country}")
    else:
        # Insert new city
        cursor.execute(
            'INSERT INTO cities (name, country, description, keywords) VALUES (?, ?, ?, ?)',
            (name, country, description, keywords)
        )
        city_id = cursor.lastrowid
        added_count += 1
        print(f" Added: {name}, {country}")
    
    # Add car-specific activities
    car_activities = [
        ("Visit the automotive museum to see classic and modern vehicles.", "cars,museums,history"),
        ("Tour a car manufacturing facility or headquarters.", "cars,automotive,engineering,industry"),
        ("Attend a car show, meet, or automotive event.", "cars,automotive,culture,social"),
        ("Drive or ride on a famous racing circuit.", "cars,racing,motorsport,adventure"),
        ("Spot exotic supercars and luxury vehicles.", "cars,supercars,luxury"),
    ]
    
    # Check if activities already exist
    cursor.execute('SELECT COUNT(*) FROM activities WHERE city_id = ? AND activity LIKE "%car%" OR activity LIKE "%automotive%"', (city_id,))
    has_car_activities = cursor.fetchone()[0] > 0
    
    if not has_car_activities:
        for activity, act_keywords in car_activities:
            cursor.execute(
                'INSERT INTO activities (city_id, activity, keywords) VALUES (?, ?, ?)',
                (city_id, activity, act_keywords)
            )

conn.commit()

# Show statistics
cursor.execute('SELECT COUNT(*) FROM cities WHERE keywords LIKE "%car%" OR keywords LIKE "%automotive%"')
car_cities = cursor.fetchone()[0]

conn.close()

print(f"\n{'='*60}")
print(f" Car/automotive destinations processing complete!")
print(f" Statistics:")
print(f"    New destinations added: {added_count}")
print(f"    Existing destinations updated: {updated_count}")
print(f"    Total car-related destinations: {car_cities}")
print(f"{'='*60}")