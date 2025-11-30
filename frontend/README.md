# Oil Drilling Data Visualization Dashboard

A modern, responsive web application for visualizing oil drilling data and querying insights using AI-powered natural language processing. Built with Next.js, TypeScript, and cutting-edge UI components.

## 🚀 Features

### 📊 Data Visualization

- **Interactive Charts**: Real-time visualization of drilling parameters including:
  - Rock Composition Analysis (multi-line charts)
  - DT (Sonic) Log Charts
  - GR (Gamma Ray) Log Charts
- **Synchronized Y-Axis**: Consistent depth scaling across all charts
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices

### 🤖 AI-Powered Chat

- **Natural Language Queries**: Ask questions about drilling data in plain English
- **Context-Aware Responses**: AI understands drilling terminology and data relationships
- **Session Management**: Persistent chat sessions with data context

### 📁 Data Management

- **File Upload Support**: Import drilling data from Excel (.xlsx/.xls) and CSV files
- **Real-time Processing**: Instant data analysis and visualization
- **Data Persistence**: Secure session-based data storage

### 🎨 User Experience

- **Modern UI**: Clean, professional interface using shadcn/ui components
- **Dark/Light Mode**: Theme switching capability
- **Loading States**: Comprehensive loading indicators and error handling
- **Toast Notifications**: User-friendly feedback system

## 🛠️ Technology Stack

### Frontend Framework

- **Next.js 16**: React framework with App Router
- **React 19**: Latest React features and hooks
- **TypeScript**: Type-safe development

### UI & Styling

- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: High-quality React components
- **Radix UI**: Accessible component primitives
- **Lucide React**: Beautiful icon library

### Data Visualization

- **Recharts**: Declarative charting library for React
- **Responsive Charts**: Mobile-optimized data visualization

### State Management

- **Zustand**: Lightweight state management
- **Local Storage**: Persistent session storage

### Development Tools

- **ESLint**: Code linting
- **Prettier**: Code formatting
- **TypeScript**: Static type checking

## 📋 Prerequisites

- **Node.js**: Version 18 or higher
- **pnpm**: Package manager (recommended)
- **Backend API**: Running drilling data processing service

## 🚀 Getting Started

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

## 📁 Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── (dashboard)/       # Dashboard layout
│   ├── globals.css        # Global styles
│   └── layout.tsx         # Root layout
├── components/            # Reusable UI components
│   ├── layout/           # Layout components
│   └── ui/               # shadcn/ui components
├── features/             # Feature-based architecture
│   ├── drilling/         # Drilling data management
│   │   ├── components/   # Drilling-specific components
│   │   ├── stores/       # Zustand stores
│   │   ├── types/        # TypeScript types
│   │   └── utils/        # Utility functions
│   └── chat/             # Chat functionality
├── lib/                  # Shared utilities
│   ├── api.ts           # API client
│   └── storage.ts       # Local storage utilities
└── hooks/               # Custom React hooks
```

## 🔧 Available Scripts

- `pnpm dev` - Start development server
- `pnpm build` - Build for production
- `pnpm start` - Start production server
- `pnpm lint` - Run ESLint
- `pnpm format` - Format code with Prettier
- `pnpm format:check` - Check code formatting

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

## 📊 Data Format

The application accepts drilling data in the following format:

### Required Columns

- `depth`: Depth measurement (ft)
- `dt`: Sonic travel time (µs/ft)
- `gr`: Gamma ray (API)
- Rock composition percentages:
  - `sh`: Shale (%)
  - `anh`: Anhydrite (%)
  - `ls`: Limestone (%)
  - `coal`: Coal (%)
  - `salt`: Salt (%)
  - `dol`: Dolomite (%)

### Supported File Types

- Excel files (.xlsx, .xls)
- CSV files (.csv)

## 🔒 Environment Variables

| Variable                   | Description          | Required |
| -------------------------- | -------------------- | -------- |
| `NEXT_PUBLIC_API_BASE_URL` | Backend API base URL | Yes      |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is proprietary software. All rights reserved.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Contact the development team

## 🚀 Roadmap

- [ ] Real-time data streaming
- [ ] Advanced filtering and search
- [ ] Export capabilities
- [ ] Multi-well comparison
- [ ] Predictive analytics
- [ ] Mobile app companion

---

Built with ❤️ for the oil and gas industry
