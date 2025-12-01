# 🏭 DrillData AI - Intelligent Oil Drilling Data Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-orange.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**DrillData AI** is an enterprise-grade AI-powered platform that transforms oil drilling data analysis through natural language processing and retrieval-augmented generation (RAG). Upload drilling reports, well logs, and operational data, then query them conversationally to extract insights, identify patterns, and make data-driven decisions.

## Problem Solved

Traditional oil drilling data analysis is trapped in spreadsheets and static reports. **DrillData AI** democratizes access to complex drilling data by enabling natural language queries.

## Key Features

###  AI-Powered Analysis
- **Conversational Queries**: Ask questions in natural language
- **Contextual Responses**: AI understands drilling terminology and concepts
- **Multi-Modal Support**: Works with CSV, Excel, and structured drilling reports
- **Intelligent Insights**: Identifies patterns and correlations in drilling data

### Enterprise Architecture
- **Microservices Design**: Scalable API and AI services
- **Session Isolation**: Secure, per-user data sessions with automatic cleanup
- **Vector Search**: Fast similarity search using ChromaDB
- **Production Ready**: Comprehensive logging, error handling, and monitoring

### 🔧 Flexible Deployment
- **Multi-Model Support**: OpenAI GPT-4 or local Ollama models (Llama, Mistral, etc.)
- **Docker Ready**: Containerized deployment with docker-compose
- **Configurable**: Environment-based configuration for different environments
- **API First**: RESTful APIs for easy integration

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Service   │    │   AI Service    │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (LangGraph)   │
│                 │    │                 │    │                 │
│ • File Upload   │    │ • Data Ingestion│    │ • Agent Workflow│
│ • Chat Interface│    │ • Session Mgmt  │    │ • Code Execution│
│ • Data Viz      │    │ • Vector Storage│    │ • Response Gen  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ChromaDB      │    │   Redis         │    │   Ollama/       │
│ (Embeddings)    │    │ (DataFrames)    │    │ OpenAI API      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow Architecture

**Ingestion Pipeline:**
```
File Upload → Loader → Cleaner → Profiler → Vector Store + Redis Cache
```

**Query Processing:**
```
User Query → API → AI Agent → Classify → Retrieve → Generate → Execute → Respond
```

**Storage Strategy:**
- **ChromaDB**: Semantic search and embeddings for RAG
- **Redis**: Fast DataFrame access and session data caching
- **Session Isolation**: Per-user data sessions with automatic cleanup

## Technology Stack

### Backend Framework
- **FastAPI**: High-performance async web framework
- **Pydantic**: Data validation and serialization
- **SQLAlchemy**: Database ORM (future extensibility)

### AI & NLP
- **LangChain**: LLM orchestration and RAG pipelines
- **LangGraph**: Agent workflow management and state machines
- **ChromaDB**: Vector database for embeddings and similarity search
- **Redis**: High-performance caching and DataFrame storage
- **Upstash Redis**: Cloud Redis service support

### LLM Support
- **OpenAI**: GPT-4, GPT-3.5-turbo (cloud)
- **Ollama**: Llama 2, Mistral, CodeLlama (local)
- **Anthropic**: Claude models via LangChain
- **VoyageAI**: Specialized embedding models

### Data Processing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Data Cleaning Pipeline**: Automated data preprocessing
- **Data Profiling**: Statistical analysis and metadata generation

### Storage & Caching
- **ChromaDB**: Vector embeddings for semantic search
- **Redis**: Fast DataFrame storage and session caching
- **Session Management**: Isolated user sessions with TTL

## Data Ingestion Pipeline

The platform processes drilling data through a comprehensive pipeline:

1. **File Loading**: CSV/Excel files loaded using Pandas
2. **Data Cleaning**: Automated preprocessing (missing values, data types, outliers)
3. **Data Profiling**: Statistical analysis and metadata generation
4. **Vector Embedding**: Text chunks converted to embeddings for semantic search
5. **Dual Storage**: DataFrames stored in Redis, embeddings in ChromaDB

## AI Agent Architecture

### LangGraph Workflow
The drilling data agent uses a sophisticated state machine with 7 specialized nodes:

- **Query Classification Node**: Determines if query needs simple response or complex analysis
- **Data Retrieval Node**: Fetches relevant data from vector store and Redis
- **Code Generation Node**: Creates Python analysis code based on query requirements
- **Code Execution Node**: Safely executes generated code in isolated environment
- **Response Generation Node**: Formats analysis results into natural language
- **Error Handling Node**: Manages execution errors and provides fallbacks
- **Simple Answer Node**: Direct responses for straightforward queries

