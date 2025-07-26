# app/services/reporting_service.py

import pandas as pd
from sqlalchemy.orm import Session
from db import models

def generate_project_report(db: Session, project_id: int):
    """
    Queries all historical data for a project and generates an aggregated report
    using the pandas library.
    """
    # First, get the project to ensure it exists
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        return None # The endpoint will handle the 404 error

    # Construct a query to get all issues and their parent analysis data
    query = (
        db.query(
            models.Issue.id,
            models.Issue.issue_type,
            models.Issue.status,
            models.Analysis.analysis_date,
            models.Analysis.score
        )
        .join(models.Analysis, models.Issue.analysis_id == models.Analysis.id)
        .filter(models.Analysis.project_id == project_id)
    )

    # Use pandas to execute the SQL query and load the results into a DataFrame
    df = pd.read_sql(query.statement, db.bind)

    if df.empty:
        # Handle case where a project exists but has no analyses/issues yet
        return {
            "project_id": project.id,
            "project_name": project.name,
            "total_analyses": 0,
            "total_open_issues": 0,
            "score_over_time": [],
            "issues_by_type": [],
            "issues_by_status": [],
        }

    # --- Perform Data Aggregations using Pandas ---

    # 1. Time-series data for score over time
    score_df = df[['analysis_date', 'score']].drop_duplicates().sort_values(by='analysis_date')
    score_over_time = [
        {"date": row.analysis_date, "score": row.score} for _, row in score_df.iterrows()
    ]

    # 2. Count of issues by type (Pylint, Flake8, etc.)
    type_counts = df['issue_type'].value_counts().reset_index()
    type_counts.columns = ['category', 'value']
    issues_by_type = type_counts.to_dict(orient='records')
    
    # 3. Count of issues by status (open, resolved)
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['category', 'value']
    issues_by_status = status_counts.to_dict(orient='records')

    # 4. Overall statistics
    total_analyses = df['analysis_date'].nunique()
    total_open_issues = len(df[df['status'] == 'open'])

    # --- Assemble the final report dictionary ---
    report = {
        "project_id": project.id,
        "project_name": project.name,
        "total_analyses": total_analyses,
        "total_open_issues": total_open_issues,
        "score_over_time": score_over_time,
        "issues_by_type": issues_by_type,
        "issues_by_status": issues_by_status,
    }

    return report