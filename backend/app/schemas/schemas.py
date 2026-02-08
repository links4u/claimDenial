"""
Pydantic Schemas for API Request/Response Validation
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# =====================================================
# Claim Schemas
# =====================================================

class ClaimCreate(BaseModel):
    """Schema for creating a new claim."""
    claim_id: str = Field(..., description="Unique claim identifier", min_length=1, max_length=100)
    denial_code: str = Field(..., description="Denial code (e.g., CO-197)", min_length=1, max_length=50)
    denial_description: str = Field(..., description="Description of the denial reason", min_length=1)
    payer_name: str = Field(..., description="Name of the insurance payer", min_length=1, max_length=200)
    policy_text: Optional[str] = Field(None, description="Optional policy text excerpt")
    
    class Config:
        json_schema_extra = {
            "example": {
                "claim_id": "CLM-2024-006",
                "denial_code": "CO-197",
                "denial_description": "Prior authorization not obtained for specialist consultation",
                "payer_name": "Blue Cross Blue Shield",
                "policy_text": "Section 5.2: All specialist consultations require prior authorization."
            }
        }


class ClaimResponse(BaseModel):
    """Schema for claim response."""
    id: UUID
    claim_id: str
    denial_code: str
    denial_description: str
    payer_name: str
    policy_text: Optional[str]
    category: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# =====================================================
# Appeal Schemas
# =====================================================

class AppealResponse(BaseModel):
    """Schema for appeal response."""
    id: UUID
    claim_id: UUID
    draft_text: str
    policy_citations: Optional[List[str]]
    status: str
    approved: bool
    user_feedback: Optional[str]
    compliance_issues: Optional[List[str]]
    retry_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class AppealApproval(BaseModel):
    """Schema for approving/rejecting an appeal."""
    approved: bool
    feedback: Optional[str] = Field(None, description="Optional feedback if rejecting")


# =====================================================
# Workflow Schemas
# =====================================================

class WorkflowRequest(BaseModel):
    """Schema for initiating appeal workflow."""
    claim_id: str = Field(..., description="Claim ID to process")


class WorkflowResponse(BaseModel):
    """Schema for workflow execution response."""
    success: bool
    claim_id: str
    appeal_id: Optional[UUID]
    category: Optional[str]
    draft_text: Optional[str]
    policy_citations: Optional[List[str]]
    compliance_issues: Optional[List[str]]
    message: str


# =====================================================
# Policy Schemas
# =====================================================

class PolicyExcerpt(BaseModel):
    """Schema for policy excerpt from RAG."""
    id: UUID
    section_title: str
    section_text: str
    similarity_score: float
    payer_name: str


# =====================================================
# Audit Log Schemas
# =====================================================

class AuditLogResponse(BaseModel):
    """Schema for audit log response."""
    id: UUID
    claim_id: Optional[UUID]
    appeal_id: Optional[UUID]
    agent_name: str
    input_data: Optional[dict]
    output_data: Optional[dict]
    metadata: Optional[dict]
    created_at: datetime
    
    class Config:
        from_attributes = True


# =====================================================
# Health Check Schema
# =====================================================

class HealthCheck(BaseModel):
    """Schema for health check response."""
    status: str
    timestamp: datetime
    database: str
    version: str
