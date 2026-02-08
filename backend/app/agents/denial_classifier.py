"""
Denial Classifier Agent

Classifies denial into predefined categories using Claude Sonnet.
"""

from typing import Any, Dict
import time

from app.agents.base_agent import BaseAgent
from app.core.llm_factory import LLMFactory


class DenialClassifierAgent(BaseAgent):
    """
    Classifies claim denial into one of five categories.
    
    Categories:
    - Coverage
    - Medical Necessity
    - Coding
    - Authorization
    - Other
    """
    
    def __init__(self):
        super().__init__()
        
        # Use LLM factory to get provider-agnostic LLM
        self.llm = LLMFactory.get_classifier_llm()
        
        # Classification prompt
        self.system_prompt = """You are a healthcare claims classification expert. 
Your task is to classify claim denials into exactly ONE category.

Categories:
1. Coverage - Service not covered by policy
2. Medical Necessity - Procedure deemed not medically necessary
3. Coding - Incorrect CPT/ICD codes or billing errors
4. Authorization - Missing prior authorization or pre-certification
5. Other - Unusual cases that don't fit above categories

Respond with ONLY the category name. No explanation or additional text."""
    
    def get_name(self) -> str:
        return "DenialClassifierAgent"
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify the denial.
        
        Args:
            state: Contains 'claim_data'
            
        Returns:
            state with 'category' added
        """
        claim_data = state.get("claim_data", {})
        
        start_time = time.time()
        
        try:
            # Prepare prompt
            user_prompt = f"""Denial Code: {claim_data.get("denial_code")}
Denial Description: {claim_data.get("denial_description")}
Payer: {claim_data.get("payer_name")}

Category:"""
            
            # Call LLM
            response = await self.llm.agenerate(
                prompt=user_prompt,
                system_prompt=self.system_prompt
            )
            
            category = response.strip()
            
            # Normalize category (in case LLM adds extra text)
            valid_categories = ["Coverage", "Medical Necessity", "Coding", "Authorization", "Other"]
            
            # Find matching category
            matched_category = next(
                (cat for cat in valid_categories if cat.lower() in category.lower()),
                "Other"
            )
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            self.logger.info(
                "classification_complete",
                category=matched_category,
                latency_ms=latency_ms,
                provider=self.llm.get_provider_name()
            )
            
            # Update state
            state["category"] = matched_category
            
            # Log execution
            await self.log_execution(
                input_data={
                    "denial_code": claim_data.get("denial_code"),
                    "denial_description": claim_data.get("denial_description")[:100]
                },
                output_data={"category": matched_category},
                metadata={
                    "latency_ms": latency_ms, 
                    "provider": self.llm.get_provider_name(),
                    "model": self.llm.model
                }
            )
            
        except Exception as e:
            self.logger.error("classification_failed", error=str(e))
            state["category"] = "Other"
            state["error"] = f"Classification failed: {str(e)}"
        
        return state
