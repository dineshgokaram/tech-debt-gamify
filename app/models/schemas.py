# app/models/schemas.py

from pydantic import BaseModel
from typing import List
import datetime

# --- User and Token Schemas ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class Badge(BaseModel):
    name: str
    description: str
    class Config:
        from_attributes = True

class UserBadge(BaseModel):
    awarded_date: datetime.datetime
    badge: Badge
    class Config:
        from_attributes = True

class LeaderboardUser(BaseModel):
    id: int
    username: str
    total_points: int
    class Config:
        from_attributes = True

# --- Analysis and Project Schemas ---
class AnalyzeRequest(BaseModel):
    repo_url: str

class AnalyzeResponse(BaseModel):
    score: float
    issues: List[str]

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
    issues: List[Issue] = []
    class Config:
        from_attributes = True

class Project(BaseModel):
    id: int
    name: str
    repo_url: str
    analyses: List[Analysis] = []
    class Config:
        from_attributes = True

class ProjectSimple(BaseModel):
    id: int
    name: str
    repo_url: str
    class Config:
        from_attributes = True

# --- Reporting Schemas ---
class ReportTimeSeriesItem(BaseModel):
    date: datetime.datetime
    score: float

class ReportCategoryItem(BaseModel):
    category: str
    value: int

class ProjectReport(BaseModel):
    project_id: int
    project_name: str
    total_analyses: int
    total_open_issues: int
    score_over_time: List[ReportTimeSeriesItem]
    issues_by_type: List[ReportCategoryItem]
    issues_by_status: List[ReportCategoryItem]