from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user
from backend.app.services.health_history import get_three_month_history


router = APIRouter(
    prefix="/history",
    tags=["History"],
)


@router.get("/3-months")
def get_three_month_health_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_three_month_history(
        db=db,
        user_id=current_user.id,
    )