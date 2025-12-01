from fastapi import FastAPI
from pydantic import BaseModel
from finance_agent import PersonalFinanceAgentSystem
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Initialize multi-agent system
orchestrator = PersonalFinanceAgentSystem()

# Request model
class ExpenseInput(BaseModel):
    text: str

@app.post("/process_expense")
def process_expense(data: ExpenseInput):
    """
    Send expense text to multi-agent pipeline:
    Parser → Classifier → Analyzer
    """
    result = orchestrator.process_expense(data.text)
    summary = orchestrator.get_summary()
    return {
        "result": result,
        "summary": summary
    }

@app.get("/")
def root():
    return {"message": "Finance Agent API is running!"}
