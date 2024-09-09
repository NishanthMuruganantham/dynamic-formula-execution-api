from fastapi import APIRouter, HTTPException
from src.models import RequestBody, SuccessResponse
from src.logic import FormulaExecutor


router = APIRouter()

@router.get("/")
def home():
    return {"message": "Hello World"}


@router.post("/api/execute-formula", response_model=SuccessResponse, response_model_exclude_none=True)
async def execute_formula(request_body: RequestBody):
    data = request_body.data
    formulas = request_body.formulas
    try:
        formula_executor = FormulaExecutor(data, formulas)
        execution_result = formula_executor.perform_formula_execution()
        response = SuccessResponse(
            results=execution_result,
        )
        return response.model_dump(exclude_none=True)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
