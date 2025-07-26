# app/models/analysis.py

from pydantic import BaseModel
from typing import List
import datetime

# This class should be defined first, as it's used by the Analysis class
class Issue(BaseModel):
    id: int
    issue_type: str
    description: str

    class Config:
        from_attributes = True

class Analysis(BaseModel):
    id: int
    score: float
    analysis_date: datetime.datetime
    # --- THIS IS THE MISSING LINE THAT FIXES THE RESPONSE ---
    issues: List[Issue] = []

    class Config:
        from_attributes = True

class Project(BaseModel):
    id: int
    name: str
    repo_url: str
    # This now works because the Analysis model above has an 'issues' field
    analyses: List[Analysis] = []

    class Config:
        from_attributes = True

class ProjectSimple(BaseModel):
    id: int
    name: str
    repo_url: str

    class Config:
        from_attributes = True

# --- We no longer need these original models, but keeping them won't hurt ---
class AnalyzeRequest(BaseModel):
    repo_url: str

class AnalyzeResponse(BaseModel):
    score: float
    issues: List[str]