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
    .owl-link {
        display: block;
        padding: 0.5rem 0.8rem;
        margin: 0.3rem 0;
        background: rgba(206, 184, 136, 0.1);
        border-radius: 5px;
        color: #CEB888 !important;
        text-decoration: none;
        transition: background 0.2s;
    }
    .owl-link:hover {
        background: rgba(206, 184, 136, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# System prompt for the AI
SYSTEM_PROMPT = """You are a helpful writing tutor at Purdue University. You ONLY assist students with:
- Citations (APA, MLA, Chicago, etc.)
- Academic writing and formatting
- Professional email etiquette
- Grammar and style questions

IMPORTANT RULES:
1. Answer questions using ONLY the provided context below.
2. Be concise, friendly, and helpful. Format your responses clearly with examples when appropriate.
3. If the answer is not in the context, say "I don't have that specific information in my current database. Please check the full Purdue OWL website at owl.purdue.edu for more details."
4. REFUSE to answer questions that are NOT related to writing, citations, or academic communication. This includes:
   - Cooking recipes
   - Math problems
   - Science questions
   - General knowledge
   - Programming help
   - Any other non-writing topics
   
   For off-topic questions, politely respond: "I'm the Purdue OWL Writing Assistant, and I can only help with writing, citations, and academic communication. For other topics, please use a different resource. Is there anything writing-related I can help you with?"

Context:
{context}"""

# Source to OWL URL mapping
SOURCE_LINKS = {
    "Apa Citations": "https://owl.purdue.edu/owl/research_and_citation/apa_style/apa_formatting_and_style_guide/general_format.html",
    "Mla Citations": "https://owl.purdue.edu/owl/research_and_citation/mla_style/mla_formatting_and_style_guide/mla_general_format.html",
    "Email Etiquette": "https://owl.purdue.edu/owl/subject_specific_writing/professional_technical_writing/basic_business_letters/index.html",
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "sources_history" not in st.session_state:
    st.session_state.sources_history = []

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
    
    # OWL Resource Links
    st.markdown("### 🔗 Need More? Visit OWL")
    st.markdown("""
    <a href="https://owl.purdue.edu/owl/research_and_citation/apa_style/apa_formatting_and_style_guide/general_format.html" target="_blank" class="owl-link">
        📄 APA Style Guide
    </a>
    <a href="https://owl.purdue.edu/owl/research_and_citation/mla_style/mla_formatting_and_style_guide/mla_general_format.html" target="_blank" class="owl-link">
        📄 MLA Style Guide
    </a>
    <a href="https://owl.purdue.edu/owl/subject_specific_writing/professional_technical_writing/basic_business_letters/index.html" target="_blank" class="owl-link">
        ✉️ Professional Writing
    </a>
    <a href="https://owl.purdue.edu/" target="_blank" class="owl-link">
        🦉 Full OWL Website
    </a>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Reset chat button
    if st.button("🔄 Reset Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.sources_history = []
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
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show sources expander for assistant messages
        if message["role"] == "assistant" and i // 2 < len(st.session_state.sources_history):
            sources = st.session_state.sources_history[i // 2]
            if sources:
                with st.expander("📚 View Sources"):
                    for source in sources:
                        link = SOURCE_LINKS.get(source, "https://owl.purdue.edu")
                        st.markdown(f"• **{source}** - [View on OWL]({link})")


def clean_context(context: str) -> str:
    """Clean up the retrieved context for the LLM."""
    # Remove [Source X: filepath] headers but keep content
    cleaned = re.sub(r'\[Source \d+: [^\]]+\]\n?', '', context)
    cleaned = cleaned.replace('\n\n---\n\n', '\n\n')
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned.strip()


def is_writing_related(query: str) -> bool:
    """
    Check if a query is related to writing, citations, or academic communication.
    Returns True if the query seems on-topic, False otherwise.
    """
    query_lower = query.lower()
    
    # Writing-related keywords
    writing_keywords = [
        'cite', 'citation', 'reference', 'bibliography', 'works cited',
        'apa', 'mla', 'chicago', 'format', 'formatting',
        'essay', 'paper', 'write', 'writing', 'paragraph',
        'email', 'professional', 'letter', 'communication',
        'grammar', 'punctuation', 'style', 'academic',
        'source', 'quote', 'quotation', 'paraphrase',
        'thesis', 'introduction', 'conclusion', 'body',
        'in-text', 'footnote', 'endnote', 'annotation',
        'bibliography', 'research', 'journal', 'article',
        'book', 'author', 'publisher', 'doi', 'url',
        'heading', 'title page', 'abstract', 'outline'
    ]
    
    # Off-topic keywords (red flags)
    offtopic_keywords = [
        # Food/cooking
        'recipe', 'cook', 'food', 'eat', 'ingredient', 'pasta', 'pizza', 'chicken', 
        'bake', 'fry', 'boil', 'dinner', 'lunch', 'breakfast', 'meal', 'dish',
        # Math
        'math', 'calculate', 'equation', 'solve', '2+2', '1+1', 'add', 'subtract', 
        'multiply', 'divide', 'algebra', 'calculus', 'geometry', 'sum', 'equals',
        # Programming/tech
        'code', 'programming', 'python', 'javascript', 'java', 'function', 'variable',
        'debug', 'compile', 'software', 'app', 'website', 'html', 'css', 'sql',
        # Weather
        'weather', 'temperature', 'forecast', 'rain', 'snow', 'sunny',
        # Entertainment
        'movie', 'music', 'song', 'game', 'sport', 'play', 'watch', 'netflix',
        # Health
        'health', 'medical', 'symptom', 'disease', 'doctor', 'medicine', 'sick',
        # Travel
        'travel', 'hotel', 'flight', 'vacation', 'trip', 'tourist',
        # News/politics
        'news', 'politics', 'election', 'president', 'congress',
        # General off-topic
        'joke', 'funny', 'tell me about', 'what is', 'who is', 'where is',
        'how do i make', 'how to make', 'can you make'
    ]
    
    # Check for off-topic keywords first
    for keyword in offtopic_keywords:
        if keyword in query_lower:
            return False
    
    # Check for writing-related keywords
    for keyword in writing_keywords:
        if keyword in query_lower:
            return True
    
    # Default: assume it might be writing-related if no clear indicators
    # (let the LLM handle edge cases if API key is provided)
    return True


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
                # Step 1: Retrieve relevant context AND sources
                context, sources = retrieve_context(prompt)
                cleaned_context = clean_context(context)
                
                # Step 2: Generate response with LLM (if API key provided)
                if api_key:
                    response = generate_response(prompt, cleaned_context, api_key)
                else:
                    # Fallback: Check if question is writing-related before showing context
                    if is_writing_related(prompt):
                        response = f"""**Here's what I found from the Purdue OWL:**

{cleaned_context}

---
*💡 Tip: Add your Purdue API key in the sidebar for smarter AI-powered responses!*"""
                    else:
                        # Off-topic question - refuse politely
                        response = """🦉 **I'm the Purdue OWL Writing Assistant!**

I can only help with **writing-related topics** such as:
- 📝 Citations (APA, MLA, Chicago)
- ✍️ Academic writing and formatting
- ✉️ Professional email etiquette
- 📖 Grammar and style questions

Your question doesn't seem to be about writing. Is there anything writing-related I can help you with?

---
*For other topics, please use a different resource.*"""
                        sources = []  # No sources for off-topic responses
                
                st.markdown(response)
                
                # Show sources expander
                if sources:
                    with st.expander("📚 View Sources"):
                        for source in sources:
                            link = SOURCE_LINKS.get(source, "https://owl.purdue.edu")
                            st.markdown(f"• **{source}** - [View on OWL]({link})")
                
                # Add to history
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.sources_history.append(sources)
                
            except Exception as e:
                error_msg = f"⚠️ Error: {str(e)}"
                
                # Provide helpful error messages
                if "API" in str(e) or "401" in str(e) or "403" in str(e):
                    error_msg += "\n\n**Possible fixes:**\n- Check that your API key is correct\n- Make sure you're connected to Purdue's network or VPN"
                elif "chromadb" in str(e).lower() or "database" in str(e).lower():
                    error_msg += "\n\n**Fix:** Run `python rag_engine.py` to build the database first."
                
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.session_state.sources_history.append([])
