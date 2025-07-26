# app/db/models.py

import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    resolved_issues = relationship("Issue", back_populates="resolver")
    points = relationship("PointLog", back_populates="user")
    # --- ADD THIS RELATIONSHIP ---
    badges = relationship("UserBadge", back_populates="user")

# --- (Project, Analysis, Issue, and PointLog classes stay the same) ---
class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    repo_url = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    analyses = relationship("Analysis", back_populates="project", cascade="all, delete-orphan")

class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    score = Column(Float)
    analysis_date = Column(DateTime, default=datetime.datetime.utcnow)
    project = relationship("Project", back_populates="analyses")
    issues = relationship("Issue", back_populates="analysis", cascade="all, delete-orphan")

class Issue(Base):
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"))
    issue_type = Column(String, index=True)
    description = Column(String)
    status = Column(String, default='open', index=True)
    resolver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    analysis = relationship("Analysis", back_populates="issues")
    resolver = relationship("User", back_populates="resolved_issues")

class PointLog(Base):
    __tablename__ = "point_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    points_awarded = Column(Integer, nullable=False)
    award_date = Column(DateTime, default=datetime.datetime.utcnow)
    issue_id = Column(Integer, ForeignKey("issues.id"))
    user = relationship("User", back_populates="points")

# --- ADD THE TWO NEW TABLES BELOW ---

class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    # A unique key we can use in our code to identify badges
    badge_key = Column(String, unique=True, index=True, nullable=False) 

class UserBadge(Base):
    __tablename__ = "user_badges"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    awarded_date = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="badges")
    badge = relationship("Badge")