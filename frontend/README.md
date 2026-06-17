# Audio-Freelance Frontend

Next.js 16 dashboard for the Audio-Freelance acquisition system.

## Quick Start

```bash
npm install
npm run dev
```

Requires the backend running on `http://localhost:8080`. Start both with `make dev` from the project root.

## Pages

- **/** — Dashboard with lead counts, trends, pricing, quick actions
- **/leads** — Filterable lead list with verdict badges
- **/market** — Full market intelligence report
- **/opportunities** — Actionable opportunities and saved drafts
- **/prospect/[niche]** — Run a prospect scan per niche

## Stack

- Next.js 16 (App Router)
- Tailwind CSS 4
- shadcn/ui (Radix primitives)
- Inter Variable font
- Recharts for charts
- Dark/light theme toggle

## Build

```bash
npm run build
npm start
```
