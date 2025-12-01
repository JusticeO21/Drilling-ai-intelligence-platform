# Oil Drilling Data Visualization Dashboard

A modern, responsive web application for visualizing oil drilling data and querying insights using AI-powered natural language processing. Built with Next.js, TypeScript, and cutting-edge UI components.

## Features

### Advanced Data Visualization Dashboard

- **Multi-Chart Drilling Analytics**: Comprehensive visualization suite featuring:
  - **Rock Composition Charts**: Multi-line percentage charts for lithology analysis
  - **Sonic Log Charts (DT)**: Acoustic travel time visualization with depth correlation
  - **Gamma Ray Log Charts (GR)**: Natural radioactivity logging with API units
- **Synchronized Depth Scaling**: Consistent Y-axis across all charts for accurate correlation
- **Responsive Grid Layout**: Adaptive 1-3 column layout based on screen size
- **Interactive Charts**: Hover states, zoom capabilities, and data point inspection

### AI-Powered Conversational Intelligence

- **Streaming Chat Interface**: Real-time AI responses with Server-Sent Events
- **Contextual Data Queries**: Natural language questions about uploaded drilling data
- **Session-Aware Conversations**: Persistent chat history tied to data sessions
- **Multi-Modal AI Support**: Compatible with Ollama, OpenAI, and Anthropic models
- **Advanced Agent Processing**: LangGraph-powered query analysis and code execution

### Intelligent Data Management

- **Client-Side File Processing**: Instant Excel/CSV parsing with `xlsx` and `papaparse`
- **Dual Processing Pipeline**: Local preview + backend AI analysis
- **Session-Based Storage**: Isolated data sessions with automatic cleanup
- **Local Persistence**: Zustand-powered offline data storage and recovery
- **Type-Safe Data Handling**: Full TypeScript coverage for data operations

### Modern Responsive UI/UX

- **Professional Design System**: shadcn/ui components with Radix UI primitives
- **Adaptive Layout System**: Sidebar navigation with collapsible mobile menu
- **Multi-Tab Navigation**: Organized feature access with desktop/mobile variants
- **Loading States & Feedback**: Comprehensive overlays, skeletons, and toast notifications
- **Accessibility First**: ARIA compliance and keyboard navigation support
- **Theme Support**: Light/dark mode with next-themes integration

### Advanced Technical Features

- **Real-time Streaming**: Server-Sent Events for live AI responses
- **Optimistic Updates**: Immediate UI feedback with background synchronization
- **Error Boundaries**: Graceful error handling with user-friendly messages
- **Performance Optimized**: Code splitting, lazy loading, and efficient re-renders
- **Type Safety**: 100% TypeScript coverage with strict mode

## Technology Stack

### Core Framework & Runtime

- **Next.js 16**: React framework with App Router, server components, and edge runtime
- **React 19**: Latest React features with concurrent rendering and automatic batching
- **Node.js 18+**: JavaScript runtime with modern ES modules support
- **TypeScript 5**: Strict type checking with advanced language features

### UI & Design System

- **Tailwind CSS v4**: Utility-first CSS with CSS-in-JS capabilities
- **shadcn/ui**: Production-ready component library built on Radix UI
- **Radix UI**: Unstyled, accessible component primitives
- **Lucide React**: Consistent icon library with 1000+ icons
- **next-themes**: Theme switching with system preference detection
- **Sonner**: Modern toast notifications with stacking support

### Data Visualization & Processing

- **Recharts**: Declarative React charting library with D3.js foundation
- **xlsx**: Excel file parsing and generation
- **papaparse**: High-performance CSV parsing with streaming support
- **uuid**: RFC-compliant UUID generation for session management

### State Management & Data Fetching

- **Zustand**: Lightweight, scalable state management with persistence
- **TanStack Query**: Powerful data synchronization for server state
- **Local Storage API**: Browser storage with Zustand persistence middleware

### Development & Quality Tools

- **ESLint**: Advanced linting with Next.js and TypeScript rules
- **Prettier**: Opinionated code formatting with custom configuration
- **TypeScript Compiler**: Strict type checking and path mapping
- **Tailwind CSS IntelliSense**: IDE support for utility classes

