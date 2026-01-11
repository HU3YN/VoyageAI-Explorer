# AI Travel Planner

An AI-powered travel planning engine built with FastAPI, multi-agent AI, and Docker.

This project generates custom travel itineraries using semantic matching,
database search, and AI reasoning.

---

## Requirements

You only need:

- Docker Desktop
- Git

You do NOT need Python, pip, or virtual environments.

---

## Setup & Run Instructions

### Step 1 — Install Docker

Download and install Docker Desktop:

https://www.docker.com/products/docker-desktop/

After installing, open Docker Desktop and wait until it says:

Docker is running

Verify installation:

docker --version
docker compose version

## Step 2 — Clone the project

git clone https://github.com/yourusername/ai-travel-planner.git
cd ai-travel-planner

## Step 3 — Create your API key file

This project uses a .env file to store secrets.

Copy the example file:

cp .env.example .env


Open .env and add your OpenAI API key:

OPENAI_API_KEY=sk-your-api-key-here


Do NOT upload this file to GitHub.

## Step 4 — Run the app

docker compose up --build


Docker will:

Create a Linux container

Install Python

Install all dependencies

Start the FastAPI server


## Step 5 — Open the app

Open your browser:

http://localhost:8000


## Development:

After making code changes, rebuild the container:

docker compose down
docker compose up --build

## Stopping the App

Press:
CTRL + C

## Rebuilding Database

If the database get corrupted run: python setup_database.py
This will overwrite the database file 