### Agent Tools
- **Metadata Analysis**: Extracts data characteristics and statistics
- **Python Code Execution**: Safe execution of analysis code
- **Data Formatting**: Structures data for LLM consumption
- **Data Loading**: Retrieves DataFrames from Redis storage

## 📁 Project Structure

```
backend/
├── common/                          # Shared utilities and services
│   ├── config.py                    # Global configuration management
│   ├── database.py                  # SQLAlchemy database setup
│   ├── logging.py                   # Structured logging configuration
│   ├── rag.py                       # RAG session management and orchestration
│   ├── chroma_client.py             # ChromaDB vector database client
│   ├── redis_client.py              # Redis cache and storage client
│   └── ingestion/                   # Data processing pipeline
│       ├── ingestion_service.py     # Main data ingestion orchestrator
│       ├── cleaning/
│       │   └── data_cleaner.py      # Data cleaning and preprocessing
│       ├── embeddings/
│       │   └── embedding_service.py # Text embedding generation
│       ├── loaders/
│       │   └── file_loader.py       # CSV/Excel file loading utilities
│       ├── profiling/
│       │   └── data_profiler.py     # Data profiling and statistics
│       └── storage/                 # Storage abstraction layer
│           ├── __init__.py
│           ├── vector_store_repo.py # ChromaDB operations
│           └── redis_store_repo.py  # Redis DataFrame storage
├── services/                        # Microservices architecture
│   ├── ai/                          # AI processing microservice
│   │   ├── main.py                  # AI service entry point
│   │   ├── requirements.txt         # AI service dependencies
│   │   ├── agents/
│   │   │   └── drilling_data_agent/ # LangGraph drilling agent
│   │   │       ├── __init__.py      # Agent initialization
│   │   │       ├── graph.py         # LangGraph workflow definition
│   │   │       ├── state.py         # Agent state management
│   │   │       ├── prompts.py       # LLM prompt templates
│   │   │       ├── nodes/           # Workflow execution nodes
│   │   │       │   ├── __init__.py
│   │   │       │   ├── answer_simple_node.py    # Simple query handler
│   │   │       │   ├── classify_query_node.py   # Query classification
│   │   │       │   ├── execute_code_node.py     # Python code execution
│   │   │       │   ├── generate_code_node.py    # Code generation
│   │   │       │   ├── generate_response_node.py # Response formatting
│   │   │       │   ├── handle_error_node.py     # Error handling
│   │   │       │   └── retrieve_data_node.py    # Data retrieval
│   │   │       └── tools/           # Custom agent tools
│   │   │           ├── __init__.py
│   │   │           ├── determine_metadata_needs.py
│   │   │           ├── execute_python_code.py
│   │   │           ├── format_metadata_for_llm.py
│   │   │           ├── load_dataframe_from_storage.py
│   │   │           └── load_metadata.py
│   │   ├── common/                  # AI service utilities
│   │   │   ├── __init__.py
│   │   │   ├── config.py            # AI-specific configuration
│   │   │   ├── models.py            # LLM model configurations
│   │   │   └── utils.py             # AI utility functions
│   │   └── tests/                   # AI service tests
│   │       ├── __init__.py
│   │       └── test_ai_service.py
│   └── api/                         # REST API microservice
│       ├── __init__.py
│       ├── requirements.txt         # API service dependencies
│       └── app/
│           ├── __init__.py
│           ├── main.py              # FastAPI application
│           ├── models/
│           │   ├── __init__.py
│           │   └── well.py          # SQLAlchemy models
│           ├── routers/             # API endpoint routers
│           │   ├── __init__.py
│           │   ├── chat.py          # Chat and AI endpoints
│           │   └── drilling.py      # Data upload and query endpoints
│           ├── schemas/             # Pydantic request/response schemas
│           │   ├── __init__.py
│           │   ├── chat.py          # Chat API schemas
│           │   ├── drilling.py      # Drilling data schemas
│           │   └── well.py          # Well data schemas
│           └── tests/               # API service tests
│               ├── __init__.py
├── docker-compose.yml               # Multi-service container orchestration
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables
├── .dockerignore                    # Docker ignore patterns
├── .gitignore                       # Git ignore patterns
└── README.md                        # This documentation
```