### Build & Deployment

- **Next.js Build System**: Optimized production builds with code splitting
- **Docker**: Containerized deployment with multi-stage builds
- **Vercel/Render**: Cloud platform deployment support

### API Integration & Communication

- **Fetch API**: Modern browser API with custom client wrapper
- **Server-Sent Events**: Real-time streaming for AI chat responses
- **RESTful APIs**: Type-safe API client with error handling
- **Streaming Parser**: Custom SSE message parsing and state management

## Architecture Overview

### Next.js App Router Structure

```
app/
├── layout.tsx (Root layout with providers and metadata)
├── page.tsx (Home redirect to dashboard)
├── dashboard/
│   ├── layout.tsx (Dashboard shell with sidebar and tabs)
│   └── page.tsx (Main drilling dashboard)
└── api/
    └── parse-file/route.ts (Client-side file processing)
```

### State Management Architecture

**Dual State Management Strategy:**

- **Zustand Stores**: Local state for drilling data, UI state, and session management
  - `drilling-store`: Main data store with persistence and file upload handling
  - `wells-store`: Well information and metadata management
  - `chat-store`: Chat state with streaming message handling

- **TanStack Query**: Server state for API calls, caching, and background updates
  - Automatic request deduplication and caching
  - Optimistic updates for better UX
  - Background refetching and error retry logic

### Component Architecture

**Feature-Based Organization:**
- **Features**: Business domain separation (drilling, chat)
- **Components**: Reusable UI components with compound patterns
- **Layout**: Responsive layout system with navigation
- **UI**: shadcn/ui design system components

**Custom Hooks Pattern:**
- `useDrillingData`: Data processing and normalization
- `useChat`: Chat interaction with streaming support
- `useScreenSize`: Responsive design utilities

## Development Workflow

### Available Scripts

- `pnpm dev` - Start development server with hot reload
- `pnpm build` - Production build with optimization
- `pnpm start` - Start production server
- `pnpm lint` - ESLint with Next.js rules
- `pnpm format` - Prettier code formatting
- `pnpm format:check` - Check code formatting compliance
- `pnpm type-check` - TypeScript type checking

### Development Features

- **Hot Module Replacement**: Instant updates during development
- **TypeScript Checking**: Real-time error detection
- **ESLint Integration**: Code quality enforcement
- **Prettier Integration**: Consistent code formatting
- **Next.js Fast Refresh**: Optimized React fast refresh

## Prerequisites

- **Node.js**: Version 18 or higher
- **pnpm**: Package manager (recommended)
- **Backend API**: Running drilling data processing service

