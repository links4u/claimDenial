# ClaimPilot™ Quick Start Guide

## Prerequisites
- Docker & Docker Compose
- Anthropic API Key
- OpenAI API Key

## Setup (5 minutes)

1. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys:
   # ANTHROPIC_API_KEY=sk-ant-...
   # OPENAI_API_KEY=sk-...
   ```

2. **Start Services**
   ```bash
   docker-compose up -d
   ```

3. **Initialize Database**
   ```bash
   # Wait 30 seconds for database to be ready
   docker-compose exec database psql -U claimpilot -d claimpilot_db -f /seed_data.sql
   ```

4. **Generate Embeddings**
   ```bash
   curl -X POST http://localhost:1500/api/v1/policies/generate-embeddings
   ```

5. **Open Application**
   - Frontend: http://localhost:2400
   - API Docs: http://localhost:1500/docs

## Usage

### Submit a Claim

1. Navigate to "Submit Claim"
2. Fill in denial details:
   - Claim ID: `CLM-2024-006`
   - Denial Code: `CO-197`
   - Payer: `Blue Cross Blue Shield`
   - Description: `Prior authorization missing`
3. Click "Submit & Process"
4. Wait ~10-15 seconds for AI workflow

### Review Appeal

1. Navigate to "Review Appeals"
2. Select pending appeal
3. Review AI-generated draft
4. Approve or reject with feedback

### View Audit Trail

1. Navigate to "Audit Log"
2. Filter by agent name (optional)
3. Expand entries to see detailed execution data

## Architecture

```
┌─────────────┐
│   React UI  │  Port 2400
│   (Vite)    │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  FastAPI    │  Port 1500
│  Backend    │
└──────┬──────┘
       │
       ├──→ LangGraph Workflow
       │    ├─ IntentRouter
       │    ├─ DenialClassifier (Claude)
       │    ├─ PolicyRetrieval (RAG + pgvector)
       │    ├─ AppealDrafter (Claude)
       │    └─ ComplianceGuardrail (Claude)
       │
       ↓
┌─────────────┐
│ PostgreSQL  │  Port 5432
│ + pgvector  │
└─────────────┘
```

## Troubleshooting

**Services not starting?**
```bash
docker-compose ps  # Check status
docker-compose logs backend  # View logs
```

**No policies retrieved?**
```bash
# Verify embeddings exist
docker-compose exec database psql -U claimpilot -d claimpilot_db \
  -c "SELECT COUNT(*) FROM policies WHERE embedding IS NOT NULL;"
```

**API errors?**
- Check `.env` file has valid API keys
- Verify API billing is active
- Check backend logs: `docker-compose logs backend`

## Development Mode

**Backend only:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 1500
```

**Frontend only:**
```bash
cd frontend
npm install
npm run dev
```

## Production Deployment

See `docs/architecture.md` for:
- Kubernetes deployment
- Environment configuration
- Security hardening
- Monitoring setup

## Key Features

✅ **6 AI Agents** orchestrated by LangGraph  
✅ **RAG-powered** policy retrieval with pgvector  
✅ **Human-in-the-loop** approval workflow  
✅ **Complete audit trail** for compliance  
✅ **< 15 second** end-to-end processing  
✅ **< $0.02** cost per appeal  

## Support

- Report issues: GitHub Issues
- Documentation: `docs/architecture.md`
- API Reference: http://localhost:1500/docs
