from datetime import date

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user
from backend.app.db_models.tracking import Tracking

router = APIRouter(prefix="/tracking", tags=["Tracking"])


class TrackingCreate(BaseModel):
    date: date
    symptoms: str | None = None
    mood: str | None = None
    sleep_hours: float | None = None
    weight: float | None = None
    cycle_day: int | None = None
    period_started: str | None = None
    notes: str | None = None


@router.post("/")
def create_tracking(
    tracking: TrackingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    new_tracking = Tracking(
        user_id=current_user.id,
        date=tracking.date,
        symptoms=tracking.symptoms,
        mood=tracking.mood,
        sleep_hours=tracking.sleep_hours,
        weight=tracking.weight,
        cycle_day=tracking.cycle_day,
        period_started=tracking.period_started,
        notes=tracking.notes,
    )

    db.add(new_tracking)
    db.commit()
    db.refresh(new_tracking)

    return new_tracking

@router.get("/")
def get_tracking_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return (
        db.query(Tracking)
        .filter(Tracking.user_id == current_user.id)
        .order_by(Tracking.date.desc())
        .all()
    )