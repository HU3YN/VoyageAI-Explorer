# add_ski_destinations.py - Add 50+ ski destinations to database
import sqlite3

conn = sqlite3.connect('travel_data.db')
cursor = conn.cursor()

# 50+ Major ski destinations with proper keywords
ski_destinations = [
    ("Aspen", "United States", "Luxury ski resort in the Rocky Mountains known for world-class skiing and upscale amenities.", "skiing,snow,winter,cold,mountains,luxury,adventure"),
    ("Vail", "United States", "America's largest ski resort with extensive terrain and excellent snow conditions.", "skiing,snow,winter,cold,mountains,adventure"),
    ("Whistler", "Canada", "Top ski destination hosting Winter Olympics with incredible mountain scenery.", "skiing,snow,winter,cold,mountains,adventure"),
    ("Banff", "Canada", "Stunning mountain town in Canadian Rockies with world-class skiing and natural beauty.", "skiing,snow,winter,cold,mountains,nature,adventure"),
    ("Lake Louise", "Canada", "Picturesque ski resort with breathtaking mountain views and pristine powder.", "skiing,snow,winter,cold,mountains,nature"),
    ("Chamonix", "France", "Historic alpine town beneath Mont Blanc offering extreme skiing and mountaineering.", "skiing,snow,winter,cold,mountains,adventure"),
    ("Val d'Isère", "France", "Premier French ski resort with extensive terrain and lively après-ski.", "skiing,snow,winter,cold,mountains,nightlife"),
    ("Courchevel", "France", "Exclusive ski resort in French Alps known for luxury and excellent skiing.", "skiing,snow,winter,cold,mountains,luxury"),
    ("St. Moritz", "Switzerland", "Glamorous Swiss resort pioneering winter tourism with world-class skiing.", "skiing,snow,winter,cold,mountains,luxury"),
    ("Verbier", "Switzerland", "Legendary off-piste skiing and vibrant nightlife in Swiss Alps.", "skiing,snow,winter,cold,mountains,adventure,nightlife"),
    ("Davos", "Switzerland", "Highest town in Alps offering extensive skiing and hosting World Economic Forum.", "skiing,snow,winter,cold,mountains"),
    ("Interlaken", "Switzerland", "Alpine adventure capital between two lakes with access to Jungfrau region.", "skiing,snow,winter,cold,mountains,adventure"),
    ("Innsbruck", "Austria", "Historic Olympic city surrounded by spectacular alpine skiing.", "skiing,snow,winter,cold,mountains,culture"),
    ("St. Anton", "Austria", "Legendary ski resort birthplace of alpine skiing with challenging terrain.", "skiing,snow,winter,cold,mountains,adventure"),
    ("Kitzbühel", "Austria", "Medieval town offering glamorous skiing and famous Hahnenkamm downhill.", "skiing,snow,winter,cold,mountains,luxury"),
    ("Cortina d'Ampezzo", "Italy", "Chic Italian ski resort in Dolomites with stunning mountain scenery.", "skiing,snow,winter,cold,mountains,luxury,culture"),
    ("Val Gardena", "Italy", "Beautiful Dolomites valley with extensive skiing and Italian charm.", "skiing,snow,winter,cold,mountains,food"),
    ("Niseko", "Japan", "Powder paradise with legendary dry snow and traditional Japanese culture.", "skiing,snow,winter,cold,mountains,japanese,food"),
    ("Hakuba", "Japan", "Olympic ski resort offering varied terrain and authentic Japanese experience.", "skiing,snow,winter,cold,mountains,japanese"),
    ("Queenstown", "New Zealand", "Adventure capital with skiing and extreme sports in stunning landscapes.", "skiing,adventure,mountains,nature,hiking"),
    ("Wanaka", "New Zealand", "Scenic alpine town with excellent skiing and outdoor adventures.", "skiing,mountains,nature,adventure,hiking"),
    ("Tromsø", "Norway", "Arctic city offering skiing, northern lights, and midnight sun.", "skiing,snow,winter,cold,aurora,nordic"),
    ("Åre", "Sweden", "Scandinavia's premier ski resort with excellent facilities and northern lights.", "skiing,snow,winter,cold,nordic,aurora"),
    ("Riksgränsen", "Sweden", "Unique skiing under midnight sun in Swedish Lapland.", "skiing,snow,winter,cold,nordic,aurora"),
    ("Reykjavik", "Iceland", "Capital city base for exploring glaciers, northern lights, and unique skiing.", "cold,winter,aurora,adventure,nature"),
    ("Akureyri", "Iceland", "Northern Iceland's ski capital with aurora viewing and geothermal pools.", "skiing,snow,winter,cold,aurora"),
    ("Levi", "Finland", "Lapland ski resort with Santa Claus village and northern lights.", "skiing,snow,winter,cold,nordic,aurora"),
    ("Trysil", "Norway", "Norway's largest ski resort with family-friendly slopes and Nordic charm.", "skiing,snow,winter,cold,nordic"),
    ("Jackson Hole", "United States", "Steep terrain and wild west charm in Wyoming's Tetons.", "skiing,snow,winter,cold,mountains,adventure"),
    ("Park City", "United States", "Utah's largest ski resort with Olympic legacy and diverse terrain.", "skiing,snow,winter,cold,mountains"),
    ("Breckenridge", "United States", "High-altitude Colorado resort with historic mining town charm.", "skiing,snow,winter,cold,mountains"),
    ("Steamboat", "United States", "Colorado ski town famous for champagne powder and western culture.", "skiing,snow,winter,cold,mountains"),
    ("Sun Valley", "United States", "America's first destination ski resort in Idaho mountains.", "skiing,snow,winter,cold,mountains,luxury"),
    ("Taos", "United States", "New Mexico ski resort blending Native American culture with challenging skiing.", "skiing,snow,winter,cold,mountains,culture"),
    ("Big Sky", "United States", "Montana's massive ski resort with wide-open terrain and minimal crowds.", "skiing,snow,winter,cold,mountains"),
    ("Lake Tahoe", "United States", "California/Nevada border offering multiple ski resorts and beautiful lake.", "skiing,snow,winter,mountains,beaches"),
    ("Andermatt", "Switzerland", "Historic alpine village with modern skiing and traditional charm.", "skiing,snow,winter,cold,mountains"),
    ("Lech", "Austria", "Exclusive Austrian resort with pristine slopes and luxury ambiance.", "skiing,snow,winter,cold,mountains,luxury"),
    ("Zell am See", "Austria", "Medieval lakeside town with glacier skiing and year-round activities.", "skiing,snow,winter,cold,mountains"),
    ("Gstaad", "Switzerland", "Ultra-luxurious Swiss resort attracting celebrities and royalty.", "skiing,snow,winter,cold,mountains,luxury"),
    ("Morzine", "France", "Traditional Savoyard village in Portes du Soleil ski area.", "skiing,snow,winter,cold,mountains"),
    ("Saalbach", "Austria", "Austrian ski circus with extensive terrain and vibrant après-ski.", "skiing,snow,winter,cold,mountains,nightlife"),
    ("Cervinia", "Italy", "Italian resort sharing slopes with Zermatt under Matterhorn.", "skiing,snow,winter,cold,mountains"),
    ("Livigno", "Italy", "Tax-free Italian ski town near Swiss border with excellent snow.", "skiing,snow,winter,cold,mountains,shopping"),
    ("Saas-Fee", "Switzerland", "Glacier skiing village offering year-round snow sports.", "skiing,snow,winter,cold,mountains"),
    ("Engelberg", "Switzerland", "Traditional Swiss village with Mount Titlis glacier skiing.", "skiing,snow,winter,cold,mountains"),
    ("Meribel", "France", "Central Three Valleys resort with British charm and extensive skiing.", "skiing,snow,winter,cold,mountains"),
    ("Tignes", "France", "High-altitude glacier skiing with snow guarantee and modern facilities.", "skiing,snow,winter,cold,mountains"),
    ("Alpe d'Huez", "France", "Sunny French resort famous for Tour de France and varied terrain.", "skiing,snow,winter,cold,mountains"),
]

