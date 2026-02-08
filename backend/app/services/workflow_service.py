"""
LangGraph Workflow Orchestration

Defines the agent workflow using LangGraph StateGraph.
"""

from typing import TypedDict, Optional, List, Any
from langgraph.graph import StateGraph, END
import structlog

from app.agents.intent_router import IntentRouterAgent
from app.agents.denial_classifier import DenialClassifierAgent
from app.agents.policy_retrieval import PolicyRetrievalAgent
from app.agents.appeal_drafting import AppealDraftingAgent
from app.agents.compliance_guardrail import ComplianceGuardrailAgent
from app.core.config import settings

logger = structlog.get_logger()


# =====================================================
# Workflow State Definition
# =====================================================

class WorkflowState(TypedDict):
    """
    Shared state across all agents in the workflow.
    """
    # Input
    claim_data: dict
    
    # Router
    routing_decision: Optional[str]
    validation_message: Optional[str]
    missing_fields: Optional[List[str]]
    
    # Classifier
    category: Optional[str]
    
    # Retrieval
    policy_excerpts: Optional[List[dict]]
    
    # Drafting
    draft_text: Optional[str]
    policy_citations: Optional[List[str]]
    
    # Compliance
    compliance_passed: Optional[bool]
    compliance_issues: Optional[List[str]]
    compliance_details: Optional[dict]
    
    # Retry tracking
    retry_count: int
    
    # Human approval (handled in API layer)
    approved: Optional[bool]
    user_feedback: Optional[str]
    
    # Errors
    error: Optional[str]


# =====================================================
# Agent Node Functions
# =====================================================

async def route_intent(state: WorkflowState) -> WorkflowState:
    """Execute IntentRouterAgent."""
    agent = IntentRouterAgent()
    return await agent.execute(state)


async def classify_denial(state: WorkflowState) -> WorkflowState:
    """Execute DenialClassifierAgent."""
    agent = DenialClassifierAgent()
    return await agent.execute(state)


async def retrieve_policies(state: WorkflowState) -> WorkflowState:
    """Execute PolicyRetrievalAgent."""
    agent = PolicyRetrievalAgent()
    return await agent.execute(state)


async def draft_appeal(state: WorkflowState) -> WorkflowState:
    """Execute AppealDraftingAgent."""
    agent = AppealDraftingAgent()
    return await agent.execute(state)


async def check_compliance(state: WorkflowState) -> WorkflowState:
    """Execute ComplianceGuardrailAgent."""
    agent = ComplianceGuardrailAgent()
    return await agent.execute(state)


# =====================================================
# Conditional Routing Functions
# =====================================================

def should_proceed(state: WorkflowState) -> str:
    """Router conditional: proceed or reject."""
    decision = state.get("routing_decision", "reject")
    
    if decision == "proceed":
        return "classify"
    else:
        return "end"


def is_compliant(state: WorkflowState) -> str:
    """Compliance conditional: pass or retry."""
    compliance_passed = state.get("compliance_passed", False)
    retry_count = state.get("retry_count", 0)
    
    if compliance_passed:
        return "complete"
    elif retry_count < settings.MAX_COMPLIANCE_RETRIES:
        logger.info("compliance_retry", retry_count=retry_count + 1)
        return "retry"
    else:
        logger.warning("compliance_max_retries_exceeded")
        return "escalate"


# =====================================================
# Build Workflow Graph
# =====================================================

def create_workflow() -> StateGraph:
    """
    Build the LangGraph workflow.
    
    Flow:
    1. IntentRouter → validates input
    2. DenialClassifier → categorizes denial
    3. PolicyRetrieval → finds relevant policies (RAG)
    4. AppealDrafting → generates letter
    5. ComplianceGuardrail → validates draft
    6. (Conditional retry if non-compliant)
    7. Human approval (outside workflow)
    
    Returns:
        Compiled StateGraph
    """
    workflow = StateGraph(WorkflowState)
    
    # Add nodes
    workflow.add_node("route", route_intent)
    workflow.add_node("classify", classify_denial)
    workflow.add_node("retrieve", retrieve_policies)
    workflow.add_node("draft", draft_appeal)
    workflow.add_node("compliance", check_compliance)
    
    # Add edges
    workflow.set_entry_point("route")
    
    # Router → Classifier or End
    workflow.add_conditional_edges(
        "route",
        should_proceed,
        {
            "classify": "classify",
            "end": END
        }
    )
    
    # Classifier → Retrieval
    workflow.add_edge("classify", "retrieve")
    
    # Retrieval → Drafting
    workflow.add_edge("retrieve", "draft")
    
    # Drafting → Compliance
    workflow.add_edge("draft", "compliance")
    
    # Compliance → Complete, Retry, or Escalate
    workflow.add_conditional_edges(
        "compliance",
        is_compliant,
        {
            "complete": END,
            "retry": "draft",  # Loop back to drafting
            "escalate": END
        }
    )
    
    return workflow.compile()


# =====================================================
# Workflow Execution
# =====================================================

async def execute_workflow(claim_data: dict) -> WorkflowState:
    """
    Execute the full agent workflow.
    
    Args:
        claim_data: Claim input data
        
    Returns:
        Final workflow state
    """
    # Initialize state
    initial_state: WorkflowState = {
        "claim_data": claim_data,
        "routing_decision": None,
        "validation_message": None,
        "missing_fields": None,
        "category": None,
        "policy_excerpts": None,
        "draft_text": None,
        "policy_citations": None,
        "compliance_passed": None,
        "compliance_issues": None,
        "compliance_details": None,
        "retry_count": 0,
        "approved": None,
        "user_feedback": None,
        "error": None
    }
    
    # Create and execute workflow
    workflow = create_workflow()
    
    logger.info("workflow_started", claim_id=claim_data.get("claim_id"))
    
    try:
        final_state = await workflow.ainvoke(initial_state)
        logger.info("workflow_completed", claim_id=claim_data.get("claim_id"))
        return final_state
    except Exception as e:
        logger.error("workflow_failed", error=str(e), claim_id=claim_data.get("claim_id"))
        initial_state["error"] = str(e)
        return initial_state
