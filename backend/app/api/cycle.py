from fastapi import APIRouter, Depends
from pydantic import BaseModel

from backend.app.core.dependencies import get_current_user
from modules.cycle_tracker import menstrual_cycle_tracker


router = APIRouter(
    prefix="/cycle",
    tags=["Cycle"]
)


class CycleRequest(BaseModel):
    last_period: str
    cycle_length: int
    period_duration: int


@router.post("/")
def track_cycle(
    data: CycleRequest,
    current_user=Depends(get_current_user),
):
    result = menstrual_cycle_tracker(
        data.last_period,
        data.cycle_length,
        data.period_duration,
    )

    return {
        "result": result
    }