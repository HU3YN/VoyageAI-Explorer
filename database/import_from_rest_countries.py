# import_from_rest_countries.py - FIXED VERSION
import requests
import sqlite3
import time

print(" Fetching data from REST Countries API...")

try:
    # ⭐ FIX: Specify fields as required by REST Countries API
    # Using v3.1 endpoint with specific fields (max 10)
    fields = 'name,capital,region,subregion,population'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(
        f'https://restcountries.com/v3.1/all?fields={fields}',
        headers=headers,
        timeout=10
    )
    response.raise_for_status()
    countries = response.json()
    print(f" Successfully fetched {len(countries)} countries")
except requests.exceptions.RequestException as e:
    print(f" Error fetching from API: {e}")
    print(" The REST Countries API requires field specification. Trying with minimal fields...")
    try:
        # Try with even fewer fields
        response = requests.get(
            'https://restcountries.com/v3.1/all?fields=name,capital,region',
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        countries = response.json()
        print(f" Successfully fetched {len(countries)} countries with minimal fields")
    except Exception as e2:
        print(f" Alternative attempt also failed: {e2}")
        print(" REST Countries API may be down. Database will work with existing cities.")
        exit(1)

# Validate response
if not isinstance(countries, list) or len(countries) == 0:
    print(f" Invalid API response")
    exit(1)

conn = sqlite3.connect('travel_data.db')
cursor = conn.cursor()

added_count = 0
skipped_count = 0

print(f" Processing {len(countries)} countries...")
print(" Adding capital cities to database...\n")

for country in countries:
    try:
        # Validate country is a dict
        if not isinstance(country, dict):
            continue
            
        # Extract country info safely (handle both v2 and v3 formats)
        if isinstance(country.get('name'), dict):
            country_name = country['name'].get('common', '')
        else:
            country_name = country.get('name', '')
            
        capital_list = country.get('capital', [])
        if isinstance(capital_list, str):
            capital = capital_list
        elif isinstance(capital_list, list) and capital_list:
            capital = capital_list[0]
        else:
            continue
            
        region = country.get('region', '')
        subregion = country.get('subregion', '')
        population = country.get('population', 0)
        
        # Skip if no valid data
        if not capital or not country_name:
            continue
        
        # Check if city already exists
        cursor.execute('SELECT id FROM cities WHERE name = ? AND country = ?', (capital, country_name))
        if cursor.fetchone():
            skipped_count += 1
            continue
        
        # Build description
        description = f"Capital of {country_name}"
        if region:
            description += f" in {region}"
        if population > 1000000:
            description += f", major city with over {population//1000000}M people"
        description += "."
        
        # Build keywords based on region
        keywords = ['culture', 'city', 'capital']
        
        # Regional keywords
        if region == 'Europe':
            keywords.extend(['european', 'history', 'culture', 'art'])
        elif region == 'Asia':
            keywords.extend(['asian', 'culture', 'food'])
        elif region == 'Africa':
            keywords.extend(['african', 'culture', 'wildlife'])
        elif region == 'Americas':
            if 'South' in str(subregion):
                keywords.extend(['latin', 'culture', 'food', 'adventure'])
            elif 'Central' in str(subregion):
                keywords.extend(['latin', 'beaches', 'tropical'])
            elif 'North' in str(subregion):
                keywords.extend(['modern', 'culture'])
            elif 'Caribbean' in str(subregion):
                keywords.extend(['tropical', 'beaches', 'relaxation'])
        elif region == 'Oceania':
            keywords.extend(['beaches', 'nature', 'adventure'])
        
        keywords_str = ','.join(set(keywords))
        
        # Insert city
        cursor.execute(
            'INSERT INTO cities (name, country, description, keywords) VALUES (?, ?, ?, ?)',
            (capital, country_name, description, keywords_str)
        )
        city_id = cursor.lastrowid
        
        # Add generic activities
        activities = [
            ("Visit major landmarks and government buildings.", "culture,history"),
            ("Explore museums and cultural institutions.", "culture,art,history"),
            ("Try authentic local cuisine at restaurants.", "food,culture"),
            ("Walk through historic districts and neighborhoods.", "culture,history"),
            ("Visit local markets and shopping areas.", "shopping,culture"),
        ]
        
        for activity, act_keywords in activities:
            cursor.execute(
                'INSERT INTO activities (city_id, activity, keywords) VALUES (?, ?, ?)',
                (city_id, activity, act_keywords)
            )
        
        added_count += 1
        if added_count <= 10 or added_count % 50 == 0:
            print(f" Added: {capital}, {country_name} ({region})")
        
        # Small delay to be respectful to API
        if added_count % 10 == 0:
            time.sleep(0.1)
        
    except Exception as e:
        print(f" Error processing {country.get('name', 'unknown')}: {e}")
        continue

conn.commit()

# Get final statistics
cursor.execute('SELECT COUNT(*) FROM cities')
total_cities = cursor.fetchone()[0]

conn.close()

print(f"\n{'='*60}")
print(f" REST Countries API import complete!")
print(f" Statistics:")
print(f"    Added: {added_count} new capital cities")
print(f"    Skipped: {skipped_count}")
print(f"    Total cities in database: {total_cities}")
print(f"{'='*60}")