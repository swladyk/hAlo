---
name: react-shadcn-ui
description: Conventions for hAlo frontend code — React 19 + Vite + TypeScript, Tailwind, shadcn/ui, API calls via lib/api.ts, responsive layout. Use when writing or changing anything under frontend/.
---

# Frontend conventions (Node 24, React, Vite, TS, Tailwind v4, shadcn/ui)

## Structure
- Your code lives in `src/features/<f>/`: `types.ts` + components + hooks. Export one top-level component; mount it with one line in `src/App.tsx`.
- Import with the `@/` alias (`@/components/ui/button`, `@/lib/api`).

## API calls
- **Only** via `src/lib/api.ts`: `getJson<T>(path)`, `postJson<T>(path, body)`, `streamSSE(path, body, onEvent)`. Paths start with `/api/<feature>`. Never build URLs or call `fetch` elsewhere.
- Type every response with types in `features/<f>/types.ts` that match the backend schemas exactly.
- Show loading and error states (a short text or a red `Badge` is enough).

## UI
- Use shadcn/ui from `src/components/ui/` (button, input, card, badge already installed). Need more? `cd frontend && npx shadcn@latest add <name>` — that edits shared `components/ui/`, so announce it.
- Styling: Tailwind utility classes only. No new `.css` files, no inline style objects, no CSS-in-JS.
- Mobile first: design at ~375px wide, then `sm:`/`md:` for larger. No fixed widths that overflow; use `w-full`, `flex-wrap`, `min-w-0`, `break-words`.
- State: `useState`/`useEffect`/custom hooks. No Redux/Zustand/React Query unless the team agrees.

## Env
`import.meta.env.VITE_*` only; add new vars to `frontend/.env.example`. `VITE_API_URL` is empty locally (Vite proxies `/api` → `localhost:8000`).

## Check
`cd frontend && npm run lint && npm run build`
