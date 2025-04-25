import streamlit as st
import requests

# API endpoint
API_URL = "http://127.0.0.1:8000/recommend"

# UI
st.set_page_config(page_title="Emotion-Based Recommender", layout="centered")
st.title("🎵 Emotion-Based Music & Movie Recommendations 🎬")

st.markdown(
    """
    Welcome! Tell me how you're feeling, and I'll suggest **songs & movies** that match your mood! 😊
    """
)

query = st.text_input("How are you feeling today?", placeholder="Enter your mood or feelings here...")

if st.button("🎧 Get Recommendations"):
    if query:
        with st.spinner("🔍 Finding the best recommendations..."):
            response = requests.get(API_URL, params={"query": query})
        
        if response.status_code == 200:
            data = response.json()
            
            # Display chatbot response
            st.subheader("🗣 Chatbot Response")
            st.write(data["chatbot_response"])
            
            # Display detected mood
            st.subheader(f"💡 Detected Mood: `{data['mood'].capitalize()}`")

            # Display song recommendations
            st.subheader("🎶 Recommended Songs:")
            for song in data["songs"]:
                st.markdown(f"🎵 **[{song['name']} - {song['artist']}]({song['url']})**", unsafe_allow_html=True)

            # Display movie recommendations
            st.subheader("🎬 Recommended Movies:")
            for movie in data["movies"]:
                st.write(f"🎥 {movie['title']}")
        else:
            st.error("❌ Failed to fetch recommendations. Please try again.")
    else:
        st.warning("⚠️ Please enter how you're feeling.")
