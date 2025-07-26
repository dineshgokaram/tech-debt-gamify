# app/db/seed.py

from sqlalchemy.orm import Session
from . import models

# A list of all the badges available in the game
BADGES_TO_CREATE = [
    {
        "name": "First Fix",
        "description": "You resolved your very first issue!",
        "badge_key": "FIRST_FIX",
    },
    {
        "name": "Bug Squasher",
        "description": "You resolved 10 issues!",
        "badge_key": "TEN_FIXES",
    },
    {
        "name": "Code Cleaner",
        "description": "You resolved 5 Pylint issues!",
        "badge_key": "FIVE_PYLINT_FIXES",
    },
]

def seed_badges(db: Session):
    """
    Checks if badges exist in the database and creates them if they do not.
    This ensures our badge definitions are always available.
    """
    for badge_data in BADGES_TO_CREATE:
        db_badge = db.query(models.Badge).filter(models.Badge.badge_key == badge_data["badge_key"]).first()
        if not db_badge:
            new_badge = models.Badge(
                name=badge_data["name"],
                description=badge_data["description"],
                badge_key=badge_data["badge_key"],
            )
            db.add(new_badge)
    db.commit()