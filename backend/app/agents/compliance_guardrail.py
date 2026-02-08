"""
Compliance Guardrail Agent

Validates appeal drafts for compliance, tone, and completeness.
"""

from typing import Any, Dict
import time
import json

from app.agents.base_agent import BaseAgent
from app.core.llm_factory import LLMFactory


class ComplianceGuardrailAgent(BaseAgent):
    """
    Validates appeal drafts against compliance criteria.
    
    Checks:
    - Professional tone
    - Policy citation accuracy
    - Addresses denial reason
    - Appropriate length
    - No hallucinations
    """
    
    def __init__(self):
        super().__init__()
        
        # Use LLM factory
        self.llm = LLMFactory.get_guardrail_llm()
        
        # Compliance check prompt
        self.system_prompt = """You are a compliance officer reviewing appeal letters.

Evaluate the appeal draft against these criteria:

1. TONE: Is the letter professional, respectful, and non-accusatory?
2. CITATIONS: Does it reference only the provided policy excerpts (no fabrications)?
3. ADDRESSES_DENIAL: Does it directly address the denial reason?
4. LENGTH: Is it between 200-500 words?

Respond ONLY with valid JSON:
{
  "tone_compliant": true/false,
  "citations_valid": true/false,
  "addresses_denial": true/false,
  "length_appropriate": true/false,
  "issues": ["list of specific issues found, or empty array"]
}"""
    
    def get_name(self) -> str:
        return "ComplianceGuardrailAgent"
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate appeal draft.
        
        Args:
            state: Contains 'draft_text', 'policy_excerpts', 'claim_data'
            
        Returns:
            state with 'compliance_passed' and 'compliance_issues' added
        """
        draft_text = state.get("draft_text", "")
        policy_excerpts = state.get("policy_excerpts", [])
        claim_data = state.get("claim_data", {})
        
        start_time = time.time()
        
        try:
            # Format policy excerpts
            formatted_excerpts = "\n".join([
                f"- {e['section_title']}" 
                for e in policy_excerpts
            ])
            
            # Prepare prompt
            user_prompt = f"""Review this appeal draft:

DRAFT:
{draft_text}

PROVIDED POLICY EXCERPTS:
{formatted_excerpts or "None provided"}

DENIAL REASON:
{claim_data.get("denial_description")}

Compliance evaluation (JSON only):"""
            
            # Call LLM
            response = await self.llm.agenerate(
                prompt=user_prompt,
                system_prompt=self.system_prompt
            )
            
            # Parse JSON response
            try:
                compliance_result = json.loads(response.strip())
            except json.JSONDecodeError:
                # Fallback: treat as non-compliant if can't parse
                self.logger.warning("failed_to_parse_compliance_json")
                compliance_result = {
                    "tone_compliant": False,
                    "citations_valid": False,
                    "addresses_denial": False,
                    "length_appropriate": False,
                    "issues": ["Failed to parse compliance evaluation"]
                }
            
            # Determine if passed
            compliance_passed = all([
                compliance_result.get("tone_compliant", False),
                compliance_result.get("citations_valid", False),
                compliance_result.get("addresses_denial", False),
                compliance_result.get("length_appropriate", False)
            ])
            
            issues = compliance_result.get("issues", [])
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            self.logger.info(
                "compliance_check_complete",
                passed=compliance_passed,
                issues_count=len(issues),
                latency_ms=latency_ms,
                provider=self.llm.get_provider_name()
            )
            
            # Update state
            state["compliance_passed"] = compliance_passed
            state["compliance_issues"] = issues
            state["compliance_details"] = compliance_result
            
            # Log execution
            await self.log_execution(
                input_data={"draft_length": len(draft_text)},
                output_data={
                    "passed": compliance_passed,
                    "issues": issues
                },
                metadata={
                    "latency_ms": latency_ms,
                    "provider": self.llm.get_provider_name(),
                    "model": self.llm.model
                }
            )
            
        except Exception as e:
            self.logger.error("compliance_check_failed", error=str(e))
            state["compliance_passed"] = False
            state["compliance_issues"] = [f"Compliance check failed: {str(e)}"]
            state["error"] = f"Compliance check error: {str(e)}"
        
        return state
