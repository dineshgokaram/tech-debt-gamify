# app/api/endpoints.py

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import func, desc
from sqlalchemy.orm import Session, selectinload
from typing import List
from services import reporting_service

from models import schemas
from services import analysis_service, gamification_service
from db.database import get_db
from db import models
from services import security_service

router = APIRouter()

@router.post("/analyze", response_model=schemas.AnalyzeResponse)
def analyze_repo_endpoint(request: schemas.AnalyzeRequest, db: Session = Depends(get_db), current_user: models.User = Depends(security_service.get_current_user)):
    return analysis_service.run_and_save_analysis(db=db, repo_url=request.repo_url)

@router.get("/projects", response_model=List[schemas.ProjectSimple])
def get_all_projects(db: Session = Depends(get_db), current_user: models.User = Depends(security_service.get_current_user)):
    projects = db.query(models.Project).all()
    return projects

@router.get("/projects/{project_id}", response_model=schemas.Project)
def get_project_details(project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(security_service.get_current_user)):
    project = (
        db.query(models.Project)
        .options(selectinload(models.Project.analyses).selectinload(models.Analysis.issues))
        .filter(models.Project.id == project_id).first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("/issues/{issue_id}/resolve", status_code=status.HTTP_200_OK)
def resolve_issue(issue_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(security_service.get_current_user)):
    issue_to_resolve = db.query(models.Issue).filter(models.Issue.id == issue_id).first()
    if not issue_to_resolve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
    if issue_to_resolve.status == 'resolved':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Issue is already resolved")
    issue_to_resolve.status = 'resolved'
    issue_to_resolve.resolver_id = current_user.id
    points_awarded = gamification_service.award_points_for_issue(db=db, issue=issue_to_resolve, user=current_user)
    db.commit()
    return {"message": f"Issue {issue_id} resolved! You earned {points_awarded} points."}

@router.get("/leaderboard", response_model=List[schemas.LeaderboardUser])
def get_leaderboard(db: Session = Depends(get_db), current_user: models.User = Depends(security_service.get_current_user)):
    leaderboard_data = (
        db.query(models.User.id, models.User.username, func.sum(models.PointLog.points_awarded).label("total_points"))
        .join(models.PointLog, models.User.id == models.PointLog.user_id)
        .group_by(models.User.id).order_by(desc("total_points")).all()
    )
    return leaderboard_data

@router.get("/users/me/badges", response_model=List[schemas.UserBadge])
def get_my_badges(current_user: models.User = Depends(security_service.get_current_user), db: Session = Depends(get_db)):
    user_badges = db.query(models.UserBadge).options(selectinload(models.UserBadge.badge)).filter(models.UserBadge.user_id == current_user.id).all()
    return user_badges

@router.get("/projects/{project_id}/report", response_model=schemas.ProjectReport)
def get_project_report(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security_service.get_current_user),
):
    """
    Generates and retrieves a comprehensive report for a single project,
    aggregating all historical analysis data.
    """
    report = reporting_service.generate_project_report(db=db, project_id=project_id)
    if not report:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return report