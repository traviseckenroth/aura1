import streamlit as st
from PIL import Image
import os
from app.services.memory_store import memory_store
from app.services.vision_encoder import vision_encoder
from app.services.llm_inference import twin_engine

st.set_page_config(page_title="Twin Forge: Onboarding", layout="centered")

def run_onboarding():
    st.title("🧬 Forging Your Digital Twin")
    
    if 'step' not in st.session_state:
        st.session_state.step = 1
        st.session_state.liked_images = []

    # --- PHASE 1: PASSIVE HARVESTING (SIMULATED) ---
    if st.session_state.step == 1:
        st.header("Step 1: Data Ingestion")
        st.write("Upload your 'DNA' (Chat exports, bio, or Google Drive link).")
        
        raw_bio = st.text_area("Paste a short bio or chat logs to begin:", height=200)
        
        if st.button("Initialize Ingestion"):
            if raw_bio:
                # In production, this triggers the background ETL pipeline
                memory_store.upsert_memory("user_001", "core_persona", raw_bio)
                st.session_state.step = 2
                st.rerun()

    # --- PHASE 2: VISUAL CALIBRATION (SWIPING GAME) ---
    elif st.session_state.step == 2:
        st.header("Step 2: Visual Calibration")
        st.write("Like at least 5 images to establish your 'type'.")

        # Simulated AI-generated training images directory
        image_folder = "data/training_images/"
        images = [os.path.join(image_folder, f) for f in os.listdir(image_folder)]
        
        current_img_idx = len(st.session_state.liked_images)
        if current_img_idx < 10:  # Train on 10 swipes
            img_path = images[current_img_idx]
            st.image(img_path, width=400)
            
            col1, col2 = st.columns(2)
            if col1.button("❌ Dislike"):
                # Move to next without adding to vector
                st.session_state.liked_images.append(None) 
                st.rerun()
            if col2.button("❤️ Like"):
                st.session_state.liked_images.append(img_path)
                st.rerun()
        else:
            # Calculate the Centroid
            valid_likes = [img for img in st.session_state.liked_images if img]
            pref_vector = vision_encoder.calculate_preference_centroid(valid_likes)
            # Store preference vector (placeholder for DB storage)
            st.session_state.pref_vector = pref_vector
            st.success("Physical Preference Vector Calculated!")
            if st.button("Continue to Turing Test"):
                st.session_state.step = 3
                st.rerun()

    # --- PHASE 3: THE TWIN TURING TEST ---
    elif st.session_state.step == 3:
        st.header("Step 3: The Turing Test")
        st.write("Chat with your twin. Correct it if it sounds off.")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask your twin a question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response = twin_engine.chat("user_001", st.session_state.messages)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

        if st.button("Approve & Deploy Twin"):
            st.balloons()
            st.success("Twin deployed to the Arena. Check back tomorrow for your daily drop!")

if __name__ == "__main__":
    run_onboarding()