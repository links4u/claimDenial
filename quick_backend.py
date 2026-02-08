#!/usr/bin/env python3
"""
Quick Start Backend Server - Simplified for Demo

Runs FastAPI backend with minimal dependencies for demo purposes.
Uses in-memory mock data instead of PostgreSQL.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime

app = FastAPI(title="ClaimPilot™ API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:2400", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data
MOCK_CLAIMS = []
MOCK_APPEALS = []

@app.get("/")
def root():
    return {"message": "ClaimPilot™ API", "status": "running", "version": "1.0.0"}

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "up",
            "database": "mock",
            "llm": "configured"
        }
    }

@app.post("/api/v1/claims")
def create_claim(claim: dict):
    claim_id = f"CLM-{len(MOCK_CLAIMS) + 1:05d}"
    claim_data = {
        "id": claim_id,
        **claim,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    MOCK_CLAIMS.append(claim_data)
    return claim_data

@app.get("/api/v1/claims")
def list_claims():
    return MOCK_CLAIMS

@app.get("/api/v1/claims/{claim_id}")
def get_claim(claim_id: str):
    for claim in MOCK_CLAIMS:
        if claim["id"] == claim_id:
            return claim
    return JSONResponse(status_code=404, content={"error": "Claim not found"})

@app.post("/api/v1/appeals")
def create_appeal(appeal: dict):
    appeal_id = f"APL-{len(MOCK_APPEALS) + 1:05d}"
    appeal_data = {
        "id": appeal_id,
        **appeal,
        "status": "draft",
        "created_at": datetime.now().isoformat(),
        "draft_text": f"""Dear Appeals Committee,

I am writing to appeal the denial of Claim {appeal.get('claim_id', 'UNKNOWN')}.

DENIAL REASON:
The claim was denied with code {appeal.get('denial_code', 'N/A')}.

POLICY EVIDENCE:
Based on applicable policy sections, this service should be covered.

REQUEST FOR RECONSIDERATION:
We respectfully request reconsideration of this denial.

Sincerely,
Healthcare Provider Billing Department"""
    }
    MOCK_APPEALS.append(appeal_data)
    return appeal_data

@app.get("/api/v1/appeals")
def list_appeals():
    return MOCK_APPEALS

@app.get("/api/v1/appeals/{appeal_id}")
def get_appeal(appeal_id: str):
    for appeal in MOCK_APPEALS:
        if appeal["id"] == appeal_id:
            return appeal
    return JSONResponse(status_code=404, content={"error": "Appeal not found"})

@app.put("/api/v1/appeals/{appeal_id}/approve")
def approve_appeal(appeal_id: str):
    for appeal in MOCK_APPEALS:
        if appeal["id"] == appeal_id:
            appeal["status"] = "approved"
            appeal["approved_at"] = datetime.now().isoformat()
            return appeal
    return JSONResponse(status_code=404, content={"error": "Appeal not found"})

@app.get("/api/v1/audit-logs")
def list_audit_logs():
    return [
        {
            "id": 1,
            "timestamp": datetime.now().isoformat(),
            "action": "claim_submitted",
            "user": "demo_user",
            "details": "Claim CLM-00001 submitted"
        },
        {
            "id": 2,
            "timestamp": datetime.now().isoformat(),
            "action": "appeal_drafted",
            "user": "system",
            "details": "Appeal APL-00001 drafted"
        }
    ]

@app.post("/api/v1/claims/process")
def process_claim(data: dict):
    """Process a claim through the agentic workflow"""
    claim_id = data.get("claim_id") 
   
    # Simulate the 6-agent workflow
    workflow_result = {
        "claim_id": claim_id,
        "status": "completed",
        "workflow_steps": [
            {"agent": "Intent Router", "status": "completed", "result": "PROCEED"},
            {"agent": "Denial Classifier", "status": "completed", "result": "Coverage"},
            {"agent": "Policy Retrieval", "status": "completed", "result": "3 policies found"},
            {"agent": "Appeal Drafting", "status": "completed", "result": "Draft created"},
            {"agent": "Compliance Guardrail", "status": "completed", "result": "PASSED"},
            {"agent": "Human Approval", "status": "pending", "result": "Awaiting review"}
        ],
        "appeal_id": f"APL-{len(MOCK_APPEALS) + 1:05d}",
        "processing_time_ms": 8432
    }
    
    # Auto-create the appeal
    appeal_data = {
        "id": workflow_result["appeal_id"],
        "claim_id": claim_id,
        "status": "draft",
        "created_at": datetime.now().isoformat(),
        "draft_text": f"""Dear Appeals Committee,

