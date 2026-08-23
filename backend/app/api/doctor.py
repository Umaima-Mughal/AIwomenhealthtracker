from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user
from backend.app.services.health_history import (
    get_three_month_history,
    analyze_health_patterns,
)


router = APIRouter(
    prefix="/doctor",
    tags=["Doctor Summary"],
)


@router.get("/summary")
def get_doctor_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Generate a 3-month health summary for the authenticated user.

    The summary combines the user's existing:
    - Tracking records
    - Chat messages
    - Insights
    - Notifications

    No additional database table is required.
    """

    history = get_three_month_history(
        db=db,
        user_id=current_user.id,
    )

    patterns = analyze_health_patterns(
        history
    )

    return {
        "user_id": str(current_user.id),
        "period": patterns["period"],
        "overall_status": patterns["overall_status"],
        "pattern_count": patterns["pattern_count"],
        "patterns_detected": patterns["patterns_detected"],
    }