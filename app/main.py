# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

# Correct, relative imports
from api import endpoints, auth_endpoints
from db import database, models, seed

# --- The Lifespan Event Handler ---
# This is the recommended way to run startup/shutdown logic.
# It's cleaner and safer than running code at the module level.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Code to run on application startup ---
    print("Application startup: Creating database tables...")
    # This creates all tables based on your db.models
    models.Base.metadata.create_all(bind=database.engine)
    
    print("Application startup: Seeding badges...")
    # Use a context manager for the session to ensure it's closed
    with database.SessionLocal() as db_session:
        seed.seed_badges(db_session)
    
    print("Application startup complete.")
    
    yield # The application runs here

    # --- Code to run on application shutdown (optional) ---
    print("Application shutdown.")


# --- Create the FastAPI App ---
# We pass the lifespan manager to the app constructor.
app = FastAPI(
    title="Technical-Debt Management Platform",
    description="Analyze and manage technical debt with gamification.",
    version="0.1.0",
    lifespan=lifespan
)

# --- Mount Static Files and Include Routers ---
# This part remains the same, but it's now cleaner.

# Mount the static directory for CSS and JS files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the API routers
app.include_router(endpoints.router, prefix="/api/v1", tags=["Analysis"])
app.include_router(auth_endpoints.router, prefix="/auth", tags=["Authentication"])


# --- Serve the Frontend ---
@app.get("/", include_in_schema=False)
async def read_index():
    """Serves the main HTML file for the frontend."""
    return FileResponse('static/index.html')