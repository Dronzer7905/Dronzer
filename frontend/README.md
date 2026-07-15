# Dronzer Enterprise Dashboard

This is the official administrative web dashboard for the Dronzer AI Gateway. It is a modern, production-grade Next.js application built to seamlessly manage the underlying Orchestration Engine and Python Gateway.

## Architecture

The frontend follows a strictly component-driven clean architecture pattern:

- **App Router (`src/app`)**: Encapsulates all page routing. Uses Server Components for static layouts and Client Components (`"use client"`) strictly at the leaf nodes where interactivity is required.
- **UI Primitives (`src/components/ui`)**: Highly reusable, accessible, and stateless UI building blocks implemented using Radix primitives and styled with TailwindCSS (Shadcn pattern).
- **Layouts (`src/components/layout`)**: Stateful wrapper components (Sidebar, Navbar) handling the global UI shell.
- **State Management**: (Placeholder for TanStack Query integration)
- **Styling**: Tailwind v4 with a unified Dark Mode default aesthetic via `globals.css` CSS variables.

## Folder Structure
- `/app/dashboard/*`: Protected routes for the authenticated dashboard.
- `/app/login`: Authentication entry point.
- `/components`: Component library.

## Developer Guide

1. Ensure the Python backend is running locally on port `8000`.
2. Ensure you have Node.js 20+ installed.
3. Run `npm install` inside the `/frontend` directory.
4. Run `npm run dev` to start the dashboard on `http://localhost:3000`.

## Component Conventions
- All components must be strictly typed with TypeScript interfaces.
- Avoid passing massive objects as props; pass primitives where possible.
- Use the `cn()` utility (`lib/utils.ts`) for dynamically merging Tailwind classes safely.
