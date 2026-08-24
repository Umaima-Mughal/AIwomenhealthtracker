from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.app.core.dependencies import get_current_user
from modules.pregnancy_tracker import pregnancy_analysis


router = APIRouter(
    prefix="/pregnancy",
    tags=["Pregnancy"]
)


class PregnancyRequest(BaseModel):
    lmp_date: date


@router.post("/")
def track_pregnancy(
    data: PregnancyRequest,
    current_user=Depends(get_current_user),
):
    try: # cv
        result = pregnancy_analysis(data.lmp_date)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    return {
        "result": result
    }