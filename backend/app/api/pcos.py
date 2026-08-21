from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.app.core.dependencies import get_current_user

from modules.pcos_checker import (
    pcos_risk_checker,
    prepare_input,
    predict_pcos,
)


router = APIRouter(prefix="/pcos", tags=["PCOS"])


class PCOSRequest(BaseModel):
    age: float
    weight: float
    height: float
    cycle: int
    cycle_length: float
    weight_gain: int
    hair_growth: int
    skin_darkening: int
    hair_loss: int
    pimples: int
    fast_food: int
    exercise: int


@router.post("/")
def check_pcos(
    data: PCOSRequest,
    current_user=Depends(get_current_user),
):
    sample, answers = prepare_input(
        data.age,
        data.weight,
        data.height,
        data.cycle,
        data.cycle_length,
        data.weight_gain,
        data.hair_growth,
        data.skin_darkening,
        data.hair_loss,
        data.pimples,
        data.fast_food,
        data.exercise,
    )

    prediction = predict_pcos(sample)

    return {
        "prediction": prediction["prediction"],
        "value": prediction["value"],
        "confidence": prediction["confidence"],
        "user_id": current_user.id,
    }