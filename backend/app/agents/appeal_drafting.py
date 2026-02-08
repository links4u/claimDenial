"""
Appeal Drafting Agent

Generates professional appeal letters using Claude Sonnet.
"""

from typing import Any, Dict
import time

from app.agents.base_agent import BaseAgent
from app.core.llm_factory import LLMFactory


class AppealDraftingAgent(BaseAgent):
    """
    Drafts formal appeal letters with policy citations.
    
    Uses retrieved policy excerpts to construct evidence-based appeals.
    """
    
    def __init__(self):
        super().__init__()
        
        # Use LLM factory
        self.llm = LLMFactory.get_drafter_llm()
        
        # Appeal drafting prompt
        self.system_prompt = """You are a medical billing specialist drafting formal appeal letters.

Your appeals must:
1. Reference specific policy sections provided
2. Explain why the denial should be overturned
3. Maintain professional, respectful tone
4. Be concise (200-500 words)
5. Use formal business letter format
6. NOT make assumptions beyond provided data
7. NOT fabricate policy quotes

Structure:
- Greeting to Appeals Committee
- Reference to claim and denial code
- Explanation citing provided policies
- Request for reconsideration
- Professional closing"""
    
    def get_name(self) -> str:
        return "AppealDraftingAgent"
    
    def format_policy_excerpts(self, excerpts: list) -> str:
        """Format policy excerpts for prompt."""
        if not excerpts:
            return "No specific policy excerpts available for this payer."
        
        formatted = []
        for i, excerpt in enumerate(excerpts, 1):
            formatted.append(
                f"{i}. {excerpt['section_title']}\n"
                f"   \"{excerpt['section_text']}\"\n"
                f"   (Relevance: {excerpt['similarity_score']:.2f})"
            )
        
        return "\n\n".join(formatted)
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate appeal draft.
        
        Args:
            state: Contains 'claim_data', 'category', 'policy_excerpts'
            
        Returns:
            state with 'draft_text' and 'policy_citations' added
        """
        claim_data = state.get("claim_data", {})
        category = state.get("category", "Other")
        policy_excerpts = state.get("policy_excerpts", [])
        
        start_time = time.time()
        
        try:
            # Format policy excerpts
            formatted_excerpts = self.format_policy_excerpts(policy_excerpts)
            
            # Prepare prompt
            user_prompt = f"""Draft an appeal letter for this denied claim:

Claim ID: {claim_data.get("claim_id")}
Payer: {claim_data.get("payer_name")}
Denial Code: {claim_data.get("denial_code")}
Denial Reason: {claim_data.get("denial_description")}
Classification Category: {category}

Relevant Policy Excerpts:
{formatted_excerpts}

Draft the appeal letter:"""
            
            # Call LLM
            draft_text = await self.llm.agenerate(
                prompt=user_prompt,
                system_prompt=self.system_prompt
            )
            
            draft_text = draft_text.strip()
            
            # Extract policy citations (section titles)
            policy_citations = [
                excerpt["section_title"] 
                for excerpt in policy_excerpts
            ]
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            self.logger.info(
                "drafting_complete",
                draft_length=len(draft_text),
                citations_count=len(policy_citations),
                latency_ms=latency_ms,
                provider=self.llm.get_provider_name()
            )
            
            # Update state
            state["draft_text"] = draft_text
            state["policy_citations"] = policy_citations
            
            # Log execution
            await self.log_execution(
                input_data={
                    "claim_id": claim_data.get("claim_id"),
                    "category": category,
                    "num_policies": len(policy_excerpts)
                },
                output_data={
                    "draft_length": len(draft_text),
                    "citations": len(policy_citations)
                },
                metadata={
                    "latency_ms": latency_ms, 
                    "provider": self.llm.get_provider_name(),
                    "model": self.llm.model
                }
            )
            
        except Exception as e:
            self.logger.error("drafting_failed", error=str(e))
            state["draft_text"] = ""
            state["policy_citations"] = []
            state["error"] = f"Appeal drafting failed: {str(e)}"
        
        return state
