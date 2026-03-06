# AI Summarizer Frontend

An elegant, modern frontend for the AI Summarizer API built with React, TypeScript, and Vite.

## Features

- 🔐 Firebase Authentication (Google Sign-In)
- ⚡ Real-time AI text analysis
- 📊 Multiple use case categories
- 📜 Analysis history tracking
- 🎨 Modern, responsive UI with dark theme
- 🚀 Fast and optimized with Vite

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

3. Configure your Firebase project:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create a new project or use existing one
   - Enable Google Authentication in Authentication > Sign-in method
   - Copy your Firebase config values to `.env`

4. Update the API URL in `.env` if your backend runs on a different port:
```
VITE_API_URL=http://localhost:8000
```

## Development

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## Build

Build for production:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## Backend

Make sure the backend API is running on `http://localhost:8000` (or your configured URL).

See the main project README for backend setup instructions.

## Tech Stack

- React 19
- TypeScript
- Vite 8
- Firebase Authentication
- CSS Variables for theming
- Modern ES modules

## Project Structure

```
src/
├── components/       # React components
│   ├── Login.tsx    # Authentication page
│   ├── Dashboard.tsx # Main dashboard
│   ├── Analyzer.tsx  # Text analysis interface
│   └── History.tsx   # Analysis history viewer
├── contexts/        # React contexts
│   └── AuthContext.tsx # Authentication state
├── lib/            # Utilities and services
│   ├── firebase.ts # Firebase configuration
│   └── api.ts      # API client
├── App.tsx         # Root component
├── main.tsx        # Entry point
└── index.css       # Global styles
```

## Features Overview

### Authentication
- Secure Google Sign-In via Firebase
- Automatic token refresh
- Protected routes

### Analyzer
- Multi-category use cases
- Real-time character count
- Language selection for translation tasks
- Copy result to clipboard
- Clear and intuitive interface

### History
- View all past analyses
- Delete individual items
- Detailed view with input and result
- Timestamp tracking
- Responsive list/detail layout

## Styling

The app uses CSS variables for consistent theming:
- Dark mode optimized
- Smooth animations and transitions
- Responsive design for all screen sizes
- Custom scrollbars
- Gradient accents

## License

MIT
