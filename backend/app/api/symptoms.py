from fastapi import APIRouter, Depends
from pydantic import BaseModel

from backend.app.core.dependencies import get_current_user
from modules.symptom_checker import check_symptoms


router = APIRouter(
    prefix="/symptoms",
    tags=["Symptoms"]
)


class SymptomsRequest(BaseModel):
    symptoms: str


@router.post("/")
def check_user_symptoms(
    data: SymptomsRequest,
    current_user=Depends(get_current_user),
):
    results = check_symptoms(data.symptoms)

    return {
        "results": results
    }