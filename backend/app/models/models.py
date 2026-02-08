"""
SQLAlchemy Models

Defines database models for claims, policies, appeals, and audit logs.
"""

from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
import uuid

from app.db.session import Base


class Claim(Base):
    """Claim denial record."""
    __tablename__ = "claims"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(String(100), unique=True, nullable=False, index=True)
    denial_code = Column(String(50), nullable=False)
    denial_description = Column(Text, nullable=False)
    payer_name = Column(String(200), nullable=False, index=True)
    policy_text = Column(Text, nullable=True)
    category = Column(String(50), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    appeals = relationship("Appeal", back_populates="claim", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="claim", cascade="all, delete-orphan")


class Policy(Base):
    """Policy document with vector embeddings for RAG."""
    __tablename__ = "policies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    payer_name = Column(String(200), nullable=False, index=True)
    section_title = Column(String(500), nullable=False)
    section_text = Column(Text, nullable=False)
    embedding = Column(Vector(1536), nullable=True)  # OpenAI text-embedding-3-small
    metadata = Column(JSONB, nullable=True)
    indexed_at = Column(DateTime(timezone=True), server_default=func.now())


class Appeal(Base):
    """Generated appeal letter."""
    __tablename__ = "appeals"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey("claims.id", ondelete="CASCADE"), nullable=False)
    draft_text = Column(Text, nullable=False)
    policy_citations = Column(JSONB, nullable=True)
    status = Column(String(50), default="draft", index=True)
    approved = Column(Boolean, default=False)
    user_feedback = Column(Text, nullable=True)
    compliance_issues = Column(JSONB, nullable=True)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    approved_at = Column(DateTime(timezone=True), nullable=True)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    version = Column(Integer, default=1)
    
    # Relationships
    claim = relationship("Claim", back_populates="appeals")
    audit_logs = relationship("AuditLog", back_populates="appeal", cascade="all, delete-orphan")


class AuditLog(Base):
    """Audit trail for agent executions."""
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey("claims.id", ondelete="CASCADE"), nullable=True)
    appeal_id = Column(UUID(as_uuid=True), ForeignKey("appeals.id", ondelete="CASCADE"), nullable=True)
    agent_name = Column(String(100), nullable=False, index=True)
    input_data = Column(JSONB, nullable=True)
    output_data = Column(JSONB, nullable=True)
    metadata = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    claim = relationship("Claim", back_populates="audit_logs")
    appeal = relationship("Appeal", back_populates="audit_logs")
