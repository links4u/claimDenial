"""
Policies API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from langchain_openai import OpenAIEmbeddings

from app.db.session import get_db
from app.models.models import Policy
from app.core.config import settings
import structlog

logger = structlog.get_logger()

router = APIRouter()


@router.get("/")
async def list_policies(
    payer_name: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all policy excerpts with optional payer filter."""
    query = db.query(Policy)
    
    if payer_name:
        query = query.filter(Policy.payer_name == payer_name)
    
    policies = query.offset(skip).limit(limit).all()
    
    return [
        {
            "id": str(p.id),
            "payer_name": p.payer_name,
            "section_title": p.section_title,
            "section_text": p.section_text[:200] + "..." if len(p.section_text) > 200 else p.section_text,
            "has_embedding": p.embedding is not None,
            "metadata": p.metadata
        }
        for p in policies
    ]


@router.post("/generate-embeddings")
async def generate_embeddings(
    db: Session = Depends(get_db)
):
    """
    Generate embeddings for all policies that don't have them.
    
    This is a maintenance endpoint for populating the vector database.
    """
    embeddings_model = OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        openai_api_key=settings.OPENAI_API_KEY
    )
    
    # Find policies without embeddings
    policies_without_embeddings = db.query(Policy).filter(Policy.embedding == None).all()
    
    if not policies_without_embeddings:
        return {"message": "All policies already have embeddings"}
    
    logger.info("generating_embeddings", count=len(policies_without_embeddings))
    
    for policy in policies_without_embeddings:
        try:
            # Generate embedding
            embedding = await embeddings_model.aembed_query(policy.section_text)
            
            # Update policy
            policy.embedding = embedding
            
        except Exception as e:
            logger.error("embedding_generation_failed", policy_id=str(policy.id), error=str(e))
    
    db.commit()
    
    return {
        "message": f"Generated embeddings for {len(policies_without_embeddings)} policies"
    }


@router.get("/payers")
async def list_payers(db: Session = Depends(get_db)):
    """Get list of unique payer names in the database."""
    from sqlalchemy import distinct
    
    payers = db.query(distinct(Policy.payer_name)).all()
    
    return {
        "payers": [p[0] for p in payers]
    }