## Getting Started

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd oil-drilling-dashboard/frontend
   ```

2. **Install dependencies**

   ```bash
   pnpm install
   ```

3. **Environment Setup**

   ```bash
   cp .env.example .env
   ```

   Configure your environment variables:

   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

4. **Start Development Server**

   ```bash
   pnpm dev
   ```

5. **Open Browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Project Structure

```
frontend/
├── app/                          # Next.js App Router (v13+)
│   ├── api/                      # API routes
│   │   └── parse-file/           # Client-side file processing
│   │       └── route.ts          # File parsing endpoint
│   ├── dashboard/                # Dashboard route group
│   │   ├── layout.tsx            # Dashboard layout with sidebar
│   │   └── page.tsx              # Main dashboard page
│   ├── globals.css               # Global styles with Tailwind
│   ├── layout.tsx                # Root layout with providers
│   ├── page.tsx                  # Home page (redirects to dashboard)
│   ├── providers.tsx             # React context providers
│   └── not-found.tsx             # 404 error page
├── components/                   # Reusable UI components
│   ├── layout/                   # Layout system components
│   │   ├── app-sidebar.tsx       # Main navigation sidebar
│   │   ├── header.tsx            # Top application header
│   │   ├── tab-navigation.tsx    # Multi-tab navigation
│   │   ├── navigation-tabs.tsx   # Tab navigation logic
│   │   ├── chat-panel.tsx        # Chat panel component
│   │   └── Navigation/           # Navigation sub-components
│   │       ├── desktop-tabs.tsx  # Desktop tab navigation
│   │       └── index.tsx         # Navigation exports
│   └── ui/                       # shadcn/ui component library
│       ├── index.ts              # Component exports
│       ├── loading-overlay.tsx   # Loading state overlay
│       ├── scroll-area.tsx       # Custom scroll area
│       ├── select-dropdown.tsx   # Enhanced select component
│       ├── sidebar.tsx           # Sidebar component
│       └── sonner.tsx            # Toast notifications
├── features/                     # Feature-based architecture
│   ├── drilling/                 # Drilling data visualization
│   │   ├── components/           # Drilling-specific components
│   │   │   ├── drilling-dashboard.tsx  # Main dashboard component
│   │   │   ├── rock-composition.tsx    # Rock composition chart
│   │   │   ├── dt-log-chart.tsx        # Sonic log chart
│   │   │   ├── gr-log-chart.tsx        # Gamma ray log chart
│   │   │   ├── log-chart.tsx           # Base log chart component
│   │   │   ├── chart-label.tsx         # Chart labeling utilities
│   │   │   ├── no-data.tsx             # Empty state component
│   │   │   └── index.ts                # Feature exports
│   │   ├── stores/               # Zustand state management
│   │   │   ├── drilling-store.ts # Main drilling data store
│   │   │   └── wells-store.ts    # Well information store
│   │   ├── hooks/                # Custom React hooks
│   │   │   └── useDrillingData.ts # Data processing hook
│   │   ├── types/                # TypeScript type definitions
│   │   │   └── drilling.types.ts # Drilling domain types
│   │   ├── utils/                # Utility functions
│   │   │   └── data-parser.ts     # Client-side file parsing
│   │   └── index.ts              # Feature barrel exports
│   └── chat/                     # AI chat functionality
│       ├── components/           # Chat UI components
│       │   ├── chat-widget.tsx       # Floating chat widget
│       │   ├── chat-panel.tsx        # Chat panel interface
│       │   ├── chat-message.tsx      # Individual message component
│       │   ├── clear-history-dialog.tsx # History management
│       │   └── index.ts              # Component exports
│       ├── stores/               # Chat state management
│       │   ├── chat-slice.ts         # Chat state slice
│       │   └── index.ts              # Store exports
│       ├── hooks/                # Chat-specific hooks
│       │   └── use-chat.ts          # Chat interaction hook
│       ├── lib/                  # Chat utilities
│       └── types/                # Chat type definitions
├── lib/                          # Shared utilities and services
│   ├── api.ts                    # Comprehensive API client
│   ├── storage.ts                # Local storage utilities
│   └── utils.ts                  # General utility functions
├── hooks/                        # Custom React hooks
│   └── use-screen-size.ts        # Responsive design hook
├── types/                        # Global type definitions
├── public/                       # Static assets
│   ├── favicon.ico              # Favicon
│   └── og-image.jpg             # Open Graph image
├── next.config.ts               # Next.js configuration
├── tailwind.config.ts           # Tailwind CSS configuration
├── components.json              # shadcn/ui configuration
├── package.json                 # Dependencies and scripts
├── tsconfig.json                # TypeScript configuration
├── eslint.config.mjs            # ESLint configuration
├── prettier.config.mjs          # Prettier configuration
└── README.md                    # This documentation
```

## 🔧 Development Scripts

### Core Development
- `pnpm dev` - Start Next.js development server with hot reload
- `pnpm build` - Create optimized production build
- `pnpm start` - Start production server
- `pnpm type-check` - Run TypeScript type checking

### Code Quality
- `pnpm lint` - Run ESLint with Next.js configuration
- `pnpm format` - Format code with Prettier
- `pnpm format:check` - Verify code formatting compliance

### Advanced Development
- `pnpm lint:fix` - Auto-fix ESLint issues
- `pnpm clean` - Clean build artifacts and caches

## 📱 Responsive Design System

### Layout Architecture

**Breakpoint System:**
- **Mobile**: `< 768px` - Single column, collapsible sidebar
- **Tablet**: `768px - 1024px` - Adaptive chart layout
- **Desktop**: `> 1024px` - Multi-column dashboard with full sidebar

**Component Responsiveness:**
- **Charts**: Dynamic axis hiding based on screen size
- **Navigation**: Desktop tabs ↔ Mobile hamburger menu
- **Sidebar**: Collapsible with persistent state
- **Chat Widget**: Floating design with mobile optimization

### Adaptive Features

- **Grid Layout**: 1-3 column responsive grid for charts
- **Synchronized Scaling**: Consistent depth axis across breakpoints
- **Touch Optimization**: Mobile-friendly interactions
- **Performance**: Conditional rendering based on screen size

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t oil-drilling-dashboard .
```

