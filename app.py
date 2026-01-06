"""
Purdue OWL Chatbot - Streamlit Frontend
A chat interface for asking questions about citations and writing
"""

import streamlit as st
import re
from rag_engine import retrieve_context

# Page configuration
st.set_page_config(
    page_title="Purdue OWL Chatbot",
    page_icon="assets/purdue_logo.png",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
    }
    .main-header h1 {
        color: #CEB888;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .main-header p {
        color: #b0b0b0;
        font-size: 1rem;
    }
    .sidebar-description {
        background: rgba(206, 184, 136, 0.1);
        border-left: 3px solid #CEB888;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    .sidebar-description p {
        color: #e0e0e0;
        font-size: 0.9rem;
        line-height: 1.5;
        margin: 0;
    }
    .topic-list {
        background: rgba(255,255,255,0.05);
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .response-section {
        background: rgba(206, 184, 136, 0.05);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .response-section h4 {
        color: #CEB888;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    # Purdue Logo (local file)
    st.image("assets/purdue_logo.png", width=120)
    st.markdown("---")
    
    # About section
    st.markdown("### About Purdue OWL")
    st.markdown("""
    <div class="sidebar-description">
        <p>The <strong>Purdue Online Writing Lab (OWL)</strong> is a free writing resource maintained by Purdue University. 
        Since 1995, the OWL has helped millions of users worldwide improve their writing skills.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📚 I can help with:")
    st.markdown("""
    <div class="topic-list">
        • APA Citation Format<br>
        • MLA Citation Format<br>
        • Professional Email Writing<br>
        • Academic Writing Tips
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Reset chat button
    if st.button("🔄 Reset Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.caption("Based on Purdue OWL resources")
    st.caption("owl.purdue.edu")

# Main header
st.markdown("""
<div class="main-header">
    <h1>Purdue OWL Writing Assistant</h1>
    <p>Get help with citations, formatting, and academic writing</p>
</div>
""", unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def clean_response(context: str) -> str:
    """
    Clean up the retrieved context for a nicer display.
    Removes source headers and formats the content cleanly.
    """
    # Remove [Source X: filepath] headers
    cleaned = re.sub(r'\[Source \d+: [^\]]+\]\n?', '', context)
    
    # Remove the separator lines
    cleaned = cleaned.replace('\n\n---\n\n', '\n\n')
    
    # Remove duplicate newlines
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    
    # Trim whitespace
    cleaned = cleaned.strip()
    
    return cleaned


# Chat input
if prompt := st.chat_input("Ask about citations, formatting, or email etiquette..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get relevant context from the knowledge base
    with st.chat_message("assistant"):
        with st.spinner("Searching Purdue OWL resources..."):
            try:
                context = retrieve_context(prompt)
                cleaned_context = clean_response(context)
                
                # Format response nicely
                response = f"""Here's what I found from the Purdue OWL:

{cleaned_context}

---
*For more details, visit [Purdue OWL](https://owl.purdue.edu)*"""
                
                st.markdown(response)
                
                # Add assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_msg = f"⚠️ Error retrieving information: {str(e)}\n\nMake sure you've built the database by running `python rag_engine.py`"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
