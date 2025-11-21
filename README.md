# Author: Justice Owusu 
# 🏭 Oil Drilling Data Analysis Dashboard

## Demo Video
[Watch the demo video](https://drive.google.com/file/d/11O4EBxYd5EMJTuMnKm6yLSjLMRnUB5ap/view?usp=sharing)


[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-16+-black.svg)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue.svg)](https://typescriptlang.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A fullstack AI-powered platform for oil drilling data analysis, featuring natural language queries, interactive visualizations, and intelligent insights. Upload drilling data and ask questions conversationally to unlock hidden patterns and correlations.

## 🎯 What It Does

Traditional oil drilling analysis relies on static spreadsheets and manual interpretation. This platform democratizes complex drilling data through:

- **Conversational AI**: Ask questions like *"What were the drilling parameters during the stuck pipe incident?"* or *"Show me ROP trends in shale formations"*
- **Interactive Visualizations**: Real-time charts for rock composition, sonic logs, gamma ray data, and more
- **Intelligent Analysis**: AI-powered pattern recognition and correlation identification
- **Multi-Modal Support**: Works with CSV, Excel, and structured drilling reports

## 🚀 Key Features

### 🤖 AI-Powered Analysis
- **Natural Language Queries**: Ask questions in plain English
- **Contextual Understanding**: AI trained on drilling terminology and concepts
- **Session-Based Analysis**: Persistent data sessions with automatic cleanup
- **Multi-Model Support**: OpenAI GPT-4 or local Ollama models (Llama, Mistral, etc.)

### 📊 Data Visualization
- **Interactive Charts**: Real-time visualization of drilling parameters
- **Multi-Well Analysis**: Compare data across different wells
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **Synchronized Views**: Consistent depth scaling across all charts

### 🏗️ Enterprise Architecture
- **Microservices Design**: Scalable API, AI, and frontend services
- **Vector Search**: Fast similarity search using ChromaDB
- **Session Isolation**: Secure, per-user data sessions
- **Production Ready**: Comprehensive logging, monitoring, and error handling

## 🏛️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Service   │    │   AI Service    │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (LangChain)   │
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
                              │
                              ▼
                       ┌─────────────────┐
                       │ PostgreSQL      │
                       │ (Optional)      │
                       └─────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance async web framework
- **LangChain**: LLM orchestration and RAG pipelines
- **ChromaDB**: Vector database for embeddings
- **SQLAlchemy**: Database ORM
- **Pydantic**: Data validation and serialization

### Frontend
- **Next.js 16**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **shadcn/ui**: High-quality React components
- **Recharts**: Interactive data visualization

### AI & Data
- **Ollama**: Local LLM server (Llama, Mistral, CodeLlama)
- **OpenAI**: Cloud LLM integration (GPT-4, GPT-3.5-turbo)
- **Pandas**: Data manipulation and analysis
- **Unstructured**: Document processing

## 🚀 Quick Start

### Prerequisites
- **Docker & Docker Compose**
- **Git**

### Fullstack Deployment

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd oil-drilling-dashboard
   ```

2. **Start the application**
   ```bash
   # Full stack with AI and database
   docker-compose --profile ai --profile db up -d

   # Or minimal stack (API + Frontend)
   docker-compose up -d
   ```

3. **Access the application**
   - **Frontend**: http://localhost:3000
   - **API**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs

### Development Setup

For development with hot reloading:

```bash
# Backend development
cd backend
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

# Frontend development
cd frontend
pnpm install
pnpm dev
```

See [backend/README.md](backend/README.md) and [frontend/README.md](frontend/README.md) for detailed development instructions.

## 📊 Data Format

The platform accepts drilling data with these key columns:
- `depth`: Depth measurement (ft)
- `dt`: Sonic travel time (µs/ft)
- `gr`: Gamma ray (API)
- Rock composition: `sh`, `anh`, `ls`, `coal`, `salt`, `dol` (%)

**Supported formats**: Excel (.xlsx/.xls), CSV (.csv)

## 📚 API Overview

### Core Endpoints
- `POST /api/v1/drilling/upload` - Upload drilling data files
- `POST /api/v1/chat/` - Query data with natural language
- `GET /api/v1/drilling/session/{session_id}` - Get session info

### Example Usage
```python
import requests

# Upload data
files = {'file': open('drilling_data.xlsx', 'rb')}
response = requests.post('http://localhost:8000/api/v1/drilling/upload', files=files)
session_id = response.json()['session_id']

# Query data
query = {
    "session_id": session_id,
    "message": {"role": "user", "content": "What is the average ROP in shale?"}
}
response = requests.post('http://localhost:8000/api/v1/chat/', json=query)
print(response.json()['message']['content'])
```

See [backend/README.md](backend/README.md) for complete API documentation.

## ⚙️ Configuration

Create a `.env` file in the backend directory:

```bash
# AI Configuration
AI_MODEL_PROVIDER=ollama  # or "openai"
AI_OLLAMA_BASE_URL=http://ollama:11434
AI_OLLAMA_MODEL=llama2

# Database (optional)
POSTGRES_PASSWORD=your_password
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests (when implemented)
cd frontend
pnpm test
```

## 🔒 Security & Privacy

- **Session Isolation**: Each upload creates isolated data sessions
- **Automatic Cleanup**: Sessions expire after 24 hours
- **No Permanent Storage**: Uploaded data is not persisted long-term
- **Environment Variables**: Sensitive keys stored securely

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- **Backend**: Black formatter, isort imports, minimum 80% test coverage
- **Frontend**: ESLint, Prettier, TypeScript strict mode
- **Documentation**: Update READMEs for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain** for LLM orchestration
- **ChromaDB** for vector database functionality
- **Ollama** for local LLM accessibility
- **FastAPI** for the async web framework
- **Next.js** for the React framework
- **shadcn/ui** for beautiful components

---

**Oil Drilling Data Analysis Dashboard** - Transforming drilling data analysis through conversational AI and interactive visualization. 🚀
