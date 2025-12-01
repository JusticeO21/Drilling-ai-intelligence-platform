# Oil Drilling Data Analysis Platform - Architecture Overview

## Table of Contents
1. [System Overview](#system-overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Component Architecture](#component-architecture)
4. [Data Flow Architecture](#data-flow-architecture)
5. [LangGraph Agent Workflow](#langgraph-agent-workflow)
6. [Storage Architecture](#storage-architecture)
7. [API Architecture](#api-architecture)
8. [Deployment Architecture](#deployment-architecture)
9. [Security Architecture](#security-architecture)
10. [Performance Considerations](#performance-considerations)

## System Overview

The Oil Drilling Data Analysis Platform is a comprehensive AI-powered system for conversational drilling data analysis. It combines modern web technologies with advanced AI agents to provide real-time insights from drilling operational data.

### Core Capabilities
- **Conversational AI**: Natural language queries about drilling data
- **Real-time Visualization**: Interactive charts with synchronized depth scaling
- **Advanced Analytics**: AI-powered pattern recognition and correlation analysis
- **Multi-format Support**: Excel, CSV, and structured drilling reports
- **Streaming Responses**: Real-time AI chat with Server-Sent Events

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Client Layer                                  │
│  ┌─────────────────┐    ┌─────────────────┐                     │
│  │   Frontend      │    │   Browser       │                     │
│  │   (Next.js)     │    │   Client        │                     │
│  │                 │    │                 │                     │
│  │ • React 19      │    │ • File Parsing  │                     │
│  │ • TypeScript    │    │ • Local Storage │                     │
│  │ • Responsive UI │    │ • State Mgmt    │                     │
│  └─────────────────┘    └─────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────────┐
│                    API Layer                                     │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐  │
│  │   API Service   │    │   AI Service    │    │  Session     │  │
│  │   (FastAPI)     │    │   (LangGraph)   │    │  Manager     │  │
│  │                 │    │                 │    │             │  │
│  │ • REST APIs     │    │ • Agent Logic   │    │ • Isolation │  │
│  │ • Data Ingestion│    │ • LLM Integration│    │ • Cleanup   │  │
│  │ • Session Mgmt  │    │ • Code Execution│    │ • TTL        │  │
│  └─────────────────┘    └─────────────────┘    └─────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data Layer                                    │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐  │
│  │   ChromaDB      │    │   Redis         │    │  PostgreSQL │  │
│  │   Vector DB     │    │   Cache         │    │  (Optional) │  │
│  │                 │    │                 │    │             │  │
│  │ • Embeddings    │    │ • DataFrames    │    │ • Metadata  │  │
│  │ • Similarity    │    │ • Sessions      │    │ • Users     │  │
│  │ • RAG Context   │    │ • Fast Access   │    │ • Analytics │  │
│  └─────────────────┘    └─────────────────┘    └─────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    External Services                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐  │
│  │   Ollama        │    │   OpenAI        │    │  Anthropic  │  │
│  │   Local LLM     │    │   GPT-4         │    │  Claude     │  │
│  │                 │    │                 │    │             │  │
│  │ • Llama 2       │    │ • GPT-4         │    │ • Claude 3  │  │
│  │ • Mistral       │    │ • GPT-3.5-turbo │    │ • Claude 2  │  │
│  │ • CodeLlama     │    │ • Embeddings    │    │ • Embeddings│  │
│  └─────────────────┘    └─────────────────┘    └─────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Frontend Architecture

#### Next.js App Router Structure
```
app/
├── layout.tsx (Root layout with providers and theme)
├── page.tsx (Redirect to dashboard)
├── dashboard/
│   ├── layout.tsx (Dashboard shell with navigation)
│   └── page.tsx (Main drilling dashboard)
└── api/
    └── parse-file/route.ts (Client-side file processing)
```

#### Feature-Based Architecture
```
features/
├── drilling/
│   ├── components/ (Chart components, dashboard)
│   ├── stores/ (Zustand state management)
│   ├── hooks/ (Data processing hooks)
│   ├── types/ (TypeScript definitions)
│   └── utils/ (Data parsing utilities)
└── chat/
    ├── components/ (Chat UI, streaming interface)
    ├── stores/ (Chat state and history)
    ├── hooks/ (Chat interaction logic)
    └── types/ (Message and session types)
```

#### State Management
- **Zustand**: Local state for drilling data, UI state, session persistence
- **TanStack Query**: Server state for API calls, caching, background updates
- **Local Storage**: Session data persistence with automatic cleanup

### Backend Architecture

#### Microservices Design
```
services/
├── api/
│   ├── app/
│   │   ├── main.py (FastAPI application)
│   │   ├── routers/ (API endpoints)
│   │   ├── schemas/ (Pydantic models)
│   │   └── models/ (SQLAlchemy models)
│   └── Dockerfile
└── ai/
    ├── agents/drilling_data_agent/
    │   ├── graph.py (LangGraph workflow)
    │   ├── nodes/ (Workflow execution nodes)
    │   ├── tools/ (Agent tools)
    │   └── state.py (Agent state)
    └── common/
        ├── config.py (AI configuration)
        ├── models.py (LLM models)
        └── utils.py (AI utilities)
```

#### Shared Components
```
common/
├── config.py (Global configuration)
├── logging.py (Structured logging)
├── rag.py (RAG session management)
├── chroma_client.py (Vector database client)
├── redis_client.py (Cache client)
└── ingestion/
    ├── ingestion_service.py (Data processing pipeline)
    ├── cleaning/ (Data cleaning utilities)
    ├── embeddings/ (Text embedding services)
    ├── loaders/ (File loading utilities)
    └── storage/ (Storage abstractions)
```

## Data Flow Architecture

### File Upload & Processing Flow

```
1. User uploads file (Excel/CSV)
       ↓
2. Frontend: Client-side parsing (xlsx/papaparse)
       ↓
3. Frontend: Data validation and preview
       ↓
4. Frontend: POST to /drilling/upload
       ↓
5. API Service: Receive file and metadata
       ↓
6. Data Ingestion Pipeline:
   ├── File Loading (StructuredFileLoader)
   ├── Data Cleaning (DataCleaner)
   ├── Data Profiling (DataFrameProfiler)
   └── Storage:
       ├── Vector Storage (ChromaDB)
       └── DataFrame Storage (Redis)
       ↓
7. Session Creation with TTL
       ↓
8. Return session_id to frontend
```

### Query Processing Flow

```
1. User submits natural language query
       ↓
2. Frontend: POST to /chat/ with streaming
       ↓
3. API Service: Validate session and route to AI
       ↓
4. AI Service: Initialize LangGraph agent
       ↓
5. Agent Workflow Execution:
   ├── Query Classification Node
   ├── Data Retrieval Node (ChromaDB + Redis)
   ├── Code Generation Node
   ├── Code Execution Node (Isolated environment)
   ├── Response Generation Node
   └── Error Handling Node
       ↓
6. Streaming Response via Server-Sent Events
       ↓
7. Frontend: Real-time UI updates
```

## LangGraph Agent Workflow

### Agent State Management

```python
class DrillAgentState(TypedDict):
    user_id: str
    dataset_id: str
    messages: List[HumanMessage]
    metadata: Optional[Dict[str, Any]]
    query_type: Optional[str]
    retrieved_data: Optional[Dict[str, Any]]
    generated_code: Optional[str]
    execution_result: Optional[Any]
    final_response: Optional[str]
    error: Optional[str]
```

### Workflow Graph Structure

```
┌─────────────────┐
│   START         │
└─────────────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│ Classify Query  │────▶│  Retrieve Data  │
│ Node            │     │  Node           │
└─────────────────┘     └─────────────────┘
         │                        │
         ▼                        ▼
┌─────────────────┐     ┌─────────────────┐
│ Simple Response │     │ Generate Code   │
│ Node            │     │ Node            │
└─────────────────┘     └─────────────────┘
         │                        │
         │                        ▼
         │               ┌─────────────────┐
         │               │ Execute Code    │
         │               │ Node            │
         │               └─────────────────┘
         │                        │
         │                        ▼
         │               ┌─────────────────┐
         │               │ Generate        │
         │               │ Response Node   │
         │               └─────────────────┘
         │                        │
         ▼                        ▼
┌─────────────────┐     ┌─────────────────┐
│   END           │◄────┤ Handle Error    │
│   (Success)     │     │ Node            │
└─────────────────┘     └─────────────────┘
```

### Node Details

#### 1. Query Classification Node
- **Purpose**: Determine query complexity and routing strategy
- **Logic**: Analyze query length, keywords, and context
- **Output**: `query_type` ("simple" or "complex")
- **Tools**: Natural language processing, keyword matching

#### 2. Data Retrieval Node
- **Purpose**: Fetch relevant data from storage systems
- **Logic**: Semantic search + structured queries
- **Storage Access**:
  - ChromaDB: Vector similarity search for embeddings
  - Redis: Fast DataFrame retrieval by session ID
- **Output**: `retrieved_data` with context and metadata

#### 3. Code Generation Node
- **Purpose**: Generate Python analysis code based on query
- **Logic**: LLM-powered code generation with context
- **Safety**: Input validation and sanitization
- **Output**: `generated_code` as executable Python

#### 4. Code Execution Node
- **Purpose**: Safely execute generated analysis code
- **Environment**: Isolated execution with resource limits
- **Security**: Sandboxed execution, timeout protection
- **Output**: `execution_result` with data or error

#### 5. Response Generation Node
- **Purpose**: Format analysis results into natural language
- **Logic**: LLM-powered response formatting with context
- **Personalization**: User-friendly explanations
- **Output**: `final_response` as conversational text

#### 6. Error Handling Node
- **Purpose**: Manage execution errors and provide fallbacks
- **Logic**: Error classification and user-friendly messages
- **Recovery**: Alternative approaches for failed operations
- **Output**: `error` with recovery suggestions

### Agent Tools

#### Metadata Analysis Tool
- **Purpose**: Extract data characteristics and statistics
- **Functions**: Column analysis, data types, missing values
- **Output**: Structured metadata for LLM consumption

#### Python Code Execution Tool
- **Purpose**: Safe execution of analysis code
- **Security**: Isolated environment with resource limits
- **Libraries**: pandas, numpy, matplotlib support
- **Output**: Execution results or error messages

#### Data Formatting Tool
- **Purpose**: Structure data for LLM processing
- **Functions**: Data serialization, context preparation
- **Optimization**: Token-efficient data representation

#### Data Loading Tool
- **Purpose**: Retrieve DataFrames from Redis storage
- **Performance**: Fast access with session-based caching
- **Error Handling**: Session validation and recovery

## Storage Architecture

### ChromaDB (Vector Storage)
- **Purpose**: Semantic search and RAG context retrieval
- **Data Types**: Text embeddings, document chunks, metadata
- **Operations**: Similarity search, vector indexing, collection management
- **Performance**: Fast nearest-neighbor search with HNSW indexing
- **Persistence**: File-based storage with Docker volumes

### Redis (DataFrame Storage)
- **Purpose**: Fast DataFrame access and session data caching
- **Data Types**: Pandas DataFrames, session metadata, temporary results
- **Operations**: Key-value storage, TTL management, pub/sub (future)
- **Performance**: In-memory storage with sub-millisecond access
- **Persistence**: Configurable persistence with Docker volumes

### PostgreSQL (Optional Metadata)
- **Purpose**: User management, analytics, long-term metadata
- **Data Types**: User profiles, session history, usage analytics
- **Operations**: Relational queries, data aggregation, reporting
- **Scalability**: ACID compliance, concurrent access
- **Integration**: SQLAlchemy ORM with async support

### Session Management
- **Isolation**: Per-user data sessions with unique identifiers
- **TTL**: Automatic cleanup after 24 hours of inactivity
- **Security**: Session validation and access control
- **Persistence**: Redis-backed session storage with metadata

## API Architecture

### RESTful Endpoints

#### Data Management API
```
POST /drilling/upload
- Purpose: File upload and processing
- Request: Multipart file upload
- Response: Session metadata and column information
- Processing: Client-side parsing + backend ingestion

POST /drilling/query
- Purpose: Structured data queries
- Request: Session ID, question, parameters
- Response: Query results with metadata
- Processing: Direct database queries

GET /drilling/session/{session_id}
- Purpose: Session information retrieval
- Request: Session ID
- Response: Session metadata and statistics
- Processing: Session validation and data retrieval
```

#### AI Chat API
```
POST /chat/
- Purpose: Conversational AI queries
- Request: Session ID, message, streaming flag
- Response: AI-generated response with metadata
- Processing: LangGraph agent workflow execution

Streaming Response Format:
data: {"type": "status", "message": "Analyzing query..."}
data: {"type": "content", "delta": "Based on the data..."}
data: {"type": "error", "message": "Processing failed"}
```

### API Client Architecture

#### Type-Safe Client
```typescript
class ApiService {
  // HTTP client with error handling
  private client: HttpClient

  // Streaming parser for SSE
  private parser: StreamParser

  // Factory methods for service creation
  static createDrillingService()
  static createChatService()
}
```

#### Error Handling
- **Network Errors**: Automatic retry with exponential backoff
- **Validation Errors**: Type-safe error responses
- **Session Errors**: Automatic cleanup and user notification
- **Streaming Errors**: Graceful degradation to non-streaming mode

## Deployment Architecture

### Docker Compose Orchestration

```yaml
services:
  api:        # FastAPI service
  ai:         # LangGraph service
  ollama:     # Local LLM service
  redis:      # DataFrame cache
  chromadb:   # Vector database
  postgres:   # Optional metadata DB
  frontend:   # Next.js application
```

### Service Dependencies
- **API Service**: Depends on Redis, ChromaDB
- **AI Service**: Depends on Ollama/OpenAI API
- **Frontend**: No direct dependencies (communicates via API)
- **Storage Services**: Independent with volume persistence

### Environment Configuration
- **Development**: Hot reload, debug logging, local services
- **Production**: Optimized builds, production logging, external services
- **Staging**: Mirror production with test data

### Scaling Considerations
- **Horizontal Scaling**: Stateless API and AI services
- **Database Scaling**: Redis clustering, ChromaDB sharding
- **Load Balancing**: Nginx or cloud load balancers
- **Caching Strategy**: Multi-layer caching (Redis + CDN)

## Security Architecture

### Authentication & Authorization
- **Session-Based**: Secure session management with encryption
- **API Keys**: Environment-based LLM provider authentication
- **CORS**: Configured cross-origin resource sharing
- **Rate Limiting**: Future implementation for API protection

### Data Protection
- **Encryption**: Data at rest and in transit
- **Session Isolation**: Per-user data sandboxing
- **Input Validation**: Comprehensive sanitization
- **Code Execution**: Sandboxed Python execution environment

### Network Security
- **Service Isolation**: Docker network segmentation
- **API Security**: Input validation and error handling
- **External APIs**: Secure communication with LLM providers
- **Monitoring**: Security event logging and alerting

## Performance Considerations

### Frontend Performance
- **Code Splitting**: Route-based and component-based splitting
- **Image Optimization**: Next.js automatic image optimization
- **Caching**: Browser caching with service worker (future)
- **Bundle Analysis**: Webpack bundle analyzer integration

### Backend Performance
- **Async Processing**: FastAPI async endpoints
- **Connection Pooling**: Database connection optimization
- **Caching Layers**: Redis for frequently accessed data
- **Streaming**: Server-Sent Events for real-time responses

### AI Processing Performance
- **Model Selection**: Balance accuracy vs speed
- **Caching**: LLM response caching for similar queries
- **Batch Processing**: Future optimization for multiple queries
- **Resource Limits**: Execution timeouts and memory limits

### Database Performance
- **Indexing**: Optimized indexes for query patterns
- **Connection Pooling**: Efficient database connections
- **Query Optimization**: Efficient data retrieval patterns
- **Caching**: Multi-level caching strategy

### Monitoring & Observability
- **Logging**: Structured logging with correlation IDs
- **Metrics**: Performance metrics and error tracking
- **Health Checks**: Service health monitoring
- **Tracing**: Request tracing across services

---

This architecture provides a scalable, secure, and maintainable foundation for AI-powered drilling data analysis, with clear separation of concerns and modern development practices.
