"""
Policy Retrieval Agent

Performs semantic search over policy documents using pgvector RAG.
"""

from typing import Any, Dict, List
import time
from sqlalchemy import text
from langchain_openai import OpenAIEmbeddings

from app.agents.base_agent import BaseAgent
from app.core.config import settings
from app.db.session import SessionLocal


class PolicyRetrievalAgent(BaseAgent):
    """
    Retrieves relevant policy excerpts using RAG (Retrieval-Augmented Generation).
    
    Uses pgvector for semantic similarity search.
    """
    
    def __init__(self):
        super().__init__()
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
    
    def get_name(self) -> str:
        return "PolicyRetrievalAgent"
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve relevant policy excerpts.
        
        Args:
            state: Contains 'claim_data' and 'category'
            
        Returns:
            state with 'policy_excerpts' added
        """
        claim_data = state.get("claim_data", {})
        payer_name = claim_data.get("payer_name")
        denial_description = claim_data.get("denial_description")
        
        start_time = time.time()
        
        try:
            # Generate query embedding
            query_embedding = await self.embeddings.aembed_query(denial_description)
            
            # Convert to PostgreSQL array format
            embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"
            
            # Perform vector similarity search
            db = SessionLocal()
            
            query = text("""
                SELECT 
                    id,
                    section_title,
                    section_text,
                    payer_name,
                    1 - (embedding <=> :embedding::vector) AS similarity
                FROM policies
                WHERE payer_name = :payer_name
                ORDER BY embedding <=> :embedding::vector
                LIMIT :top_k
            """)
            
            result = db.execute(
                query,
                {
                    "embedding": embedding_str,
                    "payer_name": payer_name,
                    "top_k": settings.RAG_TOP_K
                }
            )
            
            policy_excerpts = []
            for row in result:
                policy_excerpts.append({
                    "id": str(row.id),
                    "section_title": row.section_title,
                    "section_text": row.section_text,
                    "payer_name": row.payer_name,
                    "similarity_score": float(row.similarity)
                })
            
            db.close()
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            self.logger.info(
                "retrieval_complete",
                num_excerpts=len(policy_excerpts),
                latency_ms=latency_ms
            )
            
            # Update state
            state["policy_excerpts"] = policy_excerpts
            
            # Log execution
            await self.log_execution(
                input_data={
                    "payer_name": payer_name,
                    "query_length": len(denial_description)
                },
                output_data={
                    "num_excerpts": len(policy_excerpts),
                    "top_similarity": policy_excerpts[0]["similarity_score"] if policy_excerpts else 0
                },
                metadata={"latency_ms": latency_ms, "top_k": settings.RAG_TOP_K}
            )
            
        except Exception as e:
            self.logger.error("retrieval_failed", error=str(e))
            state["policy_excerpts"] = []
            state["error"] = f"Policy retrieval failed: {str(e)}"
        
        return state
