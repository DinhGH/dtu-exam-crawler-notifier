# DTU Exam Notifier - Frontend

React frontend for the DTU Exam Notifier system.

## Features

- Modern React 19 with Vite
- Responsive design with Tailwind CSS
- Dark mode support
- React Query for API state management
- Form validation with React Hook Form & Zod
- Reusable UI components
- Real-time toast notifications

## Pages

1. **Home** - Landing page with hero section and features
2. **Register** - Subscription form for email notifications
3. **Search** - Search and filter exam schedules
4. **Files** - Browse crawled Excel files
5. **File Detail** - View details of a specific file
6. **Dashboard** - Statistics and charts

## Tech Stack

- React 19
- Vite
- Tailwind CSS
- React Router DOM
- Axios
- React Hook Form
- Zod
- Lucide React (icons)
- Recharts (charts)
- Sonner (toasts)

## Setup

1. Install dependencies:

```bash
npm install
```

2. Create `.env` file:

```bash
cp .env.example .env
```

3. Start development server:

```bash
npm run dev
```

## Environment Variables

```env
VITE_API_URL=http://localhost:8000/api
```

## API Endpoints

- `GET /files` - Get list of crawled files
- `GET /files/:id` - Get file details
- `GET /exam-schedules` - Search exam schedules
- `POST /subscriptions` - Create subscription
- `GET /dashboard/stats` - Dashboard statistics

## Project Structure

```
src/
├── assets/
├── components/
│   ├── ui/          # Reusable UI components
│   ├── layout/      # Layout components
│   └── common/      # Common components
├── pages/           # Page components
├── services/        # API services
├── hooks/           # Custom hooks
├── routes/          # React Router config
├── contexts/        # React contexts
├── utils/           # Utility functions
└── constants/       # Constants
```

## Development

- Run development server: `npm run dev`
- Build for production: `npm run build`
- Lint code: `npm run lint`
- Preview production build: `npm run preview`

## Deployment

Build the project:

```bash
npm run build
```

The built files will be in the `dist` directory.

## API Integration

The frontend expects the following backend endpoints:

- `/api/files` - File management
- `/api/exam-schedules` - Exam schedule search
- `/api/subscriptions` - Subscription management
- `/api/dashboard` - Dashboard statistics
