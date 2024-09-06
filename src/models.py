from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class InputField(BaseModel):
    var_name: str = Field(..., alias="varName")
    var_type: str = Field(..., alias="varType")


class Formula(BaseModel):
    expression: str
    inputs: List[InputField]
    output_var: Optional[str] = Field(None, alias="outputVar")


class RequestBody(BaseModel):
    data: List[Dict[str, Any]]
    formulas: List[Formula]
