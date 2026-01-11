# add_beach_destinations.py - Add 60+ beach destinations
import sqlite3

conn = sqlite3.connect('travel_data.db')
cursor = conn.cursor()

beach_destinations = [
    ("Maldives", "Maldives", "Tropical paradise with overwater bungalows, crystal clear waters, and pristine white sand beaches.", "beaches,tropical,ocean,luxury,relaxation,diving,swimming"),
    ("Bora Bora", "French Polynesia", "Iconic luxury island with turquoise lagoon, coral reefs, and romantic overwater villas.", "beaches,tropical,ocean,luxury,relaxation,diving"),
    ("Santorini", "Greece", "Stunning Greek island famous for white buildings, blue domes, and dramatic volcanic beaches.", "beaches,ocean,culture,history,romantic,wine"),
    ("Seychelles", "Seychelles", "Pristine African island paradise with giant granite boulders and untouched beaches.", "beaches,tropical,ocean,nature,luxury,diving"),
    ("Maui", "United States", "Hawaiian island offering diverse beaches, surfing, and the scenic Road to Hana.", "beaches,tropical,ocean,adventure,surfing,nature,hiking"),
    ("Phuket", "Thailand", "Thailand's largest island with stunning beaches, vibrant nightlife, and Thai culture.", "beaches,tropical,ocean,nightlife,food,asian,diving"),
    ("Bali", "Indonesia", "Indonesian paradise blending beautiful beaches, rice terraces, temples, and wellness.", "beaches,tropical,ocean,culture,yoga,surfing,food"),
    ("Fiji", "Fiji", "South Pacific archipelago known for friendly locals, coral reefs, and pristine beaches.", "beaches,tropical,ocean,diving,relaxation,adventure"),
    ("Turks and Caicos", "Turks and Caicos", "British Caribbean territory with powder-soft sand and brilliant blue waters.", "beaches,tropical,ocean,luxury,diving,relaxation"),
    ("Aruba", "Aruba", "One Happy Island with reliable sunshine, white sand beaches, and Dutch Caribbean culture.", "beaches,tropical,ocean,nightlife,relaxation,diving"),
    ("Mauritius", "Mauritius", "Indian Ocean island mixing African, Asian, and European cultures with stunning beaches.", "beaches,tropical,ocean,culture,food,diving,luxury"),
    ("Barbados", "Barbados", "Caribbean island blending British heritage, rum culture, and gorgeous coastline.", "beaches,tropical,ocean,culture,nightlife,surfing"),
    ("Costa Rica", "Costa Rica", "Eco-paradise offering Pacific and Caribbean beaches plus rainforest adventures.", "beaches,tropical,ocean,nature,adventure,wildlife,surfing"),
    ("Tulum", "Mexico", "Bohemian beach town with Mayan ruins, cenotes, and laid-back Caribbean vibes.", "beaches,tropical,ocean,culture,history,yoga,mexican"),
    ("Playa del Carmen", "Mexico", "Vibrant Mexican Caribbean town with beaches, nightlife, and Mayan culture.", "beaches,tropical,ocean,nightlife,diving,mexican,food"),
    ("Cozumel", "Mexico", "Mexican island paradise famous for world-class diving and coral reefs.", "beaches,tropical,ocean,diving,mexican,relaxation"),
    ("Amalfi Coast", "Italy", "Dramatic Italian coastline with colorful cliffside villages and Mediterranean charm.", "beaches,ocean,culture,italian,food,luxury,history"),
    ("Mykonos", "Greece", "Glamorous Greek island known for beaches, nightlife, and Cycladic architecture.", "beaches,ocean,nightlife,culture,party,greek,luxury"),
    ("Ibiza", "Spain", "World-famous party island also offering beautiful beaches and bohemian villages.", "beaches,ocean,nightlife,party,spanish,culture"),
    ("Mallorca", "Spain", "Diverse Spanish island with beaches, mountains, historic towns, and Mediterranean cuisine.", "beaches,ocean,culture,spanish,food,hiking,history"),
    ("Nice", "France", "Elegant French Riviera city with pebble beaches, promenade, and Côte d'Azur glamour.", "beaches,ocean,culture,french,food,luxury,art"),
    ("Monaco", "Monaco", "Tiny principality of luxury, casinos, and Mediterranean sophistication.", "beaches,ocean,luxury,nightlife,culture"),
    ("Miami", "United States", "Vibrant Florida city with Art Deco beaches, Cuban culture, and energetic nightlife.", "beaches,ocean,nightlife,party,food,shopping,culture"),
    ("Key West", "United States", "Quirky Florida island with sunset celebrations, water sports, and laid-back atmosphere.", "beaches,ocean,nightlife,adventure,diving,relaxation"),
    ("Honolulu", "United States", "Hawaiian capital combining Waikiki Beach, surfing culture, and island hospitality.", "beaches,tropical,ocean,surfing,culture,food,shopping"),
    ("San Diego", "United States", "California beach city with perfect weather, surf culture, and diverse neighborhoods.", "beaches,ocean,surfing,food,culture,adventure"),
    ("Gold Coast", "Australia", "Australian surf paradise with endless beaches, theme parks, and outdoor lifestyle.", "beaches,ocean,surfing,adventure,nightlife,nature"),
    ("Byron Bay", "Australia", "Bohemian Australian beach town famous for surfing, wellness, and alternative culture.", "beaches,ocean,surfing,yoga,nature,relaxation"),
    ("Whitsundays", "Australia", "Queensland island paradise with Great Barrier Reef access and pristine white sand.", "beaches,tropical,ocean,diving,nature,luxury,adventure"),
    ("Zanzibar", "Tanzania", "Exotic Tanzanian archipelago blending Swahili culture, spice history, and turquoise waters.", "beaches,tropical,ocean,culture,history,diving,african"),
    ("Goa", "India", "Indian beach state mixing Portuguese heritage, yoga retreats, and party scene.", "beaches,tropical,ocean,culture,yoga,nightlife,indian,food"),
    ("Krabi", "Thailand", "Thai province with limestone cliffs, island-hopping, and stunning beach landscapes.", "beaches,tropical,ocean,adventure,diving,asian,nature"),
    ("Koh Samui", "Thailand", "Thai island offering beaches, temples, nightlife, and wellness retreats.", "beaches,tropical,ocean,nightlife,relaxation,asian,food"),
    ("Phi Phi Islands", "Thailand", "Stunning Thai islands with dramatic cliffs, clear waters, and vibrant marine life.", "beaches,tropical,ocean,diving,adventure,asian,party"),
    ("Boracay", "Philippines", "Philippine island paradise with powder-white sand and vibrant beach atmosphere.", "beaches,tropical,ocean,party,diving,adventure,asian"),
    ("Palawan", "Philippines", "Philippine province with pristine islands, lagoons, and underground rivers.", "beaches,tropical,ocean,nature,adventure,diving,asian"),
    ("Langkawi", "Malaysia", "Malaysian archipelago offering duty-free shopping, beaches, and cable car views.", "beaches,tropical,ocean,shopping,nature,relaxation,asian"),
    ("Perhentian Islands", "Malaysia", "Budget-friendly Malaysian islands perfect for diving and beach relaxation.", "beaches,tropical,ocean,diving,nature,relaxation,asian"),
    ("Nha Trang", "Vietnam", "Vietnamese coastal city with beaches, seafood, and island-hopping adventures.", "beaches,tropical,ocean,food,diving,asian,adventure"),
    ("Da Nang", "Vietnam", "Modern Vietnamese beach city near ancient Hoi An with marble mountains.", "beaches,tropical,ocean,culture,food,asian,history"),
    ("Lombok", "Indonesia", "Indonesian island near Bali offering quieter beaches and volcano trekking.", "beaches,tropical,ocean,hiking,adventure,surfing,nature"),
    ("Gili Islands", "Indonesia", "Three tiny Indonesian islands with no cars, diving, and beach parties.", "beaches,tropical,ocean,diving,party,relaxation,asian"),
    ("El Nido", "Philippines", "Philippine paradise with limestone cliffs, lagoons, and island-hopping tours.", "beaches,tropical,ocean,adventure,diving,nature,asian"),
    ("Siargao", "Philippines", "Philippine surf capital with Cloud 9 wave, palm trees, and island vibes.", "beaches,tropical,ocean,surfing,adventure,asian,nature"),
    ("Railay Beach", "Thailand", "Thai peninsula accessible only by boat with rock climbing and stunning beaches.", "beaches,tropical,ocean,adventure,climbing,asian,nature"),
    ("Koh Lanta", "Thailand", "Relaxed Thai island with long beaches, diving, and low-key atmosphere.", "beaches,tropical,ocean,diving,relaxation,asian,nature"),
    ("Aitutaki", "Cook Islands", "Remote Pacific lagoon with stunning turquoise waters and Polynesian culture.", "beaches,tropical,ocean,diving,nature,relaxation"),
    ("Rarotonga", "Cook Islands", "Main Cook Islands destination with beaches, hiking, and Polynesian hospitality.", "beaches,tropical,ocean,culture,hiking,nature"),
    ("Moorea", "French Polynesia", "Dramatic volcanic island near Tahiti with mountain peaks and tropical beaches.", "beaches,tropical,ocean,adventure,diving,luxury"),
    ("Tahiti", "French Polynesia", "French Polynesian main island mixing black sand beaches with Polynesian culture.", "beaches,tropical,ocean,culture,diving,luxury"),
    ("Roatan", "Honduras", "Caribbean island known for affordable diving and laid-back beach lifestyle.", "beaches,tropical,ocean,diving,relaxation,adventure"),
    ("Ambergris Caye", "Belize", "Belizean island offering diving at Great Blue Hole and Caribbean relaxation.", "beaches,tropical,ocean,diving,adventure,nature"),
    ("St. Lucia", "St. Lucia", "Caribbean island famous for Piton mountains, volcanic beaches, and romantic resorts.", "beaches,tropical,ocean,adventure,luxury,nature,hiking"),
    ("Anguilla", "Anguilla", "British Caribbean territory with pristine white sand and luxury tranquility.", "beaches,tropical,ocean,luxury,relaxation,diving"),
    ("St. Barts", "St. Barthélemy", "Ultra-luxurious French Caribbean island attracting celebrities and yachts.", "beaches,tropical,ocean,luxury,french,shopping"),
    ("Antigua", "Antigua and Barbuda", "Caribbean nation claiming 365 beaches, sailing culture, and British heritage.", "beaches,tropical,ocean,adventure,culture,relaxation"),
    ("Cayman Islands", "Cayman Islands", "British Caribbean territory famous for Seven Mile Beach and stingray encounters.", "beaches,tropical,ocean,diving,luxury,food"),
    ("Bermuda", "Bermuda", "British Atlantic island with pink sand beaches and British colonial charm.", "beaches,ocean,culture,luxury,history,diving"),
    ("Providenciales", "Turks and Caicos", "Turks and Caicos main island with Grace Bay Beach voted world's best.", "beaches,tropical,ocean,luxury,diving,relaxation"),
]

