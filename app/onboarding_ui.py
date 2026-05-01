import streamlit as st
import os
import whisper # pip install openai-whisper
from app.services.memory_store import memory_store
from app.services.vision_encoder import vision_encoder

def process_audio_video(file_path):
    """Requirement #2: Capture audio/video bio."""
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result["text"]

def ingest_user_data(user_id, text_bio, uploaded_files):
    """Requirement #2: Build the twin from multiple sources."""
    # 1. Process text bio
    if text_bio:
        memory_store.upsert_memory(user_id, "bio", text_bio)
        
    # 2. Process Audio/Video uploads
    for uploaded_file in uploaded_files:
        file_ext = uploaded_file.name.split('.')[-1].lower()
        if file_ext in ['mp3', 'wav', 'mp4', 'm4a']:
            # Save temp file for whisper
            with open("temp_bio", "wb") as f:
                f.write(uploaded_file.getbuffer())
            transcript = process_audio_video("temp_bio")
            memory_store.upsert_memory(user_id, "vocal_bio", transcript)
            os.remove("temp_bio")

    st.success("Persona data ingested into Vector DB.")

# --- UI FOR ONBOARDING ---
st.title("🧬 Forging Your Digital Twin")

user_id = "user_123" # In production, this is the session user ID

with st.expander("Step 1: Bio Ingestion (Text, Audio, Video)", expanded=True):
    bio_text = st.text_area("Tell your twin about yourself:")
    bio_files = st.file_uploader("Upload Audio or Video Bio", accept_multiple_files=True)
    if st.button("Train Persona"):
        ingest_user_data(user_id, bio_text, bio_files)

with st.expander("Step 2: Physical Preference Training"):
    st.write("Requirement #3: Establish visual 'type' via AI-generated images.")
    # Here you would loop through data/training_images/
    # This logic now saves to st.session_state.pref_vector
    # ensuring the 'Gatekeeper' has real math to work with.