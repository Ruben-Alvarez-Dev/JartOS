import os
import uuid
import json
from datetime import datetime
from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
import uvicorn

# Configuration and Paths
TIER_AGENTS = "TIER-03-AGENTS"
PROMPT_PATH = "TIER-00-FOUNDATION/configs/prompts_maestros/maestro.prompt"

# Initialize FastAPI app
app = FastAPI(
    title="JartOS Maestro Orchestrator",
    description="The central brain of the JartOS Hierarchical Agent System.",
    version="1.0.0"
)

# Models (Derived from OpenSpec components/schemas)
class TaskRequest(BaseModel):
    goal: str = Field(..., example="Generar la Unidad Didactica para el RA1.")
    context: Optional[Dict] = None
    priority: str = Field(default="medium", pattern="^(low|medium|high|critical)$")

class TaskResponse(BaseModel):
    task_id: str
    status: str
    plan: List[str]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class Agent(BaseModel):
    id: str
    name: str
    role: str
    status: str

class ValidationRequest(BaseModel):
    content: str
    type: str
    metadata: Optional[Dict] = None

class ValidationResponse(BaseModel):
    approved: bool
    votes: Dict[str, str]
    feedback: Optional[str] = None

# Mock In-Memory Store (To be replaced by TIER-06 Storage)
tasks_db = {}

# Import Specialists and Concilio
from TIER_03_AGENTS.specialists import RedactorDidactico, InvestigadorNormativo, CoachOral, GestorVida
from TIER_03_AGENTS.concilio import Concilio

specialists = {
    "A-01": RedactorDidactico(),
    "A-02": InvestigadorNormativo(),
    "A-03": CoachOral(),
    "A-04": GestorVida()
}
concilio = Concilio()

@app.get("/")
async def root():
    return {"message": "JartOS Maestro Orchestrator is operational."}

@app.post("/api/v1/orchestrator/task", response_model=TaskResponse, status_code=202)
async def submit_task(request: TaskRequest):
    """
    OpenSpec Endpoint: Submit a task to the Maestro.
    The Maestro will decompose the task and plan execution.
    """
    task_id = str(uuid.uuid4())
    
    # 1. Planning (Mocked)
    plan = [
        f"Analizar meta: {request.goal}",
        "Consultar Golden RAG",
        "Delegar a especialistas",
        "Validar con el Concilio"
    ]
    
    # 2. Execution (Async in background in real system)
    # For this mock, we'll just log the intended flow
    
    tasks_db[task_id] = {
        "goal": request.goal,
        "priority": request.priority,
        "status": "processing",
        "plan": plan,
        "created_at": datetime.now().isoformat()
    }
    
    return TaskResponse(
        task_id=task_id,
        status="processing",
        plan=plan
    )

@app.get("/api/v1/agents/specialists", response_model=List[Agent])
async def list_specialists():
    """
    OpenSpec Endpoint: List all active specialist agents.
    """
    return [
        {"id": s.agent_id, "name": s.name, "role": s.role, "status": s.status}
        for s in specialists.values()
    ]

@app.post("/api/v1/concilio/validate", response_model=ValidationResponse)
async def validate_content(request: ValidationRequest):
    """
    OpenSpec Endpoint: Quality Control validation.
    """
    # Mocking Concilio voting logic
    votes = {
        "juridico": "apto",
        "pedagogico": "apto",
        "tecnico": "apto"
    }
    
    return ValidationResponse(
        approved=True,
        votes=votes,
        feedback="Contenido verificado satisfactoriamente."
    )

@app.get("/api/v1/knowledge/golden-rag")
async def query_golden_rag(q: str, domain: Optional[str] = None):
    """
    OpenSpec Endpoint: Search in verified knowledge base.
    """
    return {
        "results": [
            {
                "content": f"Informacion verificada sobre {q}",
                "source": "BOE-A-2014-11000",
                "score": 0.95
            }
        ]
    }

if __name__ == "__main__":
    # In JartOS architecture, this would typically run on port 18789
    uvicorn.run(app, host="0.0.0.0", port=18789)
