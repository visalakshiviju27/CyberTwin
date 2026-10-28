from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal
from app.services.analysis_engine import analyze

app = FastAPI(title="CyberTwin Safety API", version="1.0.0",
              description="Defensive educational cyber-safety API. Submitted URLs are treated as text and never fetched.")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
                   allow_credentials=False, allow_methods=["GET", "POST", "PUT", "DELETE"], allow_headers=["*"])

class AnalyzeRequest(BaseModel):
    category: Literal["Not sure", "Online scam / phishing", "Fake account / impersonation",
                      "Cyberbullying / harassment", "Account compromise"] = "Not sure"
    text: str = Field(min_length=8, max_length=5000)
    sender: str = Field(default="", max_length=300)
    url: str = Field(default="", max_length=1000)

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "CyberTwin", "analysis_mode": "explainable-rule-based",
            "external_ai": False, "url_fetching": False}

@app.post("/api/analyze")
def analyze_query(request: AnalyzeRequest):
    return analyze(request.category, request.text, request.sender, request.url)

@app.get("/api/progress")
def progress_info():
    return {"storage": "browser-localStorage in frontend", "external_ai": False,
            "note": "This API does not persist browser incidents. No official report is submitted."}
