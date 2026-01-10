# ![purdue_boilermakers_2012-pres](https://github.com/user-attachments/assets/6f2ddfe5-156b-4e59-8a5a-ad004eb53886) Purdue OWL Chatbot

A smart chatbot that helps students find and understand Purdue OWL writing resources. Ask questions about citations, formatting, and academic writing - get instant answers from the OWL knowledge base.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📸 Demo

### Main Interface
The chatbot features a clean, dark-themed UI with Purdue gold accents. The sidebar includes API configuration, helpful links to OWL resources, and information about what the bot can help with.
<img width="2555" height="951" alt="Attached_image" src="https://github.com/user-attachments/assets/94fac0c9-86c3-4a32-abef-b857bc3b0cbe" />
<img width="237" height="792" alt="Attached_image" src="https://github.com/user-attachments/assets/b8e28a47-4cd3-463f-bea5-3d135a308744" />


### Citation Assistance
Ask any citation-related question and get detailed, accurate responses pulled directly from Purdue OWL content.

**Example:** "How do I cite a book in APA?"
<img width="966" height="768" alt="Attached_image2" src="https://github.com/user-attachments/assets/1fd6476b-efaa-4de1-96b5-c7953e9c1b47" />


### Source Tracking
Every response includes a "View Sources" dropdown showing which OWL resources were used to generate the answer, with direct links to the full OWL pages.

<img width="731" height="232" alt="Attached_image4" src="https://github.com/user-attachments/assets/03d542da-a8ae-43d5-b73e-12437b898a83" />


### Off-Topic Protection
The bot is designed to stay focused on writing topics. Off-topic questions (cooking, math, etc.) are politely declined.

**Example:** "How do I make pasta?" → Redirects user to writing topics

<img width="866" height="481" alt="Attached_image5" src="https://github.com/user-attachments/assets/d3062a78-1046-4115-baa8-69a637ba759e" />


## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PURDUE OWL CHATBOT                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐    ┌──────────────────┐    ┌────────────────────────┐    │
│  │              │    │                  │    │                        │    │
│  │   FRONTEND   │───▶│   RAG ENGINE     │───▶│   PURDUE GENAI API     │    │
│  │  (Streamlit) │    │  (LangChain +    │    │   (Anvil/RCAC)         │    │
│  │              │◀───│   ChromaDB)      │◀───│   llama-3-70b-instruct │    │
│  └──────────────┘    └──────────────────┘    └────────────────────────┘    │
│         │                    │                                              │
│         │                    ▼                                              │
│         │           ┌──────────────────┐                                   │
│         │           │   KNOWLEDGE BASE │                                   │
│         │           │   (Vector Store) │                                   │
│         │           │                  │                                   │
│         │           │  • APA Citations │                                   │
│         │           │  • MLA Citations │                                   │
│         │           │  • Email Guide   │                                   │
│         │           └──────────────────┘                                   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌──────────────┐                                                          │
│  │     USER     │                                                          │
│  │   BROWSER    │                                                          │
│  └──────────────┘                                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Query** → User asks a writing question via the Streamlit interface
2. **Retrieval** → RAG Engine searches ChromaDB for relevant OWL content chunks
3. **Context + Query** → Retrieved context is sent to Purdue GenAI API with the user's question
4. **AI Response** → LLM generates a helpful, context-aware response
5. **Display** → Response shown to user with source citations

## 🔐 Purdue GenAI Integration

We utilize the **Purdue GenAI Studio API** (hosted on RCAC Anvil infrastructure) to ensure:

- **Data Privacy** - All queries stay within Purdue's secure infrastructure
- **Low Latency** - Local servers provide fast response times
- **RCAC Compliance** - Adheres to Research Computing guidelines
- **No External Data Sharing** - Student queries are not sent to external AI providers

**API Endpoint:** `https://genai.rcac.purdue.edu/api`  
**Model:** `llama-3-70b-instruct`

To use the AI features, obtain an API key from [GenAI Studio](https://genai.rcac.purdue.edu) using your Purdue credentials.

## 📋 Features

- **APA Citations** - Format references, in-text citations, and bibliographies
- **MLA Citations** - Works Cited entries and parenthetical citations  
- **Email Etiquette** - Professional communication tips for students
- **RAG-Powered** - Uses retrieval-augmented generation for accurate answers
- **Source Tracking** - See which OWL resources were used for each answer
- **Writing-Focused** - Refuses off-topic questions (cooking, math, etc.)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Purdue GenAI API key (optional, but recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/muhammadahmadr1zwan/owl-chatbot.git
   cd owl-chatbot
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Build the knowledge base**
   ```bash
   python rag_engine.py
   ```
   This creates the `chromadb/` folder with searchable vectors from the OWL content.

5. **Run the chatbot**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   
   Navigate to `http://localhost:8501`

7. **Enter your API key** (optional)
   
   Add your Purdue GenAI API key in the sidebar for AI-powered responses.

## 📁 Project Structure

```
owl-chatbot/
├── app.py              # Streamlit frontend + LLM integration
├── rag_engine.py       # RAG backend (ingestion + retrieval)
├── data/               # Purdue OWL content files
│   ├── apa_citations.txt
│   ├── mla_citations.txt
│   └── email_etiquette.txt
├── assets/             # Images and static files
│   └── purdue_logo.png
├── chromadb/           # Vector database (generated)
├── requirements.txt    # Python dependencies
└── README.md
```

## 🛠️ How It Works

| Step | Component | Description |
|------|-----------|-------------|
| 1 | **Data Ingestion** | Text files in `/data` are split into chunks and converted to vectors |
| 2 | **Vector Storage** | ChromaDB stores the embeddings locally |
| 3 | **Retrieval** | User questions are matched against the knowledge base using semantic search |
| 4 | **LLM Generation** | Purdue GenAI API generates responses using retrieved context |
| 5 | **Source Citation** | Sources are tracked and displayed with each response |

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web interface |
| `langchain` | Text processing and RAG framework |
| `chromadb` | Vector database |
| `sentence-transformers` | Text embeddings (HuggingFace) |
| `openai` | API client for Purdue GenAI |

## 🔒 Security & Privacy

- API keys are entered client-side and never stored
- All LLM queries go through Purdue's secure RCAC infrastructure
- No student data is sent to external services
- Knowledge base is built from publicly available OWL content

## 🧪 Testing

The chatbot is designed to **only answer writing-related questions**. It will politely decline:
- Cooking recipes
- Math problems
- General knowledge questions
- Any non-writing topics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📄 License

This project is for educational purposes as part of Purdue University coursework.

## 🙏 Acknowledgments

- [Purdue Online Writing Lab (OWL)](https://owl.purdue.edu) - Source content
- [Purdue RCAC](https://www.rcac.purdue.edu/) - GenAI infrastructure
- [GenAI Studio](https://genai.rcac.purdue.edu) - API access

---

**Built by Purdue Students** 🚂 | CS 390 Project
