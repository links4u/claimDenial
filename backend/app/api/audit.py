"""
Audit Log API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.models.models import AuditLog, Claim
from app.schemas.schemas import AuditLogResponse
import structlog

logger = structlog.get_logger()

router = APIRouter()


@router.get("/", response_model=List[AuditLogResponse])
async def list_audit_logs(
    skip: int = 0,
    limit: int = 100,
    agent_name: str = None,
    db: Session = Depends(get_db)
):
    """List audit logs with optional filtering."""
    query = db.query(AuditLog).order_by(AuditLog.created_at.desc())
    
    if agent_name:
        query = query.filter(AuditLog.agent_name == agent_name)
    
    logs = query.offset(skip).limit(limit).all()
    return logs


@router.get("/claim/{claim_id}", response_model=List[AuditLogResponse])
async def get_audit_trail_for_claim(
    claim_id: str,
    db: Session = Depends(get_db)
):
    """Get complete audit trail for a specific claim."""
    claim = db.query(Claim).filter(Claim.claim_id == claim_id).first()
    
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Claim {claim_id} not found"
        )
    
    logs = db.query(AuditLog)\
        .filter(AuditLog.claim_id == claim.id)\
        .order_by(AuditLog.created_at.asc())\
        .all()
    
    return logs


@router.get("/agents")
async def list_agent_names(db: Session = Depends(get_db)):
    """Get list of unique agent names in audit logs."""
    from sqlalchemy import distinct
    
    agents = db.query(distinct(AuditLog.agent_name)).all()
    
    return {
        "agents": [a[0] for a in agents if a[0]]
    }
