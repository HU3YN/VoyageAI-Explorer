# VoyageAI Explorer

[![GitHub Pages Deployment](https://github.com/HU3YN/VoyageAI-Explorer/actions/workflows/deploy.yml/badge.svg)](https://github.com/HU3YN/VoyageAI-Explorer/actions/workflows/deploy.yml)
[![Live Website](https://img.shields.io/badge/Live-Website-brightgreen)](https://hu3yn.github.io/VoyageAI-Explorer/)

A web-based interface for exploring VoyageAI embeddings and text analysis capabilities.

## 🚀 Live Deployment
The application is automatically deployed to GitHub Pages:
- **Live URL**: https://hu3yn.github.io/VoyageAI-Explorer/
- **Source Code**: https://github.com/HU3YN/VoyageAI-Explorer

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

Note: All commands are meant to be ran in Powershell

## Setup & Run Instructions

### Step 1 — Install Docker

Download and install Docker Desktop:

https://www.docker.com/products/docker-desktop/

After installing, restart and open Docker Desktop and wait until it says:

Engine running in the bottom left

Verify installation:

docker --version
docker compose version

## Step 2 — Clone the project

git clone https://github.com/HU3YN/VoyageAI-Explorer.git

cd VoyageAI-Explorer

This folder is in your C:\Users\your_profile_name

## Step 3 — Create your API key file

This project uses a .env file to store secrets. If you do not have an API key the program will still work it just will not have all AI semantic search capabilities just keyword searching

Copy the example file:

cp .env.example .env


Open .env and add your OpenAI API key:

OPENAI_API_KEY=sk-your-api-key-here


Do NOT upload this file to GitHub.

## Step 4 — Run the app

docker compose up --build

This will take about 10-15 minutes to build

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