##  Quick Start

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
- **API Service**: `http://localhost:8000` - REST API endpoints, data ingestion, session management
- **AI Service**: Internal service for LangGraph agent processing and LLM interactions
- **Ollama**: `http://localhost:11434` - Local LLM server
- **ChromaDB**: Vector database for embeddings (persistent volumes)
- **Redis**: In-memory cache and DataFrame storage
- **PostgreSQL**: `localhost:5432` - Optional relational database for future extensibility

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

## API Documentation

### Core Endpoints

#### Data Upload
```http
POST /drilling/upload
```
Upload CSV/Excel drilling data files for analysis.

**Request:**
- `file`: Multipart file (CSV/Excel)
- Returns: `session_id`, `filename`, `file_type`, `columns`, `num_columns`

**Response:**
```json
{
  "filename": "drilling_data.xlsx",
  "file_type": "excel",
  "num_columns": 15,
  "columns": ["depth", "rop", "wob", "rpm", "mud_weight"],
  "session_id": "uuid-here"
}
```

#### Data Query
```http
POST /drilling/query
```
Query uploaded drilling data using structured queries.

**Request:**
```json
{
  "session_id": "uuid-here",
  "question": "What is the average ROP in shale formations?",
  "n_results": 5
}
```

#### AI Chat
```http
POST /chat/
```
Query uploaded drilling data using natural language with AI agent.

**Request:**
```json
{
  "session_id": "uuid-here",
  "message": {
    "role": "user",
    "content": "What is the average ROP in shale formations?"
  },
  "stream": false
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

#### Streaming Chat
Set `"stream": true` in chat request for Server-Sent Events streaming.

#### Session Management
```http
GET /drilling/session/{session_id}
```
Get information about an active data session.

**Response:**
```json
{
  "session_id": "uuid-here",
  "columns": ["depth", "rop", "wob"],
  "created_at": "2024-01-01T10:00:00Z",
  "expires_at": "2024-01-02T10:00:00Z"
}
```

#### Health Check
```http
GET /health
```
Service health check endpoint.

### Example Usage

```python
import requests

# 1. Upload drilling data
files = {'file': open('drilling_report.xlsx', 'rb')}
response = requests.post('http://localhost:8000/drilling/upload', files=files)
data = response.json()
session_id = data['session_id']
print(f"Uploaded {data['filename']} with {data['num_columns']} columns")

# 2. Query the data with AI agent
chat_request = {
    "session_id": session_id,
    "message": {
        "role": "user",
        "content": "What were the drilling parameters during the stuck pipe incident?"
    },
    "stream": False
}
response = requests.post('http://localhost:8000/chat/', json=chat_request)
print(response.json()['message']['content'])

# 3. Get session information
session_info = requests.get(f'http://localhost:8000/drilling/session/{session_id}')
print(session_info.json())
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```bash
# Application Settings
DEBUG=false
SECRET_KEY=your-secret-key-here

# AI Service Configuration
AI_MODEL_PROVIDER=ollama  # or "openai" or "anthropic"
AI_OLLAMA_BASE_URL=http://ollama:11434
AI_OLLAMA_MODEL=llama2
AI_OLLAMA_EMBEDDING_MODEL=nomic-embed-text
AI_OPENAI_API_KEY=your-openai-key-here
AI_OPENAI_MODEL=gpt-4
AI_ANTHROPIC_API_KEY=your-anthropic-key-here
AI_VOYAGE_API_KEY=your-voyage-key-here

# Database (Optional - for future extensibility)
DATABASE_URL=sqlite:///./drilldata.db
POSTGRES_PASSWORD=your-postgres-password

# RAG Settings
AI_RAG_MAX_CHUNKS=5
AI_RAG_CHUNK_OVERLAP=200

# Redis Configuration (if using Upstash or external Redis)
REDIS_URL=redis://localhost:6379
UPSTASH_REDIS_REST_URL=your-upstash-url
UPSTASH_REDIS_REST_TOKEN=your-upstash-token
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

- **Dual Storage Architecture**: ChromaDB for semantic search, Redis for fast DataFrame access
- **Vector Search**: ChromaDB provides fast similarity search with persistent embeddings
- **Session Isolation**: Per-user data sessions prevent cross-contamination and enable cleanup
- **Streaming Responses**: Server-Sent Events for real-time AI agent responses
- **Code Execution**: Isolated Python execution for complex data analysis
- **Model Selection**: Balance between accuracy (GPT-4/Claude) and cost/speed (local Ollama models)
- **Automatic Cleanup**: Session TTL prevents storage bloat

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

**DrillData AI** - Transforming oil drilling data analysis through conversational AI. 
