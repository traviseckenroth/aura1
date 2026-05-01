import streamlit as st
from PIL import Image
import json

st.set_page_config(page_title="Digital Twin: Daily Drop", layout="wide")

def load_simulated_matches():
    """
    Simulates fetching the top results from the 'twin_simulations' table 
    populated by the overnight batch worker.
    """
    return [
        {
            "id": "user_102",
            "name": "Sarah",
            "score": 92,
            "image": "data/profiles/user_102.jpg",
            "summary": [
                "Both twins share a background in quantitative finance.",
                "High alignment on FIRE timeline (retirement by 48).",
                "Debated Python vs. Rust for trading bot execution."
            ],
            "transcript": [
                {"role": "Sarah's Twin", "content": "I noticed your profile mentions Bitcoin bots. Do you focus on high-frequency arbitrage or trend following?"},
                {"role": "Your Twin", "content": "Mostly trend following with a hint of mean reversion. It keeps the FIRE goal on track without constant manual oversight."},
                {"role": "Sarah's Twin", "content": "Efficiency is key. I'm building a similar stack for equities right now."}
            ]
        },
        {
            "id": "user_105",
            "name": "Jordan",
            "score": 85,
            "image": "data/profiles/user_105.jpg",
            "summary": [
                "Strong mutual interest in edgy, relaxed tailoring.",
                "Both value technical program management efficiency.",
                "Similar sense of humor regarding legacy codebases."
            ],
            "transcript": [
                {"role": "Your Twin", "content": "I'm a big fan of relaxed tailoring. It's hard to find that balance between professional and edgy."},
                {"role": "Jordan's Twin", "content": "Exactly. If I have to wear a suit, I want it to feel like streetwear. What brands are you tracking?"}
            ]
        }
    ]

def render_dashboard():
    st.title("📬 Your Daily Drop")
    st.info("Your Digital Twin met 50 people last night. These 2 matches showed the highest chemistry.")

    matches = load_simulated_matches()

    for match in matches:
        with st.container(border=True):
            col1, col2 = st.columns([1, 3])

            with col1:
                # Display match profile photo
                try:
                    img = Image.open(match['image'])
                    st.image(img, use_column_width=True)
                except:
                    st.warning("Profile Image Placeholder")
                
                st.metric("Compatibility Score", f"{match['score']}%")

            with col2:
                st.subheader(f"Twin Dossier: {match['name']}")
                
                # Render the 3-bullet point summary from the Evaluator Prompt
                st.markdown("**Conversational Highlights:**")
                for point in match['summary']:
                    st.write(f"- {point}")

                # Read-only vault for the AI transcript (Requirement #6)
                with st.expander("📂 View AI Conversation Transcript"):
                    for msg in match['transcript']:
                        st.write(f"**{msg['role']}:** {msg['content']}")

                # The Human Handoff (Requirement #6)
                if st.button(f"Start Real Chat with {match['name']}", key=match['id']):
                    st.session_state.current_human_chat = match['name']
                    st.session_state.icebreaker = f"Hey {match['name']}! Our twins were just geeking out over {match['summary'][0].lower()}..."
                    st.rerun()

    # --- HUMAN CHAT MODAL (STRICTLY SEPARATE) ---
    if 'current_human_chat' in st.session_state:
        st.divider()
        st.header(f"💬 Chatting with {st.session_state.current_human_chat}")
        st.caption("Strictly Human-to-Human Channel")
        
        # Display the suggested icebreaker to help the user start
        st.text_area("Icebreaker Suggestion:", value=st.session_state.icebreaker, height=70)
        
        # Standard chat input (Human only)
        user_input = st.chat_input(f"Message {st.session_state.current_human_chat}...")
        if user_input:
            st.success(f"Message sent to {st.session_state.current_human_chat}")

if __name__ == "__main__":
    render_dashboard()