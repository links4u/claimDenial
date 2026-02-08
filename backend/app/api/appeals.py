"""
Appeals API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime

from app.db.session import get_db
from app.models.models import Appeal, Claim
from app.schemas.schemas import AppealResponse, AppealApproval
import structlog

logger = structlog.get_logger()

router = APIRouter()


@router.get("/", response_model=List[AppealResponse])
async def list_appeals(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    db: Session = Depends(get_db)
):
    """List all appeals with optional status filter."""
    query = db.query(Appeal)
    
    if status_filter:
        query = query.filter(Appeal.status == status_filter)
    
    appeals = query.offset(skip).limit(limit).all()
    return appeals


@router.get("/{appeal_id}", response_model=AppealResponse)
async def get_appeal(
    appeal_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific appeal by ID."""
    appeal = db.query(Appeal).filter(Appeal.id == appeal_id).first()
    
    if not appeal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appeal {appeal_id} not found"
        )
    
    return appeal


@router.post("/{appeal_id}/approve", response_model=AppealResponse)
async def approve_or_reject_appeal(
    appeal_id: UUID,
    approval: AppealApproval,
    db: Session = Depends(get_db)
):
    """
    Approve or reject an appeal draft.
    
    This represents the Human-in-the-Loop approval step.
    """
    appeal = db.query(Appeal).filter(Appeal.id == appeal_id).first()
    
    if not appeal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appeal {appeal_id} not found"
        )
    
    if approval.approved:
        appeal.status = "approved"
        appeal.approved = True
        appeal.approved_at = datetime.utcnow()
        logger.info("appeal_approved", appeal_id=str(appeal_id))
    else:
        appeal.status = "rejected"
        appeal.approved = False
        appeal.user_feedback = approval.feedback
        logger.info("appeal_rejected", appeal_id=str(appeal_id), feedback=approval.feedback)
    
    db.commit()
    db.refresh(appeal)
    
    return appeal


@router.get("/claim/{claim_id}", response_model=List[AppealResponse])
async def get_appeals_for_claim(
    claim_id: str,
    db: Session = Depends(get_db)
):
    """Get all appeals for a specific claim."""
    claim = db.query(Claim).filter(Claim.claim_id == claim_id).first()
    
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Claim {claim_id} not found"
        )
    
    appeals = db.query(Appeal).filter(Appeal.claim_id == claim.id).all()
    return appeals
