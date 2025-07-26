# app/services/gamification_service.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from db import models

def _check_and_award_badges(db: Session, user: models.User):
    """
    Checks all badge conditions for a user and awards any new badges.
    This version directly queries the database for counts, which is more reliable.
    """
    
    # Get the user's current badge keys so we don't award duplicates
    current_badge_keys = {ub.badge.badge_key for ub in user.badges}

    # --- Rule for "First Fix" Badge ---
    # Count total resolved issues for the user
    total_fixes = db.query(func.count(models.Issue.id)).filter(models.Issue.resolver_id == user.id).scalar()

    if total_fixes >= 1 and 'FIRST_FIX' not in current_badge_keys:
        badge = db.query(models.Badge).filter(models.Badge.badge_key == 'FIRST_FIX').first()
        if badge:
            user_badge = models.UserBadge(user_id=user.id, badge_id=badge.id)
            db.add(user_badge)

    # --- Rule for "Bug Squasher" Badge (10 fixes) ---
    if total_fixes >= 10 and 'TEN_FIXES' not in current_badge_keys:
        badge = db.query(models.Badge).filter(models.Badge.badge_key == 'TEN_FIXES').first()
        if badge:
            user_badge = models.UserBadge(user_id=user.id, badge_id=badge.id)
            db.add(user_badge)

    # --- Rule for "Code Cleaner" Badge (5 Pylint fixes) ---
    pylint_fixes = db.query(func.count(models.Issue.id)).filter(
        models.Issue.resolver_id == user.id,
        models.Issue.issue_type.like('%Pylint%')
    ).scalar()

    if pylint_fixes >= 5 and 'FIVE_PYLINT_FIXES' not in current_badge_keys:
        badge = db.query(models.Badge).filter(models.Badge.badge_key == 'FIVE_PYLINT_FIXES').first()
        if badge:
            user_badge = models.UserBadge(user_id=user.id, badge_id=badge.id)
            db.add(user_badge)

def award_points_for_issue(db: Session, issue: models.Issue, user: models.User) -> int:
    """
    Awards points to a user for resolving an issue and logs the event.
    Also checks if the user has earned any new badges.
    """
    points_to_award = 0

    if "Pylint (line-too-long)" in issue.issue_type:
        points_to_award = 1
    elif "Pylint" in issue.issue_type:
        points_to_award = 5
    elif "Flake8" in issue.issue_type:
        points_to_award = 3
    else:
        points_to_award = 1

    if points_to_award > 0:
        point_log_entry = models.PointLog(
            user_id=user.id,
            points_awarded=points_to_award,
            issue_id=issue.id
        )
        db.add(point_log_entry)
    
    # After resolving an issue, check for new badges
    _check_and_award_badges(db, user)
    
    return points_to_award