from pydantic import BaseModel
import re
from typing import Any, List, Optional


class Data(BaseModel):
    id: int
    fieldA: Optional[float] = None
    fieldB: Optional[float] = None
    product: Optional[str] = None
    unitPrice: Optional[str] = None
    quantity: Optional[int] = None
    discount: Optional[str] = None

    class Config:
        extra = "allow"

    def model_post_init(self, __context: Any) -> None:
        self.discount = self.discount and self._parse_percentage(self.discount)
        self.unitPrice = self.unitPrice and self._parse_currency(self.unitPrice)
        return super().model_post_init(__context)

    @staticmethod
    def _parse_currency(value: str) -> float:
        try:
            return float(re.sub(r"[^\d.]", "", value))
        except ValueError:
            raise ValueError(f"Invalid currency value: {value}")

    @staticmethod
    def _parse_percentage(value: str) -> float:
        try:
            return float(value.strip("%").strip())
        except ValueError:
            raise ValueError(f"Invalid discount value: {value}")


class Inputs(BaseModel):
    varName: str
    varType: str


class Formula(BaseModel):
    expression: str
    inputs: List[Inputs]
    outputVar: str


class RequestBody(BaseModel):
    data: List[Data]
    formulas: List[Formula]


class ResultBody(BaseModel):
    result: Optional[List[int]] = None
    revenue: Optional[List[int]] = None
    sumResult: Optional[List[int]] = None
    finalResult: Optional[List[int]] = None


class SuccessResponse(BaseModel):
    results: ResultBody
    message: str = "The formulas were executed successfully."
    status: str = "success"
