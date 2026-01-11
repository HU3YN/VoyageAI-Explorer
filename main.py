# main.py
from dotenv import load_dotenv
load_dotenv()
import os
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from agents.master_agent import MasterAgent

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the Master Agent (but only in worker process, not in reloader)
agent = None

# Check if this is the worker process (not the reloader process)
if os.environ.get('RUN_MAIN') == 'true' or not os.environ.get('RUN_MAIN'):
    # This runs only in the actual worker process
    if '--reload' not in sys.argv or os.environ.get('RUN_MAIN') == 'true':
        agent = MasterAgent()
    else:
        # This is the reloader parent process, initialize lazily
        agent = None
else:
    agent = None

def get_agent():
    """Get or initialize agent"""
    global agent
    if agent is None:
        agent = MasterAgent()
    return agent

@app.post("/plan-trip")
async def plan_trip(request: Request):
    try:
        data = await request.json()
        user_input = data.get("user_input", "")
        total_days = int(data.get("days", 3))

        # Validate input
        if total_days < 1 or total_days > 30:
            return JSONResponse(
                content={"error": "Please choose between 1 and 30 days."},
                status_code=400
            )

        print(f"\n{'='*50}")
        print(f"Planning trip: '{user_input}' for {total_days} days")
        print(f"{'='*50}\n")

        # Get itinerary from MasterAgent
        trip_agent = get_agent()
        itinerary, matched_interests, activity_interest_map = trip_agent.generate_itinerary(
            user_input=user_input,
            days=total_days
        )

        # Log results
        print(f"\nGenerated itinerary with {len(itinerary)} cities:")
        for i, city in enumerate(itinerary):
            print(f"  {i+1}. {city['destination']}, {city['country']} - {city.get('days', 1)} days (Score: {city.get('score', 0)}%)")
            print(f"     Matched interests: {matched_interests[i]}")
            print(f"     Activity matches: {len(activity_interest_map[i])} activities")

        return JSONResponse(
            content={
                "itinerary": itinerary,
                "matched_interests": matched_interests,
                "activity_interest_map": activity_interest_map
            }
        )
    except Exception as e:
        print(f"\n[ERROR] Error planning trip: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            content={"error": "Error planning trip. Please try again."},
            status_code=500
        )

@app.get("/")
async def root():
    """Serve the main HTML page"""
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return {"message": "AI Travel Planner API running."}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "ai_powered": True,
        "features": [
            "Semantic interest matching",
            "Multi-day city planning",
            "Activity-level AI matching"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    print("\n[START] Starting AI Travel Planner...")
    print("[URL] http://127.0.0.1:8000")
    print("[FEATURES] AI-powered semantic matching, multi-day planning\n")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)