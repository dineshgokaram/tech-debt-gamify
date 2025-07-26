# app/services/analysis_service.py

import os
import json
import shutil
import tempfile
import subprocess
import re
from git import Repo, GitCommandError
from sqlalchemy.orm import Session

# Import our database models using the correct relative path
from db import models

def _get_or_create_project(db: Session, repo_url: str) -> models.Project:
    """
    Retrieves a project by its URL or creates it if it doesn't exist.
    """
    project = db.query(models.Project).filter(models.Project.repo_url == repo_url).first()
    if not project:
        # Extract a project name from the URL, e.g., "https://github.com/psf/requests-html" -> "requests-html"
        project_name = repo_url.split('/')[-1].replace('.git', '')
        project = models.Project(name=project_name, repo_url=repo_url)
        db.add(project)
        db.commit()
        db.refresh(project)
    return project

def _get_python_files(path: str) -> list[str]:
    """Walks a directory and returns a list of all .py files."""
    python_files = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files

def _clean_issue_path(issue_description: str, temp_dir: str) -> str:
    """
    Replaces the temporary absolute path with a clean, relative path.
    """
    normalized_temp_dir = os.path.normpath(temp_dir)
    return re.sub(f'^{re.escape(normalized_temp_dir + os.sep)}', '', issue_description)

def run_and_save_analysis(db: Session, repo_url: str):
    """
    The main service function. Clones a repo, runs analysis,
    and saves all results to the database.
    """
    project = _get_or_create_project(db, repo_url)
    temp_dir = tempfile.mkdtemp()
    
    try:
        Repo.clone_from(repo_url, temp_dir, depth=1)
        python_files = _get_python_files(temp_dir)
        if not python_files:
            raise Exception("No Python files were found in the repository.")

        # --- Run Linters ---
        pylint_cmd = ["pylint", "--output-format=json", *python_files]
        pylint_proc = subprocess.run(pylint_cmd, capture_output=True, text=True)
        pylint_data = json.loads(pylint_proc.stdout) if pylint_proc.stdout.strip() else []

        flake8_cmd = ["flake8", *python_files]
        flake8_proc = subprocess.run(flake8_cmd, capture_output=True, text=True)
        flake8_issues_raw = flake8_proc.stdout.strip().splitlines()

        # --- Calculate Score ---
        score = 100.0 - (len(pylint_data) * 1.0) - (len(flake8_issues_raw) * 0.5)
        score = max(0, score)
        
        # --- SAVE TO DATABASE ---
        # 1. Create the parent Analysis record
        new_analysis = models.Analysis(project_id=project.id, score=score)
        db.add(new_analysis)
        db.flush() # Use flush to get the ID of new_analysis before committing

        # 2. Create the child Issue records
        all_issues_for_response = []
        for item in pylint_data:
            desc = _clean_issue_path(f"{item['path']}:{item['line']}: {item['message']}", temp_dir)
            issue = models.Issue(analysis_id=new_analysis.id, issue_type=f"Pylint ({item['symbol']})", description=desc)
            db.add(issue)
            all_issues_for_response.append(issue.description)
            
        for item in flake8_issues_raw:
            desc = _clean_issue_path(item, temp_dir)
            issue = models.Issue(analysis_id=new_analysis.id, issue_type="Flake8", description=desc)
            db.add(issue)
            all_issues_for_response.append(issue.description)

        # 3. Commit all changes to the database
        db.commit()
        
        # Return the results in the format expected by the Pydantic response model
        return {"score": new_analysis.score, "issues": all_issues_for_response}

    except (GitCommandError, Exception) as e:
        db.rollback()
        raise e
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)