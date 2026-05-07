<div align="center">

# 🕵️ LLM-CerebroScope

**Enterprise-Grade Forensic Data Analysis & Logic Engine**

*Transparent, Traceable, AI-Powered Document Intelligence*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP%208-blue.svg)](https://pep8.org/)

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Architecture](#-architecture)
- [Troubleshooting](#-troubleshooting)
- [Use Cases](#-use-cases)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 Overview

**LLM-CerebroScope** is a sophisticated forensic data analysis platform that combines Large Language Models (LLMs) with advanced vector search technology. Designed for professionals who require transparent, auditable, and traceable document analysis, CerebroScope provides enterprise-grade capabilities for:

- **Document Intelligence**: Multi-format ingestion with intelligent chunking
- **Semantic Retrieval**: Advanced vector search using ChromaDB
- **LLM-Powered Analysis**: Integration with Ollama for local, privacy-preserving inference
- **Source Attribution**: Automatic citation tracking with chunk-level granularity
- **Conflict Detection**: AI-powered contradiction and inconsistency identification
- **Reliability Scoring**: Metadata-based source credibility assessment

### Why CerebroScope?

✅ **Transparency**: Every answer includes traceable citations to source documents  
✅ **Privacy**: Fully local processing with Ollama (no cloud dependencies)  
✅ **Accuracy**: Reliability scoring and conflict detection ensure high-quality results  
✅ **Flexibility**: Dual interfaces (CLI & Web GUI) for different workflows  
✅ **Extensibility**: Modular architecture designed for customization

---

## ✨ Key Features

### 📄 Document Processing
- **Multi-Format Support**: PDF, CSV, TXT, XLSX/XLS
- **Intelligent Chunking**: Configurable size (800 chars) and overlap (100 chars)
- **Metadata Preservation**: Source, page numbers, timestamps, and file modification dates
- **Incremental Ingestion**: Automatic detection of new/modified files

### 🔍 Semantic Search
- **Vector Database**: ChromaDB-powered persistent storage
- **Embedding Generation**: Automatic text embeddings using default models
- **Source Filtering**: Search within specific documents or collections
- **Top-K Retrieval**: Configurable result ranking (default: 5 chunks)

### 🧠 AI Analysis Engine
- **Model Agnostic**: Works with any Ollama-compatible LLM
- **Citation Tracking**: Automatic `[ID: xxxxxxxx]` format citations in responses
- **Context Awareness**: Prioritizes newer sources when conflicts arise
- **Prompt Engineering**: Optimized forensic analysis prompts

### ⚠️ Validation & Quality Assurance
- **Conflict Detection**: LLM-powered contradiction identification
- **Reliability Scoring**: Heuristic algorithm considering:
  - File format (structured data preferred)
  - Document recency (time-based decay)
  - Metadata completeness
- **Evidence Heatmaps**: Visual highlighting of used vs. ignored chunks

### 📊 Visualization & Reporting
- **Interactive Graphs**: Knowledge graph visualization using spaCy NER
- **Entity Extraction**: Automatic identification of organizations, people, locations, dates, monetary values
- **Evidence Cards**: Color-coded display (green = used, gray = ignored)
- **Markdown Reports**: Comprehensive, timestamped analysis reports

### 💻 Dual Interface
- **Rich CLI**: Beautiful terminal interface using Rich library
- **Streamlit GUI**: Modern web dashboard with drag-and-drop file upload
- **Feature Parity**: Both interfaces support all core functionality

---

## 💻 System Requirements

- **Python**: 3.8+
- **RAM**: 4 GB minimum (8 GB recommended)
- **Storage**: 500 MB + space for documents and database
- **Ollama**: [Install from ollama.ai](https://ollama.ai/)
- **Optional**: spaCy model for graph visualization (`python -m spacy download en_core_web_sm`)

---

## 🚀 Installation

```bash
# 1. Clone repository
git clone https://github.com/oskarbrzycki/llm-cerebroscope.git
cd LLM-CerebroScope

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install ollama chromadb streamlit streamlit-agraph rich pandas pypdf spacy
python -m spacy download en_core_web_sm

# 4. Setup Ollama
ollama serve  # Keep running in separate terminal
ollama pull llama3  # Download a model

# 5. Initialize data directory
mkdir -p data/raw
```

---

## 🏃 Quick Start

1. **Add documents** to `data/raw/` directory
2. **Launch interface**:
   - CLI: `python -m cerebro.cli`
   - GUI: `streamlit run cerebro/gui.py` → `http://localhost:8501`
3. **Query documents**: Ask questions in natural language
4. **Review results**: Check citations `[ID: xxxxxxxx]`, conflicts, and download reports

---

## 📖 Usage Guide

### Command-Line Interface

```bash
python -m cerebro.cli
```

**Workflow**: Select model → Auto-ingest documents → Query in natural language → View formatted results → Type `exit` to quit

### Web Interface

```bash
streamlit run cerebro/gui.py
```

**Features**: Model selection, file upload, source filtering, chat interface, graph visualization, evidence cards, report download

---

## 🏗️ Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                  │
├──────────────────────┬──────────────────────────────────┤
│   Rich CLI           │      Streamlit GUI               │
└──────────┬───────────┴────────────┬─────────────────────┘
           │                        │
           └────────────┬───────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                  Application Core                        │
├──────────────┬──────────────┬───────────────────────────┤
│   Ingester   │ VectorStore  │    Tracer                 │
│              │              │                           │
│ • PDF        │ • ChromaDB   │ • LLM Query Analysis      │
│ • CSV/TXT    │ • Embeddings │ • Citation Generation     │
│ • Excel      │ • Metadata   │ • Context Formatting      │
└──────────────┴──────────────┴───────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│              Validation & Reporting Layer                │
├──────────────┬──────────────┬───────────────────────────┤
│  Validator   │  Reporter    │    Graph                  │
│              │              │                           │
│ • Conflicts  │ • Markdown   │ • Entity Extraction       │
│ • Reliability│ • Timestamps │ • Knowledge Graphs        │
│ • Scoring    │ • Evidence   │ • Visualization           │
└──────────────┴──────────────┴───────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                   External Services                      │
├──────────────────────┬──────────────────────────────────┤
│      Ollama API      │      ChromaDB                    │
│   (LLM Inference)    │   (Vector Storage)               │
└──────────────────────┴──────────────────────────────────┘
```

### Data Flow

```
┌──────────────┐
│  Documents   │ (PDF/CSV/TXT/XLSX)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Ingester    │ → Chunks (800 chars, 100 overlap)
└──────┬───────┘   Metadata (source, page, timestamp)
       │
       ▼
┌──────────────┐
│ VectorStore  │ → Embeddings → ChromaDB
└──────┬───────┘
       │
       │ Query
       ▼
┌──────────────┐
│ VectorStore  │ → Top-K Retrieval → Chunks
└──────┬───────┘
       │
       ├─────────────────┐
       ▼                 ▼
┌──────────────┐  ┌──────────────┐
│   Tracer     │  │  Validator   │
│ (Analysis)   │  │ (Conflicts)  │
└──────┬───────┘  └──────┬───────┘
       │                 │
       └────────┬────────┘
                ▼
         ┌──────────────┐
         │   Reporter   │ → Markdown Report
         └──────────────┘
```

### Core Components

- **`Ingester`**: Document processing and chunking (PDF, CSV, TXT, Excel)
- **`CerebroVectorStore`**: ChromaDB vector database management
- **`CerebroTracer`**: LLM-powered query analysis with citation generation
- **`CerebroValidator`**: Conflict detection and reliability scoring
- **`CerebroReporter`**: Markdown report generation
- **`CerebroGraph`**: Knowledge graph visualization (spaCy NER)
- **`CerebroFormatter`**: Rich CLI formatting

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Ollama connection error | Run `ollama serve` in separate terminal |
| No models available | Download with `ollama pull llama3` |
| spaCy model missing | Run `python -m spacy download en_core_web_sm` |
| ChromaDB errors | Reset database: `rm -rf data/chroma_db` |
| Import errors | Reinstall: `pip install -r requirements.txt` |
| Memory issues | Reduce `chunk_size` or process in batches |

---

## 🚀 Performance Optimization

### For Large Document Collections

1. **Batch Processing**: Process documents in smaller batches
   ```python
   # Process files in batches of 10
   for batch in chunked(files, 10):
       chunks = ingester.ingest_directory(batch)
       vector_db.add_chunks(chunks)
   ```

2. **Optimize Chunking**: Adjust chunk size based on document type
   ```python
   # For technical documents
   ingester = Ingester(chunk_size=1000, chunk_overlap=150)
   
   # For structured data (CSV)
   ingester = Ingester(chunk_size=500, chunk_overlap=50)
   ```

3. **Database Indexing**: ChromaDB automatically indexes, but you can:
   - Use persistent storage (default)
   - Monitor database size with `du -sh data/chroma_db`

4. **Model Selection**: Use smaller models for faster inference
   ```bash
   # Faster but less accurate
   ollama pull phi
   
   # Balanced
   ollama pull llama3
   
   # Slower but more accurate
   ollama pull mistral
   ```

### For Production Deployment

1. **Use Production Ollama**: Deploy Ollama as a service
2. **Database Backup**: Regularly backup `data/chroma_db`
3. **Monitor Resources**: Track CPU, RAM, and disk usage
4. **Caching**: Implement result caching for frequent queries
5. **Load Balancing**: Use multiple Ollama instances for high traffic

---

## 📊 Use Cases

- **Legal Analysis**: Search case files, identify precedents, detect contradictions
- **Research Review**: Analyze papers, detect conflicting methodologies, extract entities
- **Business Intelligence**: Query financial reports, extract metrics, generate insights
- **Compliance Auditing**: Check policy violations, generate audit trails
- **Knowledge Base**: Internal Q&A system with traceable citations

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m "Add amazing feature"`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

**Code Style**: Follow PEP 8, use type hints, add docstrings.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

### Core Technologies
- **[Ollama](https://ollama.ai/)** - Local LLM inference engine
- **[ChromaDB](https://www.trychroma.com/)** - Open-source vector database
- **[Streamlit](https://streamlit.io/)** - Rapid web app development
- **[Rich](https://github.com/Textualize/rich)** - Beautiful terminal formatting
- **[spaCy](https://spacy.io/)** - Natural language processing

### Inspiration
Built with ❤️ for professionals who need transparent, traceable, and auditable AI-powered document analysis.

---

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/oskarbrzycki/llm-cerebroscope/issues)
- **Discussions**: [GitHub Discussions](https://github.com/oskarbrzycki/llm-cerebroscope/discussions)

---

<div align="center">

**Made with 🔍 by the CerebroScope Team**

*Empowering transparent AI-powered document intelligence*

[⬆ Back to Top](#-llm-cerebroscope)

</div>

