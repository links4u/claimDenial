# ClaimPilot™ Project Structure

```
claim-denial-management/
├── backend/                      # FastAPI Backend
│   ├── app/
│   │   ├── agents/              # LangGraph AI Agents
│   │   │   ├── base_agent.py
│   │   │   ├── intent_router.py
│   │   │   ├── denial_classifier.py
│   │   │   ├── policy_retrieval.py
│   │   │   ├── appeal_drafting.py
│   │   │   └── compliance_guardrail.py
│   │   ├── api/                 # REST API Endpoints
│   │   │   ├── claims.py
│   │   │   ├── appeals.py
│   │   │   ├── policies.py
│   │   │   └── audit.py
│   │   ├── core/                # Configuration
│   │   │   └── config.py
│   │   ├── db/                  # Database Session
│   │   │   └── session.py
│   │   ├── models/              # SQLAlchemy Models
│   │   │   └── models.py
│   │   ├── schemas/             # Pydantic Schemas
│   │   │   └── schemas.py
│   │   ├── services/            # Business Logic
│   │   │   └── workflow_service.py
│   │   └── main.py              # FastAPI App
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── SubmitClaimPage.jsx
│   │   │   ├── ReviewAppealsPage.jsx
│   │   │   └── AuditLogPage.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── database/                     # Database Scripts
│   ├── init.sql                 # Schema Definition
│   └── seeds/
│       └── seed_data.sql        # Sample Data
│
├── docs/                         # Documentation
│   └── architecture.md          # System Design Document
│
├── docker-compose.yml           # Orchestration
├── .env.example                 # Environment Template
├── .env                         # Actual Config (gitignored)
├── .gitignore
├── README.md                    # Main Documentation
├── QUICKSTART.md               # Setup Guide
└── LICENSE                      # MIT License
```

## Key Components

### Backend (Python/FastAPI)
- **Agents**: 6 specialized AI agents orchestrated by LangGraph
- **API**: RESTful endpoints for claims, appeals, policies, audit
- **Database**: PostgreSQL with pgvector for RAG
- **LLM**: Claude Sonnet via Anthropic API

### Frontend (React/Vite)
- **Pages**: Home, Submit Claim, Review Appeals, Audit Log
- **Styling**: TailwindCSS for modern UI
- **API Client**: Axios for backend communication

### Infrastructure
- **Docker Compose**: Single-command deployment
- **PostgreSQL**: 16 with pgvector extension
- **Ports**: Backend (1500), Frontend (2400), DB (5432)

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, TailwindCSS |
| Backend | Python 3.11, FastAPI |
| AI | LangChain, LangGraph, Claude Sonnet |
| Database | PostgreSQL 16, pgvector |
| Orchestration | Docker Compose |
