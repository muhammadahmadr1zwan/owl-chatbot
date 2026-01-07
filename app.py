"""
Purdue OWL Chatbot - Streamlit Frontend
A chat interface for asking questions about citations and writing
Connected to Purdue's GenAI API
"""

import streamlit as st
import re
from openai import OpenAI
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
    .api-status {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-size: 0.85rem;
    }
    .api-connected {
        background: rgba(0, 255, 0, 0.1);
        border: 1px solid #00ff00;
        color: #00ff00;
    }
    .api-disconnected {
        background: rgba(255, 165, 0, 0.1);
        border: 1px solid #ffa500;
        color: #ffa500;
    }
</style>
""", unsafe_allow_html=True)

# System prompt for the AI
SYSTEM_PROMPT = """You are a helpful writing tutor at Purdue University. You assist students with citations, formatting, and academic writing questions.

Answer questions using ONLY the provided context below. Be concise, friendly, and helpful. Format your responses clearly with examples when appropriate.

If the answer is not in the context, say "I don't have that specific information in my current database. Please check the full Purdue OWL website at owl.purdue.edu for more details."

Context:
{context}"""

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    # Purdue Logo (local file)
    st.image("assets/purdue_logo.png", width=120)
    st.markdown("---")
    
    # API Key input
    st.markdown("### 🔑 API Configuration")
    api_key = st.text_input(
        "Purdue API Key",
        type="password",
        placeholder="Enter your GenAI API key",
        help="Get your API key from GenAI Studio"
    )
    
    # API Status indicator
    if api_key:
        st.markdown('<div class="api-status api-connected">✓ API Key configured</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="api-status api-disconnected">⚠ Enter API key to enable AI responses</div>', unsafe_allow_html=True)
    
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

# Display chat history (Session State handling)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def clean_context(context: str) -> str:
    """Clean up the retrieved context for the LLM."""
    # Remove [Source X: filepath] headers but keep content
    cleaned = re.sub(r'\[Source \d+: [^\]]+\]\n?', '', context)
    cleaned = cleaned.replace('\n\n---\n\n', '\n\n')
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned.strip()


def generate_response(user_query: str, context: str, api_key: str) -> str:
    """
    Generate a response using the Purdue GenAI API.
    
    Args:
        user_query: The user's question
        context: Retrieved context from the knowledge base
        api_key: Purdue API key
        
    Returns:
        AI-generated response
    """
    # Initialize OpenAI client pointing to Purdue's server
    client = OpenAI(
        base_url="https://genai.rcac.purdue.edu/api",
        api_key=api_key
    )
    
    # Create the system prompt with context
    system_message = SYSTEM_PROMPT.format(context=context)
    
    # Generate response
    response = client.chat.completions.create(
        model="llama-3-70b-instruct",  # Purdue's available model
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_query}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    return response.choices[0].message.content


# Chat input
if prompt := st.chat_input("Ask about citations, formatting, or email etiquette..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        # Show "Thinking..." spinner while processing
        with st.spinner("🦉 Thinking..."):
            try:
                # Step 1: Retrieve relevant context
                context = retrieve_context(prompt)
                cleaned_context = clean_context(context)
                
                # Step 2: Generate response with LLM (if API key provided)
                if api_key:
                    response = generate_response(prompt, cleaned_context, api_key)
                else:
                    # Fallback: Just show retrieved context if no API key
                    response = f"""**Here's what I found from the Purdue OWL:**

{cleaned_context}

---
*💡 Tip: Add your Purdue API key in the sidebar for smarter AI-powered responses!*"""
                
                st.markdown(response)
                
                # Add assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_msg = f"⚠️ Error: {str(e)}"
                
                # Provide helpful error messages
                if "API" in str(e) or "401" in str(e) or "403" in str(e):
                    error_msg += "\n\n**Possible fixes:**\n- Check that your API key is correct\n- Make sure you're connected to Purdue's network or VPN"
                elif "chromadb" in str(e).lower() or "database" in str(e).lower():
                    error_msg += "\n\n**Fix:** Run `python rag_engine.py` to build the database first."
                
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
