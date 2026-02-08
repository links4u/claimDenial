"""
Intent Router Agent

Validates input data completeness and determines workflow routing.
This is a deterministic agent (no LLM calls).
"""

from typing import Any, Dict
from app.agents.base_agent import BaseAgent


class IntentRouterAgent(BaseAgent):
    """
    Validates claim input and routes to appropriate workflow.
    
    Responsibilities:
    - Check if all required fields are present
    - Validate data quality
    - Route to classification or error handling
    """
    
    def get_name(self) -> str:
        return "IntentRouterAgent"
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate input and determine routing.
        
        Args:
            state: Contains 'claim_data' with input fields
            
        Returns:
            state with 'routing_decision' added
        """
        claim_data = state.get("claim_data", {})
        
        # Required fields
        required_fields = [
            "claim_id",
            "denial_code",
            "denial_description",
            "payer_name"
        ]
        
        missing_fields = [
            field for field in required_fields 
            if not claim_data.get(field)
        ]
        
        if missing_fields:
            routing_decision = "reject"
            message = f"Missing required fields: {', '.join(missing_fields)}"
            self.logger.warning("incomplete_input", missing=missing_fields)
        else:
            routing_decision = "proceed"
            message = "Input validation passed"
            self.logger.info("validation_passed")
        
        # Update state
        state["routing_decision"] = routing_decision
        state["validation_message"] = message
        state["missing_fields"] = missing_fields if missing_fields else []
        
        # Log execution
        await self.log_execution(
            input_data={"claim_id": claim_data.get("claim_id")},
            output_data={
                "decision": routing_decision,
                "message": message
            }
        )
        
        return state