# Insert ski destinations
for name, country, description, keywords in ski_destinations:
    # Check if city already exists
    cursor.execute('SELECT id FROM cities WHERE name = ? AND country = ?', (name, country))
    existing = cursor.fetchone()
    
    if not existing:
        cursor.execute(
            'INSERT INTO cities (name, country, description, keywords) VALUES (?, ?, ?, ?)',
            (name, country, description, keywords)
        )
        city_id = cursor.lastrowid
        
        # Add skiing-specific activities
        activities = [
            ("Hit the slopes for world-class skiing and snowboarding.", "skiing,adventure"),
            ("Enjoy après-ski at cozy mountain lodges.", "nightlife,relaxation"),
            ("Take a scenic gondola ride for mountain views.", "nature,adventure"),
            ("Try snowshoeing or cross-country skiing.", "skiing,nature"),
            ("Relax in hot tubs with mountain vistas.", "relaxation"),
        ]
        
        for activity, act_keywords in activities:
            cursor.execute(
                'INSERT INTO activities (city_id, activity, keywords) VALUES (?, ?, ?)',
                (city_id, activity, act_keywords)
            )
        
        print(f" Added: {name}, {country}")
    else:
        print(f" Skipped: {name}, {country} (already exists)")

conn.commit()

# Show statistics
cursor.execute('SELECT COUNT(*) FROM cities')
total_cities = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM cities WHERE keywords LIKE "%skiing%"')
ski_cities = cursor.fetchone()[0]

conn.close()

print(f"\n{'='*60}")
print(f" Database expansion complete!")
print(f" Total cities: {total_cities}")
print(f"  Ski destinations: {ski_cities}")
print(f"{'='*60}")