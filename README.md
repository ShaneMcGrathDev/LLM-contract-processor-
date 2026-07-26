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

## 🗂️ Some Essential Files in the directories to check out
📝 README.md (You are here, authored in the amazing Markdown language)               
⚙️ backend/app.py (Be sure to check out the API routes too)               
🎨 frontend/src/app/page.tsx    
📦 package.json                 
🐳 docker-compose.yml  

## 🤖A special thanks to Claude LLM API
