# Dronzer Enterprise Dashboard

This is the official administrative web dashboard for the Dronzer AI Gateway — a modern, production-grade **Next.js** application built to manage the underlying AI Orchestration Engine and Python Gateway from a clean, minimal interface.

---

## Architecture

The frontend follows a strictly component-driven **Clean Architecture** pattern:

- **App Router (`src/app`):** Encapsulates all page routing. Uses Server Components for static layouts and Client Components (`"use client"`) strictly at leaf nodes where interactivity is required.
- **UI Primitives (`src/components/ui`):** Highly reusable, accessible, and stateless UI building blocks built on Radix UI primitives and styled with TailwindCSS (Shadcn/ui pattern).
- **Layouts (`src/components/layout`):** Stateful wrapper components (Sidebar, Navbar) that manage the global UI shell.
- **API Clients (`src/lib/api`):** Typed, centralized HTTP clients for communicating with the backend REST API.
- **State Management:** TanStack Query (React Query) for server-state synchronization, caching, and background refetching.
- **Styling:** Tailwind v4 with a unified **Light Theme** design system defined via CSS variables in `globals.css`.

---

## Folder Structure

```
src/
├── app/
│   ├── dashboard/          # Protected routes (API Keys, Providers, Analytics)
│   │   ├── keys/           # API Key management pages
│   │   ├── providers/      # Provider & model configuration
│   │   ├── analytics/      # Usage and cost analytics
│   │   └── settings/       # Organization settings
│   └── login/              # Authentication entry point
├── components/
│   ├── ui/                 # Radix-based primitive components (Button, Card, Table, etc.)
│   ├── layout/             # Sidebar, Navbar, PageHeader
│   └── features/           # Domain-specific composite components
└── lib/
    ├── api/                # Typed API client modules
    └── utils.ts            # cn() utility and shared helpers
```

---

## Developer Guide

### Prerequisites

| Dependency | Minimum Version |
|---|---|
| Node.js | 20+ |
| npm | 10+ |

### Running Locally

1. Ensure the **Python backend** is running on `http://localhost:8000`.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   # Dashboard available at: http://localhost:3000
   ```

### Environment Variables

Create a `.env.local` file in the `/frontend` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Component Conventions

- All components must be **strictly typed** with TypeScript interfaces — no `any` types.
- Avoid passing large objects as props; prefer passing primitives or using context where appropriate.
- Use the `cn()` utility (`lib/utils.ts`) for dynamically merging Tailwind class names safely.
- Client Components (`"use client"`) must be leaf nodes — never wrap large server-rendered trees in client boundaries unnecessarily.
- All interactive elements must have unique, descriptive `id` attributes for accessibility and testing.

---

## Design System

The dashboard uses a **Light Theme** design system built on CSS custom properties. Key design tokens are defined in `globals.css`:

- **Background:** Clean white / off-white surfaces
- **Accent:** Indigo-based primary color palette
- **Typography:** Inter (Google Fonts) for maximum readability
- **Spacing:** Tailwind's default scale (4px base unit)
- **Shadows:** Subtle `shadow-sm` used sparingly to create depth without visual noise
