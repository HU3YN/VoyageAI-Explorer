# update_food_keywords.py - Update existing destinations with food keywords
import sqlite3

conn = sqlite3.connect('travel_data.db')
cursor = conn.cursor()

# Cities that should have food keywords
food_updates = {
    # Format: (city, country): (new_keywords_to_add, updated_description)
    ("Tokyo", "Japan"): (
        "sushi,ramen,japanese,food,asian,culinary,michelin",
        "A neon-lit metropolis blending futuristic technology with deeply rooted traditions and world-class sushi and ramen."
    ),
    ("Osaka", "Japan"): (
        "food,japanese,takoyaki,street food,asian,culinary,okonomiyaki",
        "Japan's 'Kitchen', famous for its street food like takoyaki, vibrant nightlife, and modern architecture."
    ),
    ("Bangkok", "Thailand"): (
        "food,thai,street food,asian,pad thai,culinary,spicy",
        "A frantic, fascinating capital known for ornate shrines, vibrant street life, and world-renowned Thai food."
    ),
    ("Paris", "France"): (
        "food,french,pastries,wine,culinary,michelin,cheese",
        "The City of Light is world-renowned for its art, French gastronomy, pastries, and iconic landmarks like the Eiffel Tower."
    ),
    ("Lyon", "France"): (
        "food,french,gastronomy,culinary,wine,michelin,bouchon",
        "The gastronomic capital of France, famous for its historical architecture and traditional Bouchon restaurants."
    ),
    ("Rome", "Italy"): (
        "food,italian,pasta,pizza,gelato,culinary,wine",
        "The Eternal City, where nearly 3,000 years of globally influential art, architecture, culture, and Italian cuisine are on display."
    ),
    ("Bologna", "Italy"): (
        "food,italian,pasta,ragù,culinary,parmesan,balsamic",
        "The culinary heart of Italy, birthplace of ragù Bolognese, fresh pasta, Parmesan cheese, and balsamic vinegar."
    ),
    ("Naples", "Italy"): (
        "food,italian,pizza,neapolitan,culinary,seafood,mozzarella",
        "Birthplace of authentic Neapolitan pizza, with vibrant street life and coastal Italian cuisine."
    ),
    ("Mexico City", "Mexico"): (
        "food,mexican,tacos,street food,culinary,mole,tamales",
        "A high-altitude metropolis known for ancient ruins, colonial architecture, and world-class Mexican street food and tacos."
    ),
    ("Oaxaca", "Mexico"): (
        "food,mexican,mole,mezcal,culinary,street food,traditional",
        "A cultural gem famous for its indigenous traditions, colorful markets, and legendary mole sauce and mezcal."
    ),
    ("Istanbul", "Turkey"): (
        "food,turkish,kebab,mezze,culinary,baklava,street food",
        "The only city spanning two continents, rich with Byzantine and Ottoman history and diverse Turkish cuisine."
    ),
    ("Ho Chi Minh City", "Vietnam"): (
        "food,vietnamese,pho,street food,asian,culinary,banh mi",
        "A high-energy metropolis formerly known as Saigon, blending French colonial history with modern life and amazing Vietnamese food."
    ),
    ("Hanoi", "Vietnam"): (
        "food,vietnamese,pho,bun cha,street food,asian,culinary",
        "A historic, chaotic capital known for its centuries-old architecture and rich French-Vietnamese food culture."
    ),
    ("Seoul", "South Korea"): (
        "food,korean,bbq,kimchi,asian,street food,culinary",
        "A huge metropolis where modern skyscrapers meet Buddhist temples, palaces, and amazing Korean BBQ and street food."
    ),
    ("Lima", "Peru"): (
        "food,peruvian,ceviche,culinary,michelin,seafood,fusion",
        "The capital of Peru, a coastal city known for its colonial center and incredible culinary scene with ceviche."
    ),
    ("San Sebastian", "Spain"): (
        "food,spanish,pintxos,basque,culinary,michelin,seafood",
        "Basque coastal city with the highest concentration of Michelin stars per capita and famous pintxos bars."
    ),
    ("Copenhagen", "Denmark"): (
        "food,nordic,new nordic,culinary,michelin,danish,smørrebrød",
        "A city of canals, bikes, and 'hygge', home to world-renowned New Nordic cuisine and Michelin-starred restaurants."
    ),
    ("New Orleans", "United States"): (
        "food,creole,cajun,beignets,gumbo,culinary,seafood",
        "A soulful city famous for its jazz music, French-Creole cuisine, beignets, and lively Mardi Gras celebrations."
    ),
}

updated_count = 0
not_found_count = 0

print(" Updating food destinations ...\n")

for (city, country), (new_keywords, description) in food_updates.items():
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
        
        # Add food activities if not present
        cursor.execute('SELECT COUNT(*) FROM activities WHERE city_id = ? AND keywords LIKE "%food%"', (city_id,))
        has_food = cursor.fetchone()[0] > 0
        
        if not has_food:
            food_activities = [
                ("Take a food tour to sample local specialties.", "food,culinary,culture"),
                ("Dine at renowned restaurants and street food stalls.", "food,culinary,restaurants"),
                ("Visit local markets for fresh ingredients and snacks.", "food,shopping,markets"),
                ("Take a cooking class to learn traditional recipes.", "food,culinary,culture,cooking"),
            ]
            
            for activity, act_keywords in food_activities:
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
cursor.execute('SELECT COUNT(*) FROM cities WHERE keywords LIKE "%food%" OR keywords LIKE "%culinary%"')
food_cities = cursor.fetchone()[0]

conn.close()

print(f"\n{'='*60}")
print(f" Food destinations update complete!")
print(f" Statistics:")
print(f"    Destinations updated: {updated_count}")
print(f"    Not found: {not_found_count}")
print(f"    Total food destinations: {food_cities}")
print(f"{'='*60}")