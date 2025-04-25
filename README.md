Emotion-Based Movie Recommendation API

This project is an **AI-powered API** that recommends movies based on the **emotion detected from a user's sentence** (e.g., "I am feeling sad today"). It uses:

- **LLaMA 3.2 via Ollama** for emotion detection from text
- **IMDbPY** to fetch top-rated movies by genre
- **FastAPI** to provide a lightweight and efficient REST API

---

## Features

- Understands emotion from natural language sentences (e.g., "I'm so happy!")
- Maps emotions to genres like Comedy, Drama, Action, etc.
- Recommends top-rated movies based on IMDb
- Clean and fast API response using FastAPI

---

## How It Works

1. The user sends a sentence (e.g., "I am feeling down").
2. The sentence is analyzed by **LLaMA 3.2** running locally via **Ollama** to detect the emotion.
3. The emotion is mapped to a suitable **movie genre**.
4. The app queries **IMDb's Top 250 Movies** and returns recommendations matching that genre.

---

## 🔧 Tech Stack

- **Python 3**
- **FastAPI** – for creating REST APIs
- **Ollama** + **LLaMA 3.2** – for local LLM inference
- **IMDbPY** – to access movie data
- **Uvicorn** – ASGI server for FastAPI
