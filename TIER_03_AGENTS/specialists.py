from typing import Dict, List, Optional
from pydantic import BaseModel

class SpecialistAgent:
    """
    Base class for specialist agents in JartOS.
    """
    def __init__(self, agent_id: str, name: str, role: str):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.status = "idle"

    async def execute_task(self, task_description: str, context: Optional[Dict] = None) -> Dict:
        """
        Executes a specific task assigned by the Maestro.
        """
        self.status = "busy"
        # In a real implementation, this would call an LLM with a specific specialist prompt.
        result = {
            "agent_id": self.agent_id,
            "role": self.role,
            "status": "completed",
            "output": f"Resultado de la tarea: {task_description}",
            "metadata": {"source": "specialist_mock"}
        }
        self.status = "idle"
        return result

class RedactorDidactico(SpecialistAgent):
    def __init__(self):
        super().__init__("A-01", "Redactor Didactico", "DIDACTIC_WRITER")

class InvestigadorNormativo(SpecialistAgent):
    def __init__(self):
        super().__init__("A-02", "Investigador Normativo", "REGULATORY_RESEARCHER")

class CoachOral(SpecialistAgent):
    def __init__(self):
        super().__init__("A-03", "Coach Oral", "ORAL_COACH")

class GestorVida(SpecialistAgent):
    def __init__(self):
        super().__init__("A-04", "Gestor de Vida", "LIFE_MANAGER")
