# 🦉 Purdue OWL Chatbot

A smart chatbot that helps students find and understand Purdue OWL writing resources. Ask questions about citations, formatting, and academic writing - get instant answers from the OWL knowledge base.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Features

- **APA Citations** - Format references, in-text citations, and bibliographies
- **MLA Citations** - Works Cited entries and parenthetical citations  
- **Email Etiquette** - Professional communication tips for students
- **RAG-Powered** - Uses retrieval-augmented generation for accurate answers

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

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

## 📁 Project Structure

```
owl-chatbot/
├── app.py              # Streamlit frontend
├── rag_engine.py       # RAG backend (ingestion + retrieval)
├── data/               # Purdue OWL content files
│   ├── apa_citations.txt
│   ├── mla_citations.txt
│   └── email_etiquette.txt
├── assets/             # Images and static files
│   └── purdue_logo.png
├── chromadb/           # Vector database (generated)
├── .streamlit/         # Streamlit configuration
├── requirements.txt    # Python dependencies
└── README.md
```

## 🛠️ How It Works

1. **Data Ingestion** - Text files in `/data` are split into chunks and converted to vectors
2. **Vector Storage** - ChromaDB stores the embeddings locally
3. **Retrieval** - User questions are matched against the knowledge base
4. **Response** - Relevant content is returned to answer the question

## 📦 Dependencies

- `streamlit` - Web interface
- `langchain` - Text processing and RAG framework
- `chromadb` - Vector database
- `sentence-transformers` - Text embeddings (HuggingFace)
- `openai` - LLM integration (for future use)

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
- Purdue University - GenAI resources

---

**Built by Purdue Students** 🚂
