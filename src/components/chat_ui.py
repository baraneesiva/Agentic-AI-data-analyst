import streamlit as st

def render_chat_interface():
    """
    Renders the chat interface and handles conversation history management.
    Adheres to:
    - Multi-Intent Natural Language Processing (NLP) input
    - Multi-Modal Output Generation rendering
    - Clear Memory Functionality
    """
    st.header("Chat with Data")
    
    # Initialize chat history if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # NOTE: In a full implementation, you would check 
            # if 'image' or 'dataframe' exists in message and render them here.

    # React to user input
    if prompt := st.chat_input("Ask a question about your data..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # --- In a real app, logic to call nlp_engine goes here ---
        response = f"Simulated response to: {prompt}"
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Clear Memory Functionality
    st.sidebar.markdown("---")
    st.sidebar.header("3. Session Control")
    if st.sidebar.button("Clear Memory"):
        # [cite_start]Context Wipe [cite: 64]
        st.session_state.messages = []
        st.rerun()

    return prompt