Re: Appeal for Claim ID {claim_id}

We are writing to formally appeal the denial of the above-referenced claim. Based on our comprehensive analysis using AI-powered policy retrieval and medical necessity assessment, we respectfully request reconsideration.

DENIAL ANALYSIS:
The claim was denied for coverage-related reasons. However, our multi-agent review system has identified applicable policy provisions that support coverage for this service.

POLICY EVIDENCE:
Our RAG-powered policy retrieval system identified 3 relevant policy excerpts that support this appeal:
1. Outpatient Services Coverage - Section 4.2.1
2. Medical Necessity Criteria - Section 8.1.3  
3. Provider Network Requirements - Section 2.4

REQUEST FOR RECONSIDERATION:
Based on the evidence presented and applicable policy language, we respectfully request that you reconsider this denial and approve payment for the services rendered.

Thank you for your attention to this matter.

Sincerely,
Healthcare Provider Billing Department

--- Generated by ClaimPilot™ AI System ---
"""
    }
    MOCK_APPEALS.append(appeal_data)
    
    return workflow_result

@app.get("/api/v1/audit/")
def list_audit_logs_v2(limit: int = 50):    
    return [
        {
            "id": 1,
            "timestamp": datetime.now().isoformat(),
            "action": "claim_submitted",
            "agent": "Intent Router",
            "user": "demo_user",
            "details": "Claim processed successfully"
        },
        {
            "id": 2,
            "timestamp": datetime.now().isoformat(),
            "action": "appeal_drafted",
            "agent": "Appeal Drafting Agent",
            "user": "system",
            "details": "Appeal draft generated"
        }
    ][:limit]

@app.get("/api/v1/audit/agents")
def list_agents():
    return [
        {"id": 1, "name": "Intent Router", "executions": 42},
        {"id": 2, "name": "Denial Classifier", "executions": 38},
        {"id": 3, "name": "Policy Retrieval", "executions": 35},
        {"id": 4, "name": "Appeal Drafting", "executions": 32},
        {"id": 5, "name": "Compliance Guardrail", "executions": 32},
        {"id": 6, "name": "Human Approval", "executions": 28}
    ]

@app.get("/api/v1/policies/")
def list_policies():
    return {
        "policies": [
            {"id": 1, "section": "4.2.1", "title": "Outpatient Services Coverage", "excerpt_count": 127},
            {"id": 2, "section": "8.1.3", "title": "Medical Necessity Criteria", "excerpt_count": 203},
            {"id": 3, "section": "2.4", "title": "Provider Network Requirements", "excerpt_count": 89}
        ],
        "total": 1247
    }

@app.get("/api/v1/policies/payers")
def list_payers():
    return [
        "Blue Cross Blue Shield",
        "Aetna",
        "UnitedHealthcare",
        "Cigna",
        "Humana"
    ]

if __name__ == "__main__":
    print("=" * 80)
    print("🚀 Starting ClaimPilot™ Backend Server")
    print("=" * 80)
    print(f"Server URL: http://localhost:1500")
    print(f"API Docs: http://localhost:1500/docs")
    print(f"Health Check: http://localhost:1500/health")
    print("=" * 80)
    print("⚠️  Using mock data (no database required)")
    print("=" * 80)
    
    uvicorn.run(app, host="0.0.0.0", port=1500, log_level="info")
