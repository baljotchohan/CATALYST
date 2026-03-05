# CATALYST — Deployment Guide

Complete step-by-step guide to deploy CATALYST for free.

**Total Monthly Cost: $0–5** (only Claude API usage costs money)

---

## Architecture Overview

```
Vercel (Frontend) ──→ Railway (Backend API) ──→ Supabase (PostgreSQL)
                                        ↕
                               Claude API (Anthropic)
                               External APIs (Open-Meteo, WHO, etc.)
```

---

## Step 1: Supabase (PostgreSQL Database)

1. Create free account at [supabase.com](https://supabase.com)
2. Click **New Project** → choose a region close to you
3. Note your **database password**
4. Go to **SQL Editor** → paste contents of `database/schema.sql` → run
5. Then paste and run `database/init.sql` (seed data)
6. Go to **Project Settings → Database**
7. Copy the **Connection string** (URI format):
   ```
   postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
   ```
   Save this — you'll add it to Railway.

---

## Step 2: Railway (Backend API)

1. Create free account at [railway.app](https://railway.app)
2. Click **New Project → Deploy from GitHub**
3. Connect your GitHub repo and select it
4. Set **Root Directory** to `backend`
5. Set **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
6. Go to **Variables** tab, add:

| Variable | Value |
|---|---|
| `ANTHROPIC_API_KEY` | `sk-ant-...` (from console.anthropic.com) |
| `DATABASE_URL` | Your Supabase connection string |
| `ALLOWED_ORIGINS` | `https://your-project.vercel.app` |
| `NEWS_API_KEY` | Your NewsAPI key (optional, free tier) |

7. Railway will auto-deploy on every push to `main`
8. Note your deployment URL: `https://catalyst-api-xxx.railway.app`

> **Test it:** Visit `https://your-api.railway.app/health` — should return `{"status": "ok"}`

---

## Step 3: Vercel (Frontend)

1. Create free account at [vercel.com](https://vercel.com)
2. Click **Add New Project → Import from GitHub**
3. Select your repo, set **Framework**: Next.js
4. Set **Root Directory** to `frontend`
5. Go to **Environment Variables**, add:

| Variable | Value |
|---|---|
| `NEXT_PUBLIC_API_URL` | `https://your-api.railway.app` |

6. Click **Deploy** — Vercel builds and deploys automatically
7. Your site is live at: `https://your-project.vercel.app`

---

## Step 4: Update CORS

Go back to Railway, update `ALLOWED_ORIGINS`:
```
https://your-project.vercel.app
```

---

## Step 5: GitHub Secrets (for CI/CD)

For automated deployments via GitHub Actions, add these secrets to your repo
*(Settings → Secrets → Actions)*:

| Secret | Where to find |
|---|---|
| `VERCEL_TOKEN` | vercel.com → Account Settings → Tokens |
| `VERCEL_ORG_ID` | vercel.com → Settings → General |
| `VERCEL_PROJECT_ID` | In your Vercel project settings |
| `RAILWAY_TOKEN` | railway.app → Account Settings → Tokens |
| `NEXT_PUBLIC_API_URL` | Your Railway deployment URL |

---

## Local Development

### Backend (without database)
```bash
cd CATALYST
# SQLite is used automatically when DATABASE_URL is not set
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

---

## Custom Domain (Optional)

1. Buy a domain (e.g., `catalyst-ai.com`)
2. In Vercel → **Domains** → add your domain
3. Update DNS to point to Vercel nameservers
4. HTTPS is automatically provisioned

---

## Troubleshooting

| Problem | Solution |
|---|---|
| CORS errors | Check `ALLOWED_ORIGINS` in Railway matches your Vercel URL exactly |
| No agents showing | Backend not running or wrong `NEXT_PUBLIC_API_URL` |
| Claude not analyzing | Add `ANTHROPIC_API_KEY` to Railway; agents fall back to mock mode without it |
| DB connection error | Verify Supabase connection string format; check SSL settings |
| Railway build fails | Ensure `backend/requirements.txt` is up to date |
