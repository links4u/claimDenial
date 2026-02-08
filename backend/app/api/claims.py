"""
Claims API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.models.models import Claim, AuditLog
from app.schemas.schemas import ClaimCreate, ClaimResponse, WorkflowRequest, WorkflowResponse
from app.services.workflow_service import execute_workflow
from app.models.models import Appeal
import structlog

logger = structlog.get_logger()

router = APIRouter()


@router.post("/", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
async def create_claim(
    claim_data: ClaimCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new claim record.
    
    This endpoint only creates the claim in the database.
    Use POST /claims/{claim_id}/process to trigger the appeal workflow.
    """
    # Check if claim_id already exists
    existing = db.query(Claim).filter(Claim.claim_id == claim_data.claim_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Claim with ID {claim_data.claim_id} already exists"
        )
    
    # Create claim
    claim = Claim(
        claim_id=claim_data.claim_id,
        denial_code=claim_data.denial_code,
        denial_description=claim_data.denial_description,
        payer_name=claim_data.payer_name,
        policy_text=claim_data.policy_text
    )
    
    db.add(claim)
    db.commit()
    db.refresh(claim)
    
    logger.info("claim_created", claim_id=claim_data.claim_id)
    
    return claim


@router.get("/", response_model=List[ClaimResponse])
async def list_claims(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all claims with pagination."""
    claims = db.query(Claim).offset(skip).limit(limit).all()
    return claims


@router.get("/{claim_id}", response_model=ClaimResponse)
async def get_claim(
    claim_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific claim by claim_id."""
    claim = db.query(Claim).filter(Claim.claim_id == claim_id).first()
    
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Claim {claim_id} not found"
        )
    
    return claim


@router.post("/process", response_model=WorkflowResponse)
async def process_claim(
    request: WorkflowRequest,
    db: Session = Depends(get_db)
):
    """
    Process a claim through the full agent workflow.
    
    This triggers:
    1. IntentRouter
    2. DenialClassifier
    3. PolicyRetrieval (RAG)
    4. AppealDrafting
    5. ComplianceGuardrail
    
    Returns the generated appeal draft for human approval.
    """
    # Fetch claim
    claim = db.query(Claim).filter(Claim.claim_id == request.claim_id).first()
    
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Claim {request.claim_id} not found"
        )
    
    # Prepare claim data for workflow
    claim_data = {
        "claim_id": claim.claim_id,
        "denial_code": claim.denial_code,
        "denial_description": claim.denial_description,
        "payer_name": claim.payer_name,
        "policy_text": claim.policy_text
    }
    
    # Execute workflow
    logger.info("workflow_triggered", claim_id=request.claim_id)
    
    final_state = await execute_workflow(claim_data)
    
    # Update claim with category
    if final_state.get("category"):
        claim.category = final_state["category"]
        db.commit()
    
    # Create appeal record if draft was generated
    appeal_id = None
    if final_state.get("draft_text"):
        appeal = Appeal(
            claim_id=claim.id,
            draft_text=final_state["draft_text"],
            policy_citations=final_state.get("policy_citations", []),
            status="draft",
            compliance_issues=final_state.get("compliance_issues", []),
            retry_count=final_state.get("retry_count", 0)
        )
        db.add(appeal)
        db.commit()
        db.refresh(appeal)
        appeal_id = appeal.id
        
        logger.info("appeal_draft_created", claim_id=request.claim_id, appeal_id=str(appeal_id))
    
    # Determine success
    success = final_state.get("routing_decision") == "proceed" and final_state.get("draft_text") is not None
    
    return WorkflowResponse(
        success=success,
        claim_id=request.claim_id,
        appeal_id=appeal_id,
        category=final_state.get("category"),
        draft_text=final_state.get("draft_text"),
        policy_citations=final_state.get("policy_citations"),
        compliance_issues=final_state.get("compliance_issues"),
        message="Appeal draft generated successfully" if success else final_state.get("validation_message", "Workflow failed")
    )
