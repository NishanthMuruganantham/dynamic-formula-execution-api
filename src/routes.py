from fastapi import APIRouter
from src.models import RequestBody


router = APIRouter()

@router.get("/")
def home():
    return {"message": "Hello World"}

@router.post("/simple-addition")
async def execute_formula(body: RequestBody):
    return {
        "results": {"result": [20, 30]},
        "status": "success",
        "message": "The formulas were executed successfully."
    }
