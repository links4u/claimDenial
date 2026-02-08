"""
Base Agent Interface

Defines the common interface for all agents in the system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from datetime import datetime
import structlog

logger = structlog.get_logger()


class BaseAgent(ABC):
    """
    Base class for all agents in ClaimPilot™.
    
    Each agent must implement:
    - execute(): Main logic
    - get_name(): Agent identifier
    """
    
    def __init__(self):
        self.logger = logger.bind(agent=self.get_name())
    
    @abstractmethod
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's logic.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state dictionary
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the agent's name for logging and auditing."""
        pass
    
    async def log_execution(
        self, 
        input_data: Dict[str, Any], 
        output_data: Dict[str, Any],
        metadata: Dict[str, Any] = None
    ) -> None:
        """
        Log agent execution for audit trail.
        
        Args:
            input_data: Input to the agent
            output_data: Output from the agent
            metadata: Additional metadata (latency, token count, etc.)
        """
        self.logger.info(
            "agent_execution",
            agent=self.get_name(),
            input=input_data,
            output=output_data,
            metadata=metadata or {},
            timestamp=datetime.utcnow().isoformat()
        )
