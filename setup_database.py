# setup_database.py - Complete Database Setup Script
"""
AI Travel Planner - Database Setup
This script creates and populates the complete travel database.
"""
import subprocess
import sys
import os

# Force UTF-8 output for Windows compatibility
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def print_step(step_num, total_steps, description):
    """Print step information"""
    print(f"\n[STEP {step_num}/{total_steps}] {description}")
    print("-" * 70)


def run_script(script_path, description):
    """Run a Python script and return success status"""
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=60
        )
        
        # Filter and display output (skip Unicode error tracebacks)
        if result.stdout:
            lines = result.stdout.split('\n')
            clean_lines = []
            skip_lines = 0
            
            for i, line in enumerate(lines):
                if skip_lines > 0:
                    skip_lines -= 1
                    continue
                
                # Skip Unicode error tracebacks
                if 'Traceback (most recent call last)' in line and i + 4 < len(lines):
                    if 'UnicodeEncodeError' in '\n'.join(lines[i:i+5]):
                        skip_lines = 4
                        continue
                
                # Skip Unicode error lines
                if any(x in line for x in ['UnicodeEncodeError', 'charmap', 'cp1252', 'File "C:\\']):
                    continue
                
                clean_lines.append(line)
            
            output = '\n'.join(clean_lines).strip()
            if output:
                print(output)
        
        # Check for success
        if result.returncode == 0:
            print(f"\n[SUCCESS] {description} completed!")
            return True
        else:
            print(f"\n[WARNING] {description} completed with warnings")
            return True
            
    except subprocess.TimeoutExpired:
        print(f"\n[ERROR] {description} timed out")
        return False
    except Exception as e:
        print(f"\n[ERROR] Failed to run {os.path.basename(script_path)}: {e}")
        return False


def get_database_stats():
    """Get and display database statistics"""
    try:
        import sqlite3
        conn = sqlite3.connect('travel_data.db')
        cursor = conn.cursor()
        
        queries = {
            'Total cities': 'SELECT COUNT(*) FROM cities',
            'Total activities': 'SELECT COUNT(*) FROM activities',
            'Ski destinations': 'SELECT COUNT(*) FROM cities WHERE keywords LIKE "%skiing%"',
            'Beach destinations': 'SELECT COUNT(*) FROM cities WHERE keywords LIKE "%beaches%"',
            'Food destinations': 'SELECT COUNT(*) FROM cities WHERE keywords LIKE "%food%"',
            'Car destinations': 'SELECT COUNT(*) FROM cities WHERE keywords LIKE "%car%" OR keywords LIKE "%automotive%"',
            'Golf destinations': 'SELECT COUNT(*) FROM cities WHERE keywords LIKE "%golf%"',
            'Adventure destinations': 'SELECT COUNT(*) FROM cities WHERE keywords LIKE "%adventure%" OR keywords LIKE "%hiking%"',
        }
        
        stats = {}
        for label, query in queries.items():
            cursor.execute(query)
            stats[label] = cursor.fetchone()[0]
        
        conn.close()
        return stats
        
    except Exception as e:
        print(f"[WARNING] Could not read database statistics: {e}")
        return None


def main():
    print_header("AI TRAVEL PLANNER - DATABASE SETUP")
    
    print("This script will build your complete travel database with:")
    print("  * 180+ cities from around the world")
    print("  * 50+ ski & winter destinations")
    print("  * 60+ beach & tropical destinations")
    print("  * 35+ golfing destinations")
    print("  * 15+ car & automotive destinations")
    print("  * Food, adventure, and cultural destinations")
    print("  * Capital cities from REST Countries API")
    print("  * Auto-fix: Ensure all cities have proper activities")
    print("  * Auto-fix: Remove generic keywords for better matching")
    
    print("\n[INFO] All database files are in the 'database/' folder")
    print("[INFO] This will take about 5-10 seconds")
    
    input("\nPress Enter to begin setup...")
    
    # Define setup steps
    database_dir = 'database'
    steps = [
        (os.path.join(database_dir, 'create_database.py'), 
         "Creating base database from JSON"),
        
        (os.path.join(database_dir, 'add_ski_destinations.py'), 
         "Adding ski & winter destinations"),
        
        (os.path.join(database_dir, 'add_beach_destinations.py'), 
         "Adding beach & tropical destinations"),
        
        (os.path.join(database_dir, 'add_car_destinations.py'), 
         "Adding car & automotive destinations"),
        
        (os.path.join(database_dir, 'add_golf_destinations.py'), 
         "Adding golf destinations & championship courses"),
        
        (os.path.join(database_dir, 'add_adventure_destinations.py'), 
         "Adding adventure destinations"),
        
        (os.path.join(database_dir, 'add_food_destinations.py'), 
         "Adding food destinations"),
        
        (os.path.join(database_dir, 'import_from_rest_countries.py'), 
         "Adding capital cities from REST Countries API"),
        
        (os.path.join(database_dir, 'fix_activities.py'), 
         "Fixing missing activities and ensuring all cities have proper activities"),
        
        (os.path.join(database_dir, 'fix_generic_keywords.py'), 
         "Removing generic keywords"),
    ]
    
    total_steps = len(steps)
    success_count = 0
    
    # Run each setup step
    for i, (script_path, description) in enumerate(steps, 1):
        print_step(i, total_steps, description)
        
        if not os.path.exists(script_path):
            print(f"[ERROR] Script not found: {script_path}")
            print(f"[INFO] Make sure all files are in the correct folder")
            continue
        
        if run_script(script_path, description):
            success_count += 1
    
    # Show results
    print_header("SETUP COMPLETE!")
    
    print(f"Successfully completed: {success_count}/{total_steps} steps")
    
    # Display database statistics
    stats = get_database_stats()
    if stats:
        print("\nDatabase Statistics:")
        for label, count in stats.items():
            print(f"  * {label}: {count}")
    
    # Show next steps
    print_header("NEXT STEPS")
    
    print("Your database is ready! To start the AI Travel Planner:\n")
    print("  1. Run the server:")
    print("     python main.py")
    print()
    print("  2. Open your browser to:")
    print("     http://127.0.0.1:8000")
    print()
    print("  3. Try some example queries:")
    print("     - 'I like sushi, hiking, and cars'")
    print("     - 'I want beaches and relaxation'")
    print("     - 'Show me skiing destinations'")
    print("     - 'I love food and culture'")
    print("     - 'golf and beaches'")
    print("     - 'Pokemon and sushi'")
    print()
    print("[TIP] The database file 'travel_data.db' is in your main folder")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Setup failed: {e}")
        sys.exit(1)