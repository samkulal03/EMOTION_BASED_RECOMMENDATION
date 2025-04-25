from fastapi import FastAPI, HTTPException
import ollama
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from imdb import IMDb
import os
from dotenv import load_dotenv
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Use Llama 3.2 (Ollama)
model_name = "llama3.2"

# Initialize IMDb API
ia = IMDb()

# Load emotion classification model
emotion_model_name = "nateraw/bert-base-uncased-emotion"
emotion_model = AutoModelForSequenceClassification.from_pretrained(emotion_model_name)
emotion_tokenizer = AutoTokenizer.from_pretrained(emotion_model_name)

# Set up Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    raise ValueError("Spotify API credentials are missing. Set them in the .env file.")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))


def chat_with_llama(prompt):
    """
    Generates chatbot responses using Llama 3.2 (via Ollama).
    """
    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful AI that provides emotional support and recommendations."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.get("message", {}).get("content", "I'm not sure how to respond to that.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Llama3.2 error: {str(e)}")


def get_mood(text):
    """
    Detects the sentiment of the input text using an emotion classifier.
    """
    inputs = emotion_tokenizer(text, return_tensors="pt")
    outputs = emotion_model(**inputs)
    scores = torch.nn.functional.softmax(outputs.logits, dim=1)
    
    labels = ["sadness", "joy", "anger", "fear", "surprise", "disgust", "neutral"]
    mood = labels[scores.argmax().item()]

    # Map detected emotions to moods
    mood_map = {
        "joy": "happy",
        "sadness": "sad",
        "anger": "angry",
        "neutral": "neutral"
    }
    return mood_map.get(mood, "neutral")


def get_songs_by_mood(mood):
    """
    Fetches songs from Spotify based on mood and includes song links.
    """
    mood_queries = {
        "happy": "happy upbeat",
        "sad": "sad emotional",
        "angry": "rock aggressive",
        "neutral": "chill lo-fi"
    }

    query = mood_queries.get(mood, "chill music")

    try:
        results = sp.search(q=query, type="track", limit=5)
        songs = [
            {
                "name": track['name'],
                "artist": track['artists'][0]['name'],
                "url": track['external_urls']['spotify']  # Get Spotify song URL
            }
            for track in results['tracks']['items']
        ]
        return songs if songs else [{"name": "No songs found", "artist": "", "url": ""}]
    except Exception as e:
        return [{"name": f"Error fetching songs: {str(e)}", "artist": "", "url": ""}]


def get_movies_by_mood(mood):
    """
    Fetches movies from IMDb based on mood.
    """
    genre_map = {
        "happy": "Comedy",
        "sad": "Drama",
        "angry": "Action",
        "neutral": "Adventure"
    }
    genre = genre_map.get(mood, "Drama")

    try:
        search_results = ia.search_movie(genre)  # Corrected function
        movies = [{"title": movie["title"]} for movie in search_results[:5]]
        return movies if movies else [{"title": "No movies found"}]
    
    except Exception as e:
        return [{"title": f"Error fetching movies: {str(e)}"}]


@app.get("/recommend")
def recommend(query: str):
    """
    Handles user input, interacts with Llama (via Ollama), and provides recommendations.
    """
    try:
        chatbot_response = chat_with_llama(query)
        mood = get_mood(chatbot_response)
        songs = get_songs_by_mood(mood)
        movies = get_movies_by_mood(mood)
        
        return {
            "chatbot_response": chatbot_response,
            "mood": mood,
            "songs": songs,
            "movies": movies
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def home():
    return {"message": "Welcome to the Emotion-Based Movie & Music Recommendation Chatbot!"}
