import streamlit as st
from app.services.llm_inference import twin_engine

def render_turing_test():
    st.title("🛡️ Phase 3: The Turing Test")
    st.markdown("### Verify your Twin's authenticity before Arena deployment.")
    
    st.info("""
    **Mission:** Chat with your twin to ensure it accurately reflects your professional depth, 
    communication style, and life goals. If it's wrong, tell it.
    """)

    if "turing_messages" not in st.session_state:
        st.session_state.turing_messages = []

    # Display conversation history
    for msg in st.session_state.turing_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Test your twin... (e.g., 'What is our 5-year plan?')"):
        st.session_state.turing_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # The twin_engine uses the memory_store (including Drive & Audio data)
            # to generate a response in character.
            response = twin_engine.chat("user_current", st.session_state.turing_messages)
            st.markdown(response)
            st.session_state.turing_messages.append({"role": "assistant", "content": response})

    st.divider()

    # The Deployment Gate
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Does this sound like you?")
    with col2:
        if st.button("🚀 DEPLOY TO ARENA", type="primary", use_container_width=True):
            # Update user status in DB to 'Arena-Ready'
            st.balloons()
            st.success("Digital Twin Deployed. The Arena is now active.")
            st.session_state.phase = "dashboard"
            st.rerun()