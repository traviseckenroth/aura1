import streamlit as st

def show_dashboard(user_id):
    st.title("Matched Dossiers")
    
    # Fetch matches that passed both Visual and Conversational filters
    matches = db.get_validated_matches(user_id)

    for match in matches:
        with st.container(border=True):
            st.image(match.profile_pic)
            st.subheader(f"Match: {match.name}")
            
            # User reviews the AI conversation
            with st.expander("📝 Review Twin Conversation"):
                for msg in match.transcript:
                    st.write(f"**{msg['role']}:** {msg['content']}")
            
            # User engages manually
            if st.button(f"Take Over Conversation with {match.name}"):
                start_human_chat(match.id)