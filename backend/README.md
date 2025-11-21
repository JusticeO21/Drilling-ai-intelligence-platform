# 🏭 DrillData AI - Intelligent Oil Drilling Data Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-orange.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**DrillData AI** is an enterprise-grade AI-powered platform that transforms oil drilling data analysis through natural language processing and retrieval-augmented generation (RAG). Upload drilling reports, well logs, and operational data, then query them conversationally to extract insights, identify patterns, and make data-driven decisions.

## 🎯 Problem Solved

Traditional oil drilling data analysis is trapped in spreadsheets and static reports. **DrillData AI** democratizes access to complex drilling data by enabling natural language queries like:

- *"What were the drilling parameters when we hit that high-pressure zone?"*
- *"Show me all wells with ROP above 150 ft/hr in the last quarter"*
- *"Compare mud weight trends between successful and problematic wells"*
- *"What safety incidents occurred during night shifts this month?"*

## 🚀 Key Features

### 🤖 AI-Powered Analysis
- **Conversational Queries**: Ask questions in natural language
- **Contextual Responses**: AI understands drilling terminology and concepts
- **Multi-Modal Support**: Works with CSV, Excel, and structured drilling reports
- **Intelligent Insights**: Identifies patterns and correlations in drilling data

### 🏗️ Enterprise Architecture
- **Microservices Design**: Scalable API and AI services
- **Session Isolation**: Secure, per-user data sessions with automatic cleanup
- **Vector Search**: Fast similarity search using ChromaDB
- **Production Ready**: Comprehensive logging, error handling, and monitoring

### 🔧 Flexible Deployment
- **Multi-Model Support**: OpenAI GPT-4 or local Ollama models (Llama, Mistral, etc.)
- **Docker Ready**: Containerized deployment with docker-compose
- **Configurable**: Environment-based configuration for different environments
- **API First**: RESTful APIs for easy integration

## 🏛️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Service   │    │   AI Service    │
│   (React/Vue)   │◄──►│   (FastAPI)     │◄──►│   (LangChain)   │
│                 │    │                 │    │                 │
│ • File Upload   │    │ • Data Ingestion│    │ • RAG Engine    │
│ • Chat Interface│    │ • Session Mgmt  │    │ • LLM Integration│
│ • Data Viz      │    │ • Vector Storage│    │ • Agent Logic   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   ChromaDB      │    │   Ollama/       │
                       │   Vector DB     │    │   OpenAI API    │
                       └─────────────────┘    └─────────────────┘
```

## 🛠️ Technology Stack

### Backend Framework
- **FastAPI**: High-performance async web framework
- **Pydantic**: Data validation and serialization
- **SQLAlchemy**: Database ORM (future extensibility)

### AI & NLP
- **LangChain**: LLM orchestration and RAG pipelines
- **LangGraph**: Agent workflow management
- **ChromaDB**: Vector database for embeddings
- **Sentence Transformers**: Text embedding generation

### LLM Support
- **OpenAI**: GPT-4, GPT-3.5-turbo (cloud)
- **Ollama**: Llama 2, Mistral, CodeLlama (local)

### Data Processing
- **Pandas**: Data manipulation and analysis
- **Unstructured**: Document loading and parsing
- **RecursiveCharacterTextSplitter**: Intelligent text chunking

## 📁 Project Structure

```
drilldata-ai/
├── common/                          # Shared utilities
│   ├── config.py                    # Global configuration
│   ├── database.py                  # Database setup
│   ├── logging.py                   # Logging configuration
│   └── rag.py                       # RAG system orchestration
├── services/
│   ├── ai/                          # AI microservice
│   │   ├── common/                  # AI utilities & config
│   │   │   ├── config.py            # AI-specific settings
│   │   │   ├── models.py            # LLM configurations
│   │   │   ├── utils.py             # RAG utilities
│   │   │   └── document_processor.py # File processing
│   │   ├── agents/                  # AI agents
│   │   │   ├── base_agent.py        # Base agent class
│   │   │   └── drilling_agent.py    # Drilling domain expert
│   │   ├── chains/                  # LangChain chains
│   │   │   ├── conversation_chain.py # Chat orchestration
│   │   │   └── rag_chain.py         # RAG pipelines
│   │   ├── tools/                   # Custom tools
│   │   └── main.py                  # AI service entry point
│   └── api/                         # REST API microservice
│       ├── app/
│       │   ├── main.py              # FastAPI application
│       │   ├── models/              # SQLAlchemy models
│       │   ├── routers/             # API endpoints
│       │   │   ├── chat.py          # Chat endpoints
│       │   │   ├── drilling.py      # Data upload/query
│       │   │   └── wells.py         # Well information
│       │   └── schemas/             # Pydantic schemas
│       ├── tests/                   # Unit tests
│       └── Dockerfile               # Container config
├── docker-compose.yml               # Multi-service orchestration
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Docker & Docker Compose** (recommended)
- **Ollama** (for local models) OR **OpenAI API key** (for cloud models)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/drilldata-ai.git
   cd drilldata-ai
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

1. **Start Ollama (if using local models)**
   ```bash
   ollama serve
   ollama pull llama2  # or your preferred model
   ```

