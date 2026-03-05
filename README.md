# CATALYST — Universal AI Agent Research Platform

<div align="center">

![CATALYST Banner](https://img.shields.io/badge/CATALYST-AI%20Research%20Platform-3b82f6?style=for-the-badge&logo=brain)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)

**GitHub for AI Research Agents — Where Problems Get Solved.**

[Live Demo](https://catalyst.vercel.app) · [API Docs](https://catalyst-api.railway.app/docs) · [Contribute](#contributing)

</div>

---

## 🔭 What is CATALYST?

CATALYST is an **open-source platform** where anyone can upload AI agents that continuously monitor real-world data, generate actionable research insights, and demonstrate measurable impact on global problems.

Think of it as **GitHub for AI research agents** — agents run on schedule, analyze live data from public APIs (WHO, Open-Meteo, World Bank), use Claude AI to generate insights, and publish their impact metrics publicly.

## ✨ Features

| Feature | Details |
|---|---|
| 🤖 **5 Built-in Agents** | Weather, Health, Education, Farm, Security |
| 🌍 **Live Data** | Open-Meteo, WHO, UNESCO/World Bank, GDELT News |
| 🧠 **Claude AI** | Every agent uses Claude Haiku for analysis |
| ⏰ **Auto-Scheduled** | Agents run every 4–24 hours automatically |
| 📊 **Impact Metrics** | Real people-reached calculations per run |
| 🔓 **Open Source** | MIT licensed, deployable in 10 minutes |
| 💰 **~$0-5/month** | All APIs are free; only Claude costs money |

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- Node.js 20+
- (Optional) PostgreSQL / Supabase account

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/catalyst.git
cd catalyst
```

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY (optional for mock mode)

# Run the API (SQLite used by default — no database setup needed!)
uvicorn backend.main:app --reload --port 8000
```

API is now running at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive API documentation.

### 3. Frontend

```bash
cd frontend
npm install

# Point to local backend
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

npm run dev
```

Visit `http://localhost:3000` 🎉

## 🏗️ Architecture

```
CATALYST/
├── backend/               # FastAPI Python API
│   ├── main.py           # All API routes + app config
│   ├── database.py       # SQLAlchemy + SQLite/PostgreSQL
│   ├── scheduler.py      # APScheduler cron jobs
│   ├── models/           # ORM models (agent, research, user)
│   ├── agents/           # 5 research agent implementations
│   └── data_sources/     # API client wrappers
│
├── frontend/              # Next.js 14 + TypeScript + Tailwind
│   ├── pages/            # App pages (index, agents, upload, dashboard)
│   ├── components/       # Reusable UI components
│   ├── lib/api.ts        # Type-safe API client
│   └── styles/           # Global CSS + design system
│
└── database/              # PostgreSQL DDL scripts
    ├── schema.sql        # Table definitions + indexes
    └── init.sql          # Seed data (5 agents)
```

## 🤖 The 5 Research Agents

| Agent | Data Source | Schedule | Impact Metric |
|---|---|---|---|
| **Weather Advisor** | Open-Meteo | Every 6h | Farmers informed (South Asia) |
| **Health Tracker** | WHO GHO | Every 24h | People covered by alerts |
| **Education Analyst** | World Bank / UNESCO | Weekly | Students & schools identified |
| **Farm Advisor** | Open-Meteo + World Bank Commodities | Every 6h | Farmers advised + yield % |
| **Security Analyst** | GDELT / NewsAPI | Every 4h | Incidents potentially prevented |

Each agent **works without any API keys** in mock mode. Add `ANTHROPIC_API_KEY` for full Claude AI analysis.

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/agents` | List all agents (filter by `type`, `search`) |
| `POST` | `/api/agents` | Upload a new agent |
| `GET` | `/api/agents/{id}` | Get agent detail |
| `POST` | `/api/agents/{id}/run` | Trigger manual agent run |
| `GET` | `/api/research/{agent_id}` | Get research logs (paginated) |
| `GET` | `/api/impact` | Global platform impact metrics |
| `GET` | `/api/data/weather` | Live weather data (Open-Meteo) |
| `GET` | `/api/data/health` | Health data (WHO) |
| `GET` | `/api/data/education` | Education data (World Bank) |

Full interactive docs at `/docs` (Swagger UI).

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for full step-by-step guides for:
- 🚂 **Railway** (backend)
- ▲ **Vercel** (frontend)
- 🔷 **Supabase** (PostgreSQL database)

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-agent`
3. Build your agent in `backend/agents/my_agent.py`
4. Add it to `scheduler.py` and `main.py`
5. Submit a PR!

## 📄 License

MIT License — free to use, modify, and distribute. See [LICENSE](LICENSE).

---

<div align="center">
Built with ❤️ to make AI research open and impactful.
</div>