### Run Container

```bash
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_BASE_URL=http://your-api-url \
  oil-drilling-dashboard
```

## 📊 Data Processing & Formats

### Client-Side File Processing

The application performs initial file processing on the client-side using:
- **xlsx**: Excel file parsing with multi-sheet support
- **papaparse**: High-performance CSV parsing with streaming
- **Data Validation**: Type checking and format verification
- **Preview Generation**: Instant data preview before upload

### Supported Data Formats

#### Required Columns
- `depth`: Depth measurement (ft) - primary axis for all charts
- `dt`: Sonic travel time (µs/ft) - acoustic logging data
- `gr`: Gamma ray (API) - natural radioactivity measurements

#### Rock Composition Columns (%)
- `sh`: Shale percentage
- `anh`: Anhydrite percentage
- `ls`: Limestone percentage
- `coal`: Coal percentage
- `salt`: Salt percentage
- `dol`: Dolomite percentage

### File Type Support

- **Excel Files**: `.xlsx`, `.xls` with multi-sheet detection
- **CSV Files**: `.csv` with automatic delimiter detection
- **Processing**: Client-side parsing with instant validation feedback

## 🔌 API Integration

### RESTful API Client

The application uses a comprehensive API client (`lib/api.ts`) featuring:

- **Type-Safe Requests**: Full TypeScript coverage for all endpoints
- **Error Handling**: Centralized error management with user-friendly messages
- **Request/Response Types**: Strongly typed interfaces for all API interactions
- **Factory Pattern**: Service factory for different API concerns

### Streaming Chat Integration

- **Server-Sent Events**: Real-time AI responses with status updates
- **Streaming Parser**: Custom SSE message parsing and state management
- **Optimistic Updates**: Immediate UI feedback with background synchronization
- **Error Recovery**: Graceful handling of streaming interruptions

### API Endpoints

#### Data Management
- `POST /drilling/upload` - File upload with processing
- `POST /drilling/query` - Structured data queries
- `GET /drilling/session/{id}` - Session information

#### AI Chat
- `POST /chat/` - Conversational AI queries
- `POST /chat/` (stream) - Streaming chat responses

## 🔒 Environment Variables

| Variable                   | Description                    | Required | Default |
| -------------------------- | ------------------------------ | -------- | ------- |
| `NEXT_PUBLIC_API_BASE_URL` | Backend API base URL           | Yes      | -       |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is proprietary software. All rights reserved.

## Support

For support and questions:

- Create an issue in the repository
- Contact the development team

## Roadmap

### ✅ Implemented Features
- [x] Real-time AI chat with streaming responses
- [x] Advanced data visualization with synchronized charts
- [x] Client-side file processing (Excel/CSV)
- [x] Responsive design with mobile optimization
- [x] Session-based data management
- [x] Type-safe API integration
- [x] Modern UI with shadcn/ui components

### 🔄 In Development
- [ ] Advanced filtering and search capabilities
- [ ] Data export functionality (PDF/Excel)
- [ ] Multi-well comparison tools
- [ ] Predictive analytics dashboard
- [ ] Enhanced error handling and recovery

### 📋 Planned Features
- [ ] Real-time collaborative sessions
- [ ] Advanced chart customization options
- [ ] Data annotation and markup tools
- [ ] Historical data trend analysis
- [ ] Mobile app companion (React Native)
- [ ] Offline data synchronization
- [ ] Advanced user permissions and sharing

---

Built with ❤️ for the oil and gas industry