2. **Run the application**
   ```bash
   # Terminal 1: API Service
   uvicorn services.api.app.main:app --reload --port 8000

   # Terminal 2: AI Service (if running separately)
   python services/ai/main.py
   ```

3. **Access the API**
   - **API Documentation**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health

### Docker Deployment

#### Quick Start with Docker Compose
```bash
# Clone the repository
git clone <repository-url>
cd drilldata-ai

# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env  # Configure your API keys and settings

# Start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

#### Service Architecture
- **API Service**: `http://localhost:8000` - REST API endpoints
- **AI Service**: Internal service for chat processing
- **Ollama**: `http://localhost:11434` - Local LLM server
- **PostgreSQL**: `localhost:5432` - Database (optional)

#### Development Mode
```bash
# Use development overrides (hot reloading enabled)
docker-compose -f docker-compose.yml -f docker-compose.override.yml up --build
```

#### Production Deployment
```bash
# Build production images
docker-compose build

# Run with production settings
docker-compose up -d
```

#### Individual Services
```bash
# Run only API service
docker-compose up api

# Run with AI service
docker-compose --profile ai up

# Run with database
docker-compose --profile db up
```

#### Docker Image Details
- **Base Image**: `python:3.11-slim`
- **Multi-stage Build**: Optimized for production
- **Security**: Non-root user execution
- **Health Checks**: Automatic service monitoring

## 📚 API Documentation

### Core Endpoints

#### Data Management
```http
POST /api/v1/drilling/upload
```
Upload CSV/Excel drilling data files for analysis.

**Request:**
- `file`: Multipart file (CSV/Excel)
- Returns: `session_id` for subsequent queries

#### AI Chat
```http
POST /api/v1/chat/
```
Query uploaded drilling data using natural language.

**Request:**
```json
{
  "session_id": "uuid-here",
  "message": {
    "role": "user",
    "content": "What is the average ROP in shale formations?"
  },
  "chat_history": []
}
```

**Response:**
```json
{
  "message": {
    "role": "assistant",
    "content": "Based on the uploaded data, the average ROP in shale formations is 85 ft/hr..."
  },
  "session_id": "uuid-here",
  "model_provider": "ollama",
  "processing_time": 1.23
}
```

#### Session Management
```http
GET /api/v1/drilling/session/{session_id}
```
Get information about an active data session.

### Example Usage

```python
import requests

# 1. Upload drilling data
files = {'file': open('drilling_report.xlsx', 'rb')}
response = requests.post('http://localhost:8000/api/v1/drilling/upload', files=files)
session_id = response.json()['session_id']

# 2. Query the data
chat_request = {
    "session_id": session_id,
    "message": {
        "role": "user",
        "content": "What were the drilling parameters during the stuck pipe incident?"
    }
}
response = requests.post('http://localhost:8000/api/v1/chat/', json=chat_request)
print(response.json()['message']['content'])
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Application Settings
DEBUG=true
SECRET_KEY=your-secret-key-here

# AI Service Configuration
AI_MODEL_PROVIDER=ollama  # or "openai"
AI_OLLAMA_BASE_URL=http://localhost:11434
AI_OLLAMA_MODEL=llama2
AI_OLLAMA_EMBEDDING_MODEL=nomic-embed-text
AI_OPENAI_API_KEY=your-openai-key-here
AI_OPENAI_MODEL=gpt-4

# Database (for future use)
DATABASE_URL=sqlite:///./drilldata.db

# RAG Settings
AI_RAG_MAX_CHUNKS=5
AI_RAG_CHUNK_OVERLAP=200
```

### Model Configuration

**For Local Models (Ollama):**
- Install Ollama and pull your preferred model
- Set `AI_MODEL_PROVIDER=ollama`
- Configure model names in environment variables

**For Cloud Models (OpenAI):**
- Get API key from OpenAI
- Set `AI_MODEL_PROVIDER=openai`
- Set `AI_OPENAI_API_KEY` in environment

## 🧪 Testing

```bash
# Run all tests
pytest

# Run API tests only
pytest services/api/tests/

# Run AI service tests
pytest services/ai/tests/

# With coverage
pytest --cov=services --cov-report=html
```

## 🔒 Security & Privacy

- **Session Isolation**: Each data upload creates an isolated session
- **Automatic Cleanup**: Sessions expire after 24 hours
- **No Data Persistence**: Uploaded data is not stored permanently
- **API Key Security**: Sensitive keys stored as environment variables

## 📈 Performance Considerations

- **Vector Search**: ChromaDB provides fast similarity search
- **Chunking Strategy**: Recursive text splitting optimizes context windows
- **Model Selection**: Balance between accuracy (GPT-4) and cost/speed (local models)
- **Caching**: Session-based caching reduces redundant processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- **Code Style**: Black formatter, isort imports
- **Testing**: Minimum 80% test coverage
- **Documentation**: Update README for new features
- **Commits**: Use conventional commit format

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain** for the excellent LLM orchestration framework
- **ChromaDB** for reliable vector database functionality
- **Ollama** for making local LLMs accessible
- **FastAPI** for the incredible async web framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-org/drilldata-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/drilldata-ai/discussions)
- **Documentation**: [Wiki](https://github.com/your-org/drilldata-ai/wiki)

---

**DrillData AI** - Transforming oil drilling data analysis through conversational AI. 🚀