for name, country, description, keywords in beach_destinations:
    cursor.execute('SELECT id FROM cities WHERE name = ? AND country = ?', (name, country))
    existing = cursor.fetchone()
    
    if not existing:
        cursor.execute(
            'INSERT INTO cities (name, country, description, keywords) VALUES (?, ?, ?, ?)',
            (name, country, description, keywords)
        )
        city_id = cursor.lastrowid
        
        activities = [
            ("Swim in crystal-clear turquoise waters.", "beaches,swimming"),
            ("Snorkel or dive among colorful coral reefs.", "diving,beaches,adventure"),
            ("Relax on pristine white sand beaches.", "beaches,relaxation"),
            ("Try water sports like kayaking, paddleboarding, or jet skiing.", "adventure,beaches"),
            ("Watch spectacular sunsets over the ocean.", "beaches,nature"),
            ("Take a boat tour to nearby islands.", "adventure,beaches,nature"),
        ]
        
        for activity, act_keywords in activities:
            cursor.execute(
                'INSERT INTO activities (city_id, activity, keywords) VALUES (?, ?, ?)',
                (city_id, activity, act_keywords)
            )
        
        print(f" Added: {name}, {country}")
    else:
        print(f" Skipped: {name}, {country}")

conn.commit()
cursor.execute('SELECT COUNT(*) FROM cities WHERE keywords LIKE "%beaches%"')
beach_count = cursor.fetchone()[0]
conn.close()

print(f"\n{'='*60}")
print(f" Beach destinations added!")
print(f"  Total beach destinations: {beach_count}")
print(f"{'='*60}")