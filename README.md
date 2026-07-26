# LLM contract processing tool


### Overview
This is a full stack application designed to process contracts into a structured format leveraging LLM APIs. 


## 🏗️ App Architecture

```
Next.js frontend (Vercel)  --->  Flask backend (Railway)  --->  Anthropic Claude API
                                        |
                                        v
                              Postgres / Supabase (or local SQLite fallback)
```

**Frontend** — Next.js app in `frontend/`, hosted on Vercel. Auto-deploys on every push to `main`. Calls the backend via `NEXT_PUBLIC_API_URL` (see env vars below) — never hardcode the backend URL in fetch calls.

**Backend** — Flask app in `backend/`, hosted on Railway. Auto-deploys on every push to `main`. Because this is a monorepo (frontend + backend in one repo), Railway's service **Root Directory must be set to `backend`** in the service's Settings → Source, otherwise Railway's builder can't detect how to build the app. Runs via `backend/Dockerfile`.

- Railway assigns its own `PORT` env var at runtime and routes external traffic to it — `app.py` reads `PORT` from the environment (falls back to `5000` for local dev, where `PORT` isn't set). Never hardcode the listen port.
- Flask debug mode / the auto-reloader must stay **off** in Railway (`Config.DEBUG`, derived from `FLASK_ENV`) — the reloader's file-watcher flaps inside Railway's container filesystem and gets stuck restarting, which looks like the app never coming up (`502 Application failed to respond`).

### Required environment variables

**Backend** (Railway → service → Variables, and mirrored locally in `backend/.env`, which is gitignored):

| Variable | Required | Notes |
|---|---|---|
| `CLAUDE_API_KEY` | **Yes** | Anthropic API key. The Claude client is constructed at module import time, so a missing key crashes the app on startup. |
| `SECRET_KEY` | No | Falls back to `dev-secret-key` — set a real value in any environment that matters. |
| `DATABASE_URL` | No | Falls back to local SQLite (`sqlite:///app.db`). Railway's filesystem is ephemeral per deploy, so SQLite data does **not** persist there — use a real Postgres URL (e.g. Supabase) if data needs to survive redeploys. |
| `FLASK_ENV` | No | Set to `development` locally to enable Flask's debug reloader. Leave unset (or `production`) on Railway. |

**Frontend** (Vercel → project → Environment Variables, and mirrored locally in `frontend/.env.local`, which is gitignored):

| Variable | Required | Notes |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | Recommended | Base URL of the backend API (e.g. `http://localhost:5000` locally, the Railway domain in production). Some fetch call sites have no fallback if this is unset. |

## Project setup instructions

### Backend
cd backend
run python -m pip install -r requirements.txt

### Frontend

## ✅ Project Directory Quick Reference 

- ⚛️ Next.js Frontend 
- 🐍 Flask Backend/REST API 
- 🎯 CRUD operations  
- 🤖 Claude API
- 🐳 Docker Compose
- 💾 PostgreSQL database (Via Supabase platform)
- 🎨 Shadcn UI Library 

# Issue and resoluiton log (1-16 performed on 7/25/26 to bring app back online)

1. frontend/package.json broken → next was pinned to an ancient ^9.3.3, causing 106 npm vulnerabilities. Fixed by upgrading to ^16.2.12 + adding overrides for postcss/sharp/brace-expansion → 0 vulnerabilities.
2. backend/requirements.txt was UTF-16 encoded (from pip freeze > in PowerShell without -Encoding utf8) → pip couldn't parse it. Re-saved as UTF-8.
3. Wrong local venv active → backend/venv was Python 3.14 with no working dependencies (pandas wouldn't build); the real environment was backend/venv312 (Python 3.12), already fully installed.
4. Missing .env files → neither backend/.env nor frontend/.env.local existed, so the app had no CLAUDE_API_KEY or API URL locally. Created both.
5. CLAUDE_API_KEY placeholder never replaced → 401 from Anthropic. Fixed by pasting your real key in.
6. Retired Claude model IDs → claude-sonnet-4-20250514 and claude-3-haiku-20240307 had both passed their retirement dates → 404s. Updated to claude-sonnet-5 and claude-haiku-4-5.
7. message.content[0].text crash → Sonnet 5 runs adaptive thinking by default, so content[0] was a ThinkingBlock, not text. Fixed to search content blocks by type.
8. JSON truncation → max_tokens=2500 wasn't enough for a 68-line-item invoice, and thinking tokens ate into that same budget. Raised to 8192 and disabled thinking (unnecessary for deterministic extraction).
9. Stray tracked .pyc files → nested __pycache__/ dirs were committed because .gitignore only excluded the top-level one. Untracked them and broadened the ignore pattern to **/__pycache__/.
10. Railway build failure ("Railpack could not determine how to build the app") → the monorepo root confused the builder. Fixed by setting the service's Root Directory to backend.
11. Railway app crashing on startup ("Application not found") → CLAUDilway's own environment variables (it only existed in the gitignoredlocal .env, which never gets deployed). Added it in Railway's Variables tab.
12. Railway app unreachable despite running ("Application failed to respond") → app.py hardcoded port 5000, but Railway assigns its own dynamic PORT and routes to that. Fixed to read PORT from the environment.
13. Flask debug reloader flapping in the container → debug=True was hardcoded, and Railway's container filesystem caused the reloader to restart repeatedly. Switched to app.config['DEBUG'], driven by FLASK_ENV, which is unset (→ off) on Railway.
14. Frontend pointed at the wrong Railway domain entirely → NEXT_PUBLIC_API_URL referenced an old/stale casestudy2025-production... domain instead of the actual service's llm-contract-processor-production... domain.
15. Missing https:// scheme in the env var → without it, ${NEXT_PUBLIs a relative path on Vercel's own origin instead of an absolute URL to Railway, producing Vercel's 404 HTML page instead of a Railway response.
16. Stale Vercel build cache → even after fixing the env var, a cacheld baked-in value (Next.js inlines NEXT_PUBLIC_* vars at build time).Fixed by redeploying with build cache disabled.
