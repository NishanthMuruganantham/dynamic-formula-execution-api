from pydantic import BaseModel
from typing import List, Optional


class Data(BaseModel):
    id: int
    fieldA: Optional[float] = None
    fieldB: Optional[float] = None
    product: Optional[str] = None
    unitPrice: Optional[str] = None
    quantity: Optional[int] = None
    discount: Optional[str] = None


class Inputs(BaseModel):
    varName: str
    varType: str


class Formula(BaseModel):
    expression: str
    inputs: List[Inputs]
    outputVar: Optional[str] = None


class RequestBody(BaseModel):
    data: List[Data]
    formulas: List[Formula]


class ResultBody(BaseModel):
    finalResult: Optional[List[float]] = None
    result: Optional[List[float]] = None
    revenue: Optional[List[float]] = None
    sumResult: Optional[List[float]] = None


class SuccessResponse(BaseModel):
    message: str
    results: ResultBody
    status: str = "success"
