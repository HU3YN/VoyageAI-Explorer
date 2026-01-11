# fix_generic_keywords.py - Remove generic keywords EXCEPT travel
import sqlite3
import sys
import os

# Force UTF-8 output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("\n[FIX] Removing generic keywords (keeping 'travel')...\n")

# Check if database exists
if not os.path.exists('travel_data.db'):
    print("[ERROR] Database not found!")
    sys.exit(1)

try:
    conn = sqlite3.connect('travel_data.db')
    cursor = conn.cursor()
except Exception as e:
    print(f"[ERROR] Could not connect to database: {e}")
    sys.exit(1)

# Keywords to remove (too generic)
generic_keywords = [
    'travel', 
    'trip',
    'vacation',
    'tourist',
    'tourism',
    'destination',
    'city',
    'place',
    'visit',
]

# Get all cities
cursor.execute('SELECT id, name, country, keywords FROM cities')
cities = cursor.fetchall()

fixed_count = 0
total_removed = 0

for city_id, name, country, keywords_str in cities:
    if not keywords_str:
        continue
    
    # Split keywords
    keywords = keywords_str.split(',')
    original_count = len(keywords)
    
    # Remove generic keywords (but keep 'travel')
    cleaned_keywords = [kw.strip() for kw in keywords if kw.strip() not in generic_keywords]
    
    # Check if we removed anything
    if len(cleaned_keywords) < original_count:
        removed = set([k.strip() for k in keywords]) - set(cleaned_keywords)
        new_keywords_str = ','.join(cleaned_keywords)
        
        # Update database
        cursor.execute(
            'UPDATE cities SET keywords = ? WHERE id = ?',
            (new_keywords_str, city_id)
        )
        
        # Show Cusco specifically
        if name == "Cusco":
            print(f"[CUSCO] {name}, {country}")
            print(f"   Before: {keywords_str}")
            print(f"   After:  {new_keywords_str}")
            print(f"   Removed: {removed}")
        # Only print first 5 others to avoid clutter
        elif fixed_count < 5:
            print(f"[CLEANED] {name}, {country}")
            print(f"   Removed: {removed}")
        
        fixed_count += 1
        total_removed += len(removed)


print(f"\n{'='*60}")
print(f"[SUCCESS] Generic keywords removed!")
print(f"{'='*60}")
print(f"Statistics:")
print(f"   * Cities cleaned: {fixed_count}")
print(f"   * Keywords removed: {total_removed}")
print(f"   * Removed: 'travel', 'city', 'trip', 'vacation', 'tourist', etc.")
print(f"{'='*60}\n")

# Exit with success code
sys.exit(